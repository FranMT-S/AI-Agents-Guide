# OpenAI Codex CLI: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Codex CLI en cuanto a la gestión de contexto, habilidades, subagentes y automatización.

## Gestión de Contexto (Agents.md Guides)

### AGENTS.md y Overrides
Codex utiliza `AGENTS.md` como estándar principal, permitiendo priorizar reglas mediante `AGENTS.override.md`.

### Límites y Configuración de Proyecto
Impone un límite de 32 KiB (`project_doc_max_bytes`) para la cadena de instrucciones. Permite configurar nombres alternativos con `project_doc_fallback_filenames`.

### Estructura de Directorios
```text
~/.codex/AGENTS.md               (Global — preferencias universales del usuario)
mi-proyecto/
├── AGENTS.md                    (Proyecto — reglas base del repositorio)
├── AGENTS.override.md           (Proyecto — anula el AGENTS.md local)
└── src/
    └── api/
        └── AGENTS.override.md   (Modulo — anula reglas para este subdirectorio)
```
*Fuente: [Codex CLI: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)*

## Skills (Habilidades)

### Manifiestos YAML y UI Config
Las habilidades se definen en `agents/openai.yaml`. Soporta propiedades visuales como `display_name`, `icon` y `brand_color`.

### Dependencias MCP e Invocación
Usa `dependencies` para obligar a que ciertos servidores estén activos. La directiva `allow_implicit_invocation: false` fuerza la activación manual.

### Estructura de Directorio
```text
~/.agents/
└── skills/
    └── my-skill/
        └── SKILL.md
```

#### Ejemplo: Manifiesto de Skill (`agents/openai.yaml`)
```yaml
name: "my-skill"
display_name: "Code Formatter"
icon: "magic-wand"
allow_implicit_invocation: false
dependencies: ["local-linter-mcp"]
```
*Fuente: [Codex: Developers Skills](https://developers.openai.com/codex/skills)*

## MCP (Model Context Protocol)

### Configuración Compartida (CLI/IDE)
Codex sincroniza sus servidores MCP entre la terminal (CLI) y la extensión del IDE mediante un archivo `config.toml`. Soporta transportes **STDIO** (procesos locales) y **Streamable HTTP** (servidores remotos).

### Gestión de Servidores
Puedes gestionar servidores mediante comandos (`codex mcp add`) o editando directamente el archivo de configuración. Soporta autenticación mediante **Bearer Tokens** y flujos **OAuth** nativos (`codex mcp login`).

### Opciones de Configuración
Dentro de `[mcp_servers.<alias>]`, se aceptan los siguientes parámetros:

- **Para STDIO:** `command` (requerido), `args`, `cwd` y `env` (mapa de variables).
- **Para HTTP:** `url` (requerido), `bearer_token_env_var`, `http_headers` (estáticos) y `env_http_headers` (mapeo a variables de entorno).
- **Control de Ejecución:**
  - `enabled`: Permite desactivar un servidor sin borrarlo.
  - `required`: Si es `true`, Codex fallará al arrancar si el servidor no inicializa.
  - `enabled_tools`: Allowlist de herramientas.
  - `disabled_tools`: Denylist de herramientas (se aplica después del allowlist).
  - `startup_timeout_sec` (Default: 10) y `tool_timeout_sec` (Default: 60).

### Estructura de Directorio
```text
~/.codex/
└── config.toml
```

> [!NOTE]
> En entornos **Windows**, la inyección de variables de entorno en los comandos o configuraciones debe usar la sintaxis `%VAR_NAME%`.

#### Ejemplo de Configuración (`config.toml`)
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
[mcp_servers.context7.env]
MY_API_KEY = "%CONTEXT7_TOKEN%"

[mcp_servers.figma-remote]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
enabled_tools = ["get_file", "get_comments"]
tool_timeout_sec = 45
```

![[../attachments/clickup-codex-01.0.png]]

*Fuente: [Codex CLI: MCP Developers](https://developers.openai.com/codex/mcp)*

## Hooks (Disparadores)

### Intercepción de Modelos y Terminal
Scripts externos para reaccionar a eventos de terminal o interceptar llamadas a herramientas antes de su ejecución.

### Estructura de Directorio
```text
mi-proyecto/
└── .codex/
    ├── hooks.json
    └── hooks/
        └── pre_tool_use_policy.py
```

#### Ejemplo: Política Pre-Ejecución (`hooks.json`)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \".codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking Bash command"
          }
        ]
      }
    ]
  }
}
```
*Fuente: [Codex CLI: Hooks](https://developers.openai.com/codex/hooks)*

## Subagentes

> [!TIP]
> Antes de diseñar complejos ecosistemas de orquestación en Codex CLI, consulta los **[Patrones Avanzados Multi-Agente](../ai-learning-guide.md#patrones-avanzados-multi-agente)** en la guía principal. Incluye estrategias clave como Contratos de Datos estrictos, Housekeeping, y cuándo preferir Scripts deterministas sobre LLMs.

### Delegación en TOML
Define agentes especializados que operan de forma aislada. El orquestador puede spawnear múltiples subagentes según la tarea.

### Estructura de Directorio
```text
mi-proyecto/
└── .codex/
    └── agents/
        └── reviewer.toml
```

#### Ejemplo: Revisor de Código (`reviewer.toml`)
```toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-5.4"
sandbox_mode = "read-only"
developer_instructions = """
Review code like an owner. Prioritize correctness, security, behavior regressions, and missing test coverage.
"""
```
*Fuente: [Codex CLI: Subagents Guide](https://developers.openai.com/codex/subagents)*

## Automatización y Scripting

### Modo Headless y Full-Auto
El comando `codex exec` junto con `--full-auto` permite refactorizaciones masivas sin intervención humana.

### Sandboxing en CI/CD
Uso de `--sandbox` (ej. `workspace-write`) y `--output-schema` para validación estricta de salidas JSON en pipelines.

#### Ejemplo de Uso (Bash CI/CD)
```bash
codex exec "Refactoriza este archivo para usar el nuevo SDK" --full-auto --sandbox workspace-write --output-schema ./schema.json
```

![[../attachments/clickup-codex-02.jpg]]

*Fuente: [Codex: Non-interactive Usage](https://developers.openai.com/codex/noninteractive)*
