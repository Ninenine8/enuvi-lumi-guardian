# Hackathon Day 1: executable synthetic Guardian core

**Created within the 22–27 October 2026 window.** This implementation is new; the prior v0.4 policy and 21 documented assessments were preserved unchanged. This is NOT yet a full hackathon submission.

## Local run (Python 3.10+, no packages or secrets)

From repository root:

```bash
python -m unittest discover -s tests -v
python guardian.py --simulate PENDING
```

To test confirmed outcomes separately, use a new ledger path / transaction key:

```bash
python guardian.py --simulate CONFIRMED --ledger logs/confirmed.json --trace logs/confirmed.jsonl
```

The default ledger is intentionally persistent. The second execution with the same idempotency key is rejected as a duplicate rather than faking another transaction. Data is 100% synthetic. `logs/` is ignored by git.

## What is implemented

- Distinct analyst and verifier trace events with deterministic authority gate (not yet LLM-powered).
- Explicit host-supplied synthetic trusted actor and permission records.
- Exact-recipient, exact-amount scoped permission and revocation priority.
- Memories may be retrieved with source context but NEVER authorize an action.
- Provider adapter is a clearly labelled **simulation** with CONFIRMED, PENDING, TIMEOUT or FAILED outcomes.
- Action state separates AUTHORISED, INITIATED, COMPLETED, UNKNOWN, FAILED; COMPLETED requires simulated provider confirmation.
- Persistent transaction ledger and idempotency key prevent automatic duplicate attempts.
- JSONL execution audit events with runtime timestamps. Do not confuse with the prior 21 documentation-only assessments.

## Known gaps and honest limitations

- This is a **standalone local core**, not a connected payment app.
- The provided `--actor` identity and authority-file are trusted **only for fictional demo purposes**; no genuine identity verification, tamper-proof storage, revocation timestamps, cryptographic confirmation or access control is implemented. Do not expose it as an API.
- Outcome selection is a demo fixture, not an independent real-world bank receipt.
- No sponsor integrations yet. Zetaris queries, genuine Meterless H-MEM components, and Nemotron reasoning must be added and validated with actual traces. Cursor must be used in the development workflow as required by the hackathon.
- No interactive web UI yet. Reconciliation of unknown transactions is intentionally NOT automated.
- Multi-action MIXED and broader safety scenarios remain future work.
- Tests are newly added executable checks but have not been independently validated on the user's machine at commit time. GitHub Actions will run when available.

## Next (priority)

1. Inspect GitHub Actions test run and fix failures before merging.
2. Replace trusted-authority JSON fixture with actual synthetic Zetaris query/provenance, fail closed on outage.
3. Integrate official Meterless H-MEM store/retriever (not just rename a dictionary), demonstrate memory retrieval changing verifier context but not authorization.
4. Implement real Nemotron analyst and verifier tool calls with bounded retries, deterministic gate unchanged.
5. Verify published rules, Cursor use, evaluation and demo/video; then security review before switching private repo to public.
