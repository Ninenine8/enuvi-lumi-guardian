import unittest
from unittest.mock import patch
from guardian_meterless import run_guardian_with_memory

REQUEST = {
    "run_id": "t-hmem", "idempotency_key": "t-hmem",
    "request_text": "Send the simulated $800",
    "action": {
        "type": "transfer", "recipient_id": "daughter-verified",
        "amount_cents": 80000,
    },
}
PERMISSION = {
    "id": "p-1", "subject": "demo-owner", "action": "transfer",
    "recipient_id": "daughter-verified", "amount_cents": 80000,
    "verified": True, "status": "ACTIVE",
}
HMEM = {
    "engine": "official_meterless_hmem_reference",
    "memories": [{
        "id": "mem-1", "recipient_id": "daughter-verified",
        "text": "Old message suggests transfers; not authority",
        "source": "synthetic:prior_conversation",
        "verified": False,
        "provenance": {"origin": "manual", "label": "fictional"}
    }],
    "retrieval": {"scores": {"mem-1": 0.67}, "retrievalReason": "hybrid ranking"},
    "ledger_entries": 3,
}

class MeterlessBridgeTests(unittest.TestCase):
    def test_real_integration_contract_with_mocked_boundaries(self):
        with patch("guardian_zetaris.query_zetaris",
                   return_value={"records": [PERMISSION]}):
            out, _, events = run_guardian_with_memory(
                REQUEST, "fake-token", "SELECT sample", hmem_retriever=lambda _: HMEM)
        self.assertEqual(out["decision"], "ALLOW")
        self.assertEqual(out["action_state"], "UNKNOWN")
        self.assertEqual(out["memory_engine"], "official_meterless_hmem_reference")
        self.assertEqual(out["memory_context"][0]["source"], "synthetic:prior_conversation")
        self.assertFalse(out["memory_source_is_authority"])
        self.assertEqual(events[0]["kind"], "meterless_hmem_retrieval")

    def test_memory_cannot_override_missing_zetaris_permission(self):
        with patch("guardian_zetaris.query_zetaris",
                   return_value={"records": []}):
            out, _, events = run_guardian_with_memory(
                REQUEST, "fake-token", "SELECT sample", hmem_retriever=lambda _: HMEM)
        self.assertEqual(out["decision"], "ASK_CONFIRMATION")
        self.assertNotIn("simulated_tool_called", [ev["kind"] for ev in events])

    def test_revoked_permission_blocks_despite_memory(self):
        revoked = {**PERMISSION, "status": "REVOKED"}
        with patch("guardian_zetaris.query_zetaris",
                   return_value={"records": [PERMISSION, revoked]}):
            out, _, events = run_guardian_with_memory(
                REQUEST, "fake-token", "SELECT sample", outcome="CONFIRMED",
                hmem_retriever=lambda _: HMEM)
        self.assertEqual(out["decision"], "BLOCK")
        self.assertNotIn("simulated_tool_called", [ev["kind"] for ev in events])

if __name__ == "__main__":
    unittest.main()
