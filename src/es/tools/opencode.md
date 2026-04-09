# OpenCode: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de OpenCode en cuanto a la gestión de contexto, habilidades y plugins.

## Gestión de Contexto (Rules)

### Lazy Loading y Referencias (@file)
Soporta `AGENTS.md` y `opencode.json`. El `Lazy Loading` permite referenciar `@archivos` solo cuando es necesario. Genera reglas automáticamente con `/init`.

### Estructura de Directorios
```text
~/.config/opencode/opencode.json (Global — configuracion global del usuario)
mi-proyecto/
├── AGENTS.md                    (Proyecto — reglas del repositorio)
└── opencode.json                (Proyecto — configuracion y reglas del proyecto)
```

**Ejemplo de Configuración (`opencode.json`):**
```json
{
  "rules": [
    "AGENTS.md",
    "https://example.com/company-standards.md",
    "@src/backend"
  ]
}
```
*Fuente: [OpenCode: Rules](https://opencode.ai/docs/rules/)*

## Skills (Habilidades)

### Control de Permisos Granulares
Escanea carpetas `.opencode/skills/`, `.claude/skills/` y `.agents/skills/`. Los permisos se definen en `opencode.json` con niveles `ask/allow/deny`.

### Estructura de Directorio
```text
mi-proyecto/
└── .opencode/
    └── skills/
        └── my-skill/
            └── SKILL.md
```
*Fuente: [OpenCode: Skills Docs](https://opencode.ai/docs/skills/)*

## MCP (Model Context Protocol)

### Autenticación Dinámica y SSE/HTTP
Resuelve OAuth automáticamente vía `Dynamic Client Registration`. Soporta transportes locales (`Stdio`) y remotos.

### Remote Defaults (.well-known)
Permite configuraciones externas vía endpoints `.well-known/opencode` para gestión centralizada en organizaciones.

### Estructura de Directorio
```text
mi-proyecto/
└── opencode.json
```

#### Ejemplo: Servidor MCP SSE (`opencode.json`)
```json
{
  "mcp": {
    "servers": {
      "clickup": {
        "url": "https://mcp.clickup.com/sse",
        "tools": {"*": false, "list_tasks": true}
      }
    }
  }
}
```
*Fuente: [OpenCode: MCP Servers (ES)](https://opencode.ai/docs/es/mcp-servers/)*

## Plugins y Extensiones

### Arquitectura Event-Driven (Bun)
Basada en módulos nativos TS/JS ejecutados sobre Bun. Plugin interactivos vía PTY.

### Compaction Hooks
Permite personalizar cómo la IA resume sesiones largas mediante eventos como `session.compacted`.

### Estructura de Directorio
```text
mi-proyecto/
└── .opencode/
    └── plugins/
        └── my-plugin.ts
```

#### Ejemplo: Plugin TS (Compactación)
```typescript
export default {
  on: {
    "session.compacted": (context) => {
      console.log("Sesión compactada!");
    }
  }
}
```
*Fuentes: [OpenCode: Plugins (ES)](https://opencode.ai/docs/es/plugins/) | [OpenCode: Ecosystem (ES)](https://opencode.ai/docs/es/ecosystem/)*

## Subagentes y Orquestadores

OpenCode distingue dos tipos de agentes que operan en distintos roles. Los agentes primarios son los que el usuario controla directamente; los subagentes son especializados e invocados automáticamente o por mención `@nombre`.

> [!TIP]
> Antes de diseñar complejos ecosistemas de agentes en OpenCode, consulta los **[Patrones Avanzados Multi-Agente](../ai-learning-guide.md#patrones-avanzados-multi-agente)** en la guía principal. Incluye estrategias clave como Contratos de Datos estrictos, Housekeeping, y cuándo preferir Scripts deterministas sobre LLMs.

### Tipos de Agentes

#### Agentes Primarios (Primary Agents)
Son el asistente principal de la sesión. Se cambia entre ellos con la tecla `Tab` o el keybind `switch_agent`. Su acceso a herramientas se controla mediante permisos.

#### Subagentes (Subagents)
Son asistentes especializados que los agentes primarios pueden invocar para tareas específicas. También pueden ser invocados manualmente con `@nombre` en el chat.

### Agentes Integrados (Built-in)

| Nombre | Modo | Propósito |
| :--- | :--- | :--- |
| `build` | `primary` | Agente por defecto. Acceso completo a todas las tools. |
| `plan` | `primary` | Solo análisis y planificación. Todas las writes/bash son `ask`. |
| `general` | `subagent` | Multi-propósito con acceso completo (excepto `todo`). |
| `explore` | `subagent` | Solo lectura. Búsqueda rápida de archivos y código. |
| `compaction` | `primary` *oculto* | Compacta contextos largos automáticamente. |
| `title` | `primary` *oculto* | Genera títulos de sesión automáticamente. |
| `summary` | `primary` *oculto* | Crea resúmenes de sesión automáticamente. |

### Uso e Invocación

*   **Agentes Primarios:** Cicla entre ellos con `Tab` o el keybind `switch_agent`.
*   **Subagentes (manual):** Menciónalos con `@nombre` en el chat.
    ```
    @general ayúdame a buscar esta función en el repo
    ```
*   **Navegación entre sesiones hijas:** Los subagentes crean sesiones hijas separadas.
    *   `session_child_first` (`<Leader>+Down`): Entrar a la primera sesión hija.
    *   `session_child_cycle` (`Right`): Ciclar a la siguiente sesión hija.
    *   `session_child_cycle_reverse` (`Left`): Ciclar a la sesión hija anterior.
    *   `session_parent` (`Up`): Regresar a la sesión padre.

### Métodos de Configuración

Los agentes pueden configurarse de **dos formas**: JSON (en `opencode.json`) o Markdown (en archivos `.md`).

#### Método 1: JSON (`opencode.json`)

Permite configurar agentes built-in y crear agentes personalizados directamente en el archivo de configuración del proyecto o global. El campo `tools` es deprecated; usar `permission` en su lugar.

**Estructura de Directorio:**
```text
~/.config/opencode/opencode.json  (Global — todos los proyectos)
mi-proyecto/
└── opencode.json                  (Proyecto — compartido con el equipo via git)
```

**Ejemplo de Configuración (`opencode.json`):**
```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "{file:./prompts/build.txt}",
      "permission": {
        "bash": { "*": "ask", "git status *": "allow" }
      }
    },
    "plan": {
      "mode": "primary",
      "model": "anthropic/claude-haiku-4-20250514",
      "temperature": 0.1,
      "permission": { "edit": "deny", "bash": "deny" }
    },
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.1,
      "steps": 10,
      "permission": {
        "edit": "deny",
        "bash": { "*": "ask", "git diff": "allow", "git log*": "allow" },
        "webfetch": "deny"
      }
    }
  }
}
```

#### Método 2: Markdown (archivos `.md`)

El nombre del archivo se convierte en el nombre del agente. Por ejemplo, `review.md` crea el agente `@review`. El frontmatter YAML define la configuración y el cuerpo del archivo es el system prompt.

**Estructura de Directorio:**
```text
~/.config/opencode/agents/       (Global — disponibles en todos los proyectos)
    ├── security-auditor.md      (Agente simple — archivo solo)
    └── code-reviewer/           (Agente con recursos — subdirectorio)
        ├── code-reviewer.md     (El .md raiz del directorio define el agente)
        └── prompts/             (Archivos de apoyo: prompts, docs, etc.)
            └── review-rules.md
mi-proyecto/
└── .opencode/
    └── agents/                  (Proyecto — compartidos con el equipo via git)
        ├── manager.md
        └── code-reviewer/
            ├── code-reviewer.md
            └── context/
                └── api-standards.md
```

> [!TIP]
> Los subdirectorios permiten agrupar el agente con sus archivos de apoyo (prompts externos, documentación de referencia, ejemplos). El archivo `.md` cuyo nombre coincide con el directorio padre define el agente; el resto son recursos de contexto.

**Ejemplo: Revisor de Código (`code-reviewer.md`):**
```markdown
---
description: Reviews code for quality and security. Use when validating changes before commit.
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
steps: 10
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
  webfetch: deny
---
You are in code review mode. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Security considerations

Provide feedback without making direct changes.
```

### Crear un Agente con CLI

OpenCode incluye un comando interactivo para crear agentes que pregunta la ubicación (global/proyecto), la descripción, genera el prompt, selecciona las tools y crea el archivo `.md` resultante.

```bash
opencode agent create
```

### Schema de Configuración (Opciones)

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `description` | `string` | **Requerido.** Descripción del propósito del agente. |
| `mode` | `primary` \| `subagent` \| `all` | Modo de uso. Default: `all`. |
| `model` | `string` | Modelo en formato `provider/model-id`. Heredado del invocador si no se especifica. |
| `prompt` | `string` | System prompt inline o referencia externa `{file:./path}`. |
| `temperature` | `number` | Controla la aleatoriedad de las respuestas. **0.0–0.2:** respuestas deterministas, ideal para análisis y revisión de código. **0.3–0.5:** balance entre creatividad y precisión, óptimo para desarrollo general. **0.6–1.0:** respuestas más creativas, útil para brainstorming. Default: `0` para la mayoría de modelos; `0.55` para modelos Qwen. |
| `top_p` | `number` | Diversidad de respuesta alternativa a `temperature` (0.0–1.0). |
| `steps` | `number` | Máximo de iteraciones antes de forzar resumen. Sin límite si no se define. |
| `disable` | `boolean` | Deshabilitar completamente el agente. |
| `hidden` | `boolean` | Ocultar del menú `@`. Solo invocable programáticamente via `Task` tool. Solo aplica a `mode: subagent`. |
| `color` | `string` | Color en la UI: hex (`#FF5733`) o tema (`primary`, `accent`, `error`...). |
| `permission` | `object` | Permisos granulares para `edit`, `bash` y `webfetch`. |
| `permission.task` | `object` | Qué subagentes puede invocar este agente. Usa glob patterns. |
| `tools` | `object` | **Deprecated.** Usar `permission` en su lugar. |

### Sistema de Permisos

Los valores son `"ask"`, `"allow"` o `"deny"`. Para `bash`, soporta glob patterns y se aplica la **última regla que coincida** (no la primera).

> [!TIP]
> La regla `*` debe ir primero y las reglas específicas después. La última que coincida gana.

```json
{
  "agent": {
    "build": {
      "permission": {
        "bash": { "*": "ask", "git status *": "allow" },
        "edit": "allow",
        "webfetch": "deny"
      },
      "permission": {
        "task": { "*": "deny", "code-reviewer": "ask", "explore": "allow" }
      }
    }
  }
}
```

> [!NOTE]
> Los usuarios siempre pueden invocar cualquier subagente directamente via `@nombre` incluso si `permission.task` lo tiene en `deny` para el agente primario.

*Fuentes: [OpenCode: Agents](https://opencode.ai/docs/agents/) | [OpenCode: Permissions](https://opencode.ai/docs/permissions/)*
