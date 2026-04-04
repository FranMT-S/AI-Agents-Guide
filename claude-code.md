# Claude Code: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Claude Code en cuanto a la gestión de contexto, habilidades, automatización y subagentes.

## Gestión de Contexto (Memory & Agents.md)

Claude Code utiliza principalmente los archivos `CLAUDE.md`, `.claude/rules/*.md` y `CLAUDE.local.md` (útil para reglas locales ignoradas en Git). También soporta explícitamente el estándar `AGENTS.md`.

Su característica más destacada es el **Auto Memory**: Claude genera su propio archivo `MEMORY.md` de forma autónoma para recordar aprendizajes de depuración y comandos recurrentes entre sesiones. Además, usa la propiedad `paths` en el YAML `frontmatter` para limitar ciertas reglas a carpetas específicas, y admite `symlinks` para compartir reglas fácilmente entre múltiples proyectos.

**Estructura de Directorio:**
```text
mi-proyecto/
├── AGENTS.md
├── CLAUDE.md
└── .claude/
    └── rules/
        └── testing.md
```

**Ejemplo de Configuración (Frontmatter en `CLAUDE.md` o `AGENTS.md`):**
```yaml
---
description: Reglas para el backend
paths: ["src/backend/**"]
---
```
*Fuente: [Claude Code: Memory & Agents.md](https://code.claude.com/docs/en/memory#agents-md)*

## Skills (Habilidades)

Las skills en Claude se descubren a través de una jerarquía estricta: `Enterprise` > `Personal` (`~/.claude/skills/`) > `Project` (`.claude/skills/`).

Hace uso intensivo de metadatos YAML avanzados en su archivo `SKILL.md`. La propiedad `allowed-tools` aísla y restringe las herramientas disponibles; `context: fork` obliga a ejecutar la skill en un subagente separado, protegiendo el contexto principal; y `disable-model-invocation: true` fuerza la invocación manual por parte del usuario. Además, inyecta variables de entorno útiles como `${CLAUDE_SESSION_ID}` y `${CLAUDE_SKILL_DIR}` en tiempo de ejecución. Limita el trigger a 250 caracteres.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .claude/
    └── skills/
        └── my-skill/
            └── SKILL.md
```
*Fuente: [Claude: Skills Guide](https://code.claude.com/docs/en/skills)*

## MCP (Model Context Protocol)

Soporta los transportes `Stdio` y `HTTP` (nota: el transporte SSE está actualmente en desuso en esta implementación). Implementa `Tools`, `Prompts`, `Resources` y un concepto avanzado llamado **Channels** (ideal para recibir notificaciones push asíncronas de servidores, como alertas de un sistema CI).

Sigue una configuración jerárquica estricta: `Enterprise` (`managed-mcp.json`), `Local/Project` (`.mcp.json`) y `User` (`~/.claude.json`). El archivo `managed-mcp.json` permite el control centralizado de políticas en entornos corporativos. Cuenta con un `headersHelper` para ejecutar comandos shell que generen tokens dinámicos en servidores HTTP (ideal para integraciones complejas como Kerberos), y permite restringir herramientas mediante listas de acceso `allowedMcpServers` y `deniedMcpServers`.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .mcp.json
```

**Ejemplo de Configuración (`.mcp.json`):**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  },
  "allowedMcpServers": ["github"],
  "deniedMcpServers": ["local-fs"]
}
```
*Fuente: [Claude Code: MCP Guide](https://code.claude.com/docs/en/mcp)*

## Plugins y Extensiones

La arquitectura de plugins de Claude es altamente modular. Los plugins pueden agrupar skills, agentes, hooks y servidores MCP o LSP, todo definido mediante un archivo central `.claude-plugin/plugin.json`.

Destaca por soportar la inyección de **Servidores LSP (Language Server Protocol)**, lo que provee a Claude de diagnósticos en tiempo real e inteligencia de código estilo IDE directamente en la terminal. Incorpora también un sistema de "Output Styles" que altera estructuralmente cómo se comunica Claude (ej. forzando un "modo explicativo" vs un "modo aprendizaje").

**Estructura de Directorio:**
```text
mi-plugin/
├── .claude-plugin/
│   └── plugin.json
└── src/
    └── index.js
```
*Fuentes: [Claude Code: Discover Plugins](https://code.claude.com/docs/en/discover-plugins), [Claude Code: Plugins](https://code.claude.com/docs/en/plugins)*

## Subagentes y Agent Teams

Claude Code permite orquestar múltiples agentes especializados utilizando la arquitectura de **Agent Teams** (Equipos de Agentes).

Los subagentes mantienen su propio contexto aislado y un conjunto de herramientas limitado. Esto es ideal para separar tareas (por ejemplo, un agente que "Planifica" y otro agente que "Escribe Código").

*Fuente: [Claude Code: Sub-agents & Teams](https://code.claude.com/docs/en/sub-agents)*

## Hooks (Disparadores)

Los hooks permiten ejecutar scripts en respuesta a eventos del ciclo de vida. En Claude, un aspecto crítico de seguridad es la capacidad de bloqueo: si un hook de validación (por ejemplo, en el evento `PreToolUse`) retorna un código de salida `exit 2`, se aborta la ejecución de la herramienta, protegiendo el sistema. El mensaje de error impreso en `stderr` se envía tanto al usuario como de vuelta al modelo.

*Fuente: [Claude Code: Hooks Guide](https://code.claude.com/docs/en/hooks-guide)*

## Automatización y Tareas Programadas (Headless Mode)

El modo Headless permite ejecutar Claude sin intervención humana, lo cual es ideal para pipelines y scripts de CI/CD. Utiliza flags específicos para controlar la automatización.

El flag `--bare` omite la carga automática de hooks y configuración global, ideal para aislar procesos en CI. El flag `--allowedTools` sirve para aprobar explícitamente herramientas sin requerir interacción en la terminal. Además, permite forzar que el output final cumpla con un esquema específico usando `--json-schema`, y admite la programación de tareas periódicas mediante comandos como `/loop` usando sintaxis CRON estándar.

**Ejemplo de Uso (Bash para CI/CD):**
```bash
claude -p "Revisa este PR" --bare --allowedTools read_file,run_shell_command
```
*Fuentes: [Claude Code: Headless Mode](https://code.claude.com/docs/en/headless), [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)*
