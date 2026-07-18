import { NextResponse } from "next/server";
import { apiFetch, ApiError, getServerToken } from "@/lib/api";
import { mockUsers } from "@/lib/mock-data";
import type { UsersResponse } from "@/types";

/**
 * Proxy GET /api/users → Go backend GET /users.
 * Falls back to mock data when the backend is unreachable so the dashboard
 * remains usable during local development.
 */
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.toString();
  const path = query ? `/users?${query}` : "/users";

  try {
    const data = await apiFetch<UsersResponse>(path, {
      token: getServerToken(),
      revalidate: 15,
    });
    return NextResponse.json(data);
  } catch (err) {
    if (err instanceof ApiError && err.status < 500) {
      return NextResponse.json({ error: err.message }, { status: err.status });
    }
    // Backend down (network / 5xx): serve mock data with a header marker.
    return NextResponse.json(
      { data: mockUsers, pagination: { has_more: false, total: mockUsers.length } },
      { headers: { "x-data-source": "mock" } },
    );
  }
}
