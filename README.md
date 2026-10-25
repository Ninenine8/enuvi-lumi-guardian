# ENUVI — Lumi Guardian

**Status (25 October 2026):** Submission candidate based on the frozen 24 October build (tag `guardian-v0.5-freeze-20261024`, commit `214112e`). Runnable deterministic Guardian core with a live local Zetaris API adapter, official Meterless H-MEM reference engine, and live NVIDIA Nemotron analyst/verifier. **All transactions and permissions are fictional/simulated.** Publish the repository only after security review.

Start with [run commands and evidence](docs/SATURDAY_NEMOTRON.md) and [Sunday recording / slides](docs/SUNDAY_DEMO.md). **User-confirmed Saturday evidence:** 43 Python tests passed; 10 official Meterless reference tests passed; seven live NVIDIA Nemotron scenarios passed. A combined three-sponsor run returned `ALLOW / UNKNOWN` and replay with the same idempotency key returned `BLOCK / UNKNOWN`. Most Python unit tests mock API boundaries; the separately executed integration run is the live evidence. Local logs contain synthetic data and must not be posted with credentials.

Friday evidence confirmed by the user: 25 Python tests, 10 official H-MEM tests, live local Zetaris probe, and a combined run ending ALLOW / UNKNOWN with eight audit events. Zetaris permissions currently come from an **inline synthetic SELECT**, not persistent authority records. Saturday: a reviewed H-MEM test dependency update passed 10 official tests and reported zero npm audit vulnerabilities at that moment. Successful live NVIDIA and the combined three-sponsor run were confirmed separately on the user's PC; the key inputs are kept private. **The Zetaris query only emits inline synthetic authority rows — not persisted, independently verified records.**

Lumi Guardian is a proposed safety / authority layer for an AI companion. It distinguishes what an assistant can *access*, *disclose*, and *do*, with an explicit check for consequential actions and verified external outcomes.

> Just because an AI can do something, should it be allowed to?

## Frozen pre-hackathon materials

This repository begins with **existing materials** from the `Lumi_Guardian_Hackathon_Handoff.zip` package supplied on 11 October 2026:

- [`docs/pre-hackathon-v0.4/GUARDIAN_V0.4_BASELINE.md`](docs/pre-hackathon-v0.4/GUARDIAN_V0.4_BASELINE.md) — Guardian v0.4 safety protocol, labelled 7 October 2026 in its source document.
- [`docs/pre-hackathon-v0.4/TESTS_01_TO_21.md`](docs/pre-hackathon-v0.4/TESTS_01_TO_21.md) — 21 **documented scenario assessments**, not automated executable tests.
- [`docs/pre-hackathon-v0.4/README_HACKATHON_HANDOFF.md`](docs/pre-hackathon-v0.4/README_HACKATHON_HANDOFF.md) — prior project description and handoff notes.
- [`docs/pre-hackathon-v0.4/BASELINE_MANIFEST.md`](docs/pre-hackathon-v0.4/BASELINE_MANIFEST.md) — SHA-256 manifest of the original supplied handoff ZIP and the preserved texts.

These documents are **prior work**. They must not be portrayed as newly implemented hackathon features.

Other pre-existing assets (the MadeByNeon site ZIP, video, thumbnail and voiceover) remain in the original handoff ZIP and are **not included** in this repository starter. See the handoff for their descriptions. Avoid committing large media or anything containing secrets without a separate review.

## Key safety distinction

- `AUTHORIZED` — the specific requested action is permitted; it has **not** been performed.
- `INITIATED` — the external tool has been called; the result is not necessarily known.
- `COMPLETED` — a **trusted external service** has confirmed success.

An unresolved timeout / pending state must not be misreported as completion or retried blindly.

## Demo candidate

The documented **Test 4** exposed a failure: the model stated that a payment was processed without trusted service confirmation. A future working demo should use **synthetic users and simulated transactions**, demonstrate correct state tracking, and produce genuine execution traces. No real money transfers are intended.

## Implemented competition work and remaining work

- Implemented: deterministic scope/revocation checks, simulated outcome and duplicate protection, structured audit events, sponsor adapters, optional two-call Nemotron review, scenario runner.
- Remaining: final publication and Git history security review; host the already recorded 3:56 video and upload the completed five-slide deck; submit Sunday on HackOS. No new safety features are planned. The prototype is not approved for real money movement or emergency/eldercare use.

Any work undertaken in the **22–27 October 2026** build window should be clearly documented as new versus pre-existing. Verify the binding rules before submission.


## Reproduce the submission demonstration (synthetic data)

**Prerequisites:** Python 3.12+, Node.js 24+, Docker Desktop + running local Zetaris stack (including `zetaris-driver`), a private Zetaris development token and NVIDIA API key. Do **not** enter secrets into GitHub or public screenshots. See [Zetaris](docs/ZETARIS_INTEGRATION.md), [Meterless](docs/METERLESS_INTEGRATION.md), and [Nemotron](docs/SATURDAY_NEMOTRON.md) setup details. The official Meterless reference is installed locally and deliberately excluded from this repository; the demo uses original upstream code.

```powershell
python -m unittest discover -s tests -v
python guardian_scenarios.py
# With sponsor services available and official H-MEM reference installed:
python guardian_meterless.py --nemotron --simulate PENDING --ledger logs/reproduce-01.json --trace logs/reproduce-01.jsonl
```

To test duplicate prevention, re-run the same combined command with the **same ledger** and transaction key. Never describe a reset ledger as a safe replay. Traces in `logs/` are ignored and should remain local. Recorded video illustrates actual prior runs; a viewer without sponsor credentials can still run the tests and fixture scenario runner.

## Security and rights

Use synthetic data. Never commit credentials, private contact details, personal financial records or secrets. This is a private development workspace; access should be deliberately managed. No open-source licence is granted by default.

Existing public project page: https://madebyneon.com/lumi-guardian/
