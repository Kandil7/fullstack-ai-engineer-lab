import { Header } from "@/components/layout/Header";
import { SurfaceCard } from "@/components/ui/SurfaceCard";

const settings = [
  { key: "API_URL", label: "Backend API URL", value: process.env.API_URL ?? "http://localhost:8080" },
  { key: "EMBEDDING_MODEL", label: "Embedding Model", value: "text-embedding-3-small" },
  { key: "RAG_TOP_K", label: "RAG top-k", value: "10" },
];

export default function SettingsPage() {
  return (
    <>
      <Header title="Settings" />
      <main className="flex-1 space-y-4 overflow-y-auto p-6">
        <SurfaceCard className="space-y-4">
          <h2 className="text-sm font-medium text-ink-muted">System Configuration</h2>
          <dl className="divide-y divide-border">
            {settings.map((s) => (
              <div key={s.key} className="flex items-center justify-between py-3">
                <dt className="text-sm">{s.label}</dt>
                <dd className="font-mono text-sm text-ink-muted">{s.value}</dd>
              </div>
            ))}
          </dl>
        </SurfaceCard>
      </main>
    </>
  );
}
