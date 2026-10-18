# Guardian pre-build decision lock — 18 October 2026 (SGT)

**Status:** PRE-HACKATHON PLANNING ONLY. No agent implementation, automated tests, or sponsor integration code was created by this note. Existing v0.4 evidence and v0.5 proposal remain separately attributed.

## Product promise

**Lumi Guardian is an AI safety and authority layer that remembers relevant context, checks the scope of consent before acting, and never claims completion without independent confirmation.**

**Main product differentiator:** a language model's statement, a memory entry, or an authorized intention is not trusted proof that an external action succeeded.

## Scope locked for the 22–27 October build window

### Must ship first: original Guardian test #4 — simulated $800 transfer
- All users, contacts, accounts and payment operations are synthetic.
- A fictional user explicitly authorizes one specific action for one recipient and amount.
- Nemotron proposes an action and a Verifier reviews evidence, but a deterministic Guardian policy gate decides whether simulated execution may proceed.
- Display **AUTHORIZED → INITIATED → COMPLETED** only after an authoritative **simulated tool confirmation**.
- If the tool returns PENDING or TIMEOUT: report **UNKNOWN / NOT CONFIRMED**, never "paid"; prevent blind duplicate retries with an idempotency key.
- Record genuine run-generated structured events showing the permission record, attempted tool call and confirmation / uncertainty.

### Must ship second: memory is not authority (test #17/#19 + fake family message)
- A new phone number claims to be the daughter and requests urgent money.
- H-MEM retrieves old, source-labelled context and current verification status.
- A remembered statement or an unverified "new number" message **cannot authorize transfer**, replace the verified contact, or override a revocation.
- Zetaris supplies queried synthetic trusted-contact/permission/evidence data; distinguish fetched results from model claims.
- Guardian asks for independent verification via a previously established channel.

### Supporting vignette: bank impersonation
- Use the same policy and evidence path for a purported bank staff member demanding an urgent transfer.
- Do not introduce a separate banking implementation.

### Stretch / future ENUVI: simulated fall detection
- Only if the main invariants, sponsor integrations, tests, demo and submission packet are ready.
- Sensor signals and caregiver contact/escalation must be clearly labelled synthetic.
- No real emergency calls, automatic dispatch or claim that physical fall sensing exists.

## Architecture (implementation begins no earlier than the allowed window)

```
Conversation or JSON input
  → Nemotron risk/request analyst (advisory)
  → Zetaris adapter (synthetic source data and provenance)
  → Meterless H-MEM-style store/retrieval (memory context, not permission)
  → Verifier agent (conflicts, missing evidence, unsafe proposal)
  → Deterministic policy/authority gate
  → Simulated tool with transaction/idempotency ID (only if allowed)
  → Authoritative action-state machine
  → User message + JSON response + generated JSONL audit/retrieval/tool trace
```

Proposed outcomes: `ALLOW`, `ASK_CONFIRMATION`, `BLOCK`, `ESCALATE`.
Proposed action states: `AUTHORIZED`, `INITIATED`, `COMPLETED`, `UNKNOWN`, `FAILED`. A refusal/no-attempt need not be falsely labelled INITIATED.
A tool confirmation reference is required to claim COMPLETED. Timeouts may require reconciliation, not retries.
Store authorization separately from H-MEM. Never let Nemotron or memory mutate the verified authority store by assertion.

## Prepared infrastructure — verified before the build window

- Git + Cursor + private GitHub repo: `Ninenine8/enuvi-lumi-guardian`.
- Windows + WSL2 Ubuntu + Docker Desktop installed.
- Local Zetaris service, SQL Workspace and API operational on 17 Oct; `SELECT 1 AS one` returned 1.
- New Zetaris API token `ENUVI-Guardian-Dev` (expiry 16 Nov 2026) safely stored outside the repository; 17 Oct authenticated POST to `http://localhost:3000/api/proxy/query/sql/start` with bearer token and `X-Org-Id: 1` returned HTTP 200 and `records: [{seven: "7"}]`. **This is a working UI-proxy route; do not mislabel it as independently verified direct 8888 path.**
- NVIDIA model `nvidia/nemotron-3-super-120b-a12b` accessed via `https://integrate.api.nvidia.com/v1/chat/completions`; request returned `Guardian API connected`.
- H-MEM reference-architecture docs reviewed; actual H-MEM service not yet implemented.

### Secrets / repo boundaries
- `.gitignore` currently ignores `.env`, `.env.*` (except `.env.example`), key files, credential folders and `logs/`.
- Never paste/commit key values, admin credentials, real elder/family data or live banking details.
- Before first hackathon commit, verify git status and confirm the applicable in-window rules and new work attribution.
- Test a fresh clone and sanitized `.env.example`; no credentials required in sample mode.

## Acceptance order (during eligible window)

1. Genuine sample-mode request + deterministic permission gate + state machine.
2. Pass #4 for CONFIRMED, PENDING, TIMEOUT and FAILED; no fabricated completion.
3. Actual Zetaris query and meaningful H-MEM retrieval changing the decision; emit trace evidence.
4. Verifier disagreement / escalation and revoked-permission / unknown-contact negative tests.
5. Inspectable JSONL logs, clean-clone instructions, bounded retry/cost logic.
6. Short demo video, slides, documented sponsor usage, submission and confirmation.

## Verified from uploaded HackOS Submission Requirements — 18 October 2026

This is a substantive new version of `Submission Requirements`, not the previously mislinked Technical Execution Guide. **The document explicitly defers to the event-page Official Rules if they disagree.**

- **Mandatory sponsor technology:** Zetaris and Meterless must be integrated; Cursor must be used for development. NVIDIA is described as "Integrate wherever it contributes to your project, workflow or use case". Nemotron is useful and already API-tested, but do not incorrectly call NVIDIA the same mandatory integration as Zetaris/Meterless based on this document.
- **Required submission:** 1–4 minute actual-workflow demo showing Zetaris and Meterless, slide deck covering problem, solution, workflow, stack, sponsor use, differentiation, visuals and future, **public GitHub repository** with runnable README, and sponsor technology explanation (Zetaris, Meterless, Cursor, NVIDIA).
- **GitHub privacy:** Currently PRIVATE; leave it private during preparation. Before submission, review all tracked source/docs/history for sensitive information, replace real details with synthetic ones, verify no exposed credentials, and deliberately publish a clean repository. Do not assume a private repo with judge access is sufficient: this document requires PUBLIC.
- **Pre-existing:** Clearly declare v0.4 documentation, 21 documented scenario assessments, pre-built data/materials; only work during the eligible build window is newly judged.
- **Submission form:** Select exactly one primary track, confirm team/solo roster before creating first submission (team composition locks), declare pre-existing components; may update submission until deadline.
- **Demo quality:** Show real runs, not canned answers; hide credentials. Repo must work from a clean clone, with sample inputs/outputs and authentic traces. `.env.example` with placeholders and sample mode recommended.
- **UTC deadline:** 27 October 2026 23:45 UTC = **28 October 2026 07:45 SGT**, hard close. Target submit by evening of **27 October SGT**.
- Judging: Impact 30, Technical 20, Innovation 15, Demo 15, Product/UX 10, Sponsor Tech 10.

**Still to verify:** binding event-page Official Rules if contradictory; which track to enter; whether H-MEM reference-architecture implementation alone satisfies meaningful Meterless integration; exact platform upload details.

## Rule and submission checks still OPEN as of 18 October

- Compare any conflicting requirements with the **binding event-page Official Rules**. HackOS Submission Requirements now explicitly says Zetaris+Meterless integration and Cursor development are required, while NVIDIA contributes where appropriate. The older organiser response and public FAQ are secondary to binding Official Rules.
- Confirm a genuine implementation based on the Meterless H-MEM reference guide satisfies Meterless's integration requirement; alternatively use official engine code if needed.
- Confirm track and challenge fit (Reasoning Architecture vs explainability vs Wildcard). **Repository PUBLIC requirement now resolved** by Submission Requirements; do not publish until reviewed.
- Confirm exact submission fields, whether `metadata.json` is requested, and accepted video/slide upload formats in HackOS. The Submission Requirements document confirms a 1–4 minute demo video, slide deck, public GitHub repo, sponsor tech explanation and pre-existing work declaration.

**Published event dates (subject to binding rules):** opens 22 Oct 2026 00:00 UTC = 22 Oct 08:00 SGT; closes 27 Oct 2026 23:45 UTC = 28 Oct 07:45 SGT. Internal goal: submit by the evening of 27 Oct Singapore time.

## Deliberately not in scope

Physical ENUVI hardware, production fraud detection, actual payment integrations, verified real-world fall detection or emergency dispatch, unattended sensitive actions, full H-MEM dreaming/sleep, polished consumer app, or claims of tested accuracy without data.
