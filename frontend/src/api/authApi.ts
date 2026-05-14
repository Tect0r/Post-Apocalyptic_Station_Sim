import { apiPost, clearAccessToken, setAccessToken } from "./apiClient";
import type { AuthResponse, LoginRequest, RegisterRequest } from "../types/auth";

export async function registerUser(request: RegisterRequest): Promise<AuthResponse> {
  return apiPost<AuthResponse, RegisterRequest>("/auth/register", request);
}

export async function loginUser(request: LoginRequest): Promise<AuthResponse> {
  const response = await apiPost<AuthResponse, LoginRequest>("/auth/login", request);

  if (response.data?.access_token) {
    setAccessToken(response.data.access_token);
  }

  return response;
}

export function logoutUser(): void {
  clearAccessToken();
}