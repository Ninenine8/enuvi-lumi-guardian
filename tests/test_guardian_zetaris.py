"""Offline tests for the Zetaris adapter, with mocked wire protocol."""
import unittest
from unittest.mock import patch
from guardian_zetaris import parse_permissions, run_with_zetaris

REQUEST = {
    "run_id": "zetaris-test", "idempotency_key": "zetaris-test",
    "request_text": "simulated payment",
    "action": {"type": "transfer", "recipient_id": "daughter-verified",
               "amount_cents": 80000},
}
ALLOW_ROW = {
    "id": "p-1", "subject": "demo-owner", "action": "transfer",
    "recipient_id": "daughter-verified", "amount_cents": 80000,
    "verified": True, "status": "ACTIVE"
}


class ZetarisAdapterTests(unittest.TestCase):
    def test_parse_valid(self):
        self.assertEqual(parse_permissions({"records": [ALLOW_ROW]})[0]["id"], "p-1")

    def test_invalid_rows_fail_closed(self):
        for payload in ({}, {"records": [{}]}, {"records": "not a list"}):
            with self.assertRaises(ValueError):
                parse_permissions(payload)

    def test_remote_allow_pending_is_unknown(self):
        with patch("guardian_zetaris.query_zetaris", return_value={"records": [ALLOW_ROW]}):
            out, _, events = run_with_zetaris(REQUEST, "test", simulated_outcome="PENDING")
        self.assertEqual(out["decision"], "ALLOW")
        self.assertEqual(out["action_state"], "UNKNOWN")
        self.assertEqual(out["authority_source"], "zetaris")
        self.assertEqual(events[0]["kind"], "zetaris_authority_read")

    def test_remote_revocation_blocks(self):
        revocation = {**ALLOW_ROW, "id": "p-revoked", "status": "REVOKED"}
        with patch("guardian_zetaris.query_zetaris",
                   return_value={"records": [ALLOW_ROW, revocation]}):
            out, _, events = run_with_zetaris(REQUEST, "test", simulated_outcome="CONFIRMED")
        self.assertEqual(out["decision"], "BLOCK")
        self.assertNotIn("simulated_tool_called", [e["kind"] for e in events])

    def test_remote_failure_never_falls_back(self):
        with patch("guardian_zetaris.query_zetaris", side_effect=ValueError("bad data")):
            out, _, events = run_with_zetaris(REQUEST, "test", simulated_outcome="CONFIRMED")
        self.assertEqual(out["decision"], "BLOCK")
        self.assertIsNone(out["tool_confirmation_ref"])
        self.assertEqual(events[0]["kind"], "authority_fetch_failed")

    def test_unverified_permission_rejected(self):
        fake = {**ALLOW_ROW, "verified": False}
        with patch("guardian_zetaris.query_zetaris", return_value={"records": [fake]}):
            out, _, _ = run_with_zetaris(REQUEST, "test", simulated_outcome="CONFIRMED")
        self.assertEqual(out["decision"], "ASK_CONFIRMATION")

if __name__ == "__main__":
    unittest.main()
