# API Package (apps/api)

This is the Node.js REST API for the Acme platform. It uses Express, Prisma, and PostgreSQL.
See the root [AGENTS.md](../../AGENTS.md) for monorepo-wide rules.

## Package Structure

```text
apps/api/
├── src/
│   ├── routes/        (HTTP route definitions — no business logic here)
│   ├── services/      (Business logic and domain operations)
│   ├── repositories/  (Database access via Prisma)
│   ├── middleware/    (Auth, error handling, rate limiting)
│   └── lib/           (Shared utilities: logger, env, errors)
├── prisma/
│   ├── schema.prisma
│   └── migrations/
└── AGENTS.md          (this file)
```

## Dev Commands (run from this package root)

```bash
pnpm dev          # Start dev server (port 3001)
pnpm test         # Run integration + unit tests
pnpm db:migrate   # Apply pending migrations
pnpm db:studio    # Open Prisma Studio
```

## API Design Rules

- Follow RESTful conventions: `GET /users`, `POST /users`, `PATCH /users/:id`, `DELETE /users/:id`.
- Return consistent error shapes: `{ error: { code: string, message: string } }`.
- Validate all request bodies using Zod schemas from `@acme/types`.
- Never expose internal Prisma error messages to the client.

For detailed API design patterns, see [../../docs/API_CONVENTIONS.md](../../docs/API_CONVENTIONS.md).

## Database Rules

- Never write raw SQL. Use Prisma client methods exclusively.
- All schema changes require a new migration: `pnpm db:migrate:create -- --name <name>`.
- Never modify existing migration files.

For schema details and migration patterns, see [../../docs/DATABASE_SCHEMA.md](../../docs/DATABASE_SCHEMA.md).

## Authentication

JWT validation is handled by `src/middleware/auth.ts`. Do not re-implement auth logic elsewhere.
For OAuth flows and token refresh patterns, see [../../docs/AUTH.md](../../docs/AUTH.md).
