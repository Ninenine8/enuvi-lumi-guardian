"""Minimal Zetaris API connectivity probe for the ENUVI Guardian hackathon.

Read-only SQL against the local UI proxy. Do NOT save API tokens in source files,
command arguments, GitHub or screenshots. First confirm connectivity, then add
a real synthetic permission dataset before claiming Guardian integration.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "http://127.0.0.1:3000/api/proxy/query/sql/start"


def query_zetaris(sql: str, token: str, url: str = DEFAULT_URL, org_id: str = "1"):
    """Use documented local proxy path, return parsed response.

    A valid HTTP 200 and JSON result prove only that Zetaris answered the SQL.
    They do not prove an external data source is configured.
    """
    if not token:
        raise ValueError("ZETARIS_API_TOKEN is missing")
    if not url.startswith(("http://127.0.0.1:", "http://localhost:")):
        raise ValueError("Probe only allows local Zetaris endpoint")
    if not sql.strip().lower().startswith("select "):
        raise ValueError("Probe allows read-only SELECT queries only")
    req = urllib.request.Request(
        url,
        data=json.dumps({"sql": sql}).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + token,
            "X-Org-Id": org_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload


def main():
    parser = argparse.ArgumentParser(description="Zetaris local SQL connection check")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--org-id", default="1")
    args = parser.parse_args()
    token = os.environ.get("ZETARIS_API_TOKEN") or getpass.getpass(
        "Paste existing Zetaris API token (hidden input): "
    )
    # No echo or persistence. Prints safe scalar only, not raw HTTP response.
    try:
        payload = query_zetaris("SELECT 7 AS seven", token, args.url, args.org_id)
        rows = payload.get("records")
        if rows is None and isinstance(payload.get("data"), list):
            rows = payload["data"]
        if isinstance(rows, list):
            print("Zetaris API replied. Returned rows: " + str(len(rows)))
            if any(isinstance(r, dict) and str(r.get("seven")) == "7" for r in rows):
                print("PASS: SELECT 7 AS seven returned seven=7")
            else:
                print("Review API result shape; 7 not located in record dictionaries.")
                print("Response top-level keys: " + ", ".join(payload.keys()))
        else:
            print("API responded, but rows were not in expected records/data field.")
            print("Response top-level keys: " + ", ".join(payload.keys()))
    except urllib.error.HTTPError as e:
        print("Zetaris HTTP error: " + str(e.code) + " (token not printed)")
        sys.exit(1)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError) as e:
        print("Connection failed: " + type(e).__name__ + " (no secrets logged)")
        sys.exit(1)


if __name__ == "__main__":
    main()
