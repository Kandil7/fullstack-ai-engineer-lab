"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { UsagePoint } from "@/types";

/** Weekly chats vs active-users area chart. */
export function UsageChart({ data }: { data: UsagePoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
        <defs>
          <linearGradient id="chats" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="hsl(215 90% 55%)" stopOpacity={0.35} />
            <stop offset="100%" stopColor="hsl(215 90% 55%)" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(215 15% 85%)" vertical={false} />
        <XAxis dataKey="date" tickLine={false} axisLine={false} fontSize={12} />
        <YAxis tickLine={false} axisLine={false} fontSize={12} />
        <Tooltip />
        <Area type="monotone" dataKey="chats" stroke="hsl(215 90% 55%)" fill="url(#chats)" strokeWidth={2} />
        <Area type="monotone" dataKey="users" stroke="hsl(160 70% 45%)" fill="transparent" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
