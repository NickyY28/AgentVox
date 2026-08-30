import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AgentVox",
  description:
    "AgentVox is an adaptive, real-time voice AI interview platform designed to make AI-powered interviews more conversational, evidence-driven, and transparent. Built for the EchoSphere: Agora Conversational AI Hackathon 2026, AgentVox uses real-time voice interaction through Agora combined with a multi-agent AI architecture to conduct interviews that adapt to what a candidate actually says.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
