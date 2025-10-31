const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type RequestOptions = Omit<RequestInit, "headers"> & {
  token?: string | null;
  headers?: HeadersInit;
};

async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers ?? {})
  };

  if (options.token) {
    headers.Authorization = `Bearer ${options.token}`;
  }

  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail ?? res.statusText);
  }

  if (res.status === 204) {
    return {} as T;
  }

  return res.json() as Promise<T>;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  full_name?: string | null;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
}

export interface InterviewTemplate {
  id: string;
  title: string;
  description: string;
  tags: string[];
  phases: Array<Record<string, unknown>>;
  steps: Array<Record<string, unknown>>;
  weightings: Array<Record<string, unknown>>;
}

export interface InterviewStep {
  id: string;
  template_step_id: string;
  title: string;
  summary?: string | null;
  prompts?: Record<string, unknown> | null;
  scoring_guidance?: Record<string, unknown> | null;
  order: number;
  notes?: string | null;
  score?: number | null;
  is_completed: boolean;
  updated_at: string;
}

export interface InterviewSession {
  id: string;
  candidate_name: string;
  candidate_email?: string | null;
  role: string;
  template_id: string;
  status: string;
  notes_summary?: string | null;
  overall_score?: number | null;
  created_at: string;
  updated_at: string;
  steps?: InterviewStep[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail ?? "Invalid credentials");
  }

  return res.json() as Promise<LoginResponse>;
}

export const api = {
  login,
  getCurrentUser: (token: string) => apiRequest<User>("/users/me", { token }),
  listTemplates: (token: string) => apiRequest<InterviewTemplate[]>("/interviews/templates", { token }),
  createSession: (
    token: string,
    payload: { candidate_name: string; candidate_email?: string; role: string; template_id: string }
  ) => apiRequest<InterviewSession>("/interviews/sessions", { method: "POST", token, body: JSON.stringify(payload) }),
  listSessions: (token: string, page = 1, size = 10) =>
    apiRequest<PaginatedResponse<InterviewSession>>(
      `/interviews/sessions?page=${page}&size=${size}`,
      { token }
    ),
  getSession: (token: string, sessionId: string) =>
    apiRequest<InterviewSession>(`/interviews/sessions/${sessionId}`, { token }),
  updateSession: (
    token: string,
    sessionId: string,
    payload: Partial<Pick<InterviewSession, "status" | "notes_summary" | "overall_score">>
  ) => apiRequest<InterviewSession>(`/interviews/sessions/${sessionId}`, {
    method: "PATCH",
    token,
    body: JSON.stringify(payload)
  }),
  updateStep: (
    token: string,
    sessionId: string,
    stepId: string,
    payload: Partial<Pick<InterviewStep, "notes" | "score" | "is_completed">>
  ) =>
    apiRequest<InterviewStep>(`/interviews/sessions/${sessionId}/steps/${stepId}`, {
      method: "PATCH",
      token,
      body: JSON.stringify(payload)
    }),
  listUsers: (token: string) => apiRequest<User[]>("/users", { token })
};

export { API_BASE_URL };
