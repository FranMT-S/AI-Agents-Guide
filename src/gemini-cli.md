# Gemini CLI: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Gemini CLI en cuanto a la gestión de contexto, habilidades, automatización y más.

## Gestión de Contexto (Memory Management)

Gemini CLI utiliza la jerarquía de `GEMINI.md` y `AGENTS.md`, operando desde un nivel Global hacia el Proyecto y luego al Subdirectorio.

Permite una modularización total escaneando recursivamente el árbol de archivos. Incluye un sistema de memoria global que se gestiona mediante la herramienta `save_memory` (por ejemplo, `/memory show`, `/memory reload`), lo cual permite persistir datos sin necesidad de editar los archivos manualmente.

**Estructura de Directorio:**
```text
~/.gemini/GEMINI.md       (Global)
mi-proyecto/
├── AGENTS.md             (Proyecto)
└── src/
    └── auth/
        └── AGENTS.md     (Subdirectorio)
```
*Fuente: [Gemini CLI: Memory Management](https://geminicli.com/docs/cli/tutorials/memory-management/)*

## Skills (Habilidades)

Soporta tres niveles estrictos de precedencia: `Workspace` (`.gemini/skills/`), `User` (`~/.gemini/skills/`) y `Extension` (skills que vienen empaquetadas).

Requiere aprobación manual del usuario (sandboxing) antes de que el agente pueda leer archivos dentro de la carpeta de la skill. Además, soporta la ejecución de binarios empaquetados (por ejemplo, `node scripts/audit.js`).

**Estructura de Directorio:**
```text
mi-proyecto/
└── .gemini/
    └── skills/
        └── my-skill/
            └── SKILL.md
```
*Fuentes: [Gemini CLI: Skills Getting Started](https://geminicli.com/docs/cli/tutorials/skills-getting-started/), [Gemini CLI: Skills](https://geminicli.com/docs/cli/skills/)*

## MCP (Model Context Protocol)

Soporta los transportes `Stdio`, `SSE` y `Streamable HTTP`. Implementa `Tools`, `Resources` y `Prompts` (que pueden ser invocados vía slash commands).

Destaca por su `Sanitización de Entorno (Environment Sanitization)`, que censura automáticamente variables sensibles (ej. las que contienen `*TOKEN*`) por seguridad. Soporta `Service Account Impersonation` para servicios protegidos por IAP. Asigna `Fully Qualified Names (FQN)` a las herramientas automáticamente para evitar colisiones entre servidores MCP, y permite filtrar herramientas usando `includeTools` y `excludeTools`.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .gemini/
    └── settings.json
```

**Ejemplo de Configuración (`settings.json`):**
```json
{
  "mcpServers": {
    "local-db": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "excludeTools": ["drop_table", "truncate_db"]
    }
  }
}
```
*Fuente: [Gemini CLI: MCP Server Setup](https://geminicli.com/docs/tools/mcp-server/)*

## Plugins y Extensiones

Las extensiones expanden el CLI mediante un manifiesto `gemini-extension.json` y se instalan directamente desde URLs de GitHub usando `gemini extensions install <URL>`.

Pueden inyectar comandos personalizados (archivos TOML en la carpeta `commands/`), habilidades (Skills) e incluso aportar "Tier 2 security rules" al motor de políticas (`Policy Engine`) del agente. Soporta la gestión segura de credenciales en el keychain del sistema y permite el desarrollo iterativo mediante enlaces simbólicos con `gemini extensions link`.

**Estructura de Directorio:**
```text
mi-extension/
├── gemini-extension.json
├── commands/
│   └── custom-cmd.toml
└── skills/
```

**Ejemplo de Instalación (Comando CLI):**
```bash
gemini extensions install https://github.com/google/gemini-cli-github-extension
```
*Fuentes: [Gemini CLI: Extensions Guide](https://geminicli.com/docs/extensions/), [Writing Extensions](https://geminicli.com/docs/extensions/writing-extensions/), [Best Practices](https://geminicli.com/docs/extensions/best-practices/), [Reference](https://geminicli.com/docs/extensions/reference/)*

## Hooks (Disparadores)

En Gemini CLI, los hooks se comunican con el agente principal mediante un protocolo estricto de `stdin/stdout` utilizando JSON. Se configuran dentro del objeto `hooks` en `settings.json`.

Los eventos clave incluyen eventos de herramienta (`BeforeTool`, `AfterTool`), de agente (`BeforeAgent`, `AfterAgent`), de modelo (`BeforeModel`, `BeforeToolSelection`, `AfterModel`) y de ciclo de vida (`SessionStart`, `SessionEnd`, `Notification`, `PreCompress`). Si el script sale con un código `2`, se bloquea la acción.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .gemini/
    └── settings.json
```

**Ejemplo de Configuración (`settings.json`):**
```json
{
  "hooks": {
    "BeforeTool": [
      {
        "command": "./scripts/validate-tool.sh"
      }
    ]
  }
}
```

**Ejemplo de Input (stdin) para Hook:**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "BeforeTool",
  "timestamp": "2026-04-03T12:00:00Z"
}
```
*Fuente: [Gemini CLI: Hooks Reference](https://geminicli.com/docs/hooks/reference/)*

## Subagentes y Orquestadores

Los subagentes en Gemini CLI operan en ventanas de contexto aisladas y se definen mediante archivos Markdown con `frontmatter` YAML.

Los metadatos incluyen `name`, `description`, `kind` (`local` o `remote`), `tools` y `model`. Cuenta con agentes integrados como `codebase_investigator`, `cli_help`, `generalist_agent`, y `browser_agent`. Un aspecto crítico es la `Tool Isolation`: los subagentes solo pueden acceder a las herramientas que se les otorgan explícitamente en el array `tools`. Además, la recursión está protegida; un subagente no puede llamar a otro subagente, excepto si es un orquestador oficial.

### Subagentes Orquestadores (Dev Manager Orchestrator)

Gemini CLI incorpora agentes orquestadores integrados (como `dev-manager-orchestrator`) que automatizan el ciclo de desarrollo completo (escribir → revisar → arreglar) delegando tareas a otros subagentes especialistas sin intervención del usuario.

**Estructura de Directorio (Ejemplo Personalizado):**
```text
mi-proyecto/
└── .gemini/
    └── agents/
        ├── dev-orchestrator.md
        ├── code-writer.md
        └── code-reviewer.md
```

**Ejemplo de Configuración de un Orquestador (`dev-orchestrator.md`):**
```markdown
---
name: dev-orchestrator
description: Coordina el ciclo completo de desarrollo. Delega la escritura y la revisión a subagentes.
tools: [code-writer, code-reviewer, read_file]
model: gemini-3-pro
---
Eres el Mánager de Desarrollo. 
1. Pasa el requerimiento del usuario a la tool `code-writer`.
2. Una vez que termine, usa la tool `code-reviewer` para auditar el archivo.
3. Si el reviewer reporta errores, envíalos de vuelta al `code-writer`.
4. Solo finaliza cuando el `code-reviewer` diga que todo está perfecto. No escribas código tú mismo.
```
*Fuente: [Gemini CLI: Subagents Tutorial](https://geminicli.com/docs/core/subagents/)*

## Automatización y Scripting (Headless Mode)

El modo Headless de Gemini CLI se activa automáticamente en entornos `no-TTY` o explícitamente mediante comandos.

Retorna texto o JSON estructurado (`--output-format json` o `stream-json`) para facilitar su uso en scripts. Genera eventos de salida específicos (como `init`, `message`, `tool_use`, `tool_result`, `error`, `result`) y provee códigos de salida detallados (por ejemplo, `42` para errores de input, `53` si se supera el límite de turnos).

**Ejemplo de Uso (Bash):**
```bash
gemini -p "Resume git diff y devuelve JSON" --output-format json > report.json
```
*Fuente: [Gemini CLI: Headless Tutorial](https://geminicli.com/docs/cli/headless/)*
