"""Zetaris-backed synthetic Guardian demo.

Only a Zetaris SQL VIEW containing explicitly synthetic permission records is
supported. This is an educational hackathon integration, NOT a real identity,
payment, or authorization service. Errors fail closed. No API keys are logged.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError

from guardian import run_guardian
from zetaris_probe import query_zetaris

DEFAULT_SQL = ("SELECT id, subject, action, recipient_id, amount_cents, "
               "verified, status FROM ENUVI_DEMO.guardian_permissions")


def parse_permissions(payload):
    """Fail closed if a result lacks the expected authority fields."""
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError("Zetaris response lacks a records list")
    records = []
    for row in payload["records"]:
        if not isinstance(row, dict):
            raise ValueError("Invalid row from Zetaris")
        required = ("id", "subject", "action", "recipient_id", "amount_cents",
                    "verified", "status")
        if any(k not in row for k in required):
            raise ValueError("Zetaris permission row is missing required columns")
        raw_verification = row["verified"]
        verified = (raw_verification is True or
                    isinstance(raw_verification, str) and
                    raw_verification.lower() == "true")
        raw_amount = row["amount_cents"]
        if isinstance(raw_amount, bool):
            raise ValueError("Invalid permission amount")
        if isinstance(raw_amount, int):
            cents = raw_amount
        elif isinstance(raw_amount, str) and raw_amount.isdigit():
            cents = int(raw_amount)
        else:
            raise ValueError("Non-integer permission amount")
        records.append({
            "id": str(row["id"]),
            "subject": str(row["subject"]),
            "action": str(row["action"]),
            "recipient_id": str(row["recipient_id"]),
            "amount_cents": cents,
            "verified": verified,
            "status": str(row["status"]),
        })
    return records


def run_with_zetaris(request, token, ledger=None, memories=None,
                     authenticated_actor="demo-owner", simulated_outcome="PENDING",
                     sql=DEFAULT_SQL):
    """Return (output, new_ledger, events); API unavailable means BLOCK, no tool."""
    try:
        response = query_zetaris(sql, token)
        records = parse_permissions(response)
    except (HTTPError, URLError, OSError, ValueError, TimeoutError,
            json.JSONDecodeError) as exc:
        # Never fall back to local permissions after a live authority failure.
        out = {
            "run_id": str(request.get("run_id", "unknown")),
            "decision": "BLOCK",
            "action_state": "NOT_APPLICABLE",
            "tool_confirmation_ref": None,
            "simulation": True,
            "authority_source": "zetaris",
            "reason": "Zetaris authority unavailable or invalid; fail closed",
            "safe_user_message": "I cannot verify the simulated permission; no transfer attempted.",
        }
        event = {"kind": "authority_fetch_failed",
                 "source": "zetaris",
                 "error_type": type(exc).__name__,
                 "simulated_tool_called": False}
        return out, {} if ledger is None else ledger, [event]
    out, new_ledger, events = run_guardian(
        request, records, memories, ledger, authenticated_actor, simulated_outcome
    )
    out["authority_source"] = "zetaris"
    out["authority_query"] = sql
    events.insert(0, {"kind": "zetaris_authority_read", "source": "zetaris",
                      "record_count": len(records), "read_only": True,
                      "synthetic": True})
    return out, new_ledger, events


def main():
    ap = argparse.ArgumentParser(description="Run Guardian with Zetaris VIEW permissions")
    ap.add_argument("--input", default="examples/transfer_800.json")
    ap.add_argument("--memory", default="examples/memory.json")
    ap.add_argument("--ledger", default="logs/zetaris_ledger.json")
    ap.add_argument("--trace", default="logs/zetaris_trace.jsonl")
    ap.add_argument("--simulate", choices=["CONFIRMED", "PENDING", "TIMEOUT", "FAILED"],
                    default="PENDING")
    args = ap.parse_args()
    token = os.environ.get("ZETARIS_API_TOKEN") or getpass.getpass(
        "Paste Zetaris API token (hidden): "
    )
    request = json.loads(Path(args.input).read_text(encoding="utf-8"))
    memories = json.loads(Path(args.memory).read_text(encoding="utf-8"))
    ledger_path = Path(args.ledger)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.exists() else {}
    result, ledger, events = run_with_zetaris(
        request, token, ledger, memories, simulated_outcome=args.simulate
    )
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    trace_path = Path(args.trace)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("a", encoding="utf-8") as stream:
        for event in events:
            stream.write(json.dumps({"run_id": result["run_id"], **event}) + "\n")
    print(json.dumps(result, indent=2))
    print("Audit events:", len(events), "— trace:", trace_path)


if __name__ == "__main__":
    main()
