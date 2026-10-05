import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Interactive Demo — AudMi Supervisory Analytics",
  description:
    "Explore AudMi's supervisory dashboard with synthetic data. View CSE overviews, assessment dimensions, findings, and the review priority queue.",
};

export default function DemoLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
