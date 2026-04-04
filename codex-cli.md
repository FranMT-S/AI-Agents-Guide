# OpenAI Codex CLI: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Codex CLI en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Agents.md Guides)
*   **Fuente:** [Codex CLI: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)
*   **Archivos:** `AGENTS.md` y el archivo de prioridad `AGENTS.override.md`.
*   **Características Únicas:** Concatena las reglas desde la raíz hasta el directorio actual. Utiliza un límite de 32 KiB (`project_doc_max_bytes`) para la cadena de instrucciones. Permite configurar nombres alternativos para el archivo de reglas mediante `project_doc_fallback_filenames`.

## Skills (Habilidades)
*   **Fuente:** [Codex: Developers Skills](https://developers.openai.com/codex/skills)
*   **Archivos:** `~/.agents/skills/` y manifiestos `agents/openai.yaml`.
*   **Estructura de Directorio:**
    ```text
    ~/.agents/
    └── skills/
        └── my-skill/
            └── SKILL.md
    ```
*   **Características Únicas:** Soporta propiedades de interfaz gráfica (`display_name`, `icon`, `brand_color`). Utiliza la directiva `allow_implicit_invocation: false` para forzar activación manual. Permite definir dependencias (`dependencies`) para requerir servidores MCP específicos antes de poder usar la skill.

## MCP (Model Context Protocol)
*   **Fuente:** [Codex CLI: MCP Developers](https://developers.openai.com/codex/mcp)
*   **Características Técnicas:** Soporta **Stdio** y **Streamable HTTP**. Configuración compartida entre la extensión del IDE y la CLI.
*   **Archivos:** Configuración en `~/.codex/config.toml` (global) o `.codex/config.toml` (proyecto, requiere aprobación de confianza).
*   **Características Únicas:** Posee una TUI dedicada activada por el comando `/mcp`. Permite controlar explícitamente timeouts (`startup_timeout_sec` y `tool_timeout_sec`). Facilita integraciones en entornos remotos devbox al permitir sobrescribir los callbacks OAuth mediante `mcp_oauth_callback_url`. Gestiona exclusiones con `enabled_tools` y `disabled_tools`.

## Automatización y Scripting (Non-interactive Mode)
*   **Fuente:** [Codex: Non-interactive Usage](https://developers.openai.com/codex/noninteractive)
*   **Comandos:** `codex exec "prompt"`.
*   **Características Únicas:** Soporta el flag `--full-auto` para permitir ediciones automáticas de archivos sin confirmación, ideal para CI/CD. Utiliza `--sandbox <mode>` para restringir agresivamente permisos (ej. `workspace-write`). Soporta `--output-schema` para validación estricta de JSON en la respuesta, y permite el streaming de eventos en formato JSONL.
