/** Top bar with page title and a placeholder account control. */
export function Header({ title }: { title: string }) {
  return (
    <header className="flex items-center justify-between border-b border-border bg-surface/80 px-6 py-4 backdrop-blur">
      <h1 className="text-lg font-semibold tracking-tight">{title}</h1>
      <div className="flex items-center gap-3">
        <span className="text-sm text-ink-muted">Admin</span>
        <span
          className="grid h-8 w-8 place-items-center rounded-full bg-ink/10 text-xs font-medium"
          aria-hidden
        >
          A
        </span>
      </div>
    </header>
  );
}
