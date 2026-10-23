"""Run Guardian with official Meterless H-MEM reference + Zetaris demo permissions.

Uses a *real* local TypeScript reference implementation via tsx. The H-MEM
records carry provenance but never grant action permission. Zetaris SQL here
is an explicitly inline synthetic sample, not a persisted verified database.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import subprocess
from pathlib import Path

from guardian_zetaris import run_with_zetaris

ROOT = Path(__file__).resolve().parent
TSX = ROOT / "vendor/meterless-hmem/reference/node_modules/tsx/dist/cli.mjs"
BRIDGE = ROOT / "meterless_bridge.ts"


def retrieve_hmem(query: str, *, runner=subprocess.run):
    """Execute actual official H-MEM reference and parse its retrieved context.

    If official code is unavailable, raise instead of calling local fixtures
    Meterless. The caller should not fake sponsor integration.
    """
    if not TSX.exists():
        raise FileNotFoundError(
            "Official H-MEM not installed; see docs/METERLESS_INTEGRATION.md"
        )
    result = runner(
        ["node", str(TSX), str(BRIDGE)],
        input=json.dumps({"query": query, "persistDir": "logs/meterless-hmem"}),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(ROOT),
        timeout=30,
        check=True,
    )
    response = json.loads(result.stdout)
    if response.get("engine") != "official_meterless_hmem_reference":
        raise ValueError("H-MEM response missing official engine identifier")
    if not isinstance(response.get("memories"), list):
        raise ValueError("H-MEM response lacks memory array")
    return response


def run_guardian_with_memory(request, token, sql, outcome="PENDING",
                             ledger=None, hmem_retriever=retrieve_hmem):
    """Memory affects reviewed context; Zetaris alone supplies scoped authority."""
    hmem = hmem_retriever(
        "verified daughter transfer contact memory consent new phone identity"
    )
    memories = hmem["memories"]
    out, ledger_out, events = run_with_zetaris(
        request, token, ledger=ledger, memories=memories,
        simulated_outcome=outcome, sql=sql
    )
    out["memory_engine"] = hmem["engine"]
    out["memory_retrieval"] = hmem["retrieval"]
    out["memory_source_is_authority"] = False
    events.insert(0, {
        "kind": "meterless_hmem_retrieval",
        "source": hmem["engine"],
        "retrieved_ids": [m["id"] for m in memories],
        "retrieved_count": len(memories),
        "scores": hmem["retrieval"].get("scores", {}),
        "source_is_authority": False,
        "ledger_entries": hmem.get("ledger_entries", 0),
    })
    return out, ledger_out, events


def main():
    ap = argparse.ArgumentParser(description="Zetaris + official Meterless H-MEM demo")
    ap.add_argument("--sql-file", default="examples/zetaris_inline_permissions.sql")
    ap.add_argument("--input", default="examples/transfer_800.json")
    ap.add_argument("--ledger", default="logs/full_demo_ledger.json")
    ap.add_argument("--trace", default="logs/full_demo_trace.jsonl")
    ap.add_argument("--simulate", default="PENDING",
                    choices=("PENDING", "CONFIRMED", "TIMEOUT", "FAILED"))
    args = ap.parse_args()
    request = json.loads((ROOT / args.input).read_text(encoding="utf8"))
    sql = (ROOT / args.sql_file).read_text(encoding="utf8")
    ledger_file = ROOT / args.ledger
    ledger = json.loads(ledger_file.read_text(encoding="utf8")) if ledger_file.exists() else {}
    token = os.environ.get("ZETARIS_API_TOKEN") or getpass.getpass(
        "Paste existing Zetaris token (hidden input): "
    )
    try:
        out, ledger, events = run_guardian_with_memory(
            request, token, sql, outcome=args.simulate, ledger=ledger
        )
    except (FileNotFoundError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired, json.JSONDecodeError, ValueError) as e:
        print("Cannot run official H-MEM bridge: " + type(e).__name__)
        print("No synthetic transfer was attempted. See docs/METERLESS_INTEGRATION.md")
        raise SystemExit(1) from None
    ledger_file.parent.mkdir(parents=True, exist_ok=True)
    ledger_file.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf8")
    trace_file = ROOT / args.trace
    trace_file.parent.mkdir(parents=True, exist_ok=True)
    with trace_file.open("a", encoding="utf8") as f:
        for ev in events:
            f.write(json.dumps({"run_id": out["run_id"], **ev}) + "\n")
    print(json.dumps(out, indent=2))
    print("Audit events:", len(events), "— trace:", str(trace_file))


if __name__ == "__main__":
    main()
