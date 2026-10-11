# Hackathon Preparation, Sponsor Plan & Build Schedule

**As of 11 October 2026; not a binding interpretation of the rules.**

## Sources reviewed

- `welcome-guide.md` — 3 primary tracks + 2 bonus tracks, sponsor requirements, delivery checklist and dates.
- `official-rules(1).md` — explicitly a **WORKING DRAFT**, conflicting with the Welcome Guide (tracks; sponsor optionality). **Not authoritative**.
- `technical-execution-requirements(1).md`, `disqualification-checklist(1).md`, `ai-usage-policy(1).md` — technical and integrity guidance; all defer to published rules.
- Sponsor overviews: Zetaris / Meterless / Cursor / NVIDIA. Access instructions for some marked **TBC**.
- **Organiser Discord response dated 1 October 2026** to participant `java110914`, from staff `izzy0AP`, shared as screenshots on 11 October: rules 4.2, 5.1, 5.2, 5.3, 6.3 explained (see [dated clarification note](ORGANISER_DISCORD_CLARIFICATION_2026-10-01.md)). This reply predates the announced postponement; the final published rules still govern.
- `submission-requirements.md` — appears to contain a duplicate **Technical Execution Guide**, not a distinct submission policy.

**Rule resolution:** staff clarified that **Zetaris + Meterless integrations and development in Cursor are mandatory** and **NVIDIA is optional**. The dated reply also supports disclosing pre-existing v0.4 research while building the actual agent during the official window. Check **current binding event-page Official Rules** and updated tracks before submitting; do not mistake the older Discord reply for the final legal text.

## Track choice

**Provisional primary track: Reasoning Architecture** (reliable decisions and actions from data, memory and reasoning).

Alternatives: **The Agent That Can Explain Why** and **Wildcard [Tinkerer] — Bring Your Own Project**. Staff confirmed (rule 4.2) clearly declared pre-existing components may be used, but the actual agent must be built in the window and only in-window work is judged. **Which main track is the best fit remains unresolved.** Confirm the published descriptions and any track-specific eligibility.

Do **not** state “registered in Reasoning Architecture” until it is actually selected in HackOS.

## Sponsor integration proposal (not yet built)

| Sponsor | Required?* | Proposed genuine job | Unknown to confirm |
|---|---|---|---|
| **Zetaris** | **Yes** — organiser confirms | Query **synthetic** trusted-contact metadata, evidence and permission records through Zetaris as a real data source, with provenance | Actual instance access, supported connectors/API, permissible free tier and sample fallback |
| **Meterless** | **Yes** — organiser confirms | Implement/adapt a **small H-MEM memory store + retriever** with persistence, provenance and emitted retrieval/audit events; distinguish memory from verified authority | What satisfies sponsor integration/attribution: published reference architecture vs their actual engine/code |
| **Cursor** | **Yes** — organiser confirms | IDE used during the eligible implementation and test commits | Hackathon team access instructions |
| **NVIDIA** | **Optional** — organiser confirms | Optional Nemotron API for reasoning if credits and tests support it | Credits, model endpoint, costs, limits; **no mandatory GPU** |

*Source: organiser Discord response, 1 Oct 2026, quoting rules 5.1–5.3. Access details / final published rules may be updated. **Do not claim an integration until a real call and trace verify it.**

### Safety of the Zetaris plan

Even if Zetaris stores synthetic contact and permission facts, **memory retrieved through H-MEM never confers permissions**. The action gate consumes only valid verified authorization records within current scope and checks revocation / authority. If Zetaris is unavailable, the app must return honest partial/unknown status or use clearly labelled local synthetic sample mode; it must not make up an authorization.

## Preparation only — 11–21 October (SGT)

- [x] Private GitHub repository created; prior v0.4 reference docs preserved.
- [x] v0.5 *design* and proposed test matrix documented.
- [ ] Examine current HackOS **track challenge statement** and binding Official Rules; select track.
- [x] Organiser confirmed existing components can be reused **if clearly declared**, while the agent itself must be built in-window (1 Oct staff reply).
- [ ] Archive a dated declaration listing existing Guardian v0.4 components; check current binding rules for track-specific constraints.
- [ ] Check sponsor access, API examples, actual integration expectations and available credits. Do not buy tools solely on speculation.
- [x] Cursor and Git installed; GitHub repository cloned to local Cursor workspace.
- [ ] Check local Python or JavaScript tooling; practice in a throwaway sandbox if desired, **not** as undisclosed contest implementation.
- [ ] Attend/review sponsor setup workshop, particularly Zetaris + Cursor. Staff dated reply states **12 Oct 22:00 UTC = 13 Oct 06:00 SGT**; verify current calendar and seek a recording if inconvenient.
- [ ] Keep synthetic scenario fixtures and permission rules clearly labelled as prior planning.

## Eligible build window — 22–27 October 2026

Opens **22 Oct 00:00 UTC = 22 Oct 08:00 SGT**.  
Submission deadline **27 Oct 23:45 UTC = 28 Oct 07:45 SGT**.  
Aim to submit **by 27 Oct evening SGT**, not at the absolute deadline.

| Date (SGT) | Focus | Exit criterion |
|---|---|---|
| Thu 22 | Create new code skeleton, `/run`, basic auth gate and action-state machine; begin real sponsor wiring | One computed local example runs and logs |
| Fri 23 | Wire actual Zetaris access and minimal Meterless memory storage/retrieval; implement at least one genuine verifier feedback path | Sponsor usage can be demonstrated in code and traces |
| Sat 24 | Main weekend build: Test #4 with CONFIRMED/PENDING/TIMEOUT plus #10, #17, #19 | Core invariants testable automatically |
| Sun 25 | Broaden negative cases, sample mode, logging, integration fallbacks, UI polish only if core works | Clean-clone smoke test and truthful walkthrough |
| Mon 26 | Reliability, documentation, slides and video | Submission draft complete; public-access video check |
| Tue 27 | Final compliance, security scan, test rerun, commit and submit early | HackOS receipt / confirmation saved |

Actual development may be rearranged around work commitments. **Smallest working system first; no expansion until Test #4 is solid.**

## Minimum submission packet (verify against binding rules)

- 1–4 minute genuine demonstration video per Welcome Guide (some drafts recommend 2–3 minutes)
- Slide deck: user/problem, workflow, architecture, tech, sponsor roles, impact and limitations
- GitHub project with setup, usage, requirements, demonstration and tests. Organiser said **no public deployed URL required** if a runnable container with clear instructions is provided. **Private GitHub repository access for judges remains unconfirmed**; obtain explicit answer before submission.
- Clear sponsor documentation (including `metadata.json` if the submission interface requires it)
- Explicit description of the **pre-existing v0.4 work**, dates/provenance and precisely what was newly built
- Logs/trace evidence tied to real runs, no hardcoded outputs, no secrets, synthetic data and honest limitations

## Stop conditions

- If a sponsor integration cannot be verified, do not pretend it exists: ask sponsor support / change scope.
- If the mock payment adapter cannot preserve authorization vs completion state, block tool invocation rather than shipping false claims.
- If final rules materially change, update this plan, confirm compliance, and keep prior decisions traceable.
