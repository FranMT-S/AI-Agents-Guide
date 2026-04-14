# Gestión de Contexto: AGENTS.md y Archivos de Reglas

La base de cualquier flujo de trabajo con agentes de IA es la **persistencia del contexto**. Sin un mecanismo de memoria externa, cada sesión comienza desde cero: el agente no sabe en qué proyecto trabaja, qué convenciones sigue el equipo, ni qué comandos usar para compilar y testear. Los archivos de reglas — encabezados por el estándar `AGENTS.md` — resuelven este problema fundacional inyectando conocimiento estructurado en el sistema del agente antes de procesar cualquier petición.

---

> [!NOTE]
> **Mi Colección Personal:** Muchos de los *templates* para contextualizar agentes los tengo ya estructurados. Si deseas ver mis carpetas para inspirarte o reutilizarlas, puedes visitar:
> 🏗️ **[Templates para Agentes](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/templates/agents)**

---

## El Rol Fundamental de AGENTS.md

`AGENTS.md` es el estándar multiplataforma de facto para gestionar el contexto de los agentes de IA dentro de un repositorio de código. Funciona como un `README` exclusivo para agentes: un documento predecible que el orquestador lee e inyecta automáticamente en el *system prompt* al inicio de cada sesión. Su importancia radica en tres factores:

1. **Elimina la ambigüedad del modelo base.** Sin este archivo, el agente infiere (a menudo incorrectamente) el stack tecnológico, la convención de nombres y los comandos de build. Con él, estas asunciones se convierten en certezas.
2. **Habilita el ahorro de latencia y costo.** El modelo no necesita explorar el repositorio a ciegas para entender cómo compilar o testear la aplicación. El conocimiento estático ya está pre-cargado.
3. **Ofrece portabilidad entre sistemas.** Un desarrollador puede usar Cursor IDE y otro la CLI de Claude Code. Ambas herramientas respetarán las mismas directrices al leer este contrato universal.

> [!IMPORTANT]
> Este estándar es soportado nativamente por **Codex**, **Gemini CLI**, **Claude Code** (bajo el alias `CLAUDE.md`), **GitHub Copilot**, **OpenCode**, **Cursor** y **Antigravity**. Un único `AGENTS.md` en la raíz unifica a todas las herramientas.

---

## Jerarquía de Archivos y Resolución de Conflictos

Los agentes aplican una estricta jerarquía de niveles para resolver colisiones de conocimiento. Las instrucciones albergadas en un subdirectorio tienen prioridad y sobreescriben a las ubicadas en el directorio padre o globales.

```text
~/.gemini/GEMINI.md              (Global — preferencias universales del usuario)
mi-proyecto/
├── AGENTS.md                    (Proyecto — estándares base del repositorio)
├── src/
│   └── auth/
│       └── AGENTS.md            (Módulo — instrucciones prioritarias para este directorio)
└── legacy/
    └── AGENTS.override.md       (solo Codex, Override — reemplaza TODAS las instrucciones padre, )
```

| Nivel | Alcance | Propósito |
| :--- | :--- | :--- |
| **Global** | Usuario | Idioma, estilo de respuesta, preferencias personales de Output. |
| **Proyecto** | Repositorio | Stack tecnológico, comandos de compilación, arquitectura. |
| **Módulo** | Subdirectorio | Reglas restrictivas o aislamiento funcional de un *microservicio*. |
| **Override** | Reemplazo total | Monorepos donde paquetes legacy exigen convenciones radicalmente distintas. |

---

## Límites Cognitivos y Revelación Progresiva (Progressive Disclosure)

Un archivo `AGENTS.md` que crece ilimitadamente no mejora la precisión analítica del agente; la degenera. A diferencia de un lector humano, si el agente recibe demasiada información irrelevante, no ignora simplemente la información del final del documento, sino que pierde la capacidad de priorizar de forma **uniforme y aleatoria** a lo largo de todo su contexto de atención.

La solución arquitectónica a este problema es aplicar el **Principio de Progressive Disclosure** (Revelación Progresiva). Esto consiste en concentrar en el `AGENTS.md` raíz única y exclusivamente el contexto fundacional indispensable, distribuyendo todo el conocimiento profundo en archivos secundarios que el agente inyectará en su memoria sólo si la tarea actual lo exige.

### Ejemplo de Estructura Desacoplada

```text
mi-proyecto/
├── AGENTS.md                        (Raíz — mínimo indispensable + descriptores semánticos)
└── docs/
    ├── TYPESCRIPT.md                (Convenciones estrictas del lenguaje y linter)
    ├── TESTING.md                   (Estrategia, fixtures y comandos de pruebas)
    └── DATABASE_SCHEMA.md           (Diseño relacional y convenciones de Prisma)
```

### Sintaxis de Referenciación Dinámica

Para encadenar estos sub-archivos de forma eficiente, redacta tu AGENTS.md referenciándolos con descriptores claros, delegando al agente la decisión autónoma de si requiere su lectura o no.

**Formato recomendado en la raíz:**
```markdown
This is a Node.js GraphQL API using Prisma and TypeScript.
Build: `pnpm build`. Typecheck: `pnpm tsc --noEmit`.

For task-specific guidance, read only the documents meaningfully related to your current task:
- TypeScript conventions and types: docs/TYPESCRIPT.md
- Integration testing patterns: docs/TESTING.md
- Relational schema structure: docs/DATABASE_SCHEMA.md
```

> [!TIP]
> Usa referencias descriptivas, nunca imperativas. En vez de gritarle a la máquina: `ALWAYS read docs/TYPESCRIPT.md`, escribe `For TypeScript conventions, see docs/TYPESCRIPT.md`. El agente evaluará inteligentemente la semántica del problema; ahorrándote miles de tokens cuando, por ejemplo, le pides editar un simple archivo Markdown.

> [!WARNING]
> **El Presupuesto Crítico de Instrucción (Attention Window):**
> Los LLMs de la actual generación pueden sostener alta fidelidad computacional al manejar entre **150 y 200 intenciones activas**. Considera que el *System Prompt* nativo de tu orquestador (ej. Cursor o Claude) ya consume base ~50 instrucciones iniciales. Cada regla redundante merma matemáticamente la eficacia de todo tu sistema.

---

## Anatomía de un Archivo AGENTS.md Eficiente

Un documento configurado magistralmente restringe su contenido únicamente a aquellas métricas que un Linter o Compilador interno es incapaz de salvaguardar:

| Bloque Semántico | Función Práctica | Ejemplo Práctico |
| :--- | :--- | :--- |
| **Project Overview** | El contexto general en 1 sola frase. | *"This is a Next.js e-commerce storefront for B2B wholesale."* |
| **Core Tech Stack** | Versiones rígidas y el framework subyacente. | *"Use pnpm. Next.js App Router, React 19, Tailwind CSS v4."* |
| **Build & Test Macros** | Los comandos exactos que la IA usará. | *"To test: `pnpm vitest`. To build: `pnpm run build`."* |
| **Code Style Guidelines** | Convenciones que el linter no atrapa. | *"Prefer Early Returns. Order imports: external first, relative last."* |
| **Architecture Guards** | Fronteras entre carpetas críticas. | *"The `src/components/` folder CANNOT import from `src/database/`."* |
| **Security Policies** | Advertencias inesquivables antes de picar código. | *"Never write raw SQL. Always use Prisma ORM to prevent injections."* |

---

## Redacción de Instrucciones: Heurísticas y Antipatrones

La retórica aplicada en tus instrucciones altera contundentemente la obediencia probabilística del motor. Aleja tus directivas de prohibiciones abstractas hacia macros accionables:

| ❌ Antipatrón Burocrático | ✅ Estándar Accionable |
| :--- | :--- |
| `ALWAYS use async/await` | `Use async/await over promise chains` |
| `NEVER commit without tests` | `Run tests before committing: npm test` |
| `Write clean code` | `Use named exports. Prefer functional components.` |
| `Be careful with the database` | `Validate all inputs server-side. Use Prisma for queries.` |

---

## Plantilla de Referencia para Configuración a Producción

La plantilla a continuación ejemplifica un proyecto *Backend de Express robusto*, destiladando progresividad y agudeza técnica.

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

## Errores Comunes en la Ingeniería de Contexto

| Falla Estructural | Impacto Negativo (El Riesgo) | Alternativa Correcta (La Solución) |
| :--- | :--- | :--- |
| Hardcodear rutas de archivos absolutas (`src/utils/math.ts`) | El LLM se atasca y alucina código si el archivo fue movido o renombrado. | Describe **fronteras de carpetas**: *"Archivos de lógica pura están bajo `src/utils/`"*. |
| Consolidar 500 líneas en el AGENTS.md raíz | Quiebre del *Attention Window*. El modelo ignorará las directrices de mayor seguridad aleatoriamente. | Aplica el principio de **Progressive Disclosure**. Mueve reglas específicas a `/docs/*.md`. |
| Incoherencias directas entre un AGS local y el global | El sub-agente intentará lidiar con lógica cruzada y generará deuda arquitectónica. | Escribe un **bloque de Override explícito** si un paquete local debe anular las reglas padres. |
| Omitir el archivo del repositorio (ej. en `.gitignore`) | Diferentes humanos y agentes en distintos ordenadores programarán guiados por convenciones rotas. | Trata al AGENTS.md como código crítico. Házle **`git commit`** siempre para la fuente compartida. |
| Acumular Secrets, contraseñas o IPs en texto plano | Un LLM conversacional que reflexiona sobre el archivo puede filtrar los tokens por error o enviarlos a sus nubes de guardado temporal. | Enmascara la inyección usando reglas como: **"Todos los secretos cargan desde un `.env` a nivel Root"**. |

---

## Soporte y Equivalencias por Ecosistema

| Proveedor Integrado | Fichero Base Localizado   | Soporte al Estándar | Rasgos y Particularidades del Entorno                  |
| :----------------- | :------------------------ | :------------------ | :----------------------------------------------------- |
| **Codex CLI**      | `AGENTS.md`               | ✅ Nativo            | Despliega soporte singular sobre `AGENTS.override.md`. |
| **Gemini CLI**     | `GEMINI.md`               | ✅ Sí                | Barrido iterativo hacia carpetas de mayor altitud hasta topar con un nodo `.git`. |
| **Claude Code**    | `CLAUDE.md`               | ✅ Sí (Mediante Alias)| Destaca por engendrar `MEMORY.md` orgánicamente desde logs conversacionales. |
| **GitHub Copilot** | `copilot-instructions.md` | ✅ Sí                | Requiere estar estacionado estrictamente dentro el folder oculto de la organización (`.github/`). |
| **OpenCode**       | `AGENTS.md`               | ✅ Nativo            | Permite anclar `URLs` perimetrales inyectadas directamente. |
| **Cursor IDE**     | `.cursor/rules/*.mdc`     | ✅ Sí                | Sistema regido bajo activadores cruzados referenciando `Glob Patterns`. |
| **Antigravity**    | `AGENTS.md`               | ✅ Nativo            | Suma soporte híbrido permitiendo encastrar con `.agents/rules/`. |

> [!TIP]
> **Compatibilidad Absoluta para Monorepos Agudos:** 
> Genera tu `AGENTS.md` monolítico en la raíz topológica y utiliza un *symlink* virtual de cara al resto de utilidades, por ejemplo: `ln -s AGENTS.md CLAUDE.md`. Esto afianza inmutabilidad sin tener que clonar los manuales manualmente.

*Fuentes Oficiales Adicionales: [AGENTS.md Open Standard](https://github.com/agentsmd/agents.md) | [A Complete Guide to AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md) | [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)*
