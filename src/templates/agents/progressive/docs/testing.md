# Testing Patterns

This document is loaded on demand when writing or debugging tests.
Return to [AGENTS.md](../AGENTS.md) for the project overview.

## Test File Location

Tests are co-located with the source files they cover:

```text
src/
├── services/
│   ├── user.service.ts
│   └── user.service.test.ts      (unit test)
├── routes/
│   ├── users.ts
│   └── users.test.ts             (integration test)
└── components/
    ├── UserCard/
    │   ├── UserCard.tsx
    │   └── UserCard.test.tsx      (component test)
    └── ...
```

Global test setup lives in `vitest.config.ts` at the package root.

## Tools

- **Unit tests:** Vitest
- **Integration tests:** Vitest + Supertest (for API routes)
- **Component tests:** Vitest + React Testing Library (for `apps/web`)
- **Coverage threshold:** >80% for all packages

## Commands

```bash
# Run all tests across the monorepo
pnpm test

# Run tests for a specific package
pnpm test --filter @acme/api

# Run a single test file
pnpm vitest run src/services/user.service.test.ts

# Run tests matching a pattern
pnpm vitest run -t "should create user"

# Generate coverage report
pnpm test:coverage
```

## What to Test

- Write unit tests for all service methods and utility functions.
- Write integration tests for every API route (happy path + error cases).
- Write component tests for interactive UI components.
- Do not write tests for Prisma models or simple data-passing functions.

## Test File Structure

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'

describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid data', async () => {
      // arrange
      // act
      // assert
    })

    it('should throw if email already exists', async () => {
      // arrange
      // act + assert
    })
  })
})
```

## Mocking

- Use `vi.mock()` at the top of the test file.
- Mock external dependencies (email service, payment gateway) always.
- Do not mock the database in integration tests — use a dedicated test database.
- Reset mocks in `beforeEach` using `vi.resetAllMocks()`.

*Referenced from: [AGENTS.md](../AGENTS.md)*
