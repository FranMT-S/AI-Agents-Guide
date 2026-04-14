# Subagentes: Arquitectura, Configuración y Patrones

La orquestación con subagentes es el patrón de diseño más avanzado del ecosistema de agentes de IA actual. Permite transformar un único agente monolítico — que intenta diseñar, codificar, revisar y testear al mismo tiempo — en un equipo de especialistas coordinados donde cada miembro tiene un rol claro, un contexto acotado y permisos específicos. Este archivo documenta la arquitectura técnica, los esquemas de configuración por herramienta y los patrones de diseño probados en producción.

---

## Anatomía de un Subagente

Un subagente es una instancia secundaria de un modelo de lenguaje que el agente primario instancia bajo demanda. A diferencia del agente principal, un subagente posee tres características técnicas fundamentales:

1. **Contexto aislado**: solo recibe los fragmentos de código, reglas y documentación relevantes para su microtarea, previniendo la degradación por exceso de contexto.
2. **Herramientas restringidas**: su arsenal de tools y llamadas MCP está limitado a lo que su rol necesita. Un `code-reviewer` puede tener acceso a `read_file` y `git diff`, pero no a `write_file` ni `bash`.
3. **Ciclo de vida efímero**: comienza con una tarea específica, la ejecuta y termina, devolviendo solo su output al agente coordinador.

### El Patrón Manager / Specialist

```text
Usuario
  └── Agente Primario (Manager)
        ├── Delega a → architect  (diseña la solución)
        ├── Delega a → builder    (implementa el código)
        ├── Delega a → reviewer   (valida calidad y seguridad)
        └── Consolida y responde al Usuario
```

Cada delegación incluye únicamente el contexto necesario para esa fase. El `architect` no necesita saber cómo se testea el código; el `reviewer` no necesita el historial completo de la sesión. Este aislamiento es la fuente del valor arquitectónico de los subagentes.

---

> [!NOTE]
> **Mi Colección Personal:** Estoy organizando una colección de subagentes para diferentes propósitos. Si deseas verlos como guía para estructurar a tu equipo delegativo, puedes visitar:
> 🤖 **[Directorio de Subagentes (GitHub)](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/subagents)**

---

## Tipos de Subagentes

### Especializados personalizados

Son los que el equipo crea según su flujo de trabajo. Se definen como archivos Markdown (o TOML en Codex) con un frontmatter que describe el rol, el modelo y los permisos. El nombre del archivo es el identificador del agente.

**Casos de uso comunes:**
- `security-auditor`: revisión de vulnerabilidades antes de merge
- `api-designer`: diseño de contratos OpenAPI antes de codificar
- `test-generator`: generación de suites de pruebas unitarias
- `doc-writer`: documentación de funciones y módulos

### Integrados (built-in)

Vienen preconfigurados con cada herramienta. No requieren definición:

| Herramienta | Built-ins disponibles | Propósito |
| :--- | :--- | :--- |
| **OpenCode** | `build`, `plan`, `explore`, `general` | Ciclo completo de desarrollo |
| **Cursor** | `Explore`, `Bash`, `Browser` | Búsqueda, terminal y web |
| **Gemini CLI** | `codebase_investigator`, `cli_help`, `generalist_agent`, `browser_agent` | Análisis y enrutamiento |
| **Claude Code** | `Explore` (Haiku), `Plan` | Lectura y planificación |

### Híbridos

Subagentes personalizados que extienden el comportamiento de un built-in añadiendo instrucciones específicas del proyecto. Se configura el mismo `model` y `tools` del built-in pero con un `system prompt` adaptado al contexto del repositorio.

---

## Comunicación entre Subagentes

### Contratos de Datos (el error más común)

La comunicación entre subagentes **no debe ser prosa conversacional**. Cuando el `architect` le entrega su diseño al `builder`, debe hacerlo en un formato estructurado que el `builder` pueda consumir sin ambigüedad:

```markdown
ARCHITECTURE_PLAN:
routes:
  - POST /api/tasks → src/routes/tasks.ts
  - GET /api/tasks/:id → src/routes/tasks.ts
models:
  - Task: { id: uuid, title: string, status: enum(todo|done), userId: uuid }
db_schema: prisma/schema.prisma
```

El agente primario captura este bloque e inyecta exactamente ese formato en el prompt del `builder`. No parafrasea ni resume — entrega el contrato de datos íntegro. Esto elimina las tergiversaciones que ocurren cuando el modelo interpreta libremente el output del agente anterior.

### Flujo de Errores y Fallbacks

Cuando un subagente falla, el agente primario debe recibir un error estructurado:

```json
{
  "status": "failed",
  "agent": "builder",
  "reason": "prisma_schema_conflict",
  "message": "Cannot add field 'userId' — migration conflict in 003_add_users.sql",
  "retry_possible": true
}
```

El orquestador evalúa si el error es recuperable (`retry_possible: true`) y decide entre reintentar, escalar al usuario o invocar un subagente de diagnóstico.

---

## Control de Iteraciones y Recursión

> [!WARNING]
> El mayor riesgo técnico en orquestación multi-agente es el bucle infinito: el `builder` produce código con errores, el `reviewer` lo rechaza, el `builder` reintenta incorrectamente — y este ciclo se repite facturando miles de tokens sin progreso.

Todas las herramientas implementan un campo de límite de iteraciones:

| Herramienta | Campo | Default |
| :--- | :--- | :--- |
| **OpenCode** | `steps` | Sin límite (definir explícitamente) |
| **Cursor** | `maxTurns` (en frontmatter del agente) | Heredado del sistema |
| **Gemini CLI** | `max_turns` | 30 |
| **Claude Code** | `maxTurns` | Sin límite |
| **Codex CLI** | `--max-steps` (flag CLI) | Sin límite |

**Regla práctica**: define siempre `max_turns` entre 5 y 15 para subagentes de revisión y entre 10 y 25 para subagentes de implementación. Más iteraciones raramente producen mejores resultados; indican un system prompt insuficientemente específico.

---

## Permisos por Rol

El sistema de permisos es lo que convierte los subagentes de una conveniencia en una herramienta de seguridad real. Cada subagente debe tener solo los permisos que su rol requiere:

| Rol | `edit` | `bash` | `webfetch` | Propósito |
| :--- | :--- | :--- | :--- | :--- |
| `architect` | `deny` | `deny` | `deny` | Solo lee y planifica |
| `builder` | `allow` | `ask` (selectivo) | `deny` | Escribe código, bash con confirmación |
| `reviewer` | `deny` | `allow: git diff, git log` | `deny` | Lee diffs, no modifica |
| `tester` | `deny` | `allow: npm test, pytest` | `deny` | Ejecuta tests, no codifica |
| `doc-writer` | `allow: *.md` | `deny` | `allow` | Escribe docs, puede consultar web |

---

## Configuración por Herramienta

### OpenCode

OpenCode soporta dos métodos de configuración. El método Markdown es el más legible y recomendado para subagentes personalizados.

**Estructura de Directorio:**
```text
~/.config/opencode/agents/      (Global — disponibles en todos los proyectos)
    └── security-auditor.md

mi-proyecto/
└── .opencode/
    └── agents/                 (Proyecto — compartidos via git)
        ├── architect.md
        ├── builder.md
        └── code-reviewer/
            ├── code-reviewer.md
            └── standards/
                └── api-checklist.md
```

**Ejemplo: Arquitecto de APIs (`architect.md`):**
```markdown
---
description: Designs API architecture. Use when starting a new feature or endpoint.
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.2
steps: 8
permission:
  edit: deny
  bash:
    "*": deny
  webfetch: allow
---
You are a software architect. Your ONLY job is to produce a structured plan.

Given a feature request, output a plan with:
1. Route definitions (method, path, handler file)
2. Data models with field types
3. Database schema changes required
4. Dependencies between tasks

Output ONLY valid structured Markdown. No prose explanations.
```

**Ejemplo: Revisor con acceso Git (`code-reviewer.md`):**
```markdown
---
description: Reviews code for quality, security and best practices. Use before merging.
mode: subagent
model: anthropic/claude-haiku-4-20250514
temperature: 0.1
steps: 5
permission:
  edit: deny
  bash:
    "*": deny
    "git diff": allow
    "git log --oneline*": allow
  webfetch: deny
---
You are a strict code reviewer. Read the git diff and evaluate:
1. Security: injection, hardcoded secrets, missing validation
2. Quality: naming, complexity, edge cases
3. Standards: follows AGENTS.md conventions

Return a JSON array of findings:
[{ "file": "...", "line": N, "severity": "critical|high|medium", "issue": "...", "fix": "..." }]
```

*Fuentes: [OpenCode: Agents](https://opencode.ai/docs/agents/) | [OpenCode: Permissions](https://opencode.ai/docs/permissions/)*

---

### Cursor

**Estructura de Directorio:**
```text
~/.cursor/agents/               (Global — disponibles en todos los proyectos)
    └── researcher.md

mi-proyecto/
├── AGENTS.md
└── .cursor/
    └── agents/                 (Proyecto — compartidos via git)
        ├── architect.md
        └── code-reviewer.md
```

**Ejemplo: Arquitecto Planificador (`architect.md`):**
```markdown
---
name: architect
description: Plans and structures new features. Use when the user asks to build something new end-to-end.
model: inherit
is_background: false
readonly: true
---
You are a software architect. You plan; you do not code.

1. Analyze the request and break it into concrete tasks.
2. For each task, specify: file to create/modify, what changes and why.
3. Output the plan as a numbered list the builder agent can execute sequentially.
4. Do not write code. Only produce the structured task list.
```

**Ejemplo: Revisor de Código (`code-reviewer.md`):**
```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and performance. Use after implementing changes.
model: fast
readonly: true
---
You are a skeptical code reviewer. Analyze the files provided and return:
- Specific issues with file path and line number
- Severity: critical | high | medium | low
- Suggested fix for each issue

Apply the conventions from AGENTS.md in the relevant directory.
Do not approve the change if critical issues exist.
```

*Fuente: [Cursor Docs: Subagents](https://cursor.com/docs/agent/subagents)*

---

### Gemini CLI

**Estructura de Directorios:**
```text
~/.gemini/agents/               (Global — personales, no compartidos con el equipo)
    └── security-auditor.md

mi-proyecto/
└── .gemini/
    └── agents/                 (Proyecto — compartidos via git)
        ├── dev-orchestrator.md
        ├── code-writer.md
        └── code-reviewer.md
```

**Ejemplo: Escritor de Código (`code-writer.md`):**
```markdown
---
name: code-writer
description: Implements code based on a provided architectural plan. Use after architect produces the plan.
kind: local
tools:
  - read_file
  - write_file
  - edit_file
model: gemini-3.1-flash
temperature: 0.2
max_turns: 20
---
You implement code. You receive a structured plan and execute it file by file.

Rules:
- Never deviate from the plan. If the plan is unclear, report it instead of guessing.
- Apply the conventions from the project AGENTS.md.
- After implementing each file, output a brief summary of what was done.
```

**Soporte de Wildcards en `tools`:**

```yaml
tools:
  - read_file
  - write_file
  - mcp_github_*        # Todas las herramientas del MCP de GitHub
  - code-reviewer       # Puede invocar al subagente code-reviewer
```

> [!WARNING]
> Un subagente en Gemini CLI **no puede invocar a otro automáticamente** a menos que ese agente esté listado explícitamente en su campo `tools`. El `AgentRegistry` oculta todos los demás subagentes por defecto para prevenir recursión no controlada.

*Fuentes: [Gemini CLI: Subagents](https://geminicli.com/docs/core/subagents/) | [Gemini CLI: Subagents Isolation](https://geminicli.com/docs/core/subagents/#isolation-and-recursion-protection)*

---

### Claude Code

**Estructura de Directorios:**
```text
~/.claude/agents/               (Global — disponibles en todos los proyectos)
    └── researcher.md

mi-proyecto/
└── .claude/
    └── agents/                 (Proyecto — compartidos via git)
        ├── coordinator.md
        └── api-developer/
            ├── api-developer.md
            └── prompts/
                └── conventions.md
```

**Ejemplo: Coordinador de Desarrollo (`coordinator.md`):**
```markdown
---
name: coordinator
description: Manages the development cycle. Delegates to specialists based on the task type.
model: sonnet
tools: Read, Glob, Agent(api-developer), Agent(code-reviewer)
permissionMode: default
maxTurns: 30
background: false
---
You coordinate the development team. You do NOT write code.

Workflow:
1. Analyze the feature request.
2. If it involves API changes → delegate to @api-developer.
3. After implementation → delegate to @code-reviewer.
4. If reviewer finds critical issues → send findings back to @api-developer.
5. Only finalize when reviewer approves. Report the summary to the user.
```

> [!IMPORTANT]
> Para invocar a otro subagente desde un subagente en Claude Code, el agente invocador debe incluir `Agent(nombre)` en su lista de `tools`. Sin esta declaración explícita, el agente no puede instanciar al especialista.

> [!TIP]
> Usa `background: true` para subagentes que pueden correr en paralelo con otras operaciones. Usa `isolation: worktree` para subagentes que trabajan en ramas Git aisladas sin interferir con el estado local del repositorio.

*Fuente: [Claude Code: Sub-agents](https://code.claude.com/docs/en/sub-agents)*

---

### Codex CLI

**Estructura de Directorio:**
```text
mi-proyecto/
└── .codex/
    └── agents/
        ├── reviewer.toml
        └── builder.toml
```

> [!NOTE]
> Codex CLI usa formato TOML para los subagentes, a diferencia del resto del ecosistema que usa Markdown con frontmatter YAML.

**Ejemplo: Builder Autónomo (`builder.toml`):**
```toml
name = "builder"
description = "Implements code changes based on a provided plan. Use for feature implementation."
model = "gpt-5.3-codex"
sandbox_mode = "workspace-write"
developer_instructions = """
You implement code. You receive a structured plan and execute it.

Rules:
- Follow the plan exactly. Do not add unrequested features.
- Apply the conventions in AGENTS.md.
- After each file change, output a brief summary.
- If a plan step is ambiguous, output an error instead of guessing.
"""
```

**Ejemplo: Revisor de PR (`reviewer.toml`):**
```toml
name = "reviewer"
description = "Reviews code changes for correctness, security, and missing tests."
model = "gpt-5.4"
sandbox_mode = "read-only"
developer_instructions = """
Review the code like an owner. Prioritize:
1. Correctness and edge cases
2. Security vulnerabilities
3. Missing test coverage
4. Behavior regressions

Return findings as a structured list: file, line, severity (critical/high/medium), issue, suggested fix.
"""
```

*Fuente: [Codex CLI: Subagents Guide](https://developers.openai.com/codex/subagents)*

---

## Patrones Avanzados

### Lecturas Paralelas, Escrituras Secuenciales

Para tareas de análisis (leer documentación, escanear logs, revisar dependencias), instancia múltiples subagentes de lectura en paralelo. Para fases de escritura, fuerza secuencialidad estricta para evitar condiciones de carrera.

```text
PARALLEL (lectura):
  ├── security-auditor  → lee src/auth/
  ├── perf-auditor      → lee src/db/
  └── api-auditor       → lee src/routes/

SEQUENTIAL (escritura, en orden):
  1. builder   → implementa cambios
  2. tester    → ejecuta suite
  3. doc-writer → actualiza documentación
```

### Anidación Controlada

Un subagente puede invocar a otro si su schema lo permite explícitamente. Esto permite patrones de especialización de dos niveles:

```text
dev-orchestrator
  └── api-developer
        └── db-schema-designer  (sub-sub-agente, instanciado por api-developer)
```

> [!WARNING]
> Limita la anidación a máximo dos niveles. Tres o más niveles de recursión generan contextos imposibles de depurar y multiplican el coste de tokens exponencialmente.

### Housekeeping Obligatorio

Todo subagente que modifica estado (archivos, ramas Git, recursos externos) debe incluir instrucciones explícitas de limpieza ante fallo:

```markdown
If any step fails, before returning control to the coordinator:
1. Revert all file changes using `git checkout -- .`
2. Report which step failed and what the error was
3. Do NOT leave partial implementations in the working tree
```

---

## Checklist de Producción

Antes de desplegar un sistema multi-agente en un repositorio real, verifica:

- [ ] Cada subagente tiene `max_turns` o `steps` definido explícitamente
- [ ] Los permisos de `bash` usan allowlists específicas, nunca `"*": allow` en producción
- [ ] Los contratos de datos entre agentes son estructurados (JSON/Markdown), no prosa libre
- [ ] El agente coordinador tiene instrucciones de fallback explícitas para cuando un especialista falla
- [ ] Las escrituras entre subagentes son secuenciales (nunca paralelas sobre los mismos archivos)
- [ ] La descripción (`description`) de cada subagente es suficientemente específica para que el orquestador sepa exactamente cuándo invocarlo

*Fuentes generales: [OpenCode: Agents](https://opencode.ai/docs/agents/) | [Cursor: Subagents](https://cursor.com/docs/agent/subagents) | [Gemini CLI: Subagents](https://geminicli.com/docs/core/subagents/) | [Claude Code: Sub-agents](https://code.claude.com/docs/en/sub-agents) | [Codex CLI: Subagents](https://developers.openai.com/codex/subagents)*
