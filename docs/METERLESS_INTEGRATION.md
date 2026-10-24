# Meterless H-MEM — official reference integration

**23 October 2026.** ENUVI Guardian runs the actual open-source Meterless H-MEM **reference** code in a local TypeScript process, then feeds source-labelled memory context to our Python Guardian. This is not a hosted Meterless service and not production identity verification. The official reference explicitly uses a deterministic mock embedding and JSON persistence, not a production memory backend. State and audit log are under ignored `logs/meterless-hmem/`.

## Setup on the user's Windows laptop (Cursor terminal in Guardian repo)

```powershell
node --version
npm --version
npx --yes degit meterless/meterless/engines/hmem vendor/meterless-hmem
npm --prefix .\vendor\meterless-hmem\reference install
```

**Saturday security update:** the original Vitest dependency tree audited with nine vulnerabilities (two critical). Use the tested dependency overlay and locked reinstall in [SATURDAY_NEMOTRON.md](SATURDAY_NEMOTRON.md) after downloading the official source. Its updated install audited with zero vulnerabilities and passed all ten unchanged official tests plus the real bridge retrieval in the isolated Saturday checkout.

This downloads the official [Meterless/Meterless H-MEM engine](https://github.com/Meterless/Meterless/tree/main/engines/hmem) and its original Apache-2.0 LICENSE into `vendor/meterless-hmem`, which is ignored in our Git repo. No custom copy is claimed as original. It may require working Node/npm and internet. This specific official reference is released under Apache-2.0; preserve the attribution and licence.

To test official reference independently:

```powershell
npm --prefix .\vendor\meterless-hmem\reference test
```

## End-to-end Python → TypeScript H-MEM → Zetaris demo

```powershell
git pull --ff-only
python -m unittest discover -s tests -v
python guardian_meterless.py --simulate PENDING
```

The CLI privately asks for the Zetaris token. This run performs actual official H-MEM persistence + retrieval, a live Zetaris `SELECT` query returning a *fictional inline permission*, then a Python deterministic scope check and simulated transfer state. On subsequent runs with the same ledger idempotency key, Guardian BLOCKS duplicate transfers.

What qualifies as a real sponsor invocation: `meterless_bridge.ts` imports HMEM from the official downloaded implementation, writes memories with lineage into local persisted store, queries those memories using the official retrieval service, and receives an actual result and scored retrieval trace. Python never treats memory as payment authority. Run-generated `logs/meterless-hmem/ledger.jsonl` records memory writes/reads; `logs/full_demo_trace.jsonl` records Guardian operations.

**Limitations:** H-MEM reference is not a hosted service. It does not provide verified consent. Our Zetaris source currently produces inline fictional rows, not externally stored verified permissions. The Python/TypeScript bridge and official components still require real local machine verification; mocks in Python unit tests are not sufficient. Do not claim integration completed until a local run and H-MEM engine test pass. Do not commit private keys or anything under `logs/`.

A future improvement is stable persisted source tables or a Zetaris view, with authoritative revocation logs and cross-system reconciliation. Skip that if it endangers Sunday submission.
