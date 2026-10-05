import unittest
from datetime import datetime, timedelta, timezone

from src.normalization.evidence_model import (
    Alert,
    Asset,
    Case,
    CSE,
    Escalation,
    Investigation,
    Remediation,
)


UTC = timezone.utc
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


class EvidenceModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cse = CSE("cse-1", "Example CSE", "regional")
        self.asset = Asset("asset-1", self.cse.cse_id, "critical", "server")
        self.alert = Alert(
            "alert-1", self.cse.cse_id, self.asset.asset_id, "high", "malware", NOW
        )
        self.case = Case("case-1", self.cse.cse_id, self.alert.alert_id, "open", NOW)

    def test_valid_cse_creation(self) -> None:
        self.assertEqual(self.cse.name, "Example CSE")

    def test_valid_asset_linked_to_cse(self) -> None:
        self.assertEqual(self.asset.cse_id, self.cse.cse_id)

    def test_valid_alert_linked_to_cse_and_asset(self) -> None:
        self.assertEqual((self.alert.cse_id, self.alert.asset_id), (self.cse.cse_id, self.asset.asset_id))

    def test_valid_case_linked_to_alert(self) -> None:
        self.assertEqual(self.case.alert_id, self.alert.alert_id)

    def test_investigation_linked_to_case(self) -> None:
        investigation = Investigation("investigation-1", self.case.case_id, NOW, "analyst-1", 3)
        self.assertEqual(investigation.case_id, self.case.case_id)

    def test_escalation_linked_to_case(self) -> None:
        escalation = Escalation("escalation-1", self.case.case_id, "management", NOW)
        self.assertEqual(escalation.case_id, self.case.case_id)

    def test_remediation_linked_to_case(self) -> None:
        remediation = Remediation("remediation-1", self.case.case_id, "isolate host")
        self.assertEqual(remediation.case_id, self.case.case_id)

    def test_negative_evidence_count_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Investigation("investigation-1", self.case.case_id, NOW, "analyst-1", -1)

    def test_invalid_timestamp_ordering_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Alert(
                "alert-2", self.cse.cse_id, self.asset.asset_id,
                "high", "malware", NOW, NOW - timedelta(seconds=1),
            )
        with self.assertRaises(ValueError):
            Investigation(
                "investigation-2", self.case.case_id,
                NOW, "analyst-1", 0, ended_at=NOW - timedelta(seconds=1),
            )

    def test_utc_awareness_is_required(self) -> None:
        with self.assertRaises(ValueError):
            Alert(
                "alert-3", self.cse.cse_id, self.asset.asset_id,
                "high", "malware", datetime(2026, 1, 1, 12, 0),
            )

    def test_missing_optional_workflow_records_remain_valid(self) -> None:
        # Creating the CSE, asset, alert, and case does not require any workflow children.
        self.assertEqual(self.case.status, "open")
        self.assertIsNone(self.alert.closed_at)


if __name__ == "__main__":
    unittest.main()
