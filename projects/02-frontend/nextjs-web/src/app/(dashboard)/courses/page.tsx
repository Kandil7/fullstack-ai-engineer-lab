import { Header } from "@/components/layout/Header";
import { SurfaceCard } from "@/components/ui/SurfaceCard";
import { Badge } from "@/components/ui/Badge";

const courses = [
  { id: "math-101", title: "Mathematics — Grade 12", modules: 8, students: 412 },
  { id: "phys-201", title: "Physics — Grade 12", modules: 6, students: 305 },
  { id: "chem-101", title: "Chemistry — Grade 11", modules: 7, students: 288 },
];

export default function CoursesPage() {
  return (
    <>
      <Header title="Courses" />
      <main className="flex-1 space-y-4 overflow-y-auto p-6">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {courses.map((c) => (
            <SurfaceCard key={c.id} className="flex flex-col gap-3">
              <div className="flex items-start justify-between">
                <h2 className="font-medium">{c.title}</h2>
                <Badge variant="accent">{c.modules} modules</Badge>
              </div>
              <p className="text-sm text-ink-muted">{c.students} enrolled students</p>
            </SurfaceCard>
          ))}
        </div>
      </main>
    </>
  );
}
