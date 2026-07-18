import type { Kpi, RagMetric, UsagePoint, User } from "@/types";

/**
 * Deterministic sample data so the dashboard renders during development before
 * the backend endpoints are wired. Server components fall back to these when the
 * API is unreachable.
 */

export const mockKpis: Kpi[] = [
  { label: "Active Users", value: "1,284", delta: 8.2 },
  { label: "Chats Today", value: "4,913", delta: 12.5 },
  { label: "Avg. RAG Faithfulness", value: "0.87", delta: 1.4 },
  { label: "Cost / Query", value: "$0.006", delta: -4.1 },
];

export const mockUsage: UsagePoint[] = [
  { date: "Mon", chats: 320, users: 210 },
  { date: "Tue", chats: 410, users: 260 },
  { date: "Wed", chats: 380, users: 240 },
  { date: "Thu", chats: 520, users: 300 },
  { date: "Fri", chats: 610, users: 340 },
  { date: "Sat", chats: 290, users: 180 },
  { date: "Sun", chats: 250, users: 160 },
];

export const mockRagMetrics: RagMetric[] = [
  { metric: "Faithfulness", score: 0.87, target: 0.85 },
  { metric: "Answer Relevance", score: 0.82, target: 0.8 },
  { metric: "Context Precision", score: 0.78, target: 0.75 },
  { metric: "Context Recall", score: 0.71, target: 0.7 },
];

export const mockUsers: User[] = [
  { id: "usr_001", email: "ahmed@school.edu", name: "Ahmed Hassan", role: "student", created_at: "2025-01-15T10:30:00Z" },
  { id: "usr_002", email: "sara@school.edu", name: "Sara Ali", role: "student", created_at: "2025-02-02T09:10:00Z" },
  { id: "usr_003", email: "mona@school.edu", name: "Mona Youssef", role: "teacher", created_at: "2024-11-20T14:05:00Z" },
  { id: "usr_004", email: "omar@school.edu", name: "Omar Khaled", role: "student", created_at: "2025-03-11T16:45:00Z" },
  { id: "usr_005", email: "admin@thanaweya.gpt", name: "Platform Admin", role: "admin", created_at: "2024-09-01T08:00:00Z" },
];
