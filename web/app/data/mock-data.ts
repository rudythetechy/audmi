/**
 * Synthetic demo data for AudMi online demonstration.
 *
 * All data below is illustrative. It is not connected to any real
 * CSE, SOC, SIEM, or government network. Finding identifiers,
 * record IDs, and metrics are synthetic and exist solely to
 * demonstrate the intended supervisory analytics workflow.
 */

// ─── CSE entities ────────────────────────────────────────────────
export interface CSEEntity {
  cseId: string;
  name: string;
  sector: string;
  peerGroup: string;
  totalAssets: number;
  totalAlerts: number;
  totalCases: number;
  overallRisk: "low" | "moderate" | "elevated" | "high";
  findingsCount: number;
}

export const cseEntities: CSEEntity[] = [
  {
    cseId: "CSE-01",
    name: "Regional Cyber Security Entity 01",
    sector: "Energy",
    peerGroup: "regional",
    totalAssets: 50,
    totalAlerts: 1420,
    totalCases: 310,
    overallRisk: "low",
    findingsCount: 2,
  },
  {
    cseId: "CSE-02",
    name: "Regional Cyber Security Entity 02",
    sector: "Banking & Finance",
    peerGroup: "regional",
    totalAssets: 50,
    totalAlerts: 1860,
    totalCases: 380,
    overallRisk: "elevated",
    findingsCount: 8,
  },
  {
    cseId: "CSE-03",
    name: "Regional Cyber Security Entity 03",
    sector: "Telecommunications",
    peerGroup: "regional",
    totalAssets: 50,
    totalAlerts: 2100,
    totalCases: 410,
    overallRisk: "high",
    findingsCount: 6,
  },
  {
    cseId: "CSE-04",
    name: "Regional Cyber Security Entity 04",
    sector: "Transportation",
    peerGroup: "regional",
    totalAssets: 50,
    totalAlerts: 1580,
    totalCases: 320,
    overallRisk: "elevated",
    findingsCount: 5,
  },
  {
    cseId: "CSE-05",
    name: "Regional Cyber Security Entity 05",
    sector: "Healthcare",
    peerGroup: "regional",
    totalAssets: 50,
    totalAlerts: 920,
    totalCases: 180,
    overallRisk: "moderate",
    findingsCount: 3,
  },
  {
    cseId: "CSE-06",
    name: "Regional Cyber Security Entity 06",
    sector: "Government Services",
    peerGroup: "regional",
    totalAssets: 50,
    totalAlerts: 1350,
    totalCases: 290,
    overallRisk: "moderate",
    findingsCount: 4,
  },
];

// ─── Assessment dimensions ───────────────────────────────────────
export interface DimensionScore {
  dimension: string;
  score: number; // 0–100
  findingsCount: number;
  trend: "improving" | "stable" | "declining";
}

export const assessmentDimensions: DimensionScore[] = [
  { dimension: "Threat Detection", score: 72, findingsCount: 5, trend: "stable" },
  { dimension: "Investigation", score: 58, findingsCount: 8, trend: "declining" },
  { dimension: "Escalation", score: 45, findingsCount: 10, trend: "declining" },
  { dimension: "Incident Response", score: 68, findingsCount: 4, trend: "stable" },
  { dimension: "Security Operations", score: 74, findingsCount: 3, trend: "improving" },
  { dimension: "Governance & Oversight", score: 81, findingsCount: 2, trend: "stable" },
  { dimension: "Operational Discipline", score: 62, findingsCount: 6, trend: "stable" },
  { dimension: "Cyber Resilience", score: 69, findingsCount: 3, trend: "improving" },
];

// ─── Findings ────────────────────────────────────────────────────
export type SignalCategory =
  | "missing_escalation"
  | "unusually_short_investigation"
  | "repeated_alerts_without_remediation"
  | "negative_space_low_activity";

export type ReviewPriority = "critical" | "high" | "moderate" | "low";
export type ReviewStatus = "pending_review" | "under_review" | "reviewed";

export interface Finding {
  findingId: string;
  cseId: string;
  dimension: string;
  signalCategory: SignalCategory;
  signalLabel: string;
  explanation: string;
  supportingRecordIds: string[];
  contextBaseline: string;
  whyItMatters: string;
  reviewPriority: ReviewPriority;
  reviewStatus: ReviewStatus;
}

export const findings: Finding[] = [
  {
    findingId: "FND-001",
    cseId: "CSE-02",
    dimension: "Escalation",
    signalCategory: "missing_escalation",
    signalLabel: "Missing Escalation Record",
    explanation:
      "High-severity cases (CAS-00001 through CAS-00010) have documented investigation evidence but no corresponding escalation record in CSE-02's submissions.",
    supportingRecordIds: [
      "CAS-00001", "CAS-00002", "CAS-00003", "CAS-00004", "CAS-00005",
      "CAS-00006", "CAS-00007", "CAS-00008", "CAS-00009", "CAS-00010",
    ],
    contextBaseline:
      "Peer-group entities in the regional cohort escalate an average of 78% of high/critical cases with investigation evidence.",
    whyItMatters:
      "A pattern of investigated high-severity cases without escalation records may indicate a documentation gap, workflow configuration issue, or deviation from the entity's stated escalation procedures. Supervisory review can determine whether escalations occurred but were not recorded, or whether cases were closed without escalation.",
    reviewPriority: "high",
    reviewStatus: "pending_review",
  },
  {
    findingId: "FND-002",
    cseId: "CSE-02",
    dimension: "Escalation",
    signalCategory: "missing_escalation",
    signalLabel: "Missing Escalation — Extended Pattern",
    explanation:
      "An additional 90 high/critical cases (CAS-00011 through CAS-00100) within CSE-02 show investigation records but no escalation, extending the pattern observed in FND-001.",
    supportingRecordIds: [
      "CAS-00011", "CAS-00015", "CAS-00025", "CAS-00040", "CAS-00055",
      "CAS-00070", "CAS-00085", "CAS-00100",
    ],
    contextBaseline:
      "100 of 380 total cases in CSE-02 follow this pattern — approximately 26% of all cases.",
    whyItMatters:
      "The volume of cases following this pattern is above the peer-group baseline, suggesting a systemic rather than isolated issue. Review should assess whether this reflects a reporting gap or an operational process deviation.",
    reviewPriority: "critical",
    reviewStatus: "pending_review",
  },
  {
    findingId: "FND-003",
    cseId: "CSE-04",
    dimension: "Investigation",
    signalCategory: "unusually_short_investigation",
    signalLabel: "Unusually Short Investigation Duration",
    explanation:
      "100 investigations in CSE-04 (INV-00001 through INV-00100) have durations substantially below the contextual baseline established by the broader evidence cohort.",
    supportingRecordIds: [
      "INV-00001", "INV-00010", "INV-00025", "INV-00050", "INV-00075", "INV-00100",
    ],
    contextBaseline:
      "Baseline: geometric median duration of 14,400 seconds (4 hours). Lower threshold: 420 seconds (7 minutes). Observed durations range from 30 to 300 seconds.",
    whyItMatters:
      "Investigation durations well below the baseline may indicate automated closures, template-based responses, or investigations conducted through channels not reflected in the submission data. A human reviewer can determine whether the short durations reflect actual investigative work or a documentation gap.",
    reviewPriority: "high",
    reviewStatus: "under_review",
  },
  {
    findingId: "FND-004",
    cseId: "CSE-03",
    dimension: "Incident Response",
    signalCategory: "repeated_alerts_without_remediation",
    signalLabel: "Repeated Alerts Without Remediation",
    explanation:
      "Eight assets in CSE-03 (AST-03-001 through AST-03-008) show alert volumes above the entity's robust asset-level baseline, while remediation evidence covers fewer than 10% of associated cases.",
    supportingRecordIds: [
      "AST-03-001", "AST-03-002", "AST-03-003", "AST-03-004",
      "CAS-00141", "CAS-00150", "CAS-00160", "CAS-00170", "CAS-00180", "CAS-00200",
    ],
    contextBaseline:
      "CSE-03 median asset alert count: 22. Upper fence: 68. These assets have 85–120 alerts each. Remediation coverage: 3–8%.",
    whyItMatters:
      "Assets with elevated alert volumes and minimal remediation records may warrant review to determine whether remediations occurred but were not recorded, or whether recurring alerts on the same assets indicate an unresolved underlying issue.",
    reviewPriority: "critical",
    reviewStatus: "pending_review",
  },
  {
    findingId: "FND-005",
    cseId: "CSE-05",
    dimension: "Threat Detection",
    signalCategory: "negative_space_low_activity",
    signalLabel: "Negative Space — Low Detection Activity",
    explanation:
      "Eight critical assets in CSE-05 (AST-05-001 through AST-05-008) have no recorded alerts, while other critical assets in the same entity show normal detection activity.",
    supportingRecordIds: [
      "AST-05-001", "AST-05-002", "AST-05-003", "AST-05-004",
      "AST-05-005", "AST-05-006", "AST-05-007", "AST-05-008",
    ],
    contextBaseline:
      "Other critical assets in CSE-05 average 18 alerts per asset. These 8 assets have zero alerts.",
    whyItMatters:
      "The absence of alerts on critical assets, while peer assets in the same entity show typical activity, may indicate that detection coverage is not reaching these assets. This is a negative-space signal — the observation is about what is missing, not what is present. A reviewer should assess whether these assets have alternative monitoring coverage or whether there is a detection gap.",
    reviewPriority: "high",
    reviewStatus: "pending_review",
  },
  {
    findingId: "FND-006",
    cseId: "CSE-06",
    dimension: "Escalation",
    signalCategory: "missing_escalation",
    signalLabel: "Missing Escalation — Small Subset",
    explanation:
      "Ten cases in CSE-06 (CAS-00381 through CAS-00390) show investigation evidence but no escalation record, amid otherwise varied supervisory activity.",
    supportingRecordIds: [
      "CAS-00381", "CAS-00382", "CAS-00383", "CAS-00384", "CAS-00385",
      "CAS-00386", "CAS-00387", "CAS-00388", "CAS-00389", "CAS-00390",
    ],
    contextBaseline:
      "CSE-06 has 290 total cases; 10 (3.4%) follow this pattern — within the lower range of the peer group.",
    whyItMatters:
      "While the proportion is smaller than in CSE-02, the cases still warrant verification to confirm whether escalations occurred outside the recorded workflow.",
    reviewPriority: "moderate",
    reviewStatus: "reviewed",
  },
  {
    findingId: "FND-007",
    cseId: "CSE-06",
    dimension: "Investigation",
    signalCategory: "unusually_short_investigation",
    signalLabel: "Unusually Short Investigation — Minor Signal",
    explanation:
      "Five investigations in CSE-06 (INV-00101 through INV-00105) have durations below the contextual baseline, mixed with otherwise varied investigation activity.",
    supportingRecordIds: ["INV-00101", "INV-00102", "INV-00103", "INV-00104", "INV-00105"],
    contextBaseline:
      "These five investigations averaged 180 seconds. The broader cohort baseline lower threshold is 420 seconds.",
    whyItMatters:
      "A small number of short investigations in an otherwise healthy entity may represent edge cases or legitimate quick resolutions, but should be verified.",
    reviewPriority: "low",
    reviewStatus: "reviewed",
  },
  {
    findingId: "FND-008",
    cseId: "CSE-01",
    dimension: "Governance & Oversight",
    signalCategory: "missing_escalation",
    signalLabel: "Missing Escalation — Isolated Cases",
    explanation:
      "Two high-severity cases in CSE-01 have investigation evidence but no escalation record.",
    supportingRecordIds: ["CAS-00401", "CAS-00402"],
    contextBaseline:
      "CSE-01 escalation rate is 92% for high/critical cases, well within the peer-group norm. These two cases are outliers.",
    whyItMatters:
      "The small number of affected cases suggests an isolated documentation gap rather than a systemic issue, but review can confirm.",
    reviewPriority: "low",
    reviewStatus: "reviewed",
  },
];

// ─── Priority queue ──────────────────────────────────────────────
export interface QueueItem {
  findingId: string;
  cseId: string;
  signalLabel: string;
  priority: ReviewPriority;
  status: ReviewStatus;
  dimension: string;
}

export const reviewQueue: QueueItem[] = findings
  .sort((a, b) => {
    const priorityOrder: Record<ReviewPriority, number> = {
      critical: 0,
      high: 1,
      moderate: 2,
      low: 3,
    };
    return priorityOrder[a.reviewPriority] - priorityOrder[b.reviewPriority];
  })
  .map((f) => ({
    findingId: f.findingId,
    cseId: f.cseId,
    signalLabel: f.signalLabel,
    priority: f.reviewPriority,
    status: f.reviewStatus,
    dimension: f.dimension,
  }));

// ─── Monthly trend data (illustrative) ──────────────────────────
export interface TrendPoint {
  month: string;
  findings: number;
}

export const trendData: TrendPoint[] = [
  { month: "Apr", findings: 12 },
  { month: "May", findings: 15 },
  { month: "Jun", findings: 11 },
  { month: "Jul", findings: 18 },
  { month: "Aug", findings: 14 },
  { month: "Sep", findings: 28 },
];

// ─── Category summary ───────────────────────────────────────────
export const categorySummary: { category: string; label: string; count: number; color: string }[] = [
  { category: "missing_escalation", label: "Missing Escalation", count: 4, color: "var(--amber-400)" },
  { category: "unusually_short_investigation", label: "Short Investigation", count: 2, color: "var(--red-400)" },
  { category: "repeated_alerts_without_remediation", label: "Repeated Alerts / Low Remediation", count: 1, color: "var(--navy-400)" },
  { category: "negative_space_low_activity", label: "Negative Space", count: 1, color: "var(--teal-500)" },
];

// ─── Helper: human-friendly labels ──────────────────────────────
export const signalCategoryLabels: Record<SignalCategory, string> = {
  missing_escalation: "Missing Escalation",
  unusually_short_investigation: "Unusually Short Investigation",
  repeated_alerts_without_remediation: "Repeated Alerts Without Remediation",
  negative_space_low_activity: "Negative Space — Low Activity",
};

export const priorityColors: Record<ReviewPriority, string> = {
  critical: "badge-red",
  high: "badge-amber",
  moderate: "badge-navy",
  low: "badge-gray",
};

export const statusLabels: Record<ReviewStatus, string> = {
  pending_review: "Pending Review",
  under_review: "Under Review",
  reviewed: "Reviewed",
};

export const riskColors: Record<CSEEntity["overallRisk"], string> = {
  low: "badge-teal",
  moderate: "badge-navy",
  elevated: "badge-amber",
  high: "badge-red",
};
