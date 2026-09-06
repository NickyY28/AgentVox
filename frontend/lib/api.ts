import axios, { AxiosError } from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status == 401) {
      console.warn("Unauthorized! User is not logged in or token expired.");
    }
    return Promise.reject(error);
  }
);
export { AxiosError };
