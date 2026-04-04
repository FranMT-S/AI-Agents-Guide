# OpenCode: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de OpenCode en cuanto a la gestión de contexto, habilidades y plugins.

## Gestión de Contexto (Rules)

Soporta nativamente el uso de `AGENTS.md` (y su contraparte de Claude, `CLAUDE.md`) en conjunto con un archivo de configuración central `opencode.json`.

Ofrece el comando `/init` para escanear el proyecto y generar automáticamente un `AGENTS.md` a medida. Una característica destacada es el `Lazy Loading` (carga perezosa) de reglas referenciando `@archivos` solo cuando el modelo lo necesita. Además, permite definir reglas que se descargan directamente a partir de URLs definidas en su JSON.

**Estructura de Directorio:**
```text
mi-proyecto/
├── AGENTS.md
└── opencode.json
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

OpenCode escanea jerárquicamente hacia arriba buscando carpetas `.opencode/skills/`, `.claude/skills/`, y `.agents/skills/`.

Ofrece control de permisos granulares directamente en `opencode.json` (por ejemplo, usando `"permission": { "skill": { "internal-*": "deny" } }`). Los permisos se pueden personalizar a nivel de agente (ej. un agente "Plan" puede tener accesos distintos a un agente "Coder"). Permite metadatos personalizados en el frontmatter (`metadata: { "audience": "maintainers" }`).

**Estructura de Directorio:**
```text
mi-proyecto/
└── .opencode/
    └── skills/
        └── my-skill/
            └── SKILL.md
```
*Fuente: [OpenCode: Skills Docs](https://opencode.ai/docs/skills/)*

## MCP (Model Context Protocol)

Soporta servidores tanto locales (`Stdio`) como remotos (`HTTP/SSE`), configurables en `opencode.json` o `opencode.jsonc`.

Resuelve la autenticación OAuth automáticamente mediante `Dynamic Client Registration (RFC 7591)`. Almacena los tokens obtenidos en `~/.local/share/opencode/mcp-auth.json`. Destaca por permitir `Remote Defaults` mediante endpoints `.well-known/opencode`, lo cual facilita que las organizaciones ofrezcan servidores preconfigurados a sus desarrolladores de forma centralizada.

**Estructura de Directorio:**
```text
mi-proyecto/
└── opencode.json
```

**Ejemplo de Configuración (`opencode.json`):**
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

La arquitectura de plugins en OpenCode se basa en módulos nativos TypeScript/JavaScript que se ejecutan sobre el entorno **Bun**, aportando altísima velocidad.

Su arquitectura es profundamente `Event-Driven`: los plugins se adhieren a eventos internos del motor como `session.compacted` o `tool.execute.before`. Ofrecen los innovadores `Compaction Hooks` (Hooks de Compactación), permitiendo a los desarrolladores modificar cómo la IA resume sesiones largas. También soporta integración interactiva en segundo plano vía PTY (`opencode-pty`).

**Estructura de Directorio:**
```text
mi-proyecto/
└── .opencode/
    └── plugins/
        └── my-plugin.ts
```

**Ejemplo de Plugin (TS):**
```typescript
export default {
  on: {
    "session.compacted": (context) => {
      console.log("Sesión compactada!");
    }
  }
}
```
*Fuentes: [OpenCode: Plugins (ES)](https://opencode.ai/docs/es/plugins/), [OpenCode: Ecosystem (ES)](https://opencode.ai/docs/es/ecosystem/)*

## Subagentes y Orquestadores

En OpenCode, los subagentes están profundamente integrados en el ecosistema, permitiendo dividir tareas complejas. Tienen la capacidad de utilizar permisos granulares a nivel de agente definidos en `opencode.json` o a través de archivos Markdown.

### Arquitectura de Orquestación (Manager / Coder)

OpenCode soporta nativamente la figura del **Orquestador** (Planner/Manager). El flujo recomendado es tener un agente "Planificador" con herramientas de solo lectura que analiza y delega el trabajo a un agente "Programador" (Coder) con herramientas de escritura.

**Estructura de Directorio:**
```text
mi-proyecto/
├── opencode.json
└── .opencode/
    └── agents/
        ├── manager.md
        └── coder.md
```

**Ejemplo de Configuración (`opencode.json`):**
```json
{
  "agent": {
    "manager": {
      "description": "Analiza y delega tareas complejas",
      "mode": "orchestrator",
      "tools": { "write": false, "edit": false, "coder_agent": true }
    },
    "coder": {
      "description": "Implementa los cambios",
      "mode": "subagent",
      "tools": { "write": true, "edit": true }
    }
  }
}
```

**Ejemplo de Configuración (Frontmatter en `manager.md`):**
```yaml
---
description: Coordina el desarrollo de la aplicación
mode: orchestrator
tools:
  write: false
  coder_agent: true
---
Eres el arquitecto del proyecto. Planifica la estructura y usa la herramienta `coder_agent` para delegar la implementación. No escribas código tú mismo.
```
*Fuente: [OpenCode: Agents (ES)](https://opencode.ai/docs/es/agents/)*
