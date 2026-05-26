import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sentinel Evidence Defensibility Workbench",
  description: "Evidence defensibility, review vault, remediation register, and portfolio command center by Eye On Bits Pvt Ltd.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
