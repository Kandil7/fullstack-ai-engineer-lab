import { Header } from "@/components/layout/Header";
import { UsersTable } from "@/components/UsersTable";
import { mockUsers } from "@/lib/mock-data";

export default function UsersPage() {
  // Production: const { data } = await apiFetch<UsersResponse>("/users", { token, revalidate: 30 });
  const users = mockUsers;

  return (
    <>
      <Header title="Users" />
      <main className="flex-1 space-y-4 overflow-y-auto p-6">
        <p className="text-sm text-ink-muted">{users.length} users</p>
        <UsersTable users={users} />
      </main>
    </>
  );
}
