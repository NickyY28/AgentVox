import AgoraRTC, {
  IAgoraRTCClient,
  IAgoraRTCRemoteUser,
  ILocalAudioTrack,
} from "agora-rtc-sdk-ng";

export const agoraClient: IAgoraRTCClient = AgoraRTC.createClient({
  mode: "rtc",
  codec: "vp8",
});

export type AgoraConnection = {
  client: IAgoraRTCClient;
  localAudioTrack: ILocalAudioTrack | null;
};

export function createAgoraClient() {
  return AgoraRTC.createClient({
    mode: "rtc",
    codec: "vp8",
  });
}

export function playRemoteAudio(user: IAgoraRTCRemoteUser) {
  if (user.audioTrack) {
    user.audioTrack.play();
  }
}
