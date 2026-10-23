# Zetaris — synthetic permission VIEW integration (work in progress)

Zetaris proxy tested on user machine 23 October: `SELECT 7 AS seven` returned one row. New integration code is added but **not yet tested against the synthetic VIEW**. Unit tests mock the API and must not be presented as proof of end-to-end integration.

1. Start all four Docker services (UI, API, Postgres, Driver) and confirm the SQL Workspace runs `SELECT 1 AS one;`.
2. Use `examples/zetaris_permissions.sql` to create a self-contained fictional permissions VIEW, then query it from SQL Workspace. This may vary by Zetaris platform version; diagnose any SQL errors rather than guessing.
3. From Cursor repository terminal run `git pull --ff-only`, `python -m unittest discover -s tests -v`, then `python guardian_zetaris.py --simulate PENDING`.
4. The CLI prompts for a saved API token without echoing it. Never paste it into screenshots, CLI arguments or GitHub. Local default endpoint is `http://127.0.0.1:3000/api/proxy/query/sql/start` and `X-Org-Id=1`.
5. Expect `authority_source: zetaris`; synthetic `ALLOW` and `UNKNOWN` only if Zetaris actually returned the appropriate permission view. On any query failure Guardian **BLOCKS**, without local JSON fallback. See run-generated `logs/zetaris_trace.jsonl`.
6. New VIEW is a synthetic single-row data source, **not** production verification or identity. `verified=TRUE` is a simulated fixture field and does not prove anyone's real-world consent.

Potential differences in result formatting, view DDL compatibility and full source provenance still need live user-machine validation. We must not claim the sponsor has been integrated completely until those tests pass.
