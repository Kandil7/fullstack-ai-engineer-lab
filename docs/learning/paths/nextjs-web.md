# Learning Path: Next.js Web Dashboard

**Goal:** build a full-featured web dashboard with Next.js App Router, connecting to the
Go/FastAPI backend with proper auth, server components, and a polished UI.

**Primary project:** `projects/02-frontend/nextjs-web`

---

## Milestones

### 1. React Fundamentals (Week 1)
- JSX, components, props, children, key prop
- State: `useState`, `useEffect`, `useRef`, `useMemo`, `useCallback`
- Conditional rendering, list rendering, composition patterns
- Event handling, controlled vs uncontrolled inputs
- Custom hooks: extracting reusable logic
- React mental model: re-renders, reconciliation, key usage

### 2. TypeScript for React (Week 1–2)
- Types vs interfaces, generics, discriminated unions
- Component prop typing: `React.FC<Props>`, children types
- Event types: `ChangeEvent`, `FormEvent`, custom events
- API response typing: generic fetch wrapper
- `strict: true` configuration and why it catches bugs early

### 3. Next.js App Router (Week 2–3)
- `app/` directory structure: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`
- File-based routing: dynamic routes `[id]`, catch-all `[...slug]`
- Route groups `(dashboard)`, `(auth)` — organizing without URL segments
- Metadata API: `generateMetadata()`, Open Graph, dynamic titles
- Parallel routes `@analytics` for split-view layouts

### 4. Server Components vs Client Components (Week 3)
- Default server components: direct DB/API access, no JS shipped
- `'use client'` directive: interactive UI, event handlers, browser APIs
- When to use which:
  - Server: data fetching, static content, heavy computations
  - Client: forms, modals, drag-drop, real-time updates
- Data flow: server component passes data as props to client component
- `React.cache()` for deduplicating fetches within a render

### 5. Data Fetching & API Routes (Week 3–4)
- Server-side: `fetch()` in server components with `next: { revalidate }`
- `server actions` for form submissions without API routes
- API routes: `app/api/[...route]/route.ts` for custom endpoints
- Route handlers: `GET`, `POST`, `PUT`, `DELETE` exports
- Proxy pattern: API routes as BFF (backend-for-frontend) layer
- Streaming: `Suspense` boundaries + `loading.tsx` for progressive UI

### 6. Middleware (Week 4)
- `middleware.ts` at project root — runs on every matched route
- Auth check: verify JWT/session cookie, redirect to `/login`
- Geolocation, A/B testing, header manipulation
- `NextResponse.redirect()`, `NextResponse.rewrite()`, `NextResponse.next()`
- Matcher config: which routes the middleware applies to

### 7. TailwindCSS (Week 4–5)
- Utility-first approach: composing styles in JSX
- Responsive design: `sm:`, `md:`, `lg:`, `xl:` prefixes
- Dark mode: `dark:` prefix + `prefers-color-scheme`
- Custom theme: `tailwind.config.ts` — colors, spacing, fonts
- `@apply` sparingly; CSS variables for dynamic theming
- Container queries, `grid`, `flex` patterns for dashboard layouts

### 8. shadcn/ui Component Library (Week 5)
- Installation: `npx shadcn@latest add button card dialog table`
- Customization: theming via CSS variables, not Tailwind config
- Composition patterns: `Dialog` + `DialogContent` + `DialogTrigger`
- Table component: sorting, filtering, pagination for data-heavy views
- Form component + React Hook Form + Zod validation
- Accessibility: keyboard navigation, ARIA labels built-in

### 9. Auth Integration (Week 5–6)
- NextAuth.js / Auth.js setup with JWT strategy
- Credentials provider for email/password login
- Session management: `getServerSession()` in server components
- Protected layouts: wrapping `(dashboard)` group with auth check
- Token refresh: middleware-level interception
- Role-based access: user roles in session, conditional UI rendering

### 10. Production Polish (Week 6–7)
- Error boundaries: `error.tsx` per route segment
- Loading states: skeleton UI, `loading.tsx` files
- Image optimization: `next/image` with blur placeholder
- Font optimization: `next/font/local` or Google Fonts
- SEO: structured data, sitemap generation, robots.txt
- Vercel deployment, environment variables, preview deployments

---

## The 20% That Unlocks 80%

| Concept | Why It Matters |
|---|---|
| Server Components default | Zero JS shipped for data-heavy pages |
| `'use client'` boundary | Only interactive code becomes client JS |
| Middleware auth check | Single gate for entire app, not per-page |
| `Suspense` + streaming | Perceives faster even if total load is same |
| shadcn/ui | Production components without vendor lock-in |

---

## API Surface (target)

```
GET  /api/auth/session       — current user session
GET  /api/proxy/users        — proxy to Go backend /users
POST /api/proxy/auth/login   — proxy to Go backend /auth/login
GET  /api/proxy/ai/rag/query — proxy to FastAPI /ai/rag/query
```

---

## Daily Pattern

1h theory/reading → 3h build (one page or component) → 1h AI review → 1h recall/Anki.

---

## Key Resources

| Topic | Resource |
|---|---|
| Next.js docs | [nextjs.org/docs](https://nextjs.org/docs) |
| React docs | [react.dev](https://react.dev) |
| TypeScript | [typescriptlang.org](https://www.typescriptlang.org) |
| TailwindCSS | [tailwindcss.com](https://tailwindcss.com) |
| shadcn/ui | [ui.shadcn.com](https://ui.shadcn.com) |
| NextAuth.js | [next-auth.js.org](https://next-auth.js.org) |

---

## Practice Tasks

1. Scaffold Next.js app with App Router and TypeScript
2. Create a dashboard layout with sidebar navigation using `layout.tsx`
3. Build a login page with form validation (React Hook Form + Zod)
4. Implement middleware auth guard that redirects unauthenticated users
5. Create a data table page with server-side fetching and streaming
6. Proxy an API call through Next.js API route to the Go backend
7. Add dark mode toggle with Tailwind `dark:` classes
8. Deploy to Vercel and verify env variables work

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Next.js App                     │
│                                                  │
│  ┌─────────────┐  ┌──────────────────────────┐  │
│  │  Middleware  │  │   App Router (app/)      │  │
│  │  - Auth     │  │                          │  │
│  │  - Redirect │  │  ┌──────────┐ ┌────────┐ │  │
│  │  - Rewrite  │  │  │ Server   │ │ Client │ │  │
│  └─────────────┘  │  │Component │ │Component│ │  │
│                    │  └──────────┘ └────────┘ │  │
│  ┌─────────────┐  │                          │  │
│  │  API Routes  │  │  layouts / pages /       │  │
│  │  (BFF Proxy) │  │  loading / error         │  │
│  └─────────────┘  └──────────────────────────┘  │
└──────────────────────┬──────────────────────────┘
                       │ HTTP
         ┌─────────────┴─────────────┐
         │                           │
┌────────┴────────┐  ┌──────────────┴──────────┐
│   Go Backend    │  │   FastAPI AI Services    │
│   (auth, users) │  │   (RAG, embeddings)      │
└─────────────────┘  └─────────────────────────┘
```

### Server vs Client Component Decision

```
Does this component need:
├─ interactivity (onClick, onChange)?        → 'use client'
├─ browser APIs (localStorage, window)?      → 'use client'
├─ React hooks (useState, useEffect)?        → 'use client'
├─ event listeners?                          → 'use client'
│
├─ data fetching from DB/API?                → Server Component
├─ heavy computation?                        → Server Component
├─ SEO content?                              → Server Component
└─ static content?                           → Server Component
```

### Request Lifecycle

```
1. Browser requests /dashboard
2. Edge Middleware runs (auth check, redirects)
3. Next.js matches route in app/
4. Server Components execute (data fetching, rendering)
5. Client Components hydrate (interactivity)
6. HTML streamed to browser
7. JavaScript hydrates interactive parts
```

### Auth Flow Detail

```
1. User submits login form (Client Component)
2. Form POSTs to /api/proxy/auth/login (API Route)
3. API Route proxies to Go backend /auth/login
4. Go returns JWT access + refresh tokens
5. API Route sets httpOnly cookie with tokens
6. User redirected to /dashboard
7. Middleware on /dashboard verifies cookie
8. Server Component reads session via getServerSession()
9. User data passed as props to Client Components
```

### Component Composition Pattern

```tsx
// Server Component: fetches data, passes to client
async function DashboardPage() {
  const session = await getServerSession();
  const data = await fetchUsers();  // server-side fetch

  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <UserTable initialData={data} />  {/* client component */}
    </div>
  );
}

// Client Component: handles interactivity
'use client'
function UserTable({ initialData }) {
  const [users, setUsers] = useState(initialData);
  const [filter, setFilter] = useState('');

  return (
    <DataTable
      data={users.filter(u => u.name.includes(filter))}
      onFilterChange={setFilter}
    />
  );
}
```

### Tailwind Dashboard Layout Pattern

```tsx
// app/(dashboard)/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen">
      <Sidebar className="w-64 shrink-0" />
      <main className="flex-1 overflow-auto">
        <Header className="h-16 border-b" />
        <div className="p-6">{children}</div>
      </main>
    </div>
  );
}
```

### Testing Strategy

| Layer | Tool | What to Test |
|---|---|---|
| Unit | Jest + React Testing Library | Utility functions, hooks |
| Component | Storybook + Vitest | Component rendering, interactions |
| API Route | Supertest | Route handlers, proxy logic |
| E2E | Playwright | Full user flows, auth, navigation |
| Visual | Chromatic / Percy | Visual regression |

### Key Packages

```json
{
  "next": "^14.2.0",
  "react": "^18.3.0",
  "typescript": "^5.4.0",
  "tailwindcss": "^3.4.0",
  "@radix-ui/react-*": "latest",
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.1.0",
  "tailwind-merge": "^2.2.0",
  "next-auth": "^4.24.0",
  "react-hook-form": "^7.51.0",
  "zod": "^3.23.0",
  "@tanstack/react-table": "^8.17.0"
}
```

### Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| 'use client' everywhere | No SSR benefit, larger bundle | Default to server, add client only when needed |
| Fetching in useEffect | Waterfall requests, no caching | Use server component or SWR/React Query |
| Props drilling through server/client | Complex prop chains | Use URL state, context, or server action |
| Middleware too heavy | Slow response times | Keep middleware lightweight, offload to API |
| No loading.tsx | Blank page during slow fetch | Add loading skeletons for each route |

---

## Self-Check

Can you explain:
- The difference between server components and client components and when to use each?
- How middleware fits in the request lifecycle?
- Why `Suspense` boundaries improve perceived performance?
- How to structure a BFF (backend-for-frontend) with Next.js API routes?
- The auth flow: login → JWT → middleware → server component session?
- When to use server actions vs API routes?
- How `generateMetadata()` enables dynamic SEO?

---

## ملخص عربي (Arabic Summary)

مسار بناء لوحة تحكم ويب بـ Next.js: من أساسيات React وTypeScript إلى App Router
ومكونات الخادم والعميل، مع TailwindCSS وshadcn/ui للواجهة، وتكامل المصادقة.
يشمل مخططات المعمارية ودورة حياة الطلبات وتدفق المصادقة وأنماط تكوين المكونات
واستراتيجية الاختبار وأخطاء شائعة. التخزين المؤقت على الخادم، البث التدريجي،
والنشر على Vercel.
