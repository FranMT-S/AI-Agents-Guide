# Claude Code: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Claude Code en cuanto a la gestión de contexto, habilidades, automatización, sub-agentes y Agent Teams.

![[../attachments/session-agent.png]]

## Gestión de Contexto (Memory & Agents.md)

Claude Code utiliza principalmente los archivos `CLAUDE.md`, `.claude/rules/*.md` y `CLAUDE.local.md`. También soporta el estándar `AGENTS.md`.

### Auto Memory y Reglas de Ruta
Su característica más destacada es el **Auto Memory**: Claude genera su propio archivo `MEMORY.md` para recordar aprendizajes de depuración. La propiedad `paths` permite limitar reglas a carpetas específicas, y admite `symlinks` para compartir configuraciones.

### Estructura de Directorios
```text
~/.claude/CLAUDE.md              (Global — preferencias universales del usuario)
mi-proyecto/
├── AGENTS.md                    (Proyecto — reglas del repositorio)
├── CLAUDE.md                    (Proyecto — reglas del repositorio)
├── CLAUDE.local.md              (Proyecto local — ignorado en Git)
└── .claude/
    └── rules/
        └── testing.md           (Modulo — reglas específicas por contexto)
```

### Ejemplo de Configuración (Frontmatter)
```yaml
---
description: Reglas para el backend
paths: ["src/backend/**"]
---
```
*Fuente: [Claude Code: Memory & Agents.md](https://code.claude.com/docs/en/memory#agents-md)*

## Skills (Habilidades)

### Jerarquía de Descubrimiento
Las skills se descubren siguiendo la jerarquía: `Enterprise` > `Personal` (`~/.claude/skills/`) > `Project` (`.claude/skills/`).

### Metadatos y Aislamiento de Contexto
Usa metadatos YAML avanzados en `SKILL.md`. La propiedad `allowed-tools` restringe herramientas; `context: fork` obliga a ejecutar la skill en un subagente separado; y `disable-model-invocation: true` para invovación manual. Inyecta variables como `${CLAUDE_SESSION_ID}`.

### Estructura de Directorios
```text
mi-proyecto/
└── .claude/
    └── skills/
        └── my-skill/
            └── SKILL.md
```
*Fuente: [Claude: Skills Guide](https://code.claude.com/docs/en/skills)*

## MCP (Model Context Protocol)

### Transportes y Protocolos
Soporta `Stdio` y `HTTP`. Implementa `Tools`, `Prompts`, `Resources` y **Channels** para notificaciones push asíncronas (ej. alertas de sistemas CI).

### Jerarquía y Seguridad
Sigue una configuración jerárquica: `Enterprise` (`managed-mcp.json`), `Local/Project` (`.mcp.json`) y `User` (`~/.claude.json`). Permite `headersHelper` para tokens dinámicos y restricción mediante `allowedMcpServers` y `deniedMcpServers`.

### Estructura de Directorio
```text
mi-proyecto/
└── .mcp.json
```

### Ejemplo de Configuración (`.mcp.json`)
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  },
  "allowedMcpServers": ["github"],
  "deniedMcpServers": ["local-fs"]
}
```
*Fuente: [Claude Code: MCP Guide](https://code.claude.com/docs/en/mcp)*

## Plugins y Extensiones

### Arquitectura de Plugins
La arquitectura es modular; los plugins agrupan skills, agentes, hooks y servidores (MCP/LSP) mediante `.claude-plugin/plugin.json`.

### Inteligencia vía LSP y Output Styles
Soporta inyección de **Servidores LSP**, proveyendo diagnósticos e inteligencia de código en terminal. Los "Output Styles" alteran estructuralmente la comunicación del agente.

### Estructura de Directorio
```text
mi-plugin/
├── .claude-plugin/
│   └── plugin.json
└── src/
    └── index.js
```

### Gestión de Plugins (Terminal)
```bash
/plugin install @anthropic/mcp-server-github
```
*Fuentes: [Claude Code: Discover Plugins](https://code.claude.com/docs/en/discover-plugins), [Claude Code: Plugins](https://code.claude.com/docs/en/plugins)*

## Sub-agentes (Subagents)

Los sub-agentes son agentes especializados que operan en **ventanas de contexto aisladas** dentro de la misma sesión de Claude Code. El orquestador principal les delega tareas basándose en su `description`, y pueden ejecutarse en primer plano (bloqueante) o en segundo plano (concurrente con `Ctrl+B`).

### Capacidades Clave
- **Delegación automática:** El orquestador lee la `description` y decide cuándo delegar. También se pueden invocar explícitamente con `@nombre` o `--agent <nombre>`.
- **Aislamiento de herramientas:** Cada sub-agente puede restringir sus `tools` a un subconjunto (allowlist) o excluir herramientas específicas con `disallowedTools`.
- **Memoria persistente:** El campo `memory` (`user`, `project`, `local`) mantiene un `MEMORY.md` entre sesiones en `.claude/agent-memory/<nombre>/`.
- **Skills y MCP exclusivos:** Pueden precargar `skills` y definir `mcpServers` con scope exclusivo (inline o por referencia).
- **Hooks propios:** Soportan hooks del ciclo de vida (`PreToolUse`, `PostToolUse`, `Stop`) directamente en su frontmatter.
- **Sub-agentes Built-in:** Claude Code incluye `Explore` (Haiku, solo lectura), `Plan` (modelo heredado, solo lectura) y un sub-agente de propósito general.

### Estructura de Directorios
```text
~/.claude/agents/                (Global — disponibles en todos los proyectos)
    ├── researcher.md            (Sub-agente simple — archivo unico)
    └── api-auditor/             (Sub-agente con recursos — subdirectorio)
        ├── api-auditor.md       (El .md raiz define al sub-agente)
        └── context/             (Prompts de apoyo, estándares, ejemplos)
            └── api-standards.md
mi-proyecto/
└── .claude/
    ├── agents/                  (Proyecto — solo disponibles en este repo)
    │   ├── coordinator.md
    │   └── api-developer/
    │       ├── api-developer.md
    │       └── prompts/
    │           └── conventions.md
    ├── skills/                  (Skills que los sub-agentes pueden precargar)
    │   └── api-conventions.md
    └── agent-memory/            (Memoria persistente por sub-agente)
        └── researcher/
```

> [!TIP]
> La estructura por subdirectorios agrupa al sub-agente con sus archivos de apoyo. El `.md` cuyo nombre coincide con el directorio padre define al sub-agente; el resto son recursos de contexto inyectados automáticamente.

### Campos del Frontmatter (Sub-agentes)

| Campo             | Descripción                                                                      | Valores                                                       |
| ----------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `name`            | Identificador del sub-agente                                                     | string                                                        |
| `description`     | Cuándo invocarlo (el orquestador lo lee para delegar)                            | string                                                        |
| `model`           | Modelo a usar                                                                    | `haiku`, `sonnet`, `opus`, ID completo, `inherit`             |
| `tools`           | Allowlist de tools permitidas                                                    | `Read`, `Write`, `Bash`, `Agent`, `Grep`, etc.                |
| `disallowedTools` | Tools a excluir del total heredado                                               | Mismos valores que `tools`                                    |
| `skills`          | Skills a precargar en el contexto                                                | lista de nombres                                              |
| `mcpServers`      | Servidores MCP exclusivos (inline o por referencia)                              | nombre o config completa                                      |
| `hooks`           | Hooks del ciclo de vida (`PreToolUse`, `PostToolUse`, `Stop`)                    | objeto de hooks                                               |
| `memory`          | Alcance de la memoria persistente                                                | `user`, `project`, `local`                                    |
| `permissionMode`  | Modo de permisos                                                                 | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `background`      | Ejecutar concurrentemente en segundo plano                                       | `true` / `false`                                              |
| `effort`          | Nivel de esfuerzo del modelo                                                     | `low`, `medium`, `high`, `max`                                |
| `isolation`       | Ejecutar en Git Worktree aislado                                                 | `worktree`                                                    |
| `maxTurns`        | Limite de turnos de razonamiento                                                 | numero                                                        |
| `color`           | Color en la UI                                                                   | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt`   | Prompt inicial al iniciar con `--agent`                                         | string                                                        |

#### Referencia de Tools (valores para `tools` y `disallowedTools`)

| Categoria                  | Tools                                                                       |
| -------------------------- | --------------------------------------------------------------------------- |
| **Archivos**               | `Read`, `Write`, `Edit`, `Glob`, `Grep`                                     |
| **Terminal**               | `Bash`, `PowerShell`                                                        |
| **Web**                    | `WebFetch`, `WebSearch`                                                     |
| **Agentes y Skills**       | `Agent`, `Agent(nombre)`, `Skill`, `SendMessage`                            |
| **Tareas asíncronas**      | `TaskCreate`, `TaskGet`, `TaskList`, `TaskStop`, `TaskUpdate`, `TaskOutput` |
| **Modos**                  | `EnterPlanMode`, `ExitPlanMode`, `EnterWorktree`, `ExitWorktree`            |
| **Cron (scheduled tasks)** | `CronCreate`, `CronDelete`, `CronList`                                      |
| **Teams (experimental)**   | `TeamCreate`, `TeamDelete`                                                  |
| **MCP**                    | `ListMcpResourcesTool`, `ReadMcpResourceTool`, `ToolSearch`                 |
| **Otros**                  | `TodoWrite`, `NotebookEdit`, `LSP`, `AskUserQuestion`                       |

*Fuente: [Claude Code: Sub-agents](https://code.claude.com/docs/en/sub-agents)*

### Ejemplo: Sub-agente de API (`api-developer.md`)

```markdown
---
name: api-developer
description: Implements REST API endpoints following team conventions.
model: haiku
tools: Read, Glob, Grep, Write, Edit, Bash
skills:
  - api-conventions
  - error-handling-patterns
mcpServers:
  - github
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
memory: project
permissionMode: acceptEdits
effort: high
color: blue
---
Implement REST API endpoints. Follow the conventions from the preloaded skills.
Do not modify files outside of src/api/.
```

### Ejemplo: Sub-agente con Hooks de Validación (`db-reader.md`)

```markdown
---
name: db-reader
description: Execute read-only database queries.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
Only execute SELECT queries. Never modify data.
```

---

## Agent Teams (Equipos de Agentes)

> [!WARNING]
> Agent Teams es una funcionalidad **experimental**. Requiere activar el flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` en `settings.json` o como variable de entorno.

Los Agent Teams coordinan **múltiples sesiones independientes de Claude Code** trabajando en paralelo sobre un mismo proyecto. A diferencia de los sub-agentes (que operan dentro de la misma sesión), cada *teammate* es un proceso separado con su propia ventana de contexto, comunicándose mediante un sistema de mensajería y una lista de tareas compartida.

### Diferencias con los Sub-agentes

| Aspecto              | Sub-agentes                          | Agent Teams                          |
| -------------------- | ------------------------------------ | ------------------------------------ |
| **Arquitectura**     | Dentro de la misma sesión            | Procesos separados (multi-sesión)    |
| **Comunicación**     | Return value al orquestador          | Mensajería bidireccional + task list |
| **Visualización**    | Inline en el chat                    | In-process o split panes (`tmux`)    |
| **Coordinación**     | Secuencial o background              | Paralelo real con Lead + Teammates   |
| **Casos de uso**     | Tareas enfocadas, delegación simple  | Investigación paralela, refactoring multi-capa |
| **Estado**           | Estable                              | Experimental                         |

### Activación

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### Cómo Funcionan
- **Lead:** La sesión principal que crea y gestiona al equipo. Solo el Lead puede crear/destruir teammates.
- **Teammates:** Sesiones independientes que ejecutan tareas de la lista compartida. Pueden usar definiciones de sub-agentes existentes como base (`tools`, `model`, `skills`, `mcpServers`).
- **Comunicación:** `message` (a un teammate específico) o `broadcast` (a todos). Los teammates notifican automáticamente al Lead cuando terminan.
- **Task list:** Lista compartida donde el Lead asigna tareas y los teammates las reclaman (*self-claim*).

### Modos de Visualización
- **In-process:** Todos ejecutan en la misma terminal. `Shift+Down` para navegar entre teammates. Funciona en cualquier terminal.
- **Split panes:** Cada teammate en su propio panel. Requiere `tmux` o `iTerm2`.

### Ejemplo de Uso

```text
Create an agent team to review PR #142. Spawn three reviewers:
 - One focused on security implications
 - One checking performance impact
 - One validating test coverage
Have them each review and report findings.
```

### Hooks Exclusivos de Agent Teams

| Hook              | Descripción                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| `TeammateIdle`    | Se ejecuta cuando un teammate va a quedar inactivo. Exit `2` lo mantiene trabajando. |
| `TaskCreated`     | Se ejecuta al crear una tarea. Exit `2` previene la creación.           |
| `TaskCompleted`   | Se ejecuta al completar una tarea. Exit `2` previene el cierre.        |

*Fuente: [Claude Code: Agent Teams](https://code.claude.com/docs/en/agent-teams)*


## Hooks (Disparadores)

### Interceptación y Seguridad
Los hooks ejecutan scripts ante eventos de ciclo de vida. Un aspecto crítico es el bloqueo si el hook retorna `exit 2` en `PreToolUse`, abortando la herramienta.

### Estructura de Directorio
```text
mi-proyecto/
└── .claude/
    ├── settings.json
    └── hooks/
        └── protect-files.sh
```

### Ejemplo: Protección de Archivos Críticos
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```
*Fuente: [Claude Code: Hooks Guide](https://code.claude.com/docs/en/hooks-guide)*

## Automatización (Headless Mode)

### Modo Desatendido y CI/CD
Ideal para pipelines sin intervención humana. Se controla mediante flags específicos.

### Flags y Control de Salida
- `--bare`: Omite configuración global y hooks para aislamiento en CI.
- `--allowedTools`: Aprueba herramientas sin interacción.
- `--json-schema`: Fuerza un esquema de output específico.
- `/loop`: Tareas programadas vía sintaxis CRON.

### Ejemplo de Uso (Bash CI/CD)
```bash
claude -p "Revisa este PR" --bare --allowedTools read_file,run_shell_command
```
*Fuentes: [Claude Code: Headless Mode](https://code.claude.com/docs/en/headless), [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)*
