"use client";

import { useEffect, useRef, useState } from "react";
import AgoraRTC, {
  IAgoraRTCClient,
  ILocalAudioTrack,
  IAgoraRTCRemoteUser,
} from "agora-rtc-sdk-ng";

import interview from "@/lib/interview";
import { toast } from "@/components/ui/toast";

type AgoraRoomProps = {
  channelName?: string;
};

export default function AgoraRoom({
  channelName = `agentvox-`,
}: AgoraRoomProps) {
  const clientRef = useRef<IAgoraRTCClient | null>(null);
  const localAudioTrackRef = useRef<ILocalAudioTrack | null>(null);

  const [isJoined, setIsJoined] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState("Not connected");
  const [error, setError] = useState<string | null>(null);

  const appId = process.env.NEXT_PUBLIC_AGORA_APP_ID || "";

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
        return;
      }

      const client = AgoraRTC.createClient({
        mode: "rtc",
        codec: "vp8",
      });

      clientRef.current = client;

      /*
       * Remote user publishes audio
       */
      client.on(
        "user-published",
        async (user: IAgoraRTCRemoteUser, mediaType) => {
          await client.subscribe(user, mediaType);

          if (mediaType === "audio" && user.audioTrack) {
            user.audioTrack.play();
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
      setStatus("Connected");
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

  async function leaveChannel() {
    try {
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
      setStatus("Not connected");
      setError(null);
    } catch (err) {
      console.error("Agora leave error:", err);

      setError(
        err instanceof Error ? err.message : "Failed to leave interview."
      );
    }
  }

  async function toggleMute() {
    const audioTrack = localAudioTrackRef.current;

    if (!audioTrack) {
      return;
    }

    const nextMuted = !isMuted;

    await audioTrack.setEnabled(!nextMuted);

    setIsMuted(nextMuted);
  }

  useEffect(() => {
    return () => {
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

        {/* Connection status */}
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

      {/* Voice area */}
      <div className="mb-8 flex min-h-64 flex-col items-center justify-center rounded-2xl border border-zinc-800 bg-zinc-900/50">
        <div
          className={`mb-5 flex h-24 w-24 items-center justify-center rounded-full border ${
            isJoined
              ? "border-emerald-500/40 bg-emerald-500/10"
              : "border-zinc-700 bg-zinc-800"
          }`}
        >
          <span className="text-4xl">{isMuted ? "🔇" : "🎙️"}</span>
        </div>

        <h3 className="text-lg font-semibold text-white">
          {isJoined
            ? isMuted
              ? "Microphone muted"
              : "Microphone active"
            : "Ready for interview"}
        </h3>

        <p className="mt-2 text-sm text-zinc-500">
          {isJoined
            ? "Your voice connection is active."
            : "Join the room to start your voice session."}
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-col gap-3 sm:flex-row">
        {!isJoined ? (
          <button
            type="button"
            onClick={joinChannel}
            disabled={isLoading}
            className="flex-1 rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? "Connecting..." : "🎙️ Join Interview"}
          </button>
        ) : (
          <>
            <button
              type="button"
              onClick={toggleMute}
              className="flex-1 rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-3 font-semibold text-white transition hover:bg-zinc-800"
            >
              {isMuted ? "🎙️ Unmute" : "🔇 Mute"}
            </button>

            <button
              type="button"
              onClick={leaveChannel}
              className="flex-1 rounded-xl border border-red-900/50 bg-red-950/30 px-5 py-3 font-semibold text-red-400 transition hover:bg-red-950/50"
            >
              Leave Interview
            </button>
          </>
        )}
      </div>

      {/* Info */}
      <div className="mt-6 border-t border-zinc-800 pt-5">
        <div className="flex flex-wrap gap-x-6 gap-y-2 text-xs text-zinc-600">
          <span>● Agora RTC</span>
          <span>● Real-time audio</span>
          <span>● Secure token</span>
        </div>
      </div>
    </div>
  );
}
