const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`GET ${path} failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function apiPost<TResponse, TBody = unknown>(
  path: string,
  body?: TBody,
): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    const detail = errorBody?.detail ?? `POST ${path} failed with status ${response.status}`;
    throw new Error(detail);
  }

  return response.json() as Promise<TResponse>;
}