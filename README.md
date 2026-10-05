# AudMi: Auditor's Microscope

**Supervisory Analytics for SOC Assessment** · SIH26157 (SAT-SA) · NTRO · Team Elite Six

AudMi is an offline-first supervisory analytics tool. It analyzes periodic SOC alert and case-management submissions and helps a human examiner identify evidence-backed operational gaps and prioritize records for manual review. It is not a SIEM, a real-time SOC, a SOC replacement or a monitoring platform, and it makes no compliance judgments. Findings are worded as potential supervisory signals that require human review.

## Current status

This is a research prototype for SIH 2026. All data is **synthetic**; no real NCIIPC or CSE data is used. Air-gapped operation is the deployment goal and has **not** been verified yet.

| Area | Status |
|---|---|
| Canonical evidence model (7 entities) and JSON schema | Implemented, tested |
| Deterministic synthetic dataset generator with seeded conditions and separate ground truth | Implemented, tested |
| Execution-gap analytics: missing escalation, unusually short investigation, repeated alerts without remediation | Implemented, tested |
| Negative-space analytics | Planned |
| Peer / context analysis | Planned |
| Workflow pattern analysis | Planned |
| Ingestion of external CSV/JSON/DB exports | Planned |
| Prioritization, review queue, explainability layer | Planned |
| Validation against ground truth (precision / recall) | Planned; no results yet |
| Optional local SLM, SATPACK offline exchange | Planned |
| Web demo (Next.js, mock synthetic data) | Implemented; does not run the Python analytics and does not demonstrate offline operation |

## Repository layout

```
src/
  normalization/evidence_model.py   canonical entities
  analytics/execution_gaps.py       execution-gap detection
  ingestion/ evidence/ explainability/ prioritization/ review/ validation/   scaffolded modules
data/
  schemas/core-evidence.schema.json
  synthetic/generator.py            deterministic generator
  synthetic/golden_dataset/         generated records + ground_truth.json
tests/                              24 unit tests
web/                                Next.js demo site
docs/ARCHITECTURE.md                intended architecture
```

## Canonical evidence model

Seven identifier-linked entities: CSE, Asset, Alert, Case, Investigation, Escalation, Remediation. A case may have no investigation, escalation or remediation records; absence is meaningful for the analytics.

## Setup and run (Python)

Requires Python 3.11+ (tested on 3.13). The current code uses only the standard library, so no packages need installing.

```bash
git clone https://github.com/rudythetechy/audmi.git
cd audmi

# regenerate the deterministic synthetic dataset (optional; a copy is committed)
python -m data.synthetic.generator --seed 42

# run the execution-gap analytics on the dataset
python -m src.analytics.execution_gaps

# run the tests
python -m unittest tests.test_execution_gaps tests.test_evidence_model tests.test_synthetic_generator
```

The analytics command prints counts of potential signals by type. These counts show what the rules flag on synthetic data. They are not accuracy figures, and thresholds still need tuning against the ground truth.

## Setup and run (web demo)

```bash
cd web
npm install
npm run dev        # http://localhost:3000
```

The demo uses mock synthetic data and shows a notice that it does not demonstrate air-gapped operation.

## Synthetic validation data

`data/synthetic/golden_dataset/` holds a seeded dataset (seed 42: 6 CSEs, 300 assets, 10,000 alerts, 2,000 cases, 1,500 investigations, 300 escalations, 100 remediations). Seeded supervisory conditions are recorded separately in `ground_truth.json`, and operational records carry no labels, so detection can be scored fairly. The dataset is synthetic and is not real NCIIPC or CSE data.

## Deployment goal

Offline / air-gapped local deployment: no internet, cloud, SaaS or external AI API dependency. The core system must run without any language model. A local model, if added, may only help explain findings. Offline operation will be claimed only after it is tested on an isolated machine.

## Limitations

- Signals require human review; they are not findings of fault.
- Only the execution-gap module exists today; thresholds are not yet validated.
- No performance or accuracy results are published until they have been measured.

## Team

Elite Six · Smart India Hackathon 2026 · SIH26157 · Theme: Blockchain & Cybersecurity · Organization: NTRO
