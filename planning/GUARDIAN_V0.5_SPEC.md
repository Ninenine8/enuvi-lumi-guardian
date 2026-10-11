# Guardian v0.5 — Hackathon Build Specification (PLANNING ONLY)

**Prepared:** 11 October 2026 (SGT)  
**Status:** Design proposal, **NOT** implemented / tested.  
**Track (provisional):** Reasoning Architecture, subject to the published HackOS challenge statement and rules.  
**Existing baseline:** [Guardian v0.4](../docs/pre-hackathon-v0.4/GUARDIAN_V0.4_BASELINE.md) and [21 documented scenario assessments](../docs/pre-hackathon-v0.4/TESTS_01_TO_21.md). Do not count those as new hackathon implementation.

## Outcome to demonstrate

A trusted assistant must distinguish **permission to act**, **attempting an action**, and **independently verified completion**. A model's generated text is neither a payment receipt nor an authorization record.

**One-sentence proposition:** *Guardian allows helpful AI actions only within verifiable authority and reports real-world outcomes only when corroborated by a trusted tool.*

**Target user:** a person (including an older adult) using an AI companion that may encounter messaging, contacts, memory and external actions. **Hackathon demo uses fictitious users, contacts and money.**

### Signature live demonstration — scenario 04

1. A fictional user asks to send **$800** to their daughter and confirms the exact proposed recipient/amount/action.
2. An AI reasoning agent assesses the request and proposes a next step, including a warning against an unlimited future standing authorization.
3. A separate **Guardian policy gate** checks the current scoped authorization and recipient.
4. Guardian logs `AUTHORIZED` but does **not** say the transfer happened.
5. An **explicitly simulated payment adapter** is invoked with a unique transaction / idempotency key; the state becomes `INITIATED`.
6. The adapter returns one of: `CONFIRMED`, `PENDING`, `TIMEOUT`, or `FAILED`. A trusted confirmation is required before `COMPLETED`.
7. Guardian's final response describes the *actual* observed state, never a fabricated result. In an unknown state, it blocks a blind retry.

**No real payment API or real money is involved.** The demo must clearly label simulated tool events. If the simulated provider sends no confirmation, Guardian must report that it cannot confirm success.

### Second small demonstration — memory is not authority

- Guardian recalls a previously discussed transfer preference using a minimal H-MEM-inspired memory store/retriever.
- A **separate verified-permission store** is the source of authorization. A memory note by itself cannot approve a transfer or override a revocation.
- Show the recalled item, provenance / verification status, permission check, verifier critique and final decision in **genuine run-generated traces**.

## Proposed smallest executable architecture (to build during the hackathon)

```text
POST /run (JSON)  or documented CLI equivalent
    |
    v
Risk / Request Analyst (assesses request and proposes steps)
    |  -> data evidence from Zetaris adapter (synthetic data)
    |  -> context from Meterless H-MEM-style store / retrieval
    v
Guardian Verifier (checks missing evidence, scope, conflicts)
    |
    v
Deterministic Policy Gate (authoritative ALLOW / BLOCK / ASK_CONFIRMATION / ESCALATE)
    |
    v
Simulation Tool Adapter (only if authorized; idempotency key)
    |
    v
Action State Machine (AUTHORIZED / INITIATED / COMPLETED / UNKNOWN / FAILED)
    |
    v
Plain-language response + structured JSON + runtime JSONL traces
```

**Safety boundary:** neither the language model nor memories can directly set `COMPLETED` or write to the verified-permission store. Only a trusted simulator confirmation event may set completion in the demo. Refuse to retry a transaction that is pending or whose outcome is unknown.

**Cognition:** use actual, attributable agent functions with distinct responsibilities and at least one real review / feedback / branch step. Do not relabel a fixed prompt chain as multiple cooperating agents.

**Development environment:** Cursor. **Suggested implementation:** Python (FastAPI + pytest + SQLite / JSON) *or* JavaScript if implementation tests show that fits better. Final choice at build start; nothing is implemented yet.

## Proposed input / output contract

Input (illustrative schema, not executed):
- `run_id`, `request_text`, `actor_id`, `requested_action`
- `evidence_refs` and `permission_ref` (with provenance)
- `simulated_tool_outcome`: `CONFIRMED | PENDING | TIMEOUT | FAILED` for **demo only**
- `sample_mode` true / false

Output:
- `run_id`, `decision` = `ALLOW | ASK_CONFIRMATION | BLOCK | ESCALATE | MIXED`
- `risk_level`, `evidence_sources`, `reason_summary`, `uncertainty`
- `action_state`, `tool_confirmation_ref` (only if confirmed)
- `safe_user_message`, `trace_id`, `status`
- The `trace_id` links to authentic run-generated logs.

Never represent `simulated_tool_outcome` as an actual bank or payment event.

## Acceptance criteria (binary)

- [ ] A new input is actually processed through code, not mapped to a canned answer.
- [ ] An unconfirmed payment is never called completed, including timeout, pending and conflicting-source scenarios.
- [ ] Unauthorized/revoked/no-scope permission prevents simulated execution.
- [ ] Current scoped permission allows a permitted action without gratuitous re-approval.
- [ ] Each action has unique transaction ID / idempotency guard; retry of unknown transaction is blocked until reconciled.
- [ ] Trusted tool confirmation alone moves a transaction to `COMPLETED`.
- [ ] Memory retrieval affects context while **never** granting action authority.
- [ ] At least two distinct agent responsibilities and a genuine verification / branch event appear in a trace produced by code.
- [ ] Structured programmatic interface and documented clean setup work on standard CPU.
- [ ] `SAMPLE_MODE=true` runs local policy logic with synthetic samples without credentials; it is **not** a playback of prewritten answers.
- [ ] No real credentials, personal financial information, private contacts or sensitive user data are committed or logged.
- [ ] Meaningful Zetaris and Meterless usage is real, demonstrable and honestly documented; Cursor used in development.
- [ ] Demo and README distinguish **pre-existing v0.4 design** from **new v0.5 code and evaluation**.

## Not in scope for the six-day build

Physical hardware integration, bank transfers, live elder-care deployment, production identity verification, automatic emergency dispatch, full ENUVI memory dreaming/sleep, Markovian long-task engine, AgentVerse, consumer onboarding or unsupervised safety-critical action.

**No feature is considered complete until tested from a clean clone.**
