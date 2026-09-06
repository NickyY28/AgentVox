"use client";
import { Button } from "@/components/ui/button";
import { toast } from "@/components/ui/toast";
import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <div className="flex flex-col items-center gap-4">
        <p>AGENTVOX</p>

        <h1>AI Interview Platform</h1>

        <p className="description">
          Adaptive AI interviews powered by LangGraph and real-time voice.
        </p>
        <Button
          onClick={() => {
            toast.add({
              title: "Hello, World!",
              description: "This is a toast notification.",
            });
          }}
        >
          Try Toast Button
        </Button>
        <Link href="/interview" className="primary-button link-button">
          Start Interview
        </Link>
      </div>
    </main>
  );
}
