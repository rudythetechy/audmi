import json
import unittest
from datetime import datetime

from data.synthetic.generator import DEFAULT_OUTPUT_DIR, OUTPUT_FILES, generate_dataset, write_dataset
from src.normalization.evidence_model import (
    Alert,
    Asset,
    Case,
    CSE,
    Escalation,
    Investigation,
    Remediation,
)


class SyntheticGeneratorTests(unittest.TestCase):
    def test_same_seed_produces_byte_identical_files(self) -> None:
        dataset_a = generate_dataset(42)
        dataset_b = generate_dataset(42)
        first = write_dataset(dataset_a, DEFAULT_OUTPUT_DIR)
        first_bytes = {filename: (first / filename).read_bytes() for filename in OUTPUT_FILES}
        second = write_dataset(dataset_b, DEFAULT_OUTPUT_DIR)
        for filename in OUTPUT_FILES:
            self.assertEqual(first_bytes[filename], (second / filename).read_bytes(), filename)

    def test_expected_counts_and_unique_ids(self) -> None:
        dataset = generate_dataset(42)
        id_fields = (
            (dataset.cse, "cse_id"),
            (dataset.assets, "asset_id"),
            (dataset.alerts, "alert_id"),
            (dataset.cases, "case_id"),
            (dataset.investigations, "investigation_id"),
            (dataset.escalations, "escalation_id"),
            (dataset.remediations, "remediation_id"),
        )
        identifiers = []
        for records, id_field in id_fields:
            values = [getattr(record, id_field) for record in records]
            self.assertEqual(len(values), len(set(values)))
            identifiers.extend(values)
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(
            [len(dataset.cse), len(dataset.assets), len(dataset.alerts), len(dataset.cases),
             len(dataset.investigations), len(dataset.escalations), len(dataset.remediations)],
            [6, 300, 10_000, 2_000, 1_500, 300, 100],
        )

    def test_references_and_timestamps_are_valid(self) -> None:
        dataset = generate_dataset(19)
        cse_ids = {x.cse_id for x in dataset.cse}
        assets = {x.asset_id: x for x in dataset.assets}
        alerts = {x.alert_id: x for x in dataset.alerts}
        cases = {x.case_id: x for x in dataset.cases}
        for asset in dataset.assets:
            self.assertIn(asset.cse_id, cse_ids)
        for alert in dataset.alerts:
            self.assertIn(alert.cse_id, cse_ids)
            self.assertEqual(assets[alert.asset_id].cse_id, alert.cse_id)
            self.assertIsNotNone(alert.created_at.tzinfo)
            if alert.closed_at:
                self.assertGreaterEqual(alert.closed_at, alert.created_at)
        for case in dataset.cases:
            self.assertEqual(alerts[case.alert_id].cse_id, case.cse_id)
            self.assertGreaterEqual(case.opened_at, alerts[case.alert_id].created_at)
            if case.closed_at:
                self.assertGreaterEqual(case.closed_at, case.opened_at)
        for record in dataset.investigations:
            case = cases[record.case_id]
            self.assertGreaterEqual(record.started_at, case.opened_at)
            if record.ended_at:
                self.assertGreaterEqual(record.ended_at, record.started_at)
                if case.closed_at:
                    self.assertLessEqual(record.ended_at, case.closed_at)
        for record in dataset.escalations:
            self.assertIn(record.case_id, cases)
            self.assertGreaterEqual(record.escalated_at, cases[record.case_id].opened_at)
        for record in dataset.remediations:
            self.assertIn(record.case_id, cases)
            if record.completed_at:
                self.assertGreaterEqual(record.completed_at, cases[record.case_id].opened_at)

    def test_ground_truth_references_exist_and_conditions_are_present(self) -> None:
        dataset = generate_dataset(42)
        ids = {
            record_id
            for records, field in (
                (dataset.cse, "cse_id"), (dataset.assets, "asset_id"),
                (dataset.alerts, "alert_id"), (dataset.cases, "case_id"),
                (dataset.investigations, "investigation_id"),
                (dataset.escalations, "escalation_id"),
                (dataset.remediations, "remediation_id"),
            )
            for record_id in (getattr(record, field) for record in records)
        }
        asset_ids = {x.asset_id for x in dataset.assets}
        condition_types = {x["condition_type"] for x in dataset.ground_truth["conditions"]}
        self.assertTrue({
            "missing_escalation", "repeated_alerts_without_remediation",
            "unusually_short_investigation", "negative_space_low_activity",
        }.issubset(condition_types))
        for condition in dataset.ground_truth["conditions"]:
            self.assertIn(condition["cse_id"], {x.cse_id for x in dataset.cse})
            self.assertTrue(set(condition.get("record_ids", [])).issubset(ids))
            self.assertTrue(set(condition.get("asset_ids", [])).issubset(asset_ids))

        escalation_case_ids = {x.case_id for x in dataset.escalations}
        remediation_case_ids = {x.case_id for x in dataset.remediations}
        alert_count_by_asset = {}
        for alert in dataset.alerts:
            alert_count_by_asset[alert.asset_id] = alert_count_by_asset.get(alert.asset_id, 0) + 1
        for condition in dataset.ground_truth["conditions"]:
            if condition["condition_type"] == "missing_escalation":
                self.assertTrue(all(x not in escalation_case_ids for x in condition["record_ids"]))
            elif condition["condition_type"] == "repeated_alerts_without_remediation":
                self.assertTrue(all(x not in remediation_case_ids for x in condition["record_ids"]))
            elif condition["condition_type"] == "negative_space_low_activity":
                self.assertTrue(all(alert_count_by_asset.get(x, 0) <= 1 for x in condition["asset_ids"]))

    def test_json_records_validate_against_canonical_models(self) -> None:
        dataset = generate_dataset(42)
        output_dir = write_dataset(dataset, DEFAULT_OUTPUT_DIR)
        for filename in OUTPUT_FILES:
            self.assertTrue((output_dir / filename).is_file())
        files_and_models = (
            ("cse.json", CSE), ("assets.json", Asset), ("alerts.json", Alert),
            ("cases.json", Case), ("investigations.json", Investigation),
            ("escalations.json", Escalation), ("remediations.json", Remediation),
        )
        for filename, model in files_and_models:
            rows = json.loads((output_dir / filename).read_text(encoding="utf-8"))
            for row in rows:
                for key, value in row.items():
                    if key.endswith("_at") and value is not None:
                        row[key] = datetime.fromisoformat(value.replace("Z", "+00:00"))
                model(**row)


if __name__ == "__main__":
    unittest.main()
