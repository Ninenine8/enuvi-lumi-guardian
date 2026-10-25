# ENUVI Guardian — Friday to Sunday submission plan

**Internal target: submit on Sunday, 25 October 2026, before the end of the booked four-hour library session.** Monday and Tuesday are not build days.

## Verified progress
- Guardian v0.5 synthetic Python safety engine created in hackathon branch.
- Fourteen automated local tests passed on Windows.
- User successfully demonstrated PENDING → UNKNOWN, duplicate BLOCK and isolated CONFIRMED → COMPLETED.
- The 21 earlier Guardian v0.4 scenarios are documented assessments, not executable tests.
- GitHub remains private. No live financial actions are involved.
- Zetaris, Meterless and Nemotron integrations are not yet demonstrated in the runnable core.

## Friday, 23 October — 3–4 hours: sponsor integrations
1. Verify local Zetaris access without exposing credentials.
2. Add read-only Zetaris integration using synthetic trusted contacts and scoped permissions, fail closed on unavailable authority.
3. Integrate the official Meterless H-MEM reference implementation/contracts for persistent memory retrieval and provenance; memory must never grant permission.
4. Produce an actual end-to-end integration trace and run local tests.
5. Commit working code in Cursor. If time is short, prioritise real verified integrations over extra scenarios or UI.

## Saturday, 24 October — Central Library, four hours: working-demo freeze
- First 45 minutes: integrate Nemotron advisory reasoning, preserving deterministic Guardian authority and completion gates.
- Next 60 minutes: test the complete workflow and provenance.
- Next 60 minutes: test pending, timeout, confirmed, fake-family request, revoked permission, and memory-not-authority.
- Next 45 minutes: fix blockers, finalise clean-clone instructions and synthetic samples.
- Final 30 minutes: write a demo script and slide outline.

**Saturday exit condition:** a reproducible end-to-end Guardian demonstration showing genuine sponsor usage and correctly verified simulated action states. Do not expand scope into hardware or real payments.

## Sunday, 25 October — library, four hours: submission
- 0–50 min: record a real, accurate 1–4 minute demonstration video.
- 50–95 min: finalise slides.
- 95–140 min: final tests, README, security/secrets and history review.
- 140–170 min: intentionally make reviewed GitHub repository public and verify incognito access.
- 170–210 min: upload/submit HackOS materials, disclose pre-existing work and sponsor roles.
- 210–240 min: buffer, verify links and save proof of successful submission.

The goal is submission within Sunday’s booking, not work on Monday/Tuesday. All data, identities and payments in the demo are synthetic. Do not represent a mock confirmation as a real bank confirmation.
