import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

/** A raised surface card with consistent border, radius, and padding. */
export function SurfaceCard({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-xl border border-border bg-surface-raised p-5 shadow-sm",
        className,
      )}
      {...props}
    />
  );
}
