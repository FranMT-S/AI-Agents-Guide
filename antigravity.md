# Google Antigravity: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Google Antigravity en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Rules & Workflows)
*   **Fuente:** [Antigravity Docs: Rules & Workflows](https://antigravity.google/docs/rules-workflows)
*   **Archivos:** Usa `GEMINI.md` y archivos Markdown en `.agents/rules/` con un límite de 12k caracteres.
*   **Características Únicas:** Soporta menciones de contexto usando `@filename` dentro de las reglas para inyectar contenido dinámico. Los "Workflows" se definen como secuencias de pasos que se pueden invocar con slash commands (ej. `/deploy`).

## Skills (Habilidades)
*   **Fuente:** [Antigravity: Skills Docs](https://antigravity.google/docs/skills)
*   **Archivos:** Busca skills en `.agents/skills/<name>/` (proyecto) o `~/.gemini/antigravity/skills/<name>/` (global).
*   **Estructura de Directorio:**
    ```text
    mi-proyecto/
    └── .agents/
        └── skills/
            └── my-skill/
                └── SKILL.md
    ```
*   **Características Únicas:** Las skills se activan mediante una herramienta nativa (`skill({ name: "..." })`). Recomienda incluir scripts en una carpeta `/scripts` y pedirle al agente que ejecute el script con `--help` (como "caja negra") en lugar de leer todo el código fuente, ahorrando espacio en la ventana de contexto.

## MCP (Model Context Protocol)
*   **Fuente:** [Antigravity: MCP Docs](https://antigravity.google/docs/mcp)
*   **Características Técnicas:** Soporta **Stdio** y **Streamable HTTP**. Enfocado primariamente en proveer contexto en tiempo real (schemas, logs).
*   **Archivos:** Configuración en `~/.gemini/antigravity/mcp_config.json` y tokens OAuth en `~/.gemini/antigravity/mcp_oauth_tokens.json`.
*   **Características Únicas:** Soporte nativo para **Google Application Default Credentials (ADC)** (`authProviderType: "google_credentials"`). Posee un **MCP Store** integrado para descubrir e instalar servidores populares (ej. Supabase, Linear) con un solo clic. Controla herramientas deshabilitadas mediante la propiedad `"disabledTools": []`.
