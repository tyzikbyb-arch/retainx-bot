import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: "RetainX Studio — AI Video, Image & Audio Generation",
  description:
    "Generate professional AI videos, images, and audio with 15+ models. No subscription. Pay per creation.",
  keywords: ["AI video generation", "Sora", "Kling", "AI studio", "text to video"],
  openGraph: {
    title: "RetainX Studio",
    description: "Every AI model. One platform. Pay per creation.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={geist.variable}>
      <body>{children}</body>
    </html>
  );
}
