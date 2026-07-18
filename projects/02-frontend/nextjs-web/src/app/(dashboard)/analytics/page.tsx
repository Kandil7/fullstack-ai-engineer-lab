import { Header } from "@/components/layout/Header";
import { SurfaceCard } from "@/components/ui/SurfaceCard";
import { UsageChart } from "@/components/charts/UsageChart";
import { RagMetricsChart } from "@/components/charts/RagMetricsChart";
import { formatPercent } from "@/lib/utils";
import { mockRagMetrics, mockUsage } from "@/lib/mock-data";

export default function AnalyticsPage() {
  return (
    <>
      <Header title="Analytics" />
      <main className="flex-1 space-y-6 overflow-y-auto p-6">
        <SurfaceCard>
          <h2 className="mb-4 text-sm font-medium text-ink-muted">Chat & User Volume</h2>
          <UsageChart data={mockUsage} />
        </SurfaceCard>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <SurfaceCard>
            <h2 className="mb-4 text-sm font-medium text-ink-muted">RAG Metrics</h2>
            <RagMetricsChart data={mockRagMetrics} />
          </SurfaceCard>
          <SurfaceCard>
            <h2 className="mb-4 text-sm font-medium text-ink-muted">Metric Detail</h2>
            <ul className="space-y-3">
              {mockRagMetrics.map((m) => (
                <li key={m.metric} className="flex items-center justify-between text-sm">
                  <span>{m.metric}</span>
                  <span
                    className={
                      m.score >= m.target ? "text-emerald-600 dark:text-emerald-400" : "text-amber-600 dark:text-amber-400"
                    }
                  >
                    {formatPercent(m.score)} / {formatPercent(m.target)}
                  </span>
                </li>
              ))}
            </ul>
          </SurfaceCard>
        </div>
      </main>
    </>
  );
}
