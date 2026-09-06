import AgoraRoom from "@/components/AgoraRoom";

export default function InterviewPage() {
  return (
    <main className="min-h-screen bg-zinc-950 px-4 py-12 text-white sm:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-5xl flex-col items-center">
        {/* Page Header */}
        <div className="mb-10 w-full text-center">
          <p className="mb-3 text-xs font-semibold tracking-[0.3em] text-zinc-500">
            AGENTVOX
          </p>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            AI Voice Interview
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-zinc-500 sm:text-lg">
            Practice your interview with an adaptive AI interviewer powered by
            real-time voice.
          </p>
        </div>

        {/* Interview Room */}
        <AgoraRoom />

        {/* Phase information */}
        <div className="mt-8 grid w-full max-w-3xl gap-4 sm:grid-cols-3">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4 text-center">
            <p className="text-xs uppercase tracking-wider text-zinc-600">
              Voice
            </p>

            <p className="mt-2 text-sm font-medium text-zinc-300">Agora RTC</p>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4 text-center">
            <p className="text-xs uppercase tracking-wider text-zinc-600">
              Interview
            </p>

            <p className="mt-2 text-sm font-medium text-zinc-300">LangGraph</p>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4 text-center">
            <p className="text-xs uppercase tracking-wider text-zinc-600">AI</p>

            <p className="mt-2 text-sm font-medium text-zinc-300">LLM</p>
          </div>
        </div>
      </div>
    </main>
  );
}
