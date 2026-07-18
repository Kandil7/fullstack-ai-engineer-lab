import { Header } from "@/components/layout/Header";
import { KpiCard } from "@/components/KpiCard";
import { SurfaceCard } from "@/components/ui/SurfaceCard";
import { UsageChart } from "@/components/charts/UsageChart";
import { RagMetricsChart } from "@/components/charts/RagMetricsChart";
import { mockKpis, mockRagMetrics, mockUsage } from "@/lib/mock-data";

// Server component: in production these would call apiFetch() with revalidate.
export default function OverviewPage() {
  const kpis = mockKpis;
  const usage = mockUsage;
  const rag = mockRagMetrics;

  return (
    <>
      <Header title="Overview" />
      <main className="flex-1 space-y-6 overflow-y-auto p-6">
        <section aria-label="Key metrics" className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {kpis.map((kpi) => (
            <KpiCard key={kpi.label} kpi={kpi} />
          ))}
        </section>

        <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <SurfaceCard>
            <h2 className="mb-4 text-sm font-medium text-ink-muted">Weekly Usage</h2>
            <UsageChart data={usage} />
          </SurfaceCard>
          <SurfaceCard>
            <h2 className="mb-4 text-sm font-medium text-ink-muted">RAG Quality vs Target</h2>
            <RagMetricsChart data={rag} />
          </SurfaceCard>
        </section>
      </main>
    </>
  );
}
