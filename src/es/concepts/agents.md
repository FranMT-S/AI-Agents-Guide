# Gestión de Contexto: AGENTS.md y Archivos de Reglas

La base de cualquier flujo de trabajo con agentes de IA es la **persistencia del contexto**. Sin un mecanismo de memoria externa, cada sesión comienza desde cero: el agente no sabe en qué proyecto trabaja, qué convenciones sigue el equipo, ni qué comandos usar para compilar y testear. Los archivos de reglas — encabezados por el estándar `AGENTS.md` — resuelven este problema fundacional inyectando conocimiento estructurado en el sistema del agente antes de procesar cualquier petición.

---

## ¿Qué es AGENTS.md y por qué existe?

`AGENTS.md` es el estándar multiplataforma de facto para gestionar el contexto de los agentes de IA dentro de un repositorio de código. Funciona como un `README` exclusivo para agentes: un documento predecible que el orquestador lee e inyecta automáticamente en el *system prompt* al inicio de cada sesión. Su importancia radica en tres factores:

1. **Elimina la ambigüedad del modelo base.** Sin este archivo, el agente infiere (a menudo incorrectamente) el stack tecnológico, la convención de nombres y los comandos de build. Con él, estas asunciones se convierten en certezas.
2. **Reducción del coste de inferencia.** El modelo no necesita explorar el repositorio a ciegas para entender cómo compilar o testear la aplicación. El conocimiento ya está presente al inicio.
3. **Portabilidad total.** Un desarrollador puede usar Cursor IDE y otro la CLI de Claude Code. Ambas herramientas respetarán las mismas directrices porque leen el mismo archivo.

> [!IMPORTANT]
> Este estándar es soportado nativamente por **Codex**, **Gemini CLI**, **Claude Code** (bajo el alias `CLAUDE.md`), **GitHub Copilot**, **OpenCode**, **Cursor** y **Antigravity**. Un único `AGENTS.md` en la raíz unifica a todas las herramientas.

---

## Estructura y Jerarquía de Alcance

Los agentes aplican una jerarquía de niveles para resolver conflictos de reglas. Las instrucciones de un subdirectorio tienen prioridad absoluta sobre las de la raíz o las globales.

```text
~/.gemini/GEMINI.md              (Global — preferencias universales del usuario)
mi-proyecto/
├── AGENTS.md                    (Proyecto — estándares base del repositorio)
├── src/
│   └── auth/
│       └── AGENTS.md            (Módulo — instrucciones prioritarias para este directorio)
└── legacy/
    └── AGENTS.override.md       (Override — reemplaza TODAS las instrucciones padre, solo Codex)
```

| Nivel | Alcance | Propósito |
| :--- | :--- | :--- |
| **Global** | Usuario | Idioma, estilo de respuesta, preferencias personales. |
| **Proyecto** | Repositorio | Stack tecnológico, comandos de build, arquitectura. |
| **Módulo** | Subdirectorio | Reglas restrictivas de un paquete o microservicio. |
| **Override** | Reemplazo total | Monorepos con paquetes legacy de convenciones distintas. |

---

## El Presupuesto de Instrucciones

> [!WARNING]
> Los LLMs de frontera pueden mantener razonablemente entre 150 y 200 instrucciones activas. El *system prompt* interno de herramientas como Claude Code ya consume ~50 instrucciones base. Cada regla extra que añades reduce matemáticamente la fiabilidad de todas las demás.

Un archivo `AGENTS.md` que crece ilimitadamente no mejora el comportamiento del agente; lo degrada. Las reglas no se ignoran al final del archivo: se ignoran de forma **uniforme y aleatoria** en todo el documento.

La solución es el **Principio de Progressive Disclosure**: concentra en el `AGENTS.md` raíz solo el mínimo indispensable, y distribuye el conocimiento específico en archivos secundarios que el agente carga bajo demanda.

```text
mi-proyecto/
├── AGENTS.md                        (Raíz — mínimo indispensable + punteros)
└── docs/
    ├── TYPESCRIPT.md                (Convenciones estrictas del lenguaje)
    ├── TESTING.md                   (Estrategia y comandos de pruebas)
    └── DATABASE_SCHEMA.md           (Patrones de migraciones y modelos)
```

**Referenciación correcta en `AGENTS.md` raíz:**
```markdown
This is a Node.js GraphQL API using Prisma and TypeScript.
Build: `pnpm build`. Typecheck: `pnpm tsc --noEmit`.

For task-specific guidance, read only what is relevant:
- TypeScript conventions: docs/TYPESCRIPT.md
- Testing patterns: docs/TESTING.md
- Database schema: docs/DATABASE_SCHEMA.md
```

> [!TIP]
> Usa referencias descriptivas, no imperativas. En vez de `ALWAYS read docs/TYPESCRIPT.md`, escribe `For TypeScript conventions, see docs/TYPESCRIPT.md`. El agente evaluará contextualmente si lo necesita, ahorrando miles de tokens cuando la tarea no involucra TypeScript.

---

## Secciones Recomendadas del Archivo

Un `AGENTS.md` bien estructurado contiene únicamente las secciones que un agente necesita para actuar correctamente en el repositorio:

| Sección | Propósito |
| :--- | :--- |
| **Project Overview** | Una sola frase describiendo qué hace el proyecto. |
| **Tech Stack** | Lenguajes, frameworks principales y gestores de paquetes. |
| **Development Setup** | Comandos de instalación y variables de configuración inicial. |
| **Build & Test Commands** | Comandos exactos para construir, testear, linting y typechecking. |
| **Code Style Guidelines** | Convenciones del equipo que un linter automático no puede manejar. |
| **Architecture Notes** | Estructura de carpetas y patrones de diseño clave. |
| **Security Practices** | Variables de entorno, sanitización y autenticación. |

---

## Terminología de Instrucción Correcta

La forma en que se redactan las instrucciones impacta directamente en cuánto las sigue el agente. Evita los antipatrones que generan obediencia inconsistente:

| ❌ Antipatrón | ✅ Estándar Preferido |
| :--- | :--- |
| `ALWAYS use async/await` | `Use async/await over promise chains` |
| `NEVER commit without tests` | `Run tests before committing: npm test` |
| `Write clean code` | `Use named exports. Prefer functional components.` |
| `Be careful with the database` | `Validate all inputs server-side. Use Prisma for queries.` |

---

## Ejemplo Completo de AGENTS.md

El siguiente archivo representa el estándar de producción para un proyecto TypeScript con backend Node.js. Es conciso, accionable y aplica Progressive Disclosure para los detalles.

```markdown
# Project Context

This is a Node.js REST API using Express, Prisma, and TypeScript.
Package manager: pnpm. Runtime: Node.js 22.

## Commands

- Build: `pnpm build`
- Dev server: `pnpm dev`
- Tests: `pnpm test` (Vitest)
- Typecheck: `pnpm tsc --noEmit`
- Lint: `pnpm lint` (ESLint + Prettier)

## Architecture

- `src/routes/` — Express route handlers (one file per resource)
- `src/services/` — Business logic (no DB access here)
- `src/db/` — Prisma client and query helpers
- `src/types/` — Shared TypeScript interfaces and enums

## Code Conventions

- Strict TypeScript. Never use `any`.
- Named exports only. No default exports.
- All async functions must handle errors with try/catch.
- Use Zod for request validation in all routes.

## Security

- Never log secrets or tokens.
- All environment variables are in `.env.example`. Use `process.env.VAR`.
- DB queries must use Prisma — no raw SQL.

## Task-Specific Guidance

- TypeScript conventions: docs/TYPESCRIPT.md
- Testing patterns: docs/TESTING.md
- Database schema: docs/DATABASE_SCHEMA.md
```

---

## Malas Prácticas a Evitar

| Problema | Por qué es peligroso |
| :--- | :--- |
| Añadir rutas de archivos absolutas (`src/auth/handlers.ts`) | Los archivos cambian de nombre y el agente queda desorientado. Describe el mapa funcional en su lugar. |
| Usar el archivo como repositorio de toda la especificación | Satura el contexto y el agente ignora reglas aleatoriamente. |
| Instrucciones contradictorias entre niveles sin justificación | El agente aplica la más específica pero puede confundirse en decisiones de arquitectura. |
| No versionar el archivo junto con el código | El contexto del agente queda desfasado cuando el proyecto evoluciona. |
| Incluir datos de negocio sensibles (IDs, endpoints de producción) | Estos datos pueden filtrarse si el agente reproduce el contexto en sus respuestas. |

---

## Compatibilidad por Herramienta

| Herramienta        | Archivo Nativo            | Soporta `AGENTS.md` | Particularidad                                         |
| :----------------- | :------------------------ | :------------------ | :----------------------------------------------------- |
| **Codex CLI**      | `AGENTS.md`               | ✅ Nativo            | Soporta `AGENTS.override.md` para anulación total.     |
| **Gemini CLI**     | `GEMINI.md`               | ✅ Sí                | Escaneo recursivo hacia arriba hasta `.git`.           |
| **Claude Code**    | `CLAUDE.md`               | ✅ Sí (alias)        | Genera `MEMORY.md` propio para aprendizajes de sesión. |
| **GitHub Copilot** | `copilot-instructions.md` | ✅ Sí                | Lee desde `.github/copilot-instructions.md`.           |
| **OpenCode**       | `AGENTS.md`               | ✅ Nativo            | Soporta URLs remotas en el campo `rules`.              |
| **Cursor**         | `.cursor/rules/*.mdc`     | ✅ Sí                | Activación por glob patterns con frontmatter YAML.     |
| **Antigravity**    | `AGENTS.md`               | ✅ Nativo            | Combina con reglas en `.agents/rules/`.                |

> [!TIP]
> Para equipos con múltiples agentes, crea `AGENTS.md` en la raíz y usa un symlink: `ln -s AGENTS.md CLAUDE.md`. Esto garantiza que Claude Code lo lea sin duplicar contenido en Git.

*Fuentes: [AGENTS.md Open Standard](https://github.com/agentsmd/agents.md) | [A Complete Guide to AGENTS.md — AIHero](https://www.aihero.dev/a-complete-guide-to-agents-md) | [Writing a Good CLAUDE.md — HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)*
