# OpenCode: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de OpenCode en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Rules)
*   **Fuente:** [OpenCode: Rules](https://opencode.ai/docs/rules/)
*   **Archivos:** Soporta `AGENTS.md` (y su contraparte de Claude, `CLAUDE.md`) junto con un archivo de configuración `opencode.json`.
*   **Características Únicas:** Ofrece el comando `/init` para escanear el proyecto y generar automáticamente un `AGENTS.md` a medida. Soporta **Lazy Loading** (carga perezosa) de reglas referenciando `@archivos` solo cuando es necesario, y permite definir reglas a partir de URLs en su JSON.

## Skills (Habilidades)
*   **Fuente:** [OpenCode: Skills Docs](https://opencode.ai/docs/skills/)
*   **Archivos:** Escanea hacia arriba buscando `.opencode/skills/`, `.claude/skills/`, y `.agents/skills/`.
*   **Estructura de Directorio:**
    ```text
    mi-proyecto/
    └── .opencode/
        └── skills/
            └── my-skill/
                └── SKILL.md
    ```
*   **Características Únicas:** Ofrece control de permisos granulares en `opencode.json` (ej. `"permission": { "skill": { "internal-*": "deny" } }`). Los permisos se pueden personalizar por agente (ej. un agente "Plan" tiene accesos distintos a un agente "Coder"). Permite metadatos personalizados (`metadata: { "audience": "maintainers" }`).

## MCP (Model Context Protocol)
*   **Fuente:** [OpenCode: MCP Servers (ES)](https://opencode.ai/docs/es/mcp-servers/)
*   **Características Técnicas:** Soporta servidores **Locales (Stdio)** y **Remotos (HTTP/SSE)**.
*   **Archivos:** Configuración en `opencode.json` o `opencode.jsonc`.
*   **Características Únicas:** Resuelve autenticación OAuth automáticamente mediante **Dynamic Client Registration (RFC 7591)**. Almacena los tokens en `~/.local/share/opencode/mcp-auth.json`. Destaca por permitir **Remote Defaults** mediante endpoints `.well-known/opencode`, facilitando que las organizaciones ofrezcan servidores preconfigurados a sus desarrolladores.

## Plugins y Extensiones
*   **Fuentes:** [OpenCode: Plugins (ES)](https://opencode.ai/docs/es/plugins/), [OpenCode: Ecosystem (ES)](https://opencode.ai/docs/es/ecosystem/)
*   **Arquitectura:** Los plugins son módulos TypeScript/JavaScript que exportan funciones. Se ejecutan sobre el entorno **Bun**.
*   **Características Únicas:** Arquitectura profundamente **Event-Driven**: los plugins se adhieren a eventos internos como `session.compacted` o `tool.execute.before`. Ofrecen **Hooks de Compactación (Compaction Hooks)**, permitiendo a los desarrolladores modificar cómo la IA resume sesiones largas. También soporta integración interactiva en segundo plano vía PTY (`opencode-pty`).
