import { z } from "zod";

/**
 * Server-side API client. Talks to the Go backend directly from Next.js
 * server components and route handlers, keeping tokens off the browser.
 */
const API_URL = process.env.API_URL ?? "http://localhost:8080";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

interface RequestOptions {
  method?: string;
  body?: unknown;
  token?: string;
  // A Zod schema to validate the response against.
  schema?: z.ZodTypeAny;
  // Next.js fetch cache revalidation window in seconds.
  revalidate?: number;
}

/** Perform a typed request against the backend API. */
export async function apiFetch<T>(path: string, opts: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, token, schema, revalidate } = opts;

  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
    next: revalidate !== undefined ? { revalidate } : undefined,
  });

  if (!res.ok) {
    let message = res.statusText;
    try {
      const err = (await res.json()) as { error?: string };
      if (err.error) message = err.error;
    } catch {
      // Non-JSON error body; keep statusText.
    }
    throw new ApiError(res.status, message);
  }

  const json = (await res.json()) as unknown;
  return (schema ? schema.parse(json) : json) as T;
}

/** Build a bearer token from the request context (placeholder for real auth). */
export function getServerToken(): string {
  // In production this reads an httpOnly session cookie. For the scaffold we
  // fall back to an env-provided service token.
  return process.env.DASHBOARD_API_TOKEN ?? "dev-token";
}
