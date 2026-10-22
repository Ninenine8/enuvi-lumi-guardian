"""ENUVI Guardian v0.5: local, synthetic, deterministic action-safety core.

Hackathon implementation created 22 Oct 2026. No real financial tools are used.
This is a runnable demonstration, NOT production identity/authentication software.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

OUTCOMES = {"CONFIRMED", "PENDING", "TIMEOUT", "FAILED"}


def _event(events, kind, **details):
    event = {"at": datetime.now(timezone.utc).isoformat(), "kind": kind, **details}
    events.append(event)
    return event


def _memory_context(records, recipient):
    """Memory supplies cited context, never permission or tool evidence."""
    return [
        {"id": r.get("id"), "source": r.get("source", "unverified"),
         "verified": bool(r.get("verified", False)), "text": r.get("text", "")}
        for r in records if r.get("recipient_id") == recipient
    ]


def _policy(request, records, authenticated_actor):
    """Only host-supplied actor and trusted authority records may authorize.

    The free-text request and memory are explicitly NOT authority.
    """
    action = request.get("action", {})
    if action.get("type") != "transfer" or not isinstance(action.get("amount_cents"), int) or isinstance(action.get("amount_cents"), bool) or action["amount_cents"] <= 0:
        return "BLOCK", "Unsupported or invalid action", None
    if not isinstance(action.get("recipient_id"), str) or not action["recipient_id"]:
        return "ASK_CONFIRMATION", "Choose an exact recipient", None
    if authenticated_actor != "demo-owner":
        return "BLOCK", "Unverified requester cannot act for the owner", None

    matches = [p for p in records
               if p.get("subject") == authenticated_actor
               and p.get("action") == "transfer"
               and p.get("recipient_id") == action["recipient_id"]
               and p.get("verified") is True]
    # A revocation takes priority over any older permission for the same scope.
    if any(p.get("status") == "REVOKED" for p in matches):
        return "BLOCK", "Verified authorization was revoked", None
    allowed = [p for p in matches
               if p.get("status") == "ACTIVE"
               and p.get("amount_cents") == action["amount_cents"]]
    if not allowed:
        return "ASK_CONFIRMATION", "No current exact-amount, verified authorization", None
    return "ALLOW", "Current verified, recipient-scoped authorization", allowed[0]["id"]


def run_guardian(request, authority_records, memory_records=None, ledger=None,
                 authenticated_actor="demo-owner", simulated_outcome="PENDING"):
    """Process one synthetic request; return structured output, ledger, events.

    simulated_outcome is a *host* parameter for the demo adapter, not a bank
    response and not read from untrusted request_text. Ledger is durable when
    the caller persists it. Never replay a pending/unknown transaction.
    """
    if simulated_outcome not in OUTCOMES:
        raise ValueError("Unknown simulator outcome")
    if not isinstance(request, dict) or not isinstance(request.get("action"), dict):
        raise ValueError("Expected JSON request with action object")
    if ledger is None:
        ledger = {}
    events = []
    run_id = str(request.get("run_id") or uuid4())
    action = request["action"]
    key = str(request.get("idempotency_key") or run_id)
    retrieved = _memory_context(memory_records or [], action.get("recipient_id"))
    _event(events, "memory_retrieval", count=len(retrieved),
           memory_ids=[m["id"] for m in retrieved], authority_from_memory=False)
    # The analyst is advisory; untrusted instructions do not reach the gate.
    _event(events, "analyst", action_type=action.get("type"),
           user_text_is_authority=False)
    decision, reason, permission_ref = _policy(request, authority_records, authenticated_actor)
    _event(events, "verifier", decision=decision, reason=reason,
           permission_ref=permission_ref, memory_grants_authority=False)

    base = {"run_id": run_id, "decision": decision, "reason": reason,
            "action_state": "NOT_APPLICABLE", "tool_confirmation_ref": None,
            "idempotency_key": key, "permission_ref": permission_ref,
            "memory_context": retrieved, "simulation": True,
            "safe_user_message": ""}
    if decision != "ALLOW":
        base["safe_user_message"] = ("I cannot carry out this simulated transfer. "
                                     + reason + ".")
        _event(events, "policy_rejected", decision=decision)
        return base, ledger, events

    # For any previously submitted key, never call the provider a second time.
    if key in ledger:
        old = ledger[key]
        base.update(decision="BLOCK", action_state=old["state"],
                    tool_confirmation_ref=old.get("confirmation_ref"),
                    reason="Existing transaction key; reconciliation required")
        base["safe_user_message"] = ("I did not retry this simulated transfer. "
                                     "Its existing state is " + old["state"] + ".")
        _event(events, "duplicate_prevented", state=old["state"], idempotency_key=key)
        return base, ledger, events

    action_signature = {"recipient_id": action["recipient_id"],
                        "amount_cents": action["amount_cents"]}
    _event(events, "authorized", permission_ref=permission_ref,
           action=action_signature, state="AUTHORIZED")
    base["action_state"] = "AUTHORIZED"
    ledger[key] = {"state": "INITIATED", "action": action_signature,
                   "permission_ref": permission_ref, "confirmation_ref": None}
    _event(events, "simulated_tool_called", adapter="FAKE_PAYMENT_PROVIDER",
           state="INITIATED", idempotency_key=key)
    base["action_state"] = "INITIATED"

    if simulated_outcome == "CONFIRMED":
        # Only the adapter produces this confirmation, never model prose.
        confirmation = "SIM-" + uuid4().hex[:16].upper()
        ledger[key].update(state="COMPLETED", confirmation_ref=confirmation)
        base.update(action_state="COMPLETED", tool_confirmation_ref=confirmation)
        base["safe_user_message"] = ("The SIMULATED payment provider confirmed this "
                                     "test transfer, reference " + confirmation + ".")
    elif simulated_outcome in ("PENDING", "TIMEOUT"):
        ledger[key]["state"] = "UNKNOWN"
        base["action_state"] = "UNKNOWN"
        base["safe_user_message"] = ("The SIMULATED transfer was initiated but is "
                                     "NOT CONFIRMED. Do not retry until reconciled.")
    else:
        ledger[key]["state"] = "FAILED"
        base["action_state"] = "FAILED"
        base["safe_user_message"] = ("The SIMULATED provider reported failure; "
                                     "no payment completion is confirmed.")
    _event(events, "simulated_tool_result", outcome=simulated_outcome,
           state=base["action_state"],
           confirmation_ref=base["tool_confirmation_ref"])
    return base, ledger, events


def main():
    parser = argparse.ArgumentParser(description="ENUVI Guardian synthetic demo")
    parser.add_argument("--input", default="examples/transfer_800.json")
    parser.add_argument("--authority", default="examples/trusted_authority.json")
    parser.add_argument("--memory", default="examples/memory.json")
    parser.add_argument("--ledger", default="logs/demo_ledger.json")
    parser.add_argument("--trace", default="logs/demo_trace.jsonl")
    parser.add_argument("--actor", default="demo-owner",
                        help="Synthetic host-authenticated actor (NOT real authentication)")
    parser.add_argument("--simulate", choices=sorted(OUTCOMES), default="PENDING")
    args = parser.parse_args()

    def load(path, default):
        p = Path(path)
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

    ledger_file = Path(args.ledger)
    output, ledger, events = run_guardian(
        load(args.input, {}), load(args.authority, []),
        load(args.memory, []), load(args.ledger, {}),
        authenticated_actor=args.actor, simulated_outcome=args.simulate)
    ledger_file.parent.mkdir(parents=True, exist_ok=True)
    ledger_file.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    trace_file = Path(args.trace)
    trace_file.parent.mkdir(parents=True, exist_ok=True)
    with trace_file.open("a", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps({"run_id": output["run_id"], **event}) + "\n")
    print(json.dumps(output, indent=2))
    print("Events: " + str(len(events)) + "; trace: " + str(trace_file))


if __name__ == "__main__":
    main()
