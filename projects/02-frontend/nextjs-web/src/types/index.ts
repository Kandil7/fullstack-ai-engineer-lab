// Shared domain types for the dashboard.

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: "student" | "teacher" | "admin";
  created_at: string;
}

export interface Pagination {
  cursor?: string;
  has_more: boolean;
  total: number;
}

export interface UsersResponse {
  data: User[];
  pagination: Pagination;
}

export interface Kpi {
  label: string;
  value: string;
  delta: number; // percentage change vs previous period
}

export interface UsagePoint {
  date: string;
  chats: number;
  users: number;
}

export interface RagMetric {
  metric: string;
  score: number; // 0..1
  target: number; // 0..1
}
