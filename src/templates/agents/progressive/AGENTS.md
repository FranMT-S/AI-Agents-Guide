# [Project Name]

[One sentence describing the project.]
Example: "This is a pnpm monorepo containing the web frontend, Node.js API, and shared packages for the Acme platform."

## Quick Reference

- **Package manager:** pnpm workspaces
- **Build:** `pnpm build`
- **Type check:** `pnpm tsc --noEmit`
- **Test:** `pnpm test`
- **Lint:** `pnpm lint`

## Task-Specific Guides

Read only the files relevant to your current task. Do not load all of them at once.

**Code & Language**
- If working on TypeScript or general code conventions, see [docs/typescript.md](docs/typescript.md)
- If writing or debugging tests, see [docs/testing.md](docs/testing.md)
- If working on API endpoints or route design, see [docs/api-conventions.md](docs/api-conventions.md)
- If working on database migrations or schema changes, see [docs/database-schema.md](docs/database-schema.md)
- If working on authentication or authorization, see [docs/auth.md](docs/auth.md)

**Frontend & UI**
- If working on React components or UI patterns, see [docs/components.md](docs/components.md)
- If working on CSS, design tokens, or styling conventions, see [docs/styles.md](docs/styles.md)
- If working on state management, see [docs/state.md](docs/state.md)

**Architecture & Infrastructure**
- To understand the overall system design, see [docs/architecture.md](docs/architecture.md)
- To understand the tech stack and dependency decisions, see [docs/tech-stack.md](docs/tech-stack.md)
- If setting up CI/CD or deployment, see [docs/deployment.md](docs/deployment.md)
- If adding a new shared package to the monorepo, see [docs/monorepo.md](docs/monorepo.md)

## Package Structure

This monorepo contains:
- `apps/web` — Next.js frontend
- `apps/api` — Node.js REST API (Express + Prisma)
- `packages/ui` — Shared React component library
- `packages/types` — Shared TypeScript types and Zod schemas
- `packages/config` — Shared ESLint, TypeScript, and Biome configs

Each package has its own `AGENTS.md` with package-specific rules.

## Security Practices

- Never commit secrets or API keys.
- Validate all inputs using Zod schemas from `packages/types`.
- Authentication is handled by the `apps/api` service — do not implement auth logic in `apps/web`.
