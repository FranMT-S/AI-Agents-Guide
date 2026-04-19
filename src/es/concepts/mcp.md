# MCP: Dale "manos y ojos" a tu Agente (Model Context Protocol)

El **Model Context Protocol (MCP)** es el sistema nervioso que conecta la lógica de un LLM estático con tu infraestructura dinámica. En lugar de limitarse a generar y predecir texto, el MCP estandariza la comunicación para que tu agente interactúe de forma segura con el "mundo real": consultar bases de datos, consumir APIs empresariales, manipular navegadores o gestionar tickets en Jira/ClickUp. Es el puente definitivo que transforma una IA conversacional en un ingeniero que ejecuta acciones reales.

![MCP Arquitectura](../attachments/mcp_01.png)

> [!NOTE]
> Para ver la configuración MCP específica de cada agente (Gemini CLI, Claude Code, Cursor, etc.), consulta su archivo dedicado en `../tools/`. Esta guía cubre el concepto general, buenas prácticas y las configuraciones de los MCP más utilizados.

---

## Anatomía de un Servidor MCP: ¿Qué hay dentro?

La arquitectura del protocolo se basa en exponer capacidades empaquetadas. Un servidor no es una caja negra; de acuerdo a la documentación oficial, le otorga tres "superpoderes" fundamentales al modelo de lenguaje:

| Superpoder (Componente) | ¿Qué le permite hacer al agente? | Ejemplo Práctico |
| :--- | :--- | :--- |
| **Tools** (Herramientas) | **Actuar:** Ejecutar acciones y alterar el estado del sistema. | `create_github_issue`, `drop_database` |
| **Resources** (Recursos) | **Leer:** Consumir datos de solo lectura para nutrir su contexto. | Archivos estáticos, un `schema.sql` en vivo, o *logs* del servidor. |
| **Prompts** (Plantillas) | **Contextualizar:** Flujos pre-armados para no empezar de cero. | `/review_code` (inyecta parámetros y reglas de revisión de forma automática). |

*Fuentes Oficiales: [MCP Tools](https://modelcontextprotocol.io/docs/concepts/tools) | [MCP Resources](https://modelcontextprotocol.io/docs/concepts/resources) | [MCP Prompts](https://modelcontextprotocol.io/docs/concepts/prompts)*

### Canales de Transporte: ¿Cómo hablan entre ellos?
Para que el cliente (tu IDE o CLI) interactúe con el servidor MCP, necesitan un protocolo de comunicación base. El estándar define tres vías:

| Capa de Transporte | Nivel de Complejidad | Caso de Uso Ideal |
| :--- | :--- | :--- |
| **`stdio`** *(Standard I/O)*| 🟢 Bajo (Proceso local) | El más rápido y habitual. Ideal para scripts locales (`npx`, `python`) sin abrir puertos HTTP de forma insegura. |
| **`SSE`** *(Server-Sent)*| 🟡 Medio (Red/HTTP) | Múltiples aplicaciones conectadas al mismo servidor remoto o contenedores Docker virtualizados en la nube. |
| **`Streamable HTTP`** | 🔵 Alto (Full Duplex) | La variante más moderna para infraestructuras Cloud complejas de producción. |

*Fuente Oficial: [MCP Transports](https://modelcontextprotocol.io/docs/concepts/transports)*

![MCP Transportes](../attachments/mcp_02.jpg)

---

## Archivos de Configuración por Agente

### Rutas de Configuración (Windows)
```text
Antigravity   -> C:\Users\<USER>\.gemini\antigravity\mcp_config.json
Gemini CLI    -> C:\Users\<USER>\.gemini\settings.json
Codex CLI     -> C:\Users\<USER>\.codex\config.toml
Cursor        -> <project>\.cursor\mcp.json   |   ~/.cursor/mcp.json (global)
Claude Code   -> <project>\.mcp.json          |   ~/.claude.json (global)
OpenCode      -> <project>\opencode.json      |   ~/.config/opencode/opencode.json (global)
```



> [!TIP]
> Si el OAuth de Antigravity se corrompe en algún MCP, se puede resetear eliminando los archivos de `~/.mcp-auth`.

---

## Diseño Estratégico y Optimización

### El Principio del Menor Privilegio 
Exponer 50 herramientas a un agente no lo hace más inteligente; lo hace errático. Cada tool innecesaria consume tu valiosa ventana de contexto y, peor aún, amplía el margen de error probabilístico del modelo, incrementando las alucinaciones. **Desactiva cualquier herramienta que no sea estrictamente necesaria.**

### Control Quirúrgico (Lista Negra)
No asumas que las configuraciones de origen vienen optimizadas. Audita la lista de herramientas de cada servidor y restringe el acceso mediante exclusiones (`disabledTools`). Si integras Figma solo para leer tokens de diseño, bloquea rotundamente las funciones de dibujo o manipulación del canvas. Esta poda estratégica te garantiza velocidad, menor coste y un agente hiper-enfocado.

#### Ejemplo: Configuración JSON (Exclusiones)
```json
{
  "mcpServers": {
    "mi-servidor": {
      "command": "...",
      "args": ["..."],
      "disabledTools": ["tool_peligrosa", "otra_tool"]
    }
  }
}
```

#### Ejemplo: Configuración Codex CLI (TOML)
```toml
[mcp_servers.mi-servidor]
command = "docker"
args = ["..."]
disabled_tools = ["tool_peligrosa"]
```

### Docker: Persistencia vs. Saturación de Memoria
Configurar MCPs basados en Docker (como GitHub o bases de datos) con el comando `docker run --rm` directamente en los ajustes del agente es la vía más sencilla y recomendada para empezar. Sin embargo, tiene un costo a escala: **cada vez que abras tu IDE o una nueva terminal**, se levantará un contenedor nuevo. Si tienes varios proyectos abiertos, estarás duplicando recursos y consumiendo RAM en exceso.

Una **alternativa** para evitar esta saturación es optar por un enfoque de **Contenedor Compartido**:
1. Eres responsable de levantar el contenedor **manualmente** a nivel del sistema y dejarlo en *background* (`docker run -d --name mcp-hub ...`).
2. Configuras a tus agentes para que se conecten al proceso vivo mediante `exec -i`.

#### Ejemplo: Configuración (Shared Container)
```json
{
  "command": "docker",
  "args": ["exec", "-i", "github-mcp", "/server/github-mcp-server", "stdio"]
}
```

> [!TIP]
> **El Trade-off:** Usar `exec -i` ahorra muchísima memoria al reusar una única instancia para todos tus IDEs. La desventaja es que pierdes la automatización inicial; el servidor no funcionará si olvidas levantar el contenedor original antes de abrir el editor de código.

### MCP vs. Skills: Tecnologías Complementarias
Un error de diseño común es asumir que el Model Context Protocol reemplaza la necesidad de crear *Skills* o *Prompt Tools* propias. Análisis de la industria distinguen que operan en diferentes capas del sistema agentico:
- **MCP (La Conexión):** Unifica la forma en que los LLMs se comunican con el mundo (APIs, Bases de datos). Te da la herramienta "en crudo" sin que programes un cliente propio, pero no le da contexto de negocio al modelo.
- **Skills (La Orquestación):** Es la guía procedimental. Dicta las reglas de tu compañía sobre *cómo* se deben usar esas herramientas.

**Caso de Uso Práctico:** Utilizas el servidor MCP oficial de GitHub para tener la función `create_pull_request`. Simultáneamente, escribes una *Skill* local (`pr_reviewer.md`) que instruye al modelo a revisar convenciones de código y pasar un linter estructurado *antes* de atreverse a invocar la herramienta del MCP. No son enemigos, son complementos simbióticos.
*Fuentes Evaluadas:* [Anthropic: MCP Introduction](https://www.anthropic.com/news/model-context-protocol)

### Model Routing: Optimizando Costos y Latencia en Consultas MCP
El protocolo MCP suele devolver volúmenes masivos de información (como JSONs completos de tareas o logs). Usar modelos de razonamiento "Frontier" (como Claude 3.5 Opus o Gemini 3 Pro) para filtrar estos datos es ineficiente y costoso.

**La Solución: Ruteo Dinámico a "Subagentes"**
La arquitectura de ruteo dicta delegar la extracción simple a modelos ligeros y económicos (como **Gemini 3 Pro Flash** o **Claude 3.5 Haiku**). Estos actúan como "subagentes de recuperación": consultan el MCP, limpian el ruido y entregan solo la información relevante al modelo principal. Esto reduce drásticamente el consumo de tokens y la latencia total del sistema.

*Fuente: [LogRocket: LLM routing in production — Choosing the right model for every request](https://blog.logrocket.com/llm-routing/)*



---

## Colección de MCPs

### MCPs Oficiales
Servidores publicados y mantenidos por los proveedores oficiales.

#### GitHub MCP
Permite al agente operar directamente sobre repositorios como si fuera un humano: buscar código, crear ramas, abrir PRs y leer issues.

[Repositorio Oficial](https://github.com/modelcontextprotocol/servers/tree/main/src/github)

**Casos de uso (Tools destacadas):**
- **`create_pull_request`**: Automatizar la apertura de PRs inyectando plantillas predefinidas.
- **`get_file_contents` / `search_code`**: Extraer contexto de repositorios masivos sin tener que clonarlos en tu máquina.
- **`push_files`**: Que tu agente modifique archivos y los suba directamente vía API remota.

**Requisito:** Variable de entorno `GITHUB_PERSONAL_ACCESS_TOKEN` configurada localmente (o inyectada en el Docker).

**Configuración recomendada — contenedor único compartido:**

```shell
# Run once — the container stays alive with --restart unless-stopped
docker run -d -i --name github-mcp --restart unless-stopped \
  -e GITHUB_PERSONAL_ACCESS_TOKEN \
  ghcr.io/github/github-mcp-server:v0.30.3 stdio
```

#### Ejemplo: Configuración GitHub (JSON)
```json
{
  "mcpServers": {
    "github-mcp-server": {
      "command": "docker",
      "args": ["exec", "-i", "github-mcp", "/server/github-mcp-server", "stdio"],
      "disabledTools": ["sub_issue_write", "delete_file"]
    }
  }
}
```

**Configuración para Codex CLI (`config.toml`):**

```toml
[mcp_servers.github-mcp-server]
command = "docker"
args = ["exec", "-i", "github-mcp", "/server/github-mcp-server", "stdio"]
enabled = true

[mcp_servers.github-mcp-server.env]
GITHUB_PERSONAL_ACCESS_TOKEN = "<YOUR_TOKEN>"
```

![GitHub MCP](../attachments/git-hub-mcp-01.png)

> [!TIP]
> Si no tienes Docker, usa `docker run -i --rm` en lugar de `exec -i`. Recuerda que eso levanta un contenedor nuevo por cada IDE abierto.

---

#### ClickUp MCP (Oficial)
Servidor oficial para gestionar tu tracker de tareas. Ideal para sincronizar tu flujo de código con tus tableros sin salir del editor. Usa autenticación **OAuth** (el CLI/IDE abre un navegador para autorizar).

**Integración Oficial:** [ClickUp MCP Docs](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)

**Casos de uso (Tools destacadas):**
- **`get_task`**: El agente lee los criterios de aceptación del ticket antes de empezar a programar para no obviar requerimientos.
- **`update_task`**: Mover automáticamente el estado de la tarea a "En Revisión" o "Completado" una vez terminas el código.
- **`add_comment`**: Documentar hallazgos técnicos directamente en el hilo del ticket de ClickUp.

> [!WARNING]
> Si el agente no responde correctamente después de activar ClickUp MCP, deshabilita la tool `clickup_get_workspace_hierarchy`. Esta tool descarga la jerarquía completa del workspace y puede saturar la ventana de contexto.

**Configuración recomendada:**

#### Ejemplo: Configuración ClickUp (JSON)
```json
{
  "mcpServers": {
    "clickup": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.clickup.com/mcp"],
      "disabledTools": ["clickup_get_workspace_hierarchy"]
    }
  }
}
```

**Autenticación en Gemini CLI:**

```shell
# After adding the config to settings.json, run inside gemini:
/mcp auth clickup
```

![ClickUp OAuth](../attachments/clickup-oauth-01.jpg)

**Configuración para Codex CLI (`config.toml`):**

```toml
[mcp_servers.clickup-mcp]
enabled = true
url = "https://mcp.clickup.com/mcp"
```

---

#### Figma MCP (Oficial)
Servidor MCP oficial que permite al agente leer estilos, colores, extraer componentes y entender el diseño *UX/UI*. La autenticación es manejada vía **OAuth**.

**Sitio Oficial:** [Figma MCP](https://developer.figma.com/docs/mcp/introduction/) | **Extensión:** [figma-gemini-cli-extension](https://github.com/figma/figma-gemini-cli-extension)

> [!WARNING]
> Antigravity solo soporta el MCP oficial de Figma a través del **Dev Mode**, que requiere una cuenta de pago (Pro o superior) activa en Figma.

**Instalación en Gemini CLI:**

```shell
gemini extensions install https://github.com/figma/figma-gemini-cli-extension
```

```shell
# Authenticate inside gemini:
/mcp auth figma
```

---

### MCPs de Terceros (Community)
Servidores mantenidos por la comunidad que cubren casos no oficiales.

#### Figma Console MCP
Alternativa comunitaria hiper-eficiente que extrae información leyendo directamente tu aplicación de Figma Desktop mediante un plugin local, eliminando la necesidad del Dev Mode de pago.

**Casos de uso (Tools destacadas):**
- **`figma_get_selection`**: Pídele al agente: "Extrae el CSS del botón que tengo seleccionado ahora mismo en Figma".
- **`figma_get_styles` / `figma_get_variables`**: Leer todo el *Design System* y auto-generar un archivo `tailwind.config.js` sin copiar y pegar colores a mano.
- **`figma_audit_component_accessibility`**: Auditar si los colores de un frame cumplen con el contraste WCAG directamente desde terminal.

**Repositorio:** [github.com/southleft/figma-console-mcp](https://github.com/southleft/figma-console-mcp)

> [!NOTE]
> Requiere la **aplicación desktop de Figma** instalada y activa. Ejecuta el siguiente comando para obtener la ruta del manifest del plugin: `npx figma-console-mcp@latest --print-path`

**Configuración con Access Token:**

##### Ejemplo: Configuración Figma Console (JSON)
```json
{
  "mcpServers": {
    "figma-console": {
      "command": "npx",
      "args": ["-y", "figma-console-mcp@1.22.1"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "figd_TOKEN",
        "ENABLE_MCP_APPS": "true"
      }
    }
  }
}
```

Para usar la version mas reciente:

`figma-console-mcp@latest`

##### White List

```json
 // gemini-cli
 "includeTools": [
  "figma_add_component_property",
    "figma_add_mode",
    "figma_analyze_component_set",
    "figma_arrange_component_set",
    "figma_audit_component_accessibility",
    "figma_batch_create_variables",
    "figma_batch_update_variables",
    "figma_capture_screenshot",
    "figma_clone_node",
    "figma_create_child",
    "figma_create_variable",
    "figma_create_variable_collection",
    "figma_delete_component_property",
    "figma_delete_node",
    "figma_delete_variable",
    "figma_delete_variable_collection",
    "figma_edit_component_property",
    "figma_execute",
    "figma_generate_component_doc",
    "figma_get_annotation_categories",
    "figma_get_annotations",
    "figma_get_component",
    "figma_get_component_details",
    "figma_get_component_for_development",
    "figma_get_component_for_development_deep",
    "figma_get_component_image",
    "figma_get_design_changes",
    "figma_get_design_system_kit",
    "figma_get_design_system_summary",
    "figma_get_file_data",
    "figma_get_file_for_plugin",
    "figma_get_library_components",
    "figma_get_selection",
    "figma_get_status",
    "figma_get_styles",
    "figma_get_text_styles",
    "figma_get_token_values",
    "figma_get_variables",
    "figma_instantiate_component",
    "figma_lint_design",
    "figma_list_open_files",
    "figma_move_node",
    "figma_navigate",
    "figma_reconnect",
    "figma_reload_plugin",
    "figma_rename_mode",
    "figma_rename_node",
    "figma_rename_variable",
    "figma_resize_node",
    "figma_search_components",
    "figma_set_annotations",
    "figma_set_description",
    "figma_set_fills",
    "figma_set_image_fill",
    "figma_set_instance_properties",
    "figma_set_strokes",
    "figma_set_text",
    "figma_setup_design_tokens",
    "figma_take_screenshot",
    "figma_update_variable"
  ]
```

#####  Black List

Lista de tools que no son para Developers, ni Designers.

```json
  // gemini-cli
  "excludeTools": [
    "figjam_auto_arrange",
    "figjam_create_code_block",
    "figjam_create_connector",
    "figjam_create_section",
    "figjam_create_shape_with_text",
    "figjam_create_stickies",
    "figjam_create_sticky",
    "figjam_create_table",
    "figjam_get_board_contents",
    "figjam_get_connections",
    "figma_add_shape_to_slide",
    "figma_add_text_to_slide",
    "figma_check_design_parity",
    "figma_clear_console",
    "figma_create_slide",
    "figma_delete_comment",
    "figma_delete_slide",
    "figma_duplicate_slide",
    "figma_focus_slide",
    "figma_get_comments",
    "figma_get_console_logs",
    "figma_get_focused_slide",
    "figma_get_slide_content",
    "figma_get_slide_grid",
    "figma_get_slide_transition",
    "figma_list_slides",
    "figma_post_comment",
    "figma_reorder_slides",
    "figma_scan_code_accessibility",
    "figma_set_slide_background",
    "figma_set_slide_transition",
    "figma_set_slides_view_mode",
    "figma_skip_slide",
    "figma_watch_console"
  ]
```

---

#### Trello MCP
Servidor comunitario para integrar directamente la gestión de tableros Kanban.

**Casos de uso (Tools destacadas):**
- **`get_board_cards`**: Analizar rápidamente qué tareas tienes asignadas en "Doing" para el sprint actual sin abrir el navegador.
- **`move_card` / `create_card`**: Actuar como intermediario automático para crear subtareas o mover de lista (ej. pasar tarjeta a "Code Review") tras un commit.

**Repositorio:** [npmjs.com/package/mcp-server-trello](https://www.npmjs.com/package/mcp-server-trello)

**Requisitos:** Variables de entorno `TRELLO_API_KEY` y `TRELLO_TOKEN`.
Generarlas en: [trello.com/power-ups/admin](https://trello.com/power-ups/admin)

**Configuración (variables de entorno del sistema):**

```json
{
  "mcpServers": {
    "trello": {
      "command": "npx",
      "args": ["-y", "mcp-server-trello"]
    }
  }
}
```

**Configuración (variables en el archivo de config):**

```json
{
  "mcpServers": {
    "trello": {
      "command": "npx",
      "args": ["-y", "mcp-server-trello"],
      "env": {
        "TRELLO_API_KEY": "<TRELLO_API_KEY>",
        "TRELLO_TOKEN": "<TRELLO_TOKEN>"
      }
    }
  }
}
```

---

## Recursos Adicionales

### Directorios y Hubs
Recursos para descubrir y configurar nuevos servidores MCP.

| Recurso                                              | Descripción                                                       |
| :--------------------------------------------------- | :---------------------------------------------------------------- |
| [hub.docker.com/u/mcp](https://hub.docker.com/u/mcp) | Imágenes Docker oficiales de los MCPs más populares.             |
| [mcp.so](https://mcp.so)                             | Directorio comunitario de servidores MCP.                        |
| [geminicli.com/extensions](https://geminicli.com/extensions/) | Extensiones y MCPs específicos para Gemini CLI.         |
| [cursor.directory](https://cursor.directory)         | Marketplace de reglas, skills y MCPs para Cursor.                |

*Fuente: [Model Context Protocol — Specification](https://spec.modelcontextprotocol.io/)*
