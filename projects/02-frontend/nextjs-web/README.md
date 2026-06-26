# Next.js Web Dashboard — ThanaweyaGPT Admin Panel

Admin dashboard and analytics interface for the ThanaweyaGPT educational AI platform.
Provides operators with user management, course administration, usage analytics, and
system configuration.

---

## Goals

- Build a production Next.js 14 dashboard with TypeScript
- Implement admin CRUD for users, courses, and content
- Display real-time analytics: active users, chat volume, RAG quality metrics
- Integrate with the Go backend API
- Demonstrate Next.js App Router, server components, and API routes

---

## Tech Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| Framework        | Next.js 14 (App Router) |
| Language         | TypeScript 5.x          |
| Styling          | TailwindCSS 3.x         |
| UI Components    | shadcn/ui               |
| Data Fetching    | Server Components + RSC |
| State            | React Query (TanStack)  |
| Forms            | React Hook Form + Zod   |
| Charts           | Recharts                |
| Testing          | Vitest + Playwright     |

---

## Page Map

| Page        | Route                | Purpose                                |
| ----------- | -------------------- | -------------------------------------- |
| Dashboard   | `/`                  | Overview: KPIs, charts, recent activity|
| Users       | `/users`             | User management, search, roles         |
| Courses     | `/courses`           | Course CRUD, content management        |
| Analytics   | `/analytics`         | Usage stats, chat logs, RAG metrics    |
| Settings    | `/settings`          | System config, API keys, notifications |

---

## Architecture

```
src/
├── app/                    # App Router pages
│   ├── (dashboard)/        # Dashboard layout group
│   │   ├── page.tsx        # Overview
│   │   ├── users/
│   │   ├── courses/
│   │   ├── analytics/
│   │   └── settings/
│   ├── layout.tsx          # Root layout
│   └── api/                # API route handlers (proxy)
├── components/
│   ├── ui/                 # shadcn/ui primitives
│   ├── charts/             # Reusable chart components
│   └── layout/             # Sidebar, header, nav
├── lib/
│   ├── api.ts              # API client (fetch wrapper)
│   ├── auth.ts             # Auth helpers
│   └── utils.ts            # Shared utilities
├── hooks/                  # Custom React hooks
└── types/                  # TypeScript type definitions
```

### API Integration

The dashboard proxies API calls through Next.js API routes to avoid CORS issues:

```
Browser → /api/users → Go Backend (localhost:8080)
```

Server Components fetch data directly in the server, reducing client-side JavaScript.

```tsx
// Example: Server Component fetching users
async function UsersPage() {
  const users = await fetch(`${process.env.API_URL}/users`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  }).then(r => r.json());

  return <UsersTable users={users} />;
}
```

---

## Design System

Built on **shadcn/ui** — copy-paste components with full source ownership:

- Consistent color palette via CSS variables
- Dark mode support (system preference + manual toggle)
- Responsive: mobile sidebar collapses to hamburger
- Accessible: ARIA labels, keyboard navigation, screen reader support

---

## Connection to ThanaweyaGPT Capstone

This dashboard is the **web admin interface** for ThanaweyaGPT
(`projects/07-capstone/thanaweyagpt`). It connects to:

- **Go backend** (`projects/01-backend-go/`) for user/course CRUD and admin endpoints
- **PostgreSQL** (indirectly via API) for all persistent data
- **Redis** (indirectly) for session and cache metrics

---

## Getting Started

```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with API_URL=http://localhost:8080

# Run development server
npm run dev

# Run tests
npm run test          # Unit tests (Vitest)
npm run test:e2e      # E2E tests (Playwright)

# Build for production
npm run build
```

---

## Key Decisions

| Decision          | Choice            | Rationale                            |
| ----------------- | ----------------- | ------------------------------------ |
| Router            | App Router        | RSC, streaming, layouts              |
| UI library        | shadcn/ui         | Source-owned, composable, accessible |
| Data fetching     | Server Components | Reduces client JS, better SEO        |
| State             | React Query       | Caching, background refetch,乐观更新 |
| Forms             | React Hook Form   | Minimal re-renders, Zod validation   |
| Charts            | Recharts          | Declarative, responsive, SVG-based   |

---

## Testing

- **Unit tests** with Vitest for utility functions and hooks
- **Component tests** with React Testing Library
- **E2E tests** with Playwright for critical admin flows

```bash
npm run test              # Run unit tests
npm run test:coverage     # With coverage report
npx playwright test       # Run E2E tests
```
