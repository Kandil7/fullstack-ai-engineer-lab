import { Badge } from "@/components/ui/Badge";
import { SurfaceCard } from "@/components/ui/SurfaceCard";
import type { User } from "@/types";

const roleVariant = {
  student: "default",
  teacher: "accent",
  admin: "success",
} as const;

/** Read-only user management table. */
export function UsersTable({ users }: { users: User[] }) {
  return (
    <SurfaceCard className="overflow-hidden p-0">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border text-left text-ink-muted">
            <th className="px-5 py-3 font-medium">Name</th>
            <th className="px-5 py-3 font-medium">Email</th>
            <th className="px-5 py-3 font-medium">Role</th>
            <th className="px-5 py-3 font-medium">Joined</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id} className="border-b border-border/60 last:border-0 hover:bg-ink/5">
              <td className="px-5 py-3 font-medium">{u.name}</td>
              <td className="px-5 py-3 text-ink-muted">{u.email}</td>
              <td className="px-5 py-3">
                <Badge variant={roleVariant[u.role]}>{u.role}</Badge>
              </td>
              <td className="px-5 py-3 text-ink-muted">
                {new Date(u.created_at).toLocaleDateString("en-US")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </SurfaceCard>
  );
}
