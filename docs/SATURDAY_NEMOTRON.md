# Saturday 24 October 2026 — runnable increment

Personal submission target: Sunday 25 October, within the four-hour session. No Monday or Tuesday work is planned.

## What changed

`guardian_nemotron.py` calls NVIDIA's hosted chat-completions endpoint twice: an analyst produces a bounded recommendation with risk flags and memory citations; a separate verifier checks exact action scope, consistency with the deterministic gate, memory/authority separation, and the absence of premature completion claims. Both calls use Nemotron. This is consistency review of supplied evidence, not independent authentication or a second authority database. Correlated model mistakes remain possible.

The deterministic gate remains authoritative. An advisory veto can stop an otherwise allowed action; model ALLOW cannot bypass missing/revoked permissions, host identity, idempotency or tool-receipt rules. Invalid JSON, extra keys, invented citations, changed action, tool calls, truncation, API failure, or a completion claim fail closed before the fake provider runs. Model prose is never used as the completion message. The original path without `--nemotron` remains available.

No new Python dependencies. NVIDIA endpoint/model contract: https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-nano-30b-a3b-infer . Default model: `nvidia/nemotron-3-nano-30b-a3b`. If NVIDIA no longer offers it to your account, set `NVIDIA_MODEL` to an available NVIDIA Nemotron model; do not silently substitute another vendor.

## Cursor terminal in the existing repository

First apply the delivered changes, then:

```powershell
git branch --show-current
python -m unittest discover -s tests -v
python guardian_scenarios.py
```

Expected baseline: branch `hackathon-2026-day1-core`, **43 Python tests**, **7 deterministic scenario PASS** lines. API boundaries in the unit tests are mocked. The deterministic scenario runner uses local authority and memory fixtures, not sponsor calls.

For a short live NVIDIA test using local fixtures:

```powershell
python guardian_scenarios.py --nemotron --case pending --report logs/nvidia_pending.json
```

The key prompt is hidden. Never paste the key into chat, code, terminal arguments or a screenshot. Alternatively use an already securely populated `NVIDIA_API_KEY` environment variable. A live PASS requires two successfully parsed NVIDIA answers, ALLOW / UNKNOWN, and duplicate replay BLOCK / UNKNOWN without another tool call. A fail-closed API error is not a successful live evidence run. Inspect only sanitized output/report; raw API bodies and model reasoning are never logged.

Then run all seven scenarios with live NVIDIA if time permits (up to 14 API calls):

```powershell
python guardian_scenarios.py --nemotron --report logs/nvidia_scenarios.json
```

## All three sponsor paths

Keep the local Zetaris service running as on Friday and install the H-MEM reference as described in METERLESS_INTEGRATION.md. Use a distinct ledger filename for this intentionally separate synthetic demonstration:

```powershell
python guardian_meterless.py --nemotron --simulate PENDING --ledger logs/saturday_nemotron_01.json --trace logs/saturday_nemotron_01.jsonl
```

It privately prompts for Zetaris and NVIDIA credentials. Expected: `authority_source: zetaris`, `source_mode: inline_sql_demo`, `memory_engine: official_meterless_hmem_reference`, two advisory call records with `transport: nvidia_https`, and ALLOW / UNKNOWN. It should record nine audit events on a first successful run. Reusing the same ledger/key intentionally blocks the simulated duplicate. Do not delete a ledger to describe a retry as safe.

Keep all logs ignored. Review before sharing: inputs are synthetic, event timestamps and SHA-256 digests are present, credential strings and raw errors are absent. Successful call metadata is useful local evidence, not cryptographic proof of a provider response.

## Dependency assessment and reproducible repair

Saturday live npm audit of the Friday installation confirmed **9** findings: 2 critical, 4 high, 3 moderate. Critical packages: `vitest` and `tinypool`. The reference has no production runtime dependency; these are development tools, but critical findings still require repair. Do not expose Vitest UI or development servers or run untrusted test code.

In an isolated copy, the test dependency was upgraded to **vitest 5.0.5**. Official source and tests were unchanged. Audit then reported **0 vulnerabilities**, all **10 official tests passed**, and the actual H-MEM bridge successfully retrieved two memories. `tooling/meterless/package.json` and its lockfile capture that tested dependency overlay; this is our maintenance of upstream tooling, not a new implementation of H-MEM. It requires compatible Node (tested here with the installed Node 24).

Apply to the existing ignored vendor folder:

```powershell
$env:NODE_USE_SYSTEM_CA='1'
Copy-Item tooling/meterless/package.json vendor/meterless-hmem/reference/package.json
Copy-Item tooling/meterless/package-lock.json vendor/meterless-hmem/reference/package-lock.json
npm.cmd --prefix vendor/meterless-hmem/reference ci --ignore-scripts
npm.cmd --prefix vendor/meterless-hmem/reference audit
npm.cmd --prefix vendor/meterless-hmem/reference test
```

The npm lockfile records public registry URLs and integrity hashes. Repeat audit before publication; the zero count is a point-in-time result. Do not use `npm audit fix --force` as an unreviewed shortcut.

## Evidence ledger

| Claim | Status |
| --- | --- |
| Friday original 25 tests, H-MEM 10 tests, live Zetaris and combined 8-event run | User-confirmed on original PC |
| Saturday 43 Python tests; 7 deterministic scenarios | Executed in isolated checkout |
| Updated dependency audit 0; official H-MEM tests 10; actual bridge retrieval | Executed in isolated checkout |
| Live Nemotron analyst and verifier | Pending hidden key and actual run |
| New all-three-sponsor combined evidence | Pending live credentials and actual run |
| Public GitHub, video, slides, submission | Sunday work; not completed |

## Publication review before changing visibility

Review tracked content **and Git history** for credentials, private records, logs and large media. Rotate any credential ever committed. Confirm ignored vendor and logs are not tracked. Review the draft PR and the tested dependency overlay. Verify all claims against actual logs; leave unavailable evidence marked pending. Keep pre-existing v0.4 disclosure. Make GitHub public deliberately only after this review, then check unauthenticated access. No repository visibility change is included in this increment.
