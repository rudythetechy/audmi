import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "How to Use AudMi — Walkthrough & Workflow Guide",
  description:
    "Step-by-step guide for evaluators: navigate the AudMi supervisory analytics demo, explore findings, and understand execution gaps and negative-space analysis.",
};

const steps = [
  {
    title: "Open the demo dashboard",
    desc: "Navigate to the Interactive Demo page. You will see an overview of all sample Critical Sector Entities (CSEs) and their summary indicators.",
  },
  {
    title: "Select a sample CSE",
    desc: "Click on any entity in the sidebar or overview table. The dashboard updates to show that entity's assessment dimensions, findings, and metrics.",
  },
  {
    title: "Explore supervisory indicators",
    desc: "Each CSE shows scores across eight assessment dimensions — threat detection, investigation, escalation, incident response, security operations, governance, operational discipline, and cyber resilience. Indicators with lower scores or higher finding counts warrant closer attention.",
  },
  {
    title: "Open a flagged operational pattern",
    desc: "In the findings table, click on any row to open its detail panel. Flagged patterns include missing escalations, unusually short investigations, repeated alerts without remediation, and negative-space signals.",
  },
  {
    title: "Inspect the rationale and supporting record IDs",
    desc: "Each finding displays: the pattern description, the specific record IDs that support it, the contextual baseline used, and an explanation of why the pattern may warrant attention.",
  },
  {
    title: "Review the suggested priority",
    desc: "Findings are ranked by review priority (critical, high, moderate, low). The priority reflects the statistical significance and potential operational impact of the pattern — not a compliance judgment.",
  },
  {
    title: "Explore other dimensions and compare entities",
    desc: "Use the sidebar to switch between CSEs. Use the filter controls to narrow findings by category, dimension, or priority. Compare how similar patterns manifest across different entities in the peer group.",
  },
  {
    title: "Understand that a human examiner makes the final assessment",
    desc: "Every finding in AudMi is a potential signal, not a conclusion. The examiner reviews the evidence, applies professional judgment, and determines the appropriate supervisory response.",
  },
];

export default function HowToUsePage() {
  return (
    <>
      {/* Header */}
      <div className="page-header" id="how-to-use-header">
        <div className="container">
          <span className="section-label">Evaluator Guide</span>
          <h1 className="page-title">How to Use AudMi</h1>
          <p className="page-subtitle">
            A step-by-step walkthrough of the supervisory analytics demonstration, including how to explore findings, interpret signals, and understand the workflow.
          </p>
        </div>
      </div>

      {/* Notice */}
      <section className="section-sm" id="how-to-use-notice">
        <div className="container" style={{ maxWidth: 880 }}>
          <div className="alert-banner alert-banner-warning" id="demo-notice-banner">
            <span className="alert-banner-icon">⚠️</span>
            <div>
              <strong>Online Demo Notice:</strong> The interactive demonstration uses synthetic, illustrative data. It is not connected to any real SOC environment, CSE, or government network. All metrics, findings, and record IDs are fictional and exist to demonstrate the intended workflow.
            </div>
          </div>
        </div>
      </section>

      {/* Steps */}
      <section className="section" id="walkthrough-steps">
        <div className="container" style={{ maxWidth: 880 }}>
          <div className="section-header text-left" style={{ margin: "0 0 var(--sp-8)" }}>
            <span className="section-label">Walkthrough</span>
            <h2 className="section-title" style={{ textAlign: "left" }}>Step-by-Step Guide</h2>
          </div>

          <div className="step-list">
            {steps.map((step, i) => (
              <div className="step" key={i} id={`step-${i + 1}`}>
                <div className="step-number">{i + 1}</div>
                <div className="step-content">
                  <h3 className="step-title">{step.title}</h3>
                  <p className="step-desc">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow diagram */}
      <section className="section" id="workflow-diagram" style={{ background: "var(--white)" }}>
        <div className="container" style={{ maxWidth: 880 }}>
          <div className="section-header text-left" style={{ margin: "0 0 var(--sp-8)" }}>
            <span className="section-label">Architecture</span>
            <h2 className="section-title" style={{ textAlign: "left" }}>AudMi Workflow</h2>
            <p className="section-subtitle" style={{ textAlign: "left", margin: 0 }}>
              The analytical pipeline processes structured SOC assessment submissions through normalization, analysis, and prioritization stages before presenting findings to a human examiner.
            </p>
          </div>

          <div className="card mb-8">
            <div className="workflow">
              {[
                "Periodic CSE SOC Submissions",
                "Ingestion & Validation",
                "Normalized Evidence Model",
                "Supervisory Analytics",
                "Evidence-Backed Findings",
                "Prioritized Review Queue",
                "Human Examiner",
              ].map((step, i, arr) => (
                <span key={step} style={{ display: "contents" }}>
                  <span className="workflow-step">{step}</span>
                  {i < arr.length - 1 && <span className="workflow-arrow">→</span>}
                </span>
              ))}
            </div>
          </div>

          <div className="alert-banner alert-banner-info">
            <span className="alert-banner-icon">ℹ️</span>
            <div>
              In the online demo, the analytics pipeline is simulated with pre-computed synthetic results. The actual Python analytics engine is part of the planned offline application.
            </div>
          </div>
        </div>
      </section>

      {/* Concepts */}
      <section className="section" id="concepts">
        <div className="container" style={{ maxWidth: 880 }}>
          <div className="section-header text-left" style={{ margin: "0 0 var(--sp-8)" }}>
            <span className="section-label">Key Concepts</span>
            <h2 className="section-title" style={{ textAlign: "left" }}>Understanding the Signal Types</h2>
          </div>

          <div className="grid-2">
            <div className="card">
              <h3 className="feature-title" style={{ color: "var(--amber-600)" }}>Execution Gaps</h3>
              <p className="feature-desc">
                An <strong>execution gap</strong> is a pattern where expected workflow steps are absent from the evidence record. For example, a high-severity case has investigation records but no corresponding escalation. The gap is between what the entity&apos;s procedures indicate should happen and what the submitted records show.
              </p>
              <div className="mt-4" style={{ fontSize: "var(--text-sm)", color: "var(--text-muted)" }}>
                <strong>Examples:</strong>
                <ul style={{ paddingLeft: "var(--sp-5)", listStyle: "disc", marginTop: "var(--sp-2)" }}>
                  <li>High-severity case investigated but not escalated</li>
                  <li>Investigation closed in seconds when peers take hours</li>
                  <li>Repeated alerts on an asset with no remediation records</li>
                </ul>
              </div>
            </div>

            <div className="card">
              <h3 className="feature-title" style={{ color: "var(--teal-600)" }}>Negative Space</h3>
              <p className="feature-desc">
                A <strong>negative-space signal</strong> is about what is <em>not</em> present. Instead of flagging an anomalous record, it flags the absence of expected records. For example, critical assets with no alerts at all while similar assets in the same entity have normal detection activity.
              </p>
              <div className="mt-4" style={{ fontSize: "var(--text-sm)", color: "var(--text-muted)" }}>
                <strong>Examples:</strong>
                <ul style={{ paddingLeft: "var(--sp-5)", listStyle: "disc", marginTop: "var(--sp-2)" }}>
                  <li>Critical assets with zero detection activity</li>
                  <li>Time periods with no cases while peer entities remain active</li>
                  <li>Expected record types that are entirely absent</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section-sm" id="how-to-use-cta" style={{ textAlign: "center" }}>
        <div className="container">
          <Link href="/demo" className="btn btn-accent btn-lg" id="cta-try-demo">
            Try the Interactive Demo →
          </Link>
        </div>
      </section>
    </>
  );
}
