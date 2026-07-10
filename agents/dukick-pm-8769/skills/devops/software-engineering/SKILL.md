---
name: software-engineering
description: Full-stack software engineering patterns — frontend (React, Next.js, state management), backend (architecture, APIs, databases), REST API design, and cross-project coding standards. Use when building, refactoring, or reviewing web applications.
category: devops
---

# Software Engineering

Frontend patterns, backend architecture, API design, and coding standards for building and maintaining web applications.

## When to Activate

- Building or reviewing a frontend (React, Next.js, state management)
- Designing backend architecture, APIs, or database schemas
- Defining REST API conventions or endpoint naming
- Setting up coding standards for a team or project
- User says "React component", "API endpoint", "database schema", "code review", or "refactor"

---

## Frontend Patterns

### Component Architecture

- **Composition over inheritance:** Build complex UIs from simple, reusable components
- **Container/Presentation split:** Containers handle data fetching and state; presentations are pure render functions
- **Custom hooks:** Extract reusable logic (data fetching, form handling, animations) into hooks

### State Management

| Scale | Approach |
|-------|----------|
| Local component | `useState`, `useReducer` |
| Shared between siblings | Lift state up, or `useContext` |
| App-wide | Context + reducer, or Zustand/Redux |
| Server state | TanStack Query / SWR |
| Form state | React Hook Form / Formik |

### Performance

- Memoize expensive calculations with `useMemo`
- Memoize callbacks with `useCallback` when passed to optimized children
- Use `React.memo` for pure components that receive stable props
- Code-split with dynamic imports: `lazy(() => import('./Component'))`
- Virtualize long lists with `react-window` or `react-virtualized`

### Next.js Patterns

- Use App Router for new projects; Pages Router for legacy
- Server Components by default; Client Components only when interactivity needed
- Server Actions for mutations; avoid manual API routes when possible
- Image optimization with `next/image`
- Font optimization with `next/font`

---

## Backend Patterns

### Architecture

- **Layered:** Controller → Service → Repository → Database
- **Hexagonal/Clean:** Domain logic in the center; adapters for DB, HTTP, messaging at edges
- **CQRS:** Separate read and write models for complex domains
- **Event-driven:** Async processing via message queues (Redis, RabbitMQ, SQS)

### Database Optimization

- **Indexing:** Create indexes on query columns, foreign keys, and sorting fields
- **Query optimization:** Use EXPLAIN ANALYZE, avoid N+1 queries, batch inserts
- **Caching:** Redis for hot data, application-level memoization for expensive computations
- **Connection pooling:** Always pool DB connections; size = (cores × 2) + effective spindle count

### API Design

- **Versioning:** `/v1/users`, `/v2/users` — never break existing consumers
- **Rate limiting:** Token bucket or sliding window; return 429 with Retry-After header
- **Authentication:** JWT (stateless) or session tokens (stateful); HTTPS always
- **Pagination:** Cursor-based for large datasets; offset-based for small, stable sets
- **Error responses:** Consistent JSON structure with `error`, `message`, `code`, `details`

---

## REST API Design

### Resource Naming

| Good | Bad |
|------|-----|
| `GET /users` | `GET /getUsers` |
| `GET /users/123` | `GET /getUser?id=123` |
| `POST /users` | `POST /createUser` |
| `PATCH /users/123` | `POST /updateUser/123` |
| `DELETE /users/123` | `POST /deleteUser?id=123` |

### Status Codes

| Code | Use When |
|------|----------|
| 200 | Success, returning data |
| 201 | Resource created |
| 204 | Success, no body (e.g., DELETE) |
| 400 | Client error (bad input) |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, race condition) |
| 422 | Validation error (semantic) |
| 429 | Rate limit exceeded |
| 500 | Server error (generic) |

### Response Structure

```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 145
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2",
    "prev": null
  }
}
```

### Error Response Structure

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more fields failed validation",
    "details": [
      { "field": "email", "message": "Must be a valid email address" }
    ]
  }
}
```

---

## Coding Standards

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables/functions | camelCase | `getUserById` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Classes/types | PascalCase | `UserRepository` |
| Files | kebab-case | `user-repository.ts` |
| Private fields | _prefix or #private | `_internalState` |

### Code Organization

```
src/
  components/          # Reusable UI components
  pages/               # Route-level components
  hooks/               # Custom React hooks
  services/            # Business logic
  repositories/        # Data access layer
  models/              # Type definitions / schemas
  utils/               # Pure utility functions
  constants/           # Configuration values
  types/               # Shared TypeScript types
```

### Documentation Standards

- JSDoc for public APIs: `@param`, `@returns`, `@throws`, `@example`
- README for every module: purpose, setup, usage, examples
- Architecture Decision Records (ADRs) for significant choices
- Inline comments only for "why", not "what" (the code shows what)

### Testing Standards

- Unit tests for pure functions and business logic
- Integration tests for API endpoints and DB interactions
- E2E tests for critical user flows (use `e2e-testing` skill)
- Aim for >70% coverage on critical paths; >90% on business rules

### Code Review Checklist

- [ ] Does it solve the right problem?
- [ ] Are edge cases handled?
- [ ] Is error handling appropriate?
- [ ] Are there tests for new logic?
- [ ] Is naming clear and consistent?
- [ ] Is there unnecessary complexity?
- [ ] Are dependencies justified?
- [ ] Is documentation updated?

---

## Pitfalls

- **Don't over-engineer.** Start simple; add layers only when needed.
- **Don't mix concerns.** Keep UI, business logic, and data access separate.
- **Don't ignore performance early.** Design for scale but don't premature-optimize.
- **Don't skip error handling.** Every async call needs a catch; every input needs validation.
- **Don't break existing APIs.** Version changes; never surprise consumers.
- **Don't ignore type safety.** Use TypeScript or equivalent; `any` is a code smell.

## Related Skills

- `tdd-workflow` — Test-driven development for new features and bug fixes
- `nextjs-turbopack` — Next.js 16+ with Turbopack bundling
- `mcp-server-patterns` — Building MCP servers with Node/TypeScript
- `e2e-testing` — Playwright end-to-end testing
- `bun-runtime` — Bun as runtime, package manager, and bundler
