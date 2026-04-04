# OpenAI Codex CLI: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Codex CLI en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Agents.md Guides)
*   **Fuente:** [Codex CLI: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)
*   **Archivos:** `AGENTS.md` y el archivo de prioridad `AGENTS.override.md`.
*   **Características Únicas:** Concatena las reglas desde la raíz hasta el directorio actual. Utiliza un límite de 32 KiB (`project_doc_max_bytes`) para la cadena de instrucciones. Permite configurar nombres alternativos para el archivo de reglas mediante `project_doc_fallback_filenames`.

## Skills (Habilidades)
*   **Fuente:** [Codex: Developers Skills](https://developers.openai.com/codex/skills)
*   **Archivos:** `~/.agents/skills/` y manifiestos `agents/openai.yaml`.
*   **Características Únicas:** Soporta propiedades de interfaz gráfica (`display_name`, `icon`, `brand_color`). Utiliza la directiva `allow_implicit_invocation: false` para forzar activación manual. Permite definir dependencias (`dependencies`) para requerir servidores MCP específicos antes de poder usar la skill.
