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

Replace the existing setup/run sections with this. It separates running the implemented prototype from the planned installation of the final offline product, without pretending the unfinished components magically exist.

````
## Setup and Installation

AudMi is being developed as an offline-first supervisory analytics tool. The repository currently contains the canonical evidence model, synthetic dataset generator, deterministic execution-gap analytics, and a Next.js demonstration interface.

The final product is intended to run locally in a controlled environment without requiring internet access, cloud services, or external AI APIs. The complete end-to-end installation workflow is still under development.

### 1. Prerequisites

For the current Python prototype:

- Git
- Python 3.11 or later
- A terminal or command prompt

For the optional local web demo:

- Node.js and npm
- A modern web browser

The current Python implementation uses the standard library. No additional Python packages are required to run its existing modules.

### 2. Clone the Repository

```bash
git clone https://github.com/rudythetechy/audmi.git
cd audmi
````

Verify that Python is installed:

```
python --version
```

If `python` is not recognized on Windows, try:

```
py --version
```

Use the appropriate Python command for the remaining steps.

### 3. Generate the Synthetic Dataset

AudMi uses deterministic synthetic SOC records for development and testing. No real NCIIPC or Critical Sector Entity data is included.

To regenerate the dataset using seed `42`, run:

```
python -m data.synthetic.generator --seed 42
```

The generated records are stored under:

```
data/synthetic/golden_dataset/
```

The dataset includes linked entities such as CSEs, assets, alerts, cases, investigations, escalations, and remediations. Seeded conditions and their expected labels are maintained separately in `ground_truth.json`.

Note: A copy of the synthetic dataset is already included in the repository, so regeneration is optional.

### 4. Run the Implemented Analytics

The current implementation supports deterministic execution-gap analysis.

Run:

```
python -m src.analytics.execution_gaps
```

The module reports counts of potential signals for supported conditions, including:

- Cases with missing escalation records
- Investigations with unusually short durations
- Repeated alerts without corresponding remediation records

These are rule-based signals for human review, not confirmed incidents, compliance violations, or measures of detection accuracy. Thresholds and detection performance have not yet been fully validated against the synthetic ground truth.

### 5. Run the Tests

Install `pytest` if it is not already available:

```
python -m pip install pytest
```

Run the test suite from the repository root:

```
python -m pytest -v
```

The tests cover the canonical evidence model, execution-gap analytics, and synthetic dataset generator.

### 6. Access the Web Demonstration

The hosted Vercel deployment is the demonstration interface. Use the deployment URL provided for the SIH submission.

The web interface uses mock synthetic data. It is separate from the Python analytics implementation and does not currently execute the Python detection modules.

To run the web demonstration locally for development:

```
cd web
npm install
npm run dev
```

Open the local development address printed by Next.js, normally:

```
http://localhost:3000
```

To create a production build of the web interface:

```
npm run build
```

Important: Running the web interface locally does not install or launch the complete supervisory analytics backend. The hosted and local web demonstrations do not establish that AudMi operates in an offline or air-gapped environment.

## Planned Final Product Installation and Deployment

The following describes the intended deployment workflow. It is an implementation plan, not a claim that the complete workflow is currently available.

### 1. Deployment Environment

The target deployment is a locally hosted Linux workstation or server within a controlled environment. The system is intended to operate without internet access, cloud dependencies, SaaS services, or external AI APIs.

The final infrastructure and supported operating systems will be confirmed during implementation and deployment testing.

### 2. Install the Application Components

The planned installation package will include:

- The supervisory analytics backend
- The canonical evidence model and schema validation
- The data ingestion and normalization pipeline
- Deterministic analytics and rule configuration
- Local storage and evidence traceability
- The review interface and findings export workflow
- Versioned application configuration and audit records

Containerized deployment using Docker Compose is a planned option. The final packaging method and dependency versions have not yet been finalized.

### 3. Configure Data Inputs

The planned ingestion layer will support periodic SOC submissions through supported structured formats, initially targeting CSV and JSON exports.

Incoming records will be mapped to AudMi's canonical evidence model. Validation will check required fields, identifiers, timestamps, relationships, and schema compatibility.

Invalid or incomplete records should produce a validation report rather than silently entering the analytics pipeline. Missing evidence will be interpreted according to explicit rules and the availability of the relevant source data.

External database or API integrations will be added only where required and supported by the deployment environment.

### 4. Execute Supervisory Analytics

The final workflow is intended to process validated submissions using deterministic, explainable rules.

Planned analytics include:

- Execution-gap analysis: Identify potentially missing or incomplete workflow steps.
- Negative-space analysis: Identify expected evidence or telemetry that is absent, where the required source data is available.
- Workflow pattern analysis: Surface repeated or potentially templated investigation patterns for review.
- Peer and contextual analysis: Compare entities only where the available data supports a meaningful comparison.
- Evidence-linked prioritization: Organize potential signals for manual examination and retain traceability to the supporting records.

The existing execution-gap module is implemented. The other capabilities remain planned and must not be treated as available until implemented and tested.

### 5. Review and Export Findings

The intended final product will allow an examiner to inspect each potential signal, review its supporting evidence, and decide whether further investigation is warranted.

A planned review workflow will include evidence references, rule identifiers, relevant timestamps, and traceable outputs. Offline export and exchange packaging are also planned.

AudMi is designed to assist human examination. It will not independently declare an entity compliant or non-compliant.

### 6. Verify Offline Operation

Before claiming air-gapped readiness, the packaged application must be installed and tested in an isolated environment with network access disabled.

Verification should establish that:

- Required dependencies are available locally.
- The application starts without contacting external services.
- Synthetic or approved local submissions can be processed.
- Analytics and evidence references remain available offline.
- Findings can be reviewed and exported without cloud services.
- Any optional local language model operates without external API calls.

Air-gapped operation, performance, and detection accuracy will be claimed only after the corresponding tests have been completed and documented.

## Current Implementation Status

| Component                                             | Status                               |
| ----------------------------------------------------- | ------------------------------------ |
| Canonical evidence model and JSON schema              | Implemented and tested               |
| Deterministic synthetic dataset generator             | Implemented and tested               |
| Execution-gap analytics                               | Implemented and tested               |
| Negative-space analytics                              | Planned                              |
| Peer and contextual analysis                          | Planned                              |
| Workflow pattern analysis                             | Planned                              |
| External data ingestion and validation pipeline       | Planned                              |
| Complete backend API and review workflow              | Planned                              |
| Prioritization and evidence-linked findings interface | Planned                              |
| Ground-truth-based precision and recall evaluation    | Planned                              |
| Offline packaging and air-gapped verification         | Planned                              |
| Next.js demonstration interface                       | Implemented with mock synthetic data |

The current repository is a research prototype. The hosted demonstration illustrates the intended user experience, while the Python modules provide the currently implemented evidence-model and analytics functionality. The complete offline product will require further implementation, integration, and validation.

```

**One correction before committing:** your existing repository layout still references `docs/ARCHITECTURE.md`. Since you decided to keep the HTML and PDF versions, update that entry to `docs/ARCHITECTURE.html` and `docs/AudMi_Architecture.pdf`. No need to resurrect a redundant Markdown architecture document just to satisfy an outdated path.
```

## Limitations

- Signals require human review; they are not findings of fault.
- Only the execution-gap module exists today; thresholds are not yet validated.
- No performance or accuracy results are published until they have been measured.

## Team

Elite Six · Smart India Hackathon 2026 · SIH26157 · Theme: Blockchain & Cybersecurity · Organization: NTRO
