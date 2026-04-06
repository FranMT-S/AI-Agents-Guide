# Component Conventions

This document is loaded on demand when working on React components or UI patterns.
Return to [AGENTS.md](../AGENTS.md) for the project overview.

## Component Structure

- One component per file. File name matches the component name: `UserCard.tsx`.
- Co-locate styles, tests, and stories in the same folder:

```text
src/components/UserCard/
├── UserCard.tsx
├── UserCard.test.tsx
├── UserCard.module.css
└── index.ts        (re-exports UserCard for clean imports)
```

## Rules

- Default to Server Components. Add `"use client"` only when the component needs browser APIs, event listeners, or React hooks.
- Use named exports. Do not use default exports for components.
- Props must be typed with an `interface` named `[ComponentName]Props`.
- Do not fetch data inside components. Fetch in Server Components or pass data via props.

## Naming Conventions

| Type             | Convention         | Example                    |
| :--------------- | :----------------- | :------------------------- |
| Component file   | PascalCase         | `UserCard.tsx`             |
| Hook file        | camelCase          | `useUserData.ts`           |
| Utility file     | kebab-case         | `format-date.ts`           |
| CSS module       | matches component  | `UserCard.module.css`      |
| Test file        | matches component  | `UserCard.test.tsx`        |

## Shared Components

- Shared components live in `packages/ui/src/`.
- Page-specific components live in `apps/web/src/components/`.
- Extract a component to `packages/ui` only when it is used in more than one app.

*Referenced from: [AGENTS.md](../AGENTS.md)*
