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

## MCP (Model Context Protocol)
*   **Fuente:** [Claude Code: MCP Guide](https://code.claude.com/docs/en/mcp)
*   **Características Técnicas:** Soporta **Stdio** y **HTTP** (el transporte SSE está en desuso). Implementa Tools, Prompts, Resources y **Channels** (para notificaciones push).
*   **Archivos:** Configuración jerárquica estricta: Enterprise (`managed-mcp.json`), Local/Project (`.mcp.json`) y User (`~/.claude.json`).
*   **Características Únicas:** El archivo `managed-mcp.json` permite el control centralizado de políticas en entornos corporativos. **Channels** permite a los servidores enviar mensajes de forma asíncrona (ej. alertas del CI). Cuenta con un `headersHelper` para ejecutar comandos shell que generen tokens dinámicos en servidores HTTP (ideal para integraciones Kerberos). Restricción de herramientas mediante listas `allowedMcpServers` y `deniedMcpServers`.

## Plugins y Extensiones
*   **Fuentes:** [Claude Code: Discover Plugins](https://code.claude.com/docs/en/discover-plugins), [Claude Code: Plugins](https://code.claude.com/docs/en/plugins)
*   **Arquitectura:** Los plugins pueden agrupar skills, agentes, hooks y servidores MCP o LSP. Se definen mediante `.claude-plugin/plugin.json`.
*   **Características Únicas:** Soporta la inyección de **Servidores LSP (Language Server Protocol)** para proveer diagnósticos en tiempo real e inteligencia de código estilo IDE directamente en la terminal. Incorpora un sistema de "Output Styles" que altera cómo se comunica Claude (ej. "modo explicativo" vs "modo aprendizaje").
