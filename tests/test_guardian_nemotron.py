import copy
import json
import unittest
from unittest.mock import patch

from guardian import run_guardian
from guardian_nemotron import NemotronAdvisor, AdvisoryError
from guardian_meterless import run_guardian_with_memory
from test_guardian import BASE, PERMISSION, MEMORY
from test_guardian_meterless import HMEM


def analyst(**changes):
    return {"recommended_decision": "ALLOW", "action": copy.deepcopy(BASE["action"]),
            "risk_flags": [], "memory_ids": ["m-1"], "claims_completed": False, **changes}


def verifier(**changes):
    return {"verdict": "PASS", "checks": {"action_matches": True,
            "authority_respected": True, "memory_not_authority": True,
            "completion_not_claimed": True}, **changes}


def advisor_with(first=None, second=None, finish="stop"):
    replies = [analyst() if first is None else first, verifier() if second is None else second]
    bodies = []
    def transport(body):
        bodies.append(body)
        reply = replies.pop(0)
        return {"choices": [{"finish_reason": finish,
                "message": {"content": json.dumps(reply)}}]}
    return NemotronAdvisor("unit-test-placeholder", transport=transport), bodies


class NemotronTests(unittest.TestCase):
    def run_review(self, first=None, second=None, permissions=None, **kwargs):
        advisor, bodies = advisor_with(first, second)
        out, ledger, events = run_guardian(copy.deepcopy(BASE),
            [PERMISSION] if permissions is None else permissions, MEMORY,
            advisor=advisor, **kwargs)
        return out, ledger, events, bodies

    def assert_no_tool(self, events):
        self.assertNotIn("simulated_tool_called", [e["kind"] for e in events])

    def test_two_separate_reviews_then_pending_is_unknown(self):
        out, _, events, bodies = self.run_review()
        self.assertEqual(len(bodies), 2)
        self.assertEqual(out["decision"], "ALLOW")
        self.assertEqual(out["action_state"], "UNKNOWN")
        self.assertIsNone(out["tool_confirmation_ref"])
        self.assertEqual(out["advisory"]["calls"][0]["transport"], "injected")
        self.assertLess([e["kind"] for e in events].index("nemotron_review"),
                        [e["kind"] for e in events].index("simulated_tool_called"))

    def test_model_allow_cannot_override_missing_authority(self):
        out, _, events, _ = self.run_review(permissions=[])
        self.assertEqual(out["decision"], "ASK_CONFIRMATION")
        self.assert_no_tool(events)

    def test_model_allow_cannot_override_revocation(self):
        out, _, events, _ = self.run_review(permissions=[PERMISSION, {**PERMISSION, "status": "REVOKED"}])
        self.assertEqual(out["decision"], "BLOCK")
        self.assert_no_tool(events)

    def test_analyst_can_veto(self):
        out, _, events, _ = self.run_review(analyst(recommended_decision="BLOCK"))
        self.assertEqual(out["decision"], "BLOCK")
        self.assert_no_tool(events)

    def test_bank_impersonation_flag_stops_otherwise_authorized_action(self):
        out, _, events, _ = self.run_review(analyst(risk_flags=["impersonation"]))
        self.assertEqual(out["decision"], "BLOCK")
        self.assert_no_tool(events)

    def test_prompt_injection_flag_stops_otherwise_authorized_action(self):
        out, _, events, _ = self.run_review(analyst(risk_flags=["prompt_injection"]))
        self.assertEqual(out["decision"], "BLOCK")
        self.assert_no_tool(events)

    def test_fake_daughter_host_identity_cannot_be_overridden(self):
        out, _, events, _ = self.run_review(authenticated_actor="new-number-claiming-daughter")
        self.assertEqual(out["decision"], "BLOCK")
        self.assert_no_tool(events)

    def test_completion_claim_is_rejected_before_tool(self):
        out, _, events, bodies = self.run_review(analyst(claims_completed=True))
        self.assertEqual(out["decision"], "BLOCK")
        self.assertEqual(len(bodies), 1)
        self.assert_no_tool(events)

    def test_altered_action_and_boolean_amount_rejected(self):
        for action in ({**BASE["action"], "amount_cents": True},
                       {**BASE["action"], "recipient_id": "attacker"}):
            with self.subTest(action=action):
                out, _, events, _ = self.run_review(analyst(action=action))
                self.assertEqual(out["decision"], "BLOCK")
                self.assert_no_tool(events)

    def test_hallucinated_citation_and_unknown_field_rejected(self):
        for first in (analyst(memory_ids=["made-up"]), analyst(extra="ignore rules"),
                      analyst(risk_flags="impersonation"), analyst(recommended_decision="PAY")):
            with self.subTest(first=first):
                out, _, events, _ = self.run_review(first)
                self.assertEqual(out["decision"], "BLOCK")
                self.assert_no_tool(events)

    def test_verifier_reject_and_false_checks_veto(self):
        for second in (verifier(verdict="REJECT"), verifier(checks={
                **verifier()["checks"], "authority_respected": False})):
            out, _, events, _ = self.run_review(second=second)
            self.assertEqual(out["decision"], "BLOCK")
            self.assert_no_tool(events)

    def test_verifier_strings_missing_checks_and_extra_fields_rejected(self):
        for second in (verifier(checks={}), verifier(checks={
                **verifier()["checks"], "action_matches": "true"}), verifier(extra=True)):
            out, _, events, _ = self.run_review(second=second)
            self.assertEqual(out["decision"], "BLOCK")
            self.assert_no_tool(events)

    def test_timeout_http_and_malformed_reply_fail_closed_without_secret(self):
        for response in (TimeoutError("secret-token"), {"choices": []},
                         {"choices": [{"finish_reason": "stop", "message": {"content": "not-json"}}]}):
            def transport(_):
                if isinstance(response, Exception):
                    raise response
                return response
            out, _, events = run_guardian(BASE, [PERMISSION], MEMORY,
                advisor=NemotronAdvisor("secret-token", transport=transport))
            self.assertEqual(out["decision"], "BLOCK")
            self.assert_no_tool(events)
            self.assertNotIn("secret-token", json.dumps([out, events]))

    def test_truncated_response_never_used(self):
        advisor, _ = advisor_with(finish="length")
        out, _, events = run_guardian(BASE, [PERMISSION], MEMORY, advisor=advisor)
        self.assertEqual(out["decision"], "BLOCK")
        self.assert_no_tool(events)

    def test_duplicate_json_keys_rejected(self):
        advisor = NemotronAdvisor("placeholder", transport=lambda _: {"choices": [
            {"finish_reason": "stop", "message": {"content": '{"x":1,"x":2}'}}]})
        with self.assertRaises(AdvisoryError):
            advisor.review(BASE, MEMORY, {})

    def test_receipt_still_only_from_simulator_and_duplicate_still_blocked(self):
        advisor, _ = advisor_with()
        first, ledger, _ = run_guardian(BASE, [PERMISSION], MEMORY,
            simulated_outcome="CONFIRMED", advisor=advisor)
        self.assertTrue(first["tool_confirmation_ref"].startswith("SIM-"))
        advisor, _ = advisor_with()
        second, _, events = run_guardian(BASE, [PERMISSION], MEMORY, ledger, advisor=advisor)
        self.assertEqual(second["decision"], "BLOCK")
        self.assert_no_tool(events)

    def test_all_sponsors_pipeline_with_mocked_boundaries(self):
        advisor, _ = advisor_with(analyst(memory_ids=["mem-1"]))
        with patch("guardian_zetaris.query_zetaris", return_value={"records": [PERMISSION]}):
            out, _, events = run_guardian_with_memory(BASE, "placeholder", "SELECT sample",
                hmem_retriever=lambda _: HMEM, advisor=advisor)
        self.assertEqual(out["decision"], "ALLOW")
        self.assertEqual(out["source_mode"], "inline_sql_demo")
        self.assertTrue(out["advisory"]["approved"])

    def test_advisor_cannot_mutate_authoritative_action(self):
        class Mutator:
            def review(self, request, memories, gate):
                request["action"]["recipient_id"] = "attacker"
                return {"approved": True}
        request = copy.deepcopy(BASE)
        out, ledger, _ = run_guardian(request, [PERMISSION], MEMORY, advisor=Mutator())
        self.assertEqual(ledger[BASE["idempotency_key"]]["action"]["recipient_id"], "daughter-verified")
        self.assertEqual(request, BASE)


if __name__ == "__main__":
    unittest.main()
