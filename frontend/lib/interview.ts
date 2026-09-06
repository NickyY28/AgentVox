import { api, AxiosError } from "./api";

type GetAgoraTokenResponse =
  | {
      token: string;
      app_id: string;
      channel_name: string;
      uid: number;
      expires_in: number;
    }
  | AxiosError;

const interview = {
  getAgoraToken: async (
    channel_name: string,
    uid: string
  ): Promise<GetAgoraTokenResponse> => {
    try {
      const response = await api.post("/agora/token", { channel_name, uid });
      return response.data as GetAgoraTokenResponse;
    } catch (error) {
      if (error instanceof AxiosError) {
        return error;
      }
      throw error;
    }
  },
};

export default interview;
