"""Canonical, dependency-free data structures for AudMi evidence records.

Relationships are represented by identifiers. Referential integrity across a
collection of records is the responsibility of future ingestion code.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar


def _required_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _utc_datetime(value: datetime, field_name: str) -> None:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    if value.utcoffset() != timezone.utc.utcoffset(value):
        raise ValueError(f"{field_name} must be expressed in UTC")


def _optional_utc_datetime(value: datetime | None, field_name: str) -> None:
    if value is not None:
        _utc_datetime(value, field_name)


def _not_before(later: datetime | None, earlier: datetime, field_name: str) -> None:
    if later is not None and later < earlier:
        raise ValueError(f"{field_name} must be on or after its start timestamp")


@dataclass(frozen=True, slots=True)
class CSE:
    cse_id: str
    name: str
    peer_group: str

    def __post_init__(self) -> None:
        for field_name in ("cse_id", "name", "peer_group"):
            _required_text(getattr(self, field_name), field_name)


@dataclass(frozen=True, slots=True)
class Asset:
    asset_id: str
    cse_id: str
    criticality: str
    asset_type: str

    def __post_init__(self) -> None:
        for field_name in ("asset_id", "cse_id", "criticality", "asset_type"):
            _required_text(getattr(self, field_name), field_name)


@dataclass(frozen=True, slots=True)
class Alert:
    alert_id: str
    cse_id: str
    asset_id: str
    severity: str
    category: str
    created_at: datetime
    closed_at: datetime | None = None

    SEVERITIES: ClassVar[frozenset[str]] = frozenset(
        {"informational", "low", "medium", "high", "critical"}
    )

    def __post_init__(self) -> None:
        for field_name in ("alert_id", "cse_id", "asset_id", "category"):
            _required_text(getattr(self, field_name), field_name)
        if self.severity not in self.SEVERITIES:
            raise ValueError(f"severity must be one of {sorted(self.SEVERITIES)}")
        _utc_datetime(self.created_at, "created_at")
        _optional_utc_datetime(self.closed_at, "closed_at")
        _not_before(self.closed_at, self.created_at, "closed_at")


@dataclass(frozen=True, slots=True)
class Case:
    case_id: str
    cse_id: str
    alert_id: str
    status: str
    opened_at: datetime
    closed_at: datetime | None = None

    STATUSES: ClassVar[frozenset[str]] = frozenset(
        {"new", "open", "in_progress", "closed", "resolved"}
    )

    def __post_init__(self) -> None:
        for field_name in ("case_id", "cse_id", "alert_id"):
            _required_text(getattr(self, field_name), field_name)
        if self.status not in self.STATUSES:
            raise ValueError(f"status must be one of {sorted(self.STATUSES)}")
        _utc_datetime(self.opened_at, "opened_at")
        _optional_utc_datetime(self.closed_at, "closed_at")
        _not_before(self.closed_at, self.opened_at, "closed_at")


@dataclass(frozen=True, slots=True)
class Investigation:
    investigation_id: str
    case_id: str
    started_at: datetime
    analyst_id: str
    evidence_count: int
    ended_at: datetime | None = None

    def __post_init__(self) -> None:
        for field_name in ("investigation_id", "case_id", "analyst_id"):
            _required_text(getattr(self, field_name), field_name)
        if isinstance(self.evidence_count, bool) or not isinstance(self.evidence_count, int):
            raise TypeError("evidence_count must be an integer")
        if self.evidence_count < 0:
            raise ValueError("evidence_count must be non-negative")
        _utc_datetime(self.started_at, "started_at")
        _optional_utc_datetime(self.ended_at, "ended_at")
        _not_before(self.ended_at, self.started_at, "ended_at")


@dataclass(frozen=True, slots=True)
class Escalation:
    escalation_id: str
    case_id: str
    escalation_type: str
    escalated_at: datetime

    def __post_init__(self) -> None:
        for field_name in ("escalation_id", "case_id", "escalation_type"):
            _required_text(getattr(self, field_name), field_name)
        _utc_datetime(self.escalated_at, "escalated_at")


@dataclass(frozen=True, slots=True)
class Remediation:
    remediation_id: str
    case_id: str
    action: str
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        for field_name in ("remediation_id", "case_id", "action"):
            _required_text(getattr(self, field_name), field_name)
        _optional_utc_datetime(self.completed_at, "completed_at")
