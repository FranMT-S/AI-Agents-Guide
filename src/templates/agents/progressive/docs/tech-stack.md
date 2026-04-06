# Tech Stack

This document is loaded on demand when making dependency decisions or understanding the technology choices.
Return to [AGENTS.md](../AGENTS.md) for the project overview.

## Core Stack

| Layer            | Technology              | Version  | Reason                                      |
| :--------------- | :---------------------- | :------- | :------------------------------------------ |
| Runtime          | Node.js                 | 20 LTS   | LTS stability for production                |
| Language         | TypeScript              | 5.x      | Type safety across the entire monorepo      |
| Package manager  | pnpm + workspaces       | 9.x      | Fast installs, strict hoisting, monorepo support |
| Frontend         | Next.js (App Router)    | 15.x     | Server Components, streaming, optimized builds |
| API Framework    | Express                 | 4.x      | Minimal, well-understood, easy to test      |
| ORM              | Prisma                  | 5.x      | Type-safe queries, migration management     |
| Database         | PostgreSQL               | 16       | ACID compliance, JSON support               |
| Validation       | Zod                     | 3.x      | Runtime + compile-time type safety          |
| Auth             | JWT (jose library)      | 5.x      | Stateless, no session store needed          |
| Testing          | Vitest + Supertest      | latest   | Fast, ESM-native, compatible with Node      |
| Linting          | Biome                   | latest   | Fast, opinionated, replaces ESLint+Prettier |

## Dependency Policy

- **Never add a new dependency without justification.** Prefer native Node.js APIs and already-installed packages.
- **Prefer packages with zero dependencies** to keep the supply chain minimal.
- **Lock major versions.** Use `^` for minor/patch ranges, but pin `major` explicitly in `package.json`.
- Before adding a package, check if `packages/config` already re-exports a shared version.

## What We Deliberately Avoid

| Technology      | Reason for Exclusion                                         |
| :-------------- | :----------------------------------------------------------- |
| Webpack         | Replaced by Next.js Turbopack and esbuild                    |
| Jest            | Replaced by Vitest (faster, ESM-native)                      |
| ESLint/Prettier | Replaced by Biome                                            |
| Redux           | Replaced by React Server Components + Zustand for local state |
| REST client     | Using native `fetch` with TypeScript wrappers               |

*Referenced from: [AGENTS.md](../AGENTS.md)*
