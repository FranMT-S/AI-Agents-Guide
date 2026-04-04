# Google Antigravity: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Google Antigravity en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Rules & Workflows)
*   **Fuente:** [Antigravity Docs: Rules & Workflows](https://antigravity.google/docs/rules-workflows)
*   **Archivos:** Usa `GEMINI.md` y archivos Markdown en `.agents/rules/` con un límite de 12k caracteres.
*   **Características Únicas:** Soporta menciones de contexto usando `@filename` dentro de las reglas para inyectar contenido dinámico. Los "Workflows" se definen como secuencias de pasos que se pueden invocar con slash commands (ej. `/deploy`).

## Skills (Habilidades)
*   **Fuente:** [Antigravity: Skills Docs](https://antigravity.google/docs/skills)
*   **Archivos:** Busca skills en `.agents/skills/<name>/` (proyecto) o `~/.gemini/antigravity/skills/<name>/` (global).
*   **Características Únicas:** Las skills se activan mediante una herramienta nativa (`skill({ name: "..." })`). Recomienda incluir scripts en una carpeta `/scripts` y pedirle al agente que ejecute el script con `--help` (como "caja negra") en lugar de leer todo el código fuente, ahorrando espacio en la ventana de contexto.
