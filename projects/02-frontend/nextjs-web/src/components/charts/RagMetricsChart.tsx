"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { RagMetric } from "@/types";

/** RAG quality metrics vs their targets. Bars turn amber when below target. */
export function RagMetricsChart({ data }: { data: RagMetric[] }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(215 15% 85%)" vertical={false} />
        <XAxis dataKey="metric" tickLine={false} axisLine={false} fontSize={11} />
        <YAxis domain={[0, 1]} tickLine={false} axisLine={false} fontSize={12} />
        <Tooltip />
        <Bar dataKey="score" radius={[6, 6, 0, 0]}>
          {data.map((d) => (
            <Cell
              key={d.metric}
              fill={d.score >= d.target ? "hsl(160 70% 45%)" : "hsl(38 92% 50%)"}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
