# Gemini CLI: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Gemini CLI en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Memory Management)
*   **Fuente:** [Gemini CLI: Memory Management](https://geminicli.com/docs/cli/tutorials/memory-management/)
*   **Archivos:** Usa la jerarquía de `GEMINI.md` y `AGENTS.md` (Global → Proyecto → Subdirectorio).
*   **Características Únicas:** Permite una modularización total escaneando recursivamente. Incluye un sistema de memoria global que se gestiona mediante la herramienta `save_memory` (ej. `/memory show`, `/memory reload`), persistiendo datos sin editar los archivos manualmente.

## Skills (Habilidades)
*   **Fuentes:** [Gemini CLI: Skills Getting Started](https://geminicli.com/docs/cli/tutorials/skills-getting-started/), [Gemini CLI: Skills](https://geminicli.com/docs/cli/skills/)
*   **Archivos:** Soporta tres niveles: Workspace (`.gemini/skills/`), User (`~/.gemini/skills/`) y Extension (empaquetado).
*   **Características Únicas:** El orden de precedencia estricto es Workspace > User > Extension. Requiere aprobación manual del usuario (sandboxing) antes de que el agente pueda leer archivos dentro de la carpeta de la skill. Soporta ejecutar binarios empaquetados (ej. `node scripts/audit.js`).
