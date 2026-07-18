import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ThanaweyaGPT — Admin Dashboard",
  description: "Admin and analytics dashboard for the ThanaweyaGPT educational AI platform.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
