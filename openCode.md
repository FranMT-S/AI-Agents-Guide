# OpenCode: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de OpenCode en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Rules)
*   **Fuente:** [OpenCode: Rules](https://opencode.ai/docs/rules/)
*   **Archivos:** Soporta `AGENTS.md` (y su contraparte de Claude, `CLAUDE.md`) junto con un archivo de configuración `opencode.json`.
*   **Características Únicas:** Ofrece el comando `/init` para escanear el proyecto y generar automáticamente un `AGENTS.md` a medida. Soporta **Lazy Loading** (carga perezosa) de reglas referenciando `@archivos` solo cuando es necesario, y permite definir reglas a partir de URLs en su JSON.

## Skills (Habilidades)
*   **Fuente:** [OpenCode: Skills Docs](https://opencode.ai/docs/skills/)
*   **Archivos:** Escanea hacia arriba buscando `.opencode/skills/`, `.claude/skills/`, y `.agents/skills/`.
*   **Características Únicas:** Ofrece control de permisos granulares en `opencode.json` (ej. `"permission": { "skill": { "internal-*": "deny" } }`). Los permisos se pueden personalizar por agente (ej. un agente "Plan" tiene accesos distintos a un agente "Coder"). Permite metadatos personalizados (`metadata: { "audience": "maintainers" }`).
