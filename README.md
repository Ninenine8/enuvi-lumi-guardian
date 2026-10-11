# ENUVI — Lumi Guardian

**Status:** Private pre-hackathon baseline and preparation workspace. **No runnable Guardian agent or connected payment service is included in this snapshot.**

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

## Planned competition work (not implemented yet)

- Executable decision and policy-checking engine
- Programmatic test entry point with structured input/output
- Agent interaction and actual execution logs
- Simulated tool adapter with authoritative outcome state, retries and timeouts
- Sponsor integrations, subject to final published rules and access
- Fresh-clone instructions, sample mode, evaluation and accessible demo

Any work undertaken in the **22–27 October 2026** build window should be clearly documented as new versus pre-existing. Verify the binding rules before submission.

## Security and rights

Use synthetic data. Never commit credentials, private contact details, personal financial records or secrets. This is a private development workspace; access should be deliberately managed. No open-source licence is granted by default.

Existing public project page: https://madebyneon.com/lumi-guardian/
