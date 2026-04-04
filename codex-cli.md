# OpenAI Codex CLI: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Codex CLI en cuanto a la gestión de contexto, habilidades, subagentes y automatización.

## Gestión de Contexto (Agents.md Guides)

Codex adopta completamente el estándar de contexto, utilizando `AGENTS.md` como su archivo principal, complementado con un archivo de prioridad denominado `AGENTS.override.md`.

Su comportamiento de lectura concatena las reglas encontradas desde la raíz del sistema hasta el directorio actual. Por diseño de seguridad y rendimiento, impone un límite estricto de 32 KiB (`project_doc_max_bytes`) para la cadena completa de instrucciones inyectadas al modelo. También permite a los usuarios configurar nombres alternativos para el archivo de reglas mediante la propiedad `project_doc_fallback_filenames`.

**Estructura de Directorio:**
```text
mi-proyecto/
├── AGENTS.md
└── AGENTS.override.md
```
*Fuente: [Codex CLI: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)*

## Skills (Habilidades)

Las skills en Codex se alojan comúnmente en la ruta global `~/.agents/skills/` y se definen utilizando manifiestos específicos `agents/openai.yaml`.

Una característica única es que soporta propiedades dedicadas a interfaces gráficas como `display_name`, `icon`, y `brand_color`. Utiliza la directiva `allow_implicit_invocation: false` dentro del manifiesto para forzar que el modelo no pueda activar la skill por sí solo, requiriendo invocación manual. Además, permite definir requisitos previos (`dependencies`) para forzar que ciertos servidores MCP específicos estén activos antes de poder usar la skill.

**Estructura de Directorio:**
```text
~/.agents/
└── skills/
    └── my-skill/
        └── SKILL.md
```

**Ejemplo de Configuración (`agents/openai.yaml`):**
```yaml
name: "my-skill"
display_name: "Code Formatter"
icon: "magic-wand"
allow_implicit_invocation: false
dependencies: ["local-linter-mcp"]
```
*Fuente: [Codex: Developers Skills](https://developers.openai.com/codex/skills)*

## MCP (Model Context Protocol)

Codex soporta los transportes `Stdio` y `Streamable HTTP`. Una ventaja importante de su arquitectura es que la configuración MCP es compartida de manera transparente entre la extensión del IDE y la herramienta CLI.

Posee una TUI (Terminal User Interface) dedicada y visual que puede ser activada mediante el comando interactivo `/mcp`. A nivel técnico, permite controlar explícitamente los tiempos de espera a través de `startup_timeout_sec` y `tool_timeout_sec`. Facilita drásticamente las integraciones en entornos remotos (como devboxes) al permitir sobrescribir los callbacks OAuth mediante `mcp_oauth_callback_url`. Gestiona exclusiones explícitas de herramientas con las propiedades `enabled_tools` y `disabled_tools`.

**Estructura de Directorio:**
```text
~/.codex/
└── config.toml
```

**Ejemplo de Configuración (`config.toml`):**
```toml
[mcp.servers.local_tools]
command = "python"
args = ["-m", "mcp_server"]
disabled_tools = ["delete_all"]
startup_timeout_sec = 30
```
*Fuente: [Codex CLI: MCP Developers](https://developers.openai.com/codex/mcp)*

## Hooks (Disparadores)

Codex soporta el uso de hooks para reaccionar a eventos de terminal e intercepciones de modelos, proporcionando una capa de ejecución y seguridad que corre de forma externa al flujo principal de generación.

*Fuente: [Codex CLI: Hooks](https://developers.openai.com/codex/hooks)*

## Subagentes

En Codex CLI, se pueden definir subagentes especializados para delegar lógicas complejas de razonamiento o tareas que requieren un enfoque segmentado antes de retornar el output final a la terminal principal.

*Fuente: [Codex CLI: Subagents Guide](https://developers.openai.com/codex/subagents)*

## Automatización y Scripting (Non-interactive Mode)

Codex provee un poderoso modo de uso no interactivo ideal para automatización de refactorización masiva y pipelines de CI/CD.

Su comando base es `codex exec`. Soporta de manera fundamental el flag `--full-auto`, el cual permite ediciones automáticas y en lotes de archivos sin confirmación humana. Por motivos de seguridad durante operaciones automatizadas, utiliza `--sandbox <mode>` para restringir agresivamente permisos, como por ejemplo limitando a `--sandbox workspace-write`. Adicionalmente, soporta `--output-schema` para validar de forma estricta que la salida JSON cumpla un formato predefinido, y permite el streaming de la ejecución mediante un flujo JSONL en tiempo real.

**Ejemplo de Uso (Bash para CI/CD):**
```bash
codex exec "Refactoriza este archivo para usar el nuevo SDK" --full-auto --sandbox workspace-write --output-schema ./schema.json
```
*Fuente: [Codex: Non-interactive Usage](https://developers.openai.com/codex/noninteractive)*
