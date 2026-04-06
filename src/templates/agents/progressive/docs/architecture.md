# System Architecture

This document is loaded on demand when understanding or modifying system design.
Return to [AGENTS.md](../AGENTS.md) for the project overview.

## Project Directory Tree

```text
acme/
├── apps/
│   ├── web/                  (Next.js frontend)
│   │   ├── src/
│   │   │   ├── app/          (App Router pages and layouts)
│   │   │   ├── components/   (page-specific components)
│   │   │   ├── hooks/        (shared custom hooks)
│   │   │   ├── lib/          (client utilities)
│   │   │   └── styles/       (global CSS, tokens)
│   │   └── package.json
│   └── api/                  (Express REST API)
│       ├── src/
│       │   ├── routes/       (HTTP handlers — thin layer only)
│       │   ├── services/     (business logic)
│       │   ├── repositories/ (Prisma queries)
│       │   ├── middleware/   (auth, rate limit, error)
│       │   └── lib/          (logger, env, errors)
│       ├── prisma/
│       └── package.json
├── packages/
│   ├── ui/                   (shared React component library)
│   ├── types/                (Zod schemas + TypeScript types)
│   └── config/               (shared ESLint, TS, Biome configs)
├── AGENTS.md
└── package.json
```

## High-Level Architecture

This is a monorepo with a clear separation between apps and shared packages:

```text
Client (Browser)
    │
    ▼
apps/web (Next.js)          ← Server-side rendering, routing, UI
    │
    ▼  (HTTP/REST)
apps/api (Express + Prisma) ← Business logic, data access, auth
    │
    ▼
PostgreSQL Database
```

## Request Lifecycle

1. Client makes a request to `apps/web`.
2. Next.js Server Components fetch data directly from `apps/api` using `fetch()` with server-side auth headers.
3. `apps/api` validates the JWT, applies business logic, and queries the DB via Prisma.
4. Response flows back up the chain.

## Shared Package Dependency Graph

```text
apps/web  ─────────────────────────────┐
                                        ▼
apps/api  ─────────────────────► packages/types
                                        ▲
packages/ui ───────────────────────────┘
```

- `packages/types` is the only package imported by all apps. It must have zero side effects.
- `packages/ui` is imported only by `apps/web` — never by `apps/api`.
- `apps/api` must never import from `apps/web` or `packages/ui`.

## Key Design Decisions

- **No ORMs in route handlers.** All database access goes through the repository layer (`src/repositories/`).
- **No business logic in routes.** Routes only validate input and delegate to services.
- **Auth is stateless.** JWT tokens are short-lived (15 min). Refresh tokens are stored in HTTPOnly cookies.
- **Events are async.** Background jobs (email, webhooks) use a queue, not inline `setTimeout`.

*Referenced from: [AGENTS.md](../AGENTS.md)*
