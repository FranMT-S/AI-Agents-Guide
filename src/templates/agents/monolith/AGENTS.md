# [Project Name]

[One sentence describing what this project does and its core purpose.]
Example: "This is a Node.js REST API for managing e-commerce orders using Express, Prisma, and PostgreSQL."

## Tech Stack

- **Runtime:** Node.js 20 / Bun 1.x (specify which)
- **Language:** TypeScript (strict mode)
- **Framework:** Express / NestJS / Next.js (specify)
- **Package Manager:** pnpm (use pnpm, not npm or yarn)
- **Database:** PostgreSQL via Prisma ORM
- **Testing:** Vitest + Supertest
- **Linting/Formatting:** Biome (auto-fix enabled)

## Development Setup

```bash
pnpm install
cp .env.example .env
pnpm db:migrate
pnpm dev
```

## Build & Test Commands

```bash
# Development server
pnpm dev

# Type check (never skip this before committing)
pnpm tsc --noEmit

# Run all tests
pnpm test

# Lint and format
pnpm lint

# Production build
pnpm build
```

## Architecture Notes

The project follows a layered architecture:
- `src/routes/` — HTTP route definitions (thin layer, no business logic)
- `src/services/` — Business logic and domain operations
- `src/repositories/` — Database access via Prisma (no raw SQL)
- `src/middleware/` — Auth, error handling, rate limiting
- `src/lib/` — Shared utilities and helpers

Authentication uses JWT. The token is validated in `src/middleware/auth.ts`.

## Code Style Guidelines

- Use named exports over default exports.
- Use async/await over promise chains.
- Use `interface` for object shapes that may be extended; use `type` for unions and primitives.
- File naming: `kebab-case.ts` for all files.
- Co-locate tests: `user-service.ts` and `user-service.test.ts` live in the same folder.

## Common Tasks

**Add a new API endpoint:**
1. Create the route in `src/routes/<resource>.ts`
2. Create the service method in `src/services/<resource>.service.ts`
3. Add integration test in `src/routes/<resource>.test.ts`

**Add a database table:**
1. Modify `prisma/schema.prisma`
2. Run `pnpm db:migrate:create -- --name <migration_name>`
3. Test migration on dev DB before committing

**Add an environment variable:**
1. Add to `.env.example` with a placeholder value
2. Register in `src/lib/env.ts` (validated with Zod)

## Security Practices

- Never commit secrets or API keys. Use `.env` and `.env.example`.
- All user inputs must be validated server-side (Zod schemas in `src/schemas/`).
- Use parameterized queries via Prisma. Never construct raw SQL with user input.
- Rate limiting is applied globally in `src/middleware/rate-limit.ts`.

## Testing Requirements

- Write unit tests for all service methods.
- Write integration tests for all API routes.
- Maintain >80% coverage. Run `pnpm test:coverage` to check.
- Run type check and lint before committing.
