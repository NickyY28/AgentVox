"use client";

import { useEffect, useRef, useState } from "react";
import AgoraRTC, {
  IAgoraRTCClient,
  IAgoraRTCRemoteUser,
  ILocalAudioTrack,
} from "agora-rtc-sdk-ng";

import interview from "@/lib/interview";
import { toast } from "@/components/ui/toast";

type AgoraRoomProps = {
  channelName?: string;
};

type SpeechRecognitionResult = {
  transcript: string;
};

type SpeechRecognitionEventLike = Event & {
  results: {
    length: number;
    [index: number]: {
      isFinal: boolean;
      length: number;
      [index: number]: SpeechRecognitionResult;
    };
  };
};

type SpeechRecognitionLike = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;

  start: () => void;
  stop: () => void;
  abort: () => void;

  onresult: ((event: SpeechRecognitionEventLike) => void) | null;

  onend: (() => void) | null;

  onerror: ((event: Event) => void) | null;
};

type SpeechRecognitionConstructor = new () => SpeechRecognitionLike;

type InterviewStartResponse = {
  interview_id?: number;
  question?: string;
  current_question?: string;
  completed?: boolean;
};

type InterviewAnswerResponse = {
  question?: string;
  current_question?: string;
  completed?: boolean;
  next_action?: string;
  confidence?: number;
};

export default function AgoraRoom({
  channelName = `agentvox-room-${Math.floor(Math.random() * 100000)}`,
}: AgoraRoomProps) {
  // --------------------------------------------------
  // Agora
  // --------------------------------------------------

  const clientRef = useRef<IAgoraRTCClient | null>(null);
  const localAudioTrackRef = useRef<ILocalAudioTrack | null>(null);

  // --------------------------------------------------
  // Speech Recognition
  // --------------------------------------------------

  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);

  // --------------------------------------------------
  // State
  // --------------------------------------------------
  const [isJoined, setIsJoined] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [status, setStatus] = useState("Not connected");
  const [error, setError] = useState<string | null>(null);

  // --------------------------------------------------
  // Interview State
  // --------------------------------------------------
  const [interviewId, setInterviewId] = useState<number | null>(null);
  const [question, setQuestion] = useState("");
  const [transcript, setTranscript] = useState("");
  const [interviewCompleted, setInterviewCompleted] = useState(false);

  // --------------------------------------------------
  // Environment
  // --------------------------------------------------

  const appId = process.env.NEXT_PUBLIC_AGORA_APP_ID || "";
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  // ==================================================
  // TEXT TO SPEECH
  // ==================================================

  function speak(text: string) {
    if (!text) return;

    if (typeof window === "undefined" || !window.speechSynthesis) {
      return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    utterance.rate = 0.95;
    utterance.pitch = 1;
    utterance.volume = 1;

    window.speechSynthesis.speak(utterance);
  }

  // ==================================================
  // GET SPEECH RECOGNITION
  // ==================================================

  function getSpeechRecognition(): SpeechRecognitionConstructor | null {
    if (typeof window === "undefined") {
      return null;
    }

    const browserWindow = window as typeof window & {
      SpeechRecognition?: SpeechRecognitionConstructor;
      webkitSpeechRecognition?: SpeechRecognitionConstructor;
    };

    return (
      browserWindow.SpeechRecognition ||
      browserWindow.webkitSpeechRecognition ||
      null
    );
  }

  // ==================================================
  // START SPEECH RECOGNITION
  // ==================================================

  function startListening() {
    setError(null);

    const SpeechRecognition = getSpeechRecognition();

    if (!SpeechRecognition) {
      setError(
        "Speech recognition is not supported in this browser. Please use Google Chrome."
      );

      return;
    }

    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch {
        // Ignore cleanup errors.
      }
    }

    const recognition = new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = (event: SpeechRecognitionEventLike) => {
      let finalText = "";
      let interimText = "";

      for (let i = 0; i < event.results.length; i++) {
        const result = event.results[i];

        const text = result?.[0]?.transcript || "";

        if (result?.isFinal) {
          finalText += `${text} `;
        } else {
          interimText += text;
        }
      }

      setTranscript(`${finalText}${interimText}`.trim());
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    setTranscript("");
    setIsListening(true);

    try {
      recognition.start();

      setStatus("Listening to your answer...");
    } catch (err) {
      console.error("Speech recognition error:", err);

      setIsListening(false);

      setError("Unable to start speech recognition.");
    }
  }

  // ==================================================
  // STOP LISTENING
  // ==================================================

  function stopListening() {
    const recognition = recognitionRef.current;

    if (recognition) {
      try {
        recognition.stop();
      } catch {
        // Already stopped.
      }
    }

    setIsListening(false);
  }

  // ==================================================
  // START INTERVIEW
  // ==================================================

  async function startInterview() {
    try {
      setIsProcessing(true);
      setError(null);

      setStatus("Starting AI interview...");

      const response = await fetch(`${apiUrl}/api/v1/interview/start`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_context: {},
          job_context: {},
          competencies: [
            {
              name: "Communication",
            },
            {
              name: "Problem Solving",
            },
            {
              name: "Technical Skills",
            },
          ],
        }),
      });

      if (!response.ok) {
        const message = await response.text();

        throw new Error(message || "Failed to start interview.");
      }

      const data = (await response.json()) as InterviewStartResponse;

      const newInterviewId = data.interview_id;

      const firstQuestion = data.question || data.current_question || "";

      if (newInterviewId !== undefined) {
        setInterviewId(newInterviewId);
      }

      setQuestion(firstQuestion);

      setInterviewCompleted(false);

      setStatus("AI interview ready");

      if (firstQuestion) {
        speak(firstQuestion);
      }
    } catch (err) {
      console.error("Start interview error:", err);

      setError(
        err instanceof Error ? err.message : "Failed to start interview."
      );

      setStatus("Interview failed");
    } finally {
      setIsProcessing(false);
    }
  }

  // ==================================================
  // SUBMIT ANSWER
  // ==================================================

  async function submitAnswer() {
    if (!interviewId) {
      setError("Please start the AI interview first.");

      return;
    }

    const answer = transcript.trim();

    if (!answer) {
      setError("No answer detected. Please speak your answer first.");

      return;
    }

    stopListening();

    try {
      setIsProcessing(true);
      setError(null);

      setStatus("AI is analyzing your answer...");

      const response = await fetch(
        `${apiUrl}/api/v1/interview/${interviewId}/answer`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            answer,
          }),
        }
      );

      if (!response.ok) {
        const message = await response.text();

        throw new Error(message || "Failed to process answer.");
      }

      const data = (await response.json()) as InterviewAnswerResponse;

      setTranscript("");

      if (data.completed) {
        setInterviewCompleted(true);

        setQuestion("The interview is complete. Great job!");

        setStatus("Interview completed");

        speak("The interview is complete. Great job!");

        return;
      }

      const nextQuestion = data.question || data.current_question || "";

      if (nextQuestion) {
        setQuestion(nextQuestion);

        setStatus(
          data.next_action === "follow_up"
            ? "AI generated a follow-up question"
            : "AI generated the next question"
        );

        speak(nextQuestion);
      } else {
        setStatus("Answer analyzed");
      }
    } catch (err) {
      console.error("Submit answer error:", err);

      setError(
        err instanceof Error ? err.message : "Failed to analyze answer."
      );

      setStatus("Answer processing failed");
    } finally {
      setIsProcessing(false);
    }
  }

  // ==================================================
  // JOIN AGORA CHANNEL
  // ==================================================

  async function joinChannel() {
    try {
      setIsLoading(true);
      setError(null);

      if (!appId) {
        throw new Error("NEXT_PUBLIC_AGORA_APP_ID is not configured.");
      }

      setStatus("Getting Agora token...");

      const tokenData = await interview.getAgoraToken(channelName, "2");

      if (tokenData instanceof Error) {
        toast.add({
          title: "Error",
          description: `Failed to get Agora token: ${tokenData.message}`,
        });

        setError(tokenData.message);

        return;
      }

      const client = AgoraRTC.createClient({
        mode: "rtc",
        codec: "vp8",
      });

      clientRef.current = client;

      // ------------------------------------------------
      // Remote user publishes audio
      // ------------------------------------------------

      client.on(
        "user-published",
        async (user: IAgoraRTCRemoteUser, mediaType) => {
          try {
            await client.subscribe(user, mediaType);

            if (mediaType === "audio" && user.audioTrack) {
              user.audioTrack.play();
            }
          } catch (err) {
            console.error("Remote audio error:", err);
          }
        }
      );

      client.on("user-unpublished", () => {
        // Remote user stopped publishing.
      });

      client.on("user-left", () => {
        // Remote user left.
      });

      setStatus("Joining interview room...");

      await client.join(
        tokenData.app_id || appId,
        tokenData.channel_name || channelName,
        tokenData.token,
        tokenData.uid ?? 0
      );

      setStatus("Starting microphone...");

      const microphoneTrack = await AgoraRTC.createMicrophoneAudioTrack();

      localAudioTrackRef.current = microphoneTrack;

      await client.publish([microphoneTrack]);

      setIsJoined(true);

      setStatus("Connected to Agora");
    } catch (err) {
      console.error("Agora connection error:", err);

      setStatus("Connection failed");

      setError(
        err instanceof Error ? err.message : "Failed to connect to Agora."
      );
    } finally {
      setIsLoading(false);
    }
  }

  // ==================================================
  // LEAVE AGORA CHANNEL
  // ==================================================

  async function leaveChannel() {
    try {
      stopListening();

      if (typeof window !== "undefined") {
        window.speechSynthesis?.cancel();
      }

      const audioTrack = localAudioTrackRef.current;

      if (audioTrack) {
        audioTrack.stop();
        audioTrack.close();

        localAudioTrackRef.current = null;
      }

      const client = clientRef.current;

      if (client) {
        await client.leave();

        clientRef.current = null;
      }

      setIsJoined(false);
      setIsMuted(false);
      setIsListening(false);

      setStatus("Not connected");

      setError(null);
    } catch (err) {
      console.error("Agora leave error:", err);

      setError(
        err instanceof Error ? err.message : "Failed to leave interview."
      );
    }
  }

  // ==================================================
  // MUTE / UNMUTE
  // ==================================================

  async function toggleMute() {
    const audioTrack = localAudioTrackRef.current;

    if (!audioTrack) {
      return;
    }

    try {
      const nextMuted = !isMuted;

      await audioTrack.setEnabled(!nextMuted);

      setIsMuted(nextMuted);
    } catch (err) {
      console.error("Mute error:", err);

      setError("Failed to change microphone state.");
    }
  }

  // ==================================================
  // CLEANUP
  // ==================================================

  useEffect(() => {
    return () => {
      const recognition = recognitionRef.current;

      if (recognition) {
        try {
          recognition.abort();
        } catch {
          // Ignore cleanup errors.
        }
      }

      if (typeof window !== "undefined") {
        window.speechSynthesis?.cancel();
      }

      const audioTrack = localAudioTrackRef.current;

      if (audioTrack) {
        audioTrack.stop();
        audioTrack.close();
      }

      const client = clientRef.current;

      if (client) {
        client.leave().catch(() => {});
      }
    };
  }, []);

  // ==================================================
  // UI
  // ==================================================

  return (
    <div className="w-full max-w-3xl rounded-2xl border border-zinc-800 bg-zinc-950 p-6 shadow-2xl">
      {/* Header */}
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="mb-2 text-xs font-semibold tracking-[0.25em] text-zinc-500">
            AGENTVOX
          </p>

          <h2 className="text-2xl font-bold text-white">AI Interview Room</h2>

          <p className="mt-2 text-sm text-zinc-500">
            Channel:{" "}
            <span className="font-mono text-zinc-400">{channelName}</span>
          </p>
        </div>

        {/* Status */}
        <div
          className={`inline-flex w-fit items-center gap-2 rounded-full px-3 py-1.5 text-xs font-medium ${
            isJoined
              ? "bg-emerald-500/10 text-emerald-400"
              : "bg-zinc-800 text-zinc-400"
          }`}
        >
          <span
            className={`h-2 w-2 rounded-full ${
              isJoined ? "animate-pulse bg-emerald-400" : "bg-zinc-500"
            }`}
          />

          {status}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-6 rounded-xl border border-red-900/50 bg-red-950/30 p-4">
          <p className="text-sm leading-6 text-red-400">{error}</p>
        </div>
      )}

      {/* AI Question */}
      {question && (
        <div className="mb-5 rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
              AI Interviewer
            </p>

            <span className="rounded-full bg-zinc-800 px-2.5 py-1 text-[10px] font-medium text-zinc-500">
              AI
            </span>
          </div>

          <p className="text-base leading-7 text-zinc-200">{question}</p>
        </div>
      )}

      {/* Voice Area */}
      <div className="mb-5 flex min-h-56 flex-col items-center justify-center rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
        <div
          className={`mb-5 flex h-24 w-24 items-center justify-center rounded-full border transition ${
            isListening
              ? "animate-pulse border-red-500/50 bg-red-500/10"
              : isJoined
              ? "border-emerald-500/40 bg-emerald-500/10"
              : "border-zinc-700 bg-zinc-800"
          }`}
        >
          <span className="text-4xl">
            {isListening ? "🔴" : isMuted ? "🔇" : "🎙️"}
          </span>
        </div>

        <h3 className="text-lg font-semibold text-white">
          {interviewCompleted
            ? "Interview completed"
            : isListening
            ? "Listening..."
            : isProcessing
            ? "AI is thinking..."
            : isJoined
            ? "Microphone active"
            : "Ready for interview"}
        </h3>

        <p className="mt-2 text-center text-sm text-zinc-500">
          {interviewCompleted
            ? "Your interview session has finished."
            : isListening
            ? "Speak naturally. Your answer is being transcribed."
            : isProcessing
            ? "Analyzing your response and preparing the next question."
            : isJoined
            ? "Your Agora voice connection is active."
            : "Join the room to start your voice session."}
        </p>
      </div>

      {/* Transcript */}
      {transcript && (
        <div className="mb-6 rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
              Your Answer
            </p>

            {isListening && (
              <span className="text-xs text-red-400">Listening</span>
            )}
          </div>

          <p className="text-sm leading-7 text-zinc-300">{transcript}</p>
        </div>
      )}

      {/* Controls */}
      <div className="grid gap-3 sm:grid-cols-2">
        {/* Join */}
        {!isJoined && (
          <button
            type="button"
            onClick={joinChannel}
            disabled={isLoading}
            className="rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50 sm:col-span-2"
          >
            {isLoading ? "Connecting..." : "🎙️ Join Interview Room"}
          </button>
        )}

        {/* Start AI interview */}
        {isJoined && !interviewId && !interviewCompleted && (
          <button
            type="button"
            onClick={startInterview}
            disabled={isProcessing}
            className="rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50 sm:col-span-2"
          >
            {isProcessing ? "Starting AI..." : "🤖 Start AI Interview"}
          </button>
        )}

        {/* Start listening */}
        {isJoined &&
          interviewId &&
          !isListening &&
          !isProcessing &&
          !interviewCompleted && (
            <button
              type="button"
              onClick={startListening}
              className="rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-zinc-200"
            >
              🎙️ Answer Question
            </button>
          )}

        {/* Stop / submit */}
        {isListening && (
          <button
            type="button"
            onClick={submitAnswer}
            disabled={!transcript.trim()}
            className="rounded-xl bg-emerald-500 px-5 py-3 font-semibold text-black transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            ✓ Submit Answer
          </button>
        )}

        {/* Processing */}
        {isProcessing && isJoined && interviewId && (
          <button
            type="button"
            disabled
            className="rounded-xl bg-zinc-800 px-5 py-3 font-semibold text-zinc-500 sm:col-span-2"
          >
            🧠 AI is analyzing...
          </button>
        )}

        {/* Mute */}
        {isJoined && (
          <button
            type="button"
            onClick={toggleMute}
            disabled={isProcessing}
            className="rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-3 font-semibold text-white transition hover:bg-zinc-800 disabled:opacity-50"
          >
            {isMuted ? "🎙️ Unmute" : "🔇 Mute"}
          </button>
        )}

        {/* Leave */}
        {isJoined && (
          <button
            type="button"
            onClick={leaveChannel}
            className="rounded-xl border border-red-900/50 bg-red-950/30 px-5 py-3 font-semibold text-red-400 transition hover:bg-red-950/50"
          >
            Leave Interview
          </button>
        )}
      </div>

      {/* Interview ID */}
      {interviewId && (
        <div className="mt-6 border-t border-zinc-800 pt-5">
          <p className="text-center text-xs text-zinc-600">
            Interview ID:{" "}
            <span className="font-mono text-zinc-500">{interviewId}</span>
          </p>
        </div>
      )}

      {/* Info */}
      <div className="mt-5 border-t border-zinc-800 pt-5">
        <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 text-xs text-zinc-600">
          <span>● Agora RTC</span>
          <span>● Speech-to-Text</span>
          <span>● LangGraph</span>
          <span>● AI Interview</span>
          <span>● Text-to-Speech</span>
        </div>
      </div>
    </div>
  );
}
