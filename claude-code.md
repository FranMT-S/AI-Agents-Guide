# Claude Code: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Claude Code en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Memory & Agents.md)
*   **Fuente:** [Claude Code: Memory & Agents.md](https://code.claude.com/docs/en/memory#agents-md)
*   **Archivos:** Principalmente `CLAUDE.md`, `.claude/rules/*.md` y `CLAUDE.local.md` para ignorar en Git.
*   **Características Únicas:** Destaca por su **Auto Memory**: Claude genera su propio archivo `MEMORY.md` para recordar aprendizajes de depuración y comandos entre sesiones. Usa `paths` en YAML frontmatter para limitar reglas a ciertas carpetas, y admite "symlinks" para compartir reglas entre proyectos.

## Skills (Habilidades)
*   **Fuente:** [Claude: Skills Guide](https://code.claude.com/docs/en/skills)
*   **Archivos:** Jerarquía de descubrimiento: Enterprise > Personal (`~/.claude/skills/`) > Project (`.claude/skills/`).
*   **Características Únicas:** Usa metadatos YAML avanzados: `allowed-tools` aísla las herramientas disponibles, `context: fork` ejecuta la skill en un subagente separado, y `disable-model-invocation: true` fuerza invocación manual. Proporciona variables de entorno como `${CLAUDE_SESSION_ID}` y `${CLAUDE_SKILL_DIR}`. Limita el trigger a 250 caracteres.
