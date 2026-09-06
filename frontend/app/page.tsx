import Link from "next/link";

export default function Home() {
  return (
    <main className="page">
      <div className="container home">
        <p className="eyebrow">AGENTVOX</p>

        <h1>AI Interview Platform</h1>

        <p className="description">
          Adaptive AI interviews powered by LangGraph and real-time voice.
        </p>

        <Link href="/interview" className="primary-button link-button">
          Start Interview
        </Link>
      </div>
    </main>
  );
}
