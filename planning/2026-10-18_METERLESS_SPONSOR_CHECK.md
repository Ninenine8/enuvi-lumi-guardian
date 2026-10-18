# Meterless integration eligibility check — 18 October 2026

**Status:** PRE-BUILD RESEARCH / QUESTION PREPARED. Not a sponsor answer or an implemented integration.

## Why confirmation matters

The uploaded HackOS Submission Requirements says **Zetaris and Meterless integration are mandatory**, Cursor is required for development, and sponsors must be demonstrated in the 1–4 minute video and explained in README/slides. The uploaded Meterless HackOS H-MEM guide describes headless **reference architectures rather than an installable Python library**, and says the minimum for a six-day build is a memory store and memory retriever.

**New finding from public official source:** Meterless's public repository at https://github.com/Meterless/Meterless/tree/main/engines/hmem includes `AGENTS.md`, a runnable TypeScript `reference/`, `examples/`, and `conformance/`. Its README describes implementing the architecture contract with local tests. It offers a focused clone:

```
npx degit meterless/meterless/engines/hmem my-hmem
cd my-hmem/reference && npm install && npm test
npx tsx ../examples/01-add-memory/index.ts
```

This is an **official example to review when development begins**, not a command yet run, and these files have not been added to Guardian. Also inspect https://github.com/Meterless/Meterless/tree/main/templates/agentathon-starter .

## Sponsor question to send to HackOS Help Meterless / #help desk

> Hi! I'm a solo Open Agent Hackathon 2026 participant building ENUVI Lumi Guardian, an AI safety companion. The submission requirements say Meterless integration is mandatory. I plan to use the Meterless H-MEM Agent Engine for auditable cross-session memory retrieval with provenance and a safety policy that does not treat memory as authorization.
>
> Your HackOS H-MEM guide calls the engines reference architectures. The official GitHub `Meterless/Meterless/engines/hmem` also has a runnable reference implementation, examples and conformance suite.
>
> For the mandatory sponsor-technology requirement, would an independently implemented H-MEM `MemoryStoreService` + `MemoryRetrievalService`, following your documented H-MEM contracts and showing real retrieval/audit traces, qualify? Or must we reuse the official `reference/` code, template, or pass its conformance suite? We want to choose the correct approach before the 22 October build window. Thank you!

Do not treat silence or an AI @Ask answer as official organiser approval. Prefer a response from Meterless sponsor support or organisers; preserve text/screenshot and date.

## Lowest-risk implementation direction, subject to sponsor reply and binding rules

- **Preferred:** use official Meterless H-MEM reference contracts and/or actual reference component, rather than only rebadging a generic memory dictionary as "Meterless."
- Implement meaningful store + retrieval *used by Guardian's Verifier*; provenance, conflict flags and retrieval/audit JSONL are important.
- A memory saying "old permission exists" must **never** create or override verified authority.
- Demonstrate memory retrieval affecting a real new run, not only storing records.
- Retain source link, version, Apache 2.0 attribution/license and test evidence.
- Official docs: https://github.com/Meterless/Meterless and https://github.com/Meterless/Meterless/tree/main/engines/hmem .
- Do not create or import new competition-eligible Guardian integration code before 22 Oct 08:00 SGT. For now documentation/planning only.

## Related open items

- Confirm response from sponsor.
- Check official documentation version/commit at implementation time.
- Decide integration route if Python Guardian core plus TypeScript H-MEM reference needs a sidecar/bridge; alternatively implement H-MEM contracts natively in chosen language if sponsor approves.
