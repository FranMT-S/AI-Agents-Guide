# TypeScript Conventions

This document is loaded on demand when working on TypeScript-specific tasks.
Return to [AGENTS.md](../AGENTS.md) for the project overview.

## Language Rules

- Use TypeScript strict mode in all files (`"strict": true` in tsconfig).
- Use `interface` for object shapes that may be extended. Use `type` for unions, intersections, and primitive aliases.
- Prefer named exports over default exports.
- Use async/await over promise chains.
- Never use `any`. Use `unknown` and then narrow with type guards.

## File and Naming Conventions

- File names: `kebab-case.ts`
- React component files: `kebab-case.tsx`
- Co-locate tests: `user-service.ts` and `user-service.test.ts` in the same directory.
- Place shared types in `packages/types/src/`.

## Import Style

- Use absolute imports via path aliases (configured in `tsconfig.json`).
- Example: `import { UserSchema } from '@acme/types'` not `../../packages/types`.
- Group imports: 1) Node built-ins, 2) External packages, 3) Internal packages, 4) Relative files.

## React-Specific (apps/web)

- Default to Server Components. Add `"use client"` explicitly only when required.
- Co-locate component styles in `component.module.css` alongside the component file.
- Extract shared hooks to `apps/web/src/hooks/`.
- Extract shared utilities to `apps/web/src/lib/`.

*Referenced from: [AGENTS.md](../AGENTS.md)*
