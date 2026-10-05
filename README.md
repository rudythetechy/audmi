# AudMi — Auditor's Microscope

AudMi is an offline-first supervisory analytics system that analyzes periodic SOC assessment submissions and helps human examiners identify evidence-backed operational gaps and prioritize records for manual review.

## Scope

- Execution-gap detection
- Negative-space detection
- Peer/context analysis
- Evidence traceability
- Supervisory review prioritization

## Boundaries

AudMi is not a SIEM, a real-time SOC, a SOC replacement, or a centralized monitoring platform. It does not make final compliance judgments. Findings use neutral terms such as potential execution gap, negative-space signal, unusual operational pattern, evidence divergence, and requires supervisory review.

## Deployment goal

Offline / air-gapped local deployment.

## Development status

Initial project scaffold. Analytics and application functionality are not implemented yet.

## Canonical Evidence Model

The canonical model defines seven identifier-linked entities:

- **CSE** contains assets, alerts, and cases through their `cse_id` references.
- **Asset** belongs to a CSE.
- **Alert** belongs to a CSE and references an asset.
- **Case** belongs to a CSE and references an alert.
- **Investigation**, **Escalation**, and **Remediation** each reference a case.

Workflow records are optional: a case may have no investigations, escalations, or remediation records. The model establishes evidence structure; analytics are not implemented.

## Synthetic validation data

AudMi's deterministic synthetic dataset supports controlled validation of future supervisory analytics. It includes seeded supervisory conditions for repeatable development and testing, with ground truth stored separately from operational records. It is synthetic and is not real NCIIPC or CSE data.

## Execution-gap analytics

The first execution-gap module detects high/critical cases with investigation evidence but no escalation, unusually short investigation durations using a robust log-duration median/MAD baseline, and assets with statistically elevated alert volume but sparse remediation coverage. These are potential supervisory signals, not compliance judgments, and require human review. Each finding includes its reason, baseline or observed criteria, and supporting record IDs.
