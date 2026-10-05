"""Explainable execution-gap signals over AudMi's canonical evidence records.

Signals are potential supervisory indicators only. They are not compliance
judgments and require review by a human examiner.
"""

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, TypeVar

from src.normalization.evidence_model import (
    Alert,
    Asset,
    Case,
    CSE,
    Escalation,
    Investigation,
    Remediation,
)


DEFAULT_DATASET_DIR = (
    Path(__file__).resolve().parents[2] / "data" / "synthetic" / "golden_dataset"
)
SHORT_DURATION_SIGMA_MULTIPLIER = 3.5
REPEATED_ALERT_SIGMA_MULTIPLIER = 3.0
MIN_REPEAT_CASES = 3
MAX_REMEDIATION_COVERAGE_FOR_SIGNAL = 0.10
MIN_DURATION_BASELINE_SIZE = 8

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class EvidenceRecords:
    cse: tuple[CSE, ...]
    assets: tuple[Asset, ...]
    alerts: tuple[Alert, ...]
    cases: tuple[Case, ...]
    investigations: tuple[Investigation, ...] = ()
    escalations: tuple[Escalation, ...] = ()
    remediations: tuple[Remediation, ...] = ()


@dataclass(frozen=True, slots=True)
class Finding:
    signal_id: str
    signal_type: str
    cse_id: str
    reason: str
    supporting_record_ids: tuple[str, ...]
    case_id: str | None = None
    alert_id: str | None = None
    severity: str | None = None
    investigation_id: str | None = None
    duration_seconds: float | None = None
    baseline: dict[str, Any] | None = None
    asset_id: str | None = None
    alert_ids: tuple[str, ...] = ()
    case_ids: tuple[str, ...] = ()
    remediation_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation of the finding."""
        return {
            "signal_id": self.signal_id,
            "signal_type": self.signal_type,
            "cse_id": self.cse_id,
            "case_id": self.case_id,
            "alert_id": self.alert_id,
            "severity": self.severity,
            "investigation_id": self.investigation_id,
            "duration_seconds": self.duration_seconds,
            "baseline": self.baseline,
            "asset_id": self.asset_id,
            "alert_ids": list(self.alert_ids),
            "case_ids": list(self.case_ids),
            "remediation_ids": list(self.remediation_ids),
            "reason": self.reason,
            "supporting_record_ids": list(self.supporting_record_ids),
        }


def _parse_timestamp_fields(row: dict[str, Any], names: Iterable[str]) -> dict[str, Any]:
    parsed = dict(row)
    for name in names:
        value = parsed.get(name)
        if isinstance(value, str):
            parsed[name] = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed


def _read_model_records(
    dataset_dir: Path,
    filename: str,
    model: type[T],
    timestamp_fields: tuple[str, ...] = (),
    *,
    optional: bool = False,
) -> tuple[T, ...]:
    path = dataset_dir / filename
    if not path.exists():
        if optional:
            return ()
        raise FileNotFoundError(f"Required evidence file is missing: {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        if optional:
            return ()
        raise ValueError(f"Could not read required evidence file: {path}") from None
    if not isinstance(raw, list):
        if optional:
            return ()
        raise ValueError(f"Evidence file must contain a JSON array: {path}")

    records: list[T] = []
    for row in raw:
        if not isinstance(row, dict):
            continue
        try:
            records.append(model(**_parse_timestamp_fields(row, timestamp_fields)))
        except (KeyError, TypeError, ValueError):
            # A malformed optional workflow row cannot invalidate other records.
            continue
    return tuple(records)


def load_evidence(dataset_dir: str | Path = DEFAULT_DATASET_DIR) -> EvidenceRecords:
    """Load canonical JSON evidence; absent or malformed workflow files are empty."""
    root = Path(dataset_dir)
    return EvidenceRecords(
        cse=_read_model_records(root, "cse.json", CSE),
        assets=_read_model_records(root, "assets.json", Asset),
        alerts=_read_model_records(
            root, "alerts.json", Alert, ("created_at", "closed_at")
        ),
        cases=_read_model_records(root, "cases.json", Case, ("opened_at", "closed_at")),
        investigations=_read_model_records(
            root,
            "investigations.json",
            Investigation,
            ("started_at", "ended_at"),
            optional=True,
        ),
        escalations=_read_model_records(
            root, "escalations.json", Escalation, ("escalated_at",), optional=True
        ),
        remediations=_read_model_records(
            root, "remediations.json", Remediation, ("completed_at",), optional=True
        ),
    )


def _median_absolute_deviation(values: list[float]) -> tuple[float, float]:
    median = statistics.median(values)
    mad = statistics.median(abs(value - median) for value in values)
    return median, mad


def _duration_baseline(
    investigations: tuple[Investigation, ...],
) -> tuple[float, dict[str, Any]] | None:
    durations = [
        (item.ended_at - item.started_at).total_seconds()
        for item in investigations
        if item.ended_at is not None
        and item.ended_at > item.started_at
    ]
    if len(durations) < MIN_DURATION_BASELINE_SIZE:
        return None

    # Log duration makes multiplicative differences comparable. The lower
    # robust fence is derived from the cohort's median and MAD, not a fixed time.
    log_durations = [math.log(value) for value in durations]
    log_median, log_mad = _median_absolute_deviation(log_durations)
    robust_sigma = 1.4826 * log_mad
    lower_log_fence = log_median - SHORT_DURATION_SIGMA_MULTIPLIER * robust_sigma
    threshold_seconds = math.exp(lower_log_fence)
    baseline = {
        "method": "lower robust fence on log duration: median - 3.5 * 1.4826 * MAD",
        "population": "all completed investigations in the supplied evidence",
        "sample_count": len(durations),
        "geometric_median_seconds": round(math.exp(log_median), 3),
        "log_duration_mad": round(log_mad, 6),
        "sigma_multiplier": SHORT_DURATION_SIGMA_MULTIPLIER,
        "lower_threshold_seconds": round(threshold_seconds, 3),
    }
    return threshold_seconds, baseline


def _find_missing_escalations(records: EvidenceRecords) -> list[Finding]:
    alerts = {item.alert_id: item for item in records.alerts}
    investigations_by_case: dict[str, list[Investigation]] = defaultdict(list)
    for item in records.investigations:
        investigations_by_case[item.case_id].append(item)
    escalated_cases = {item.case_id for item in records.escalations}

    findings: list[Finding] = []
    for case in records.cases:
        alert = alerts.get(case.alert_id)
        investigations = investigations_by_case.get(case.case_id, [])
        if (
            alert is None
            or case.cse_id != alert.cse_id
            or alert.severity not in {"high", "critical"}
            or not investigations
            or case.case_id in escalated_cases
        ):
            continue
        supporting = (case.case_id, alert.alert_id) + tuple(
            item.investigation_id
            for item in sorted(investigations, key=lambda value: value.investigation_id)
        )
        findings.append(
            Finding(
                signal_id=f"EXG-MISSING-ESCALATION-{case.case_id}",
                signal_type="missing_escalation",
                cse_id=case.cse_id,
                case_id=case.case_id,
                alert_id=alert.alert_id,
                severity=alert.severity,
                reason=(
                    "Potential execution gap: high-severity case has investigation "
                    "evidence but no corresponding escalation record."
                ),
                supporting_record_ids=supporting,
            )
        )
    return findings


def _find_short_investigations(records: EvidenceRecords) -> list[Finding]:
    computed = _duration_baseline(records.investigations)
    if computed is None:
        return []
    threshold_seconds, baseline = computed
    cases = {item.case_id: item for item in records.cases}
    alerts = {item.alert_id: item for item in records.alerts}

    findings: list[Finding] = []
    for investigation in records.investigations:
        if investigation.ended_at is None:
            continue
        duration = (investigation.ended_at - investigation.started_at).total_seconds()
        case = cases.get(investigation.case_id)
        alert = alerts.get(case.alert_id) if case is not None else None
        if case is None or alert is None or case.cse_id != alert.cse_id:
            continue
        if duration >= threshold_seconds:
            continue
        supporting = (investigation.investigation_id, case.case_id, alert.alert_id)
        findings.append(
            Finding(
                signal_id=f"EXG-SHORT-INVESTIGATION-{investigation.investigation_id}",
                signal_type="unusually_short_investigation",
                cse_id=case.cse_id,
                investigation_id=investigation.investigation_id,
                case_id=case.case_id,
                alert_id=alert.alert_id,
                severity=alert.severity,
                duration_seconds=round(duration, 3),
                baseline=baseline,
                reason=(
                    "Potential execution gap: investigation duration is substantially "
                    "below the observed contextual baseline."
                ),
                supporting_record_ids=supporting,
            )
        )
    return findings


def _find_repeated_alerts_without_remediation(records: EvidenceRecords) -> list[Finding]:
    cse_by_id = {item.cse_id: item for item in records.cse}
    assets_by_id = {item.asset_id: item for item in records.assets}
    alerts_by_id = {item.alert_id: item for item in records.alerts}
    alerts_by_asset: dict[str, list[Alert]] = defaultdict(list)
    assets_by_cse: dict[str, list[Asset]] = defaultdict(list)
    for asset in records.assets:
        assets_by_cse[asset.cse_id].append(asset)
    for alert in records.alerts:
        asset = assets_by_id.get(alert.asset_id)
        if asset is None or asset.cse_id != alert.cse_id:
            continue
        alerts_by_asset[asset.asset_id].append(alert)

    cases_by_asset: dict[str, list[Case]] = defaultdict(list)
    for case in records.cases:
        alert = alerts_by_id.get(case.alert_id)
        if alert is None or alert.cse_id != case.cse_id:
            continue
        cases_by_asset[alert.asset_id].append(case)
    remediations_by_case: dict[str, list[Remediation]] = defaultdict(list)
    for item in records.remediations:
        remediations_by_case[item.case_id].append(item)

    asset_alert_counts_by_cse: dict[str, list[float]] = defaultdict(list)
    for cse_id, assets in assets_by_cse.items():
        for asset in assets:
            asset_alert_counts_by_cse[cse_id].append(float(len(alerts_by_asset[asset.asset_id])))

    upper_fences: dict[str, tuple[float, float, float]] = {}
    for cse_id, counts in asset_alert_counts_by_cse.items():
        if len(counts) < 5:
            continue
        median, mad = _median_absolute_deviation(counts)
        robust_sigma = 1.4826 * mad
        statistical_fence = median + REPEATED_ALERT_SIGMA_MULTIPLIER * robust_sigma
        # Require both a robust upper-tail outlier and at least twice the CSE's
        # typical asset volume, reducing flags from ordinary count variation.
        upper_fences[cse_id] = (max(statistical_fence, median * 2), median, mad)

    findings: list[Finding] = []
    for asset in sorted(records.assets, key=lambda value: value.asset_id):
        fence_data = upper_fences.get(asset.cse_id)
        if fence_data is None:
            continue
        upper_fence, median_count, mad_count = fence_data
        asset_alerts = sorted(alerts_by_asset[asset.asset_id], key=lambda value: value.alert_id)
        asset_cases = sorted(cases_by_asset[asset.asset_id], key=lambda value: value.case_id)
        if len(asset_alerts) <= upper_fence or len(asset_cases) < MIN_REPEAT_CASES:
            continue

        covered_cases = [case for case in asset_cases if remediations_by_case.get(case.case_id)]
        coverage = len(covered_cases) / len(asset_cases)
        if coverage > MAX_REMEDIATION_COVERAGE_FOR_SIGNAL:
            continue

        remediation_records = sorted(
            (item for case in asset_cases for item in remediations_by_case.get(case.case_id, [])),
            key=lambda value: value.remediation_id,
        )
        alert_ids = tuple(item.alert_id for item in asset_alerts)
        case_ids = tuple(item.case_id for item in asset_cases)
        remediation_ids = tuple(item.remediation_id for item in remediation_records)
        supporting = (asset.asset_id,) + alert_ids + case_ids + remediation_ids
        baseline = {
            "alert_count_method": "per-CSE median + 3 * 1.4826 * MAD across assets",
            "asset_alert_count_median": median_count,
            "asset_alert_count_mad": mad_count,
            "repeated_alert_upper_fence": round(upper_fence, 3),
            "minimum_multiple_of_cse_median": 2.0,
            "observed_alert_count": len(asset_alerts),
            "minimum_case_count": MIN_REPEAT_CASES,
            "observed_case_count": len(asset_cases),
            "remediation_coverage": round(coverage, 4),
            "maximum_coverage_for_signal": MAX_REMEDIATION_COVERAGE_FOR_SIGNAL,
        }
        cse_name = cse_by_id.get(asset.cse_id)
        cse_id = cse_name.cse_id if cse_name is not None else asset.cse_id
        findings.append(
            Finding(
                signal_id=f"EXG-REPEATED-LOW-REMEDIATION-{asset.asset_id}",
                signal_type="repeated_alerts_without_remediation",
                cse_id=cse_id,
                asset_id=asset.asset_id,
                alert_ids=alert_ids,
                case_ids=case_ids,
                remediation_ids=remediation_ids,
                baseline=baseline,
                reason=(
                    "Potential execution gap: this asset has alert volume above the "
                    "CSE's robust asset-level baseline, while remediation evidence "
                    "covers no more than 10% of its associated cases."
                ),
                supporting_record_ids=supporting,
            )
        )
    return findings


def analyze_evidence(records: EvidenceRecords) -> list[Finding]:
    """Return stable, evidence-backed execution-gap findings for supplied records."""
    # Keep valid canonical records and tolerate missing or malformed optional
    # workflow entries in partial hand-built inputs.
    records = EvidenceRecords(
        cse=tuple(item for item in (records.cse or ()) if isinstance(item, CSE)),
        assets=tuple(item for item in (records.assets or ()) if isinstance(item, Asset)),
        alerts=tuple(item for item in (records.alerts or ()) if isinstance(item, Alert)),
        cases=tuple(item for item in (records.cases or ()) if isinstance(item, Case)),
        investigations=tuple(
            item for item in (records.investigations or ()) if isinstance(item, Investigation)
        ),
        escalations=tuple(
            item for item in (records.escalations or ()) if isinstance(item, Escalation)
        ),
        remediations=tuple(
            item for item in (records.remediations or ()) if isinstance(item, Remediation)
        ),
    )
    findings = (
        _find_missing_escalations(records)
        + _find_short_investigations(records)
        + _find_repeated_alerts_without_remediation(records)
    )
    return sorted(findings, key=lambda item: (item.signal_type, item.cse_id, item.signal_id))


def detect_execution_gaps(
    dataset_dir: str | Path = DEFAULT_DATASET_DIR,
) -> list[Finding]:
    """Load canonical JSON records and detect potential execution gaps."""
    return analyze_evidence(load_evidence(dataset_dir))


if __name__ == "__main__":
    findings = detect_execution_gaps()
    counts: dict[str, int] = defaultdict(int)
    for finding in findings:
        counts[finding.signal_type] += 1
    print(json.dumps({"finding_counts": dict(sorted(counts.items()))}, indent=2))
