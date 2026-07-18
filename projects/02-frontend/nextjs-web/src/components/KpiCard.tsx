import { SurfaceCard } from "@/components/ui/SurfaceCard";
import { Badge } from "@/components/ui/Badge";
import { formatDelta } from "@/lib/utils";
import type { Kpi } from "@/types";

/** A single key-performance-indicator card with trend. */
export function KpiCard({ kpi }: { kpi: Kpi }) {
  const positive = kpi.delta >= 0;
  return (
    <SurfaceCard className="flex flex-col gap-2">
      <span className="text-sm text-ink-muted">{kpi.label}</span>
      <span className="text-3xl font-semibold tracking-tight">{kpi.value}</span>
      <Badge variant={positive ? "success" : "warning"}>{formatDelta(kpi.delta)}</Badge>
    </SurfaceCard>
  );
}
