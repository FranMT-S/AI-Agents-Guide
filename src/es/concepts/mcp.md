# MCP (Model Context Protocol)

El **Model Context Protocol (MCP)** es el estándar de comunicación que permite a los modelos de IA interactuar con el mundo real. Actúa como un puente entre la lógica del LLM y herramientas externas: bases de datos, APIs, navegadores, servicios de diseño, gestores de proyectos, etc.

![[../attachments/mcp_01.png]]

> [!NOTE]
> Para ver la configuración MCP específica de cada agente (Gemini CLI, Claude Code, Cursor, etc.), consulta su archivo dedicado en `../tools/`. Esta guía cubre el concepto general, buenas prácticas y las configuraciones de los MCP más utilizados.

---

## 1. Arquitectura y Componentes

### Tools, Resources y Prompts
Un servidor MCP expone tres tipos de recursos al modelo:

| Componente   | Descripción                                                                 |
| :----------- | :-------------------------------------------------------------------------- |
| **Tools**    | Funciones que el modelo puede "llamar" (ej. `get_pull_request`, `list_tasks`) |
| **Resources**| Datos estáticos o dinámicos que el modelo puede leer (ej. logs en tiempo real) |
| **Prompts**  | Instrucciones predefinidas que se pueden invocar como slash commands          |

### Transportes y Protocolos
Define cómo se comunican el cliente (IDE) e el servidor:

| Transporte        | Cuándo usarlo                                                    |
| :---------------- | :--------------------------------------------------------------- |
| `stdio`           | Proceso local. Más simple, sin red. Recomendado para desarrollo. |
| `SSE`             | HTTP con streaming. Para servers remotos o en Docker.            |
| `Streamable HTTP` | Variante moderna de SSE. Preferida en producción.                |

![[../attachments/mcp_02.jpg]]

---

## 2. Archivos de Configuración por Agente

### Rutas de Configuración (Windows)
```text
Antigravity   -> C:\Users\<USER>\.gemini\antigravity\mcp_config.json
Gemini CLI    -> C:\Users\<USER>\.gemini\settings.json
Codex CLI     -> C:\Users\<USER>\.codex\config.toml
Cursor        -> <project>\.cursor\mcp.json   |   ~/.cursor/mcp.json (global)
Claude Code   -> <project>\.mcp.json          |   ~/.claude.json (global)
```

> [!TIP]
> Si el OAuth de Antigravity se corrompe en algún MCP, se puede resetear eliminando los archivos de `~/.mcp-auth`.

---

## 3. Buenas Prácticas

### Principio de Menor Privilegio
Desactiva tools innecesarias para ahorrar tokens y mejorar la precisión del modelo.

### Patrones de Exclusión por Agente
Activa únicamente las tools que realmente vas a usar. Revisa la documentación de cada MCP y construye una lista de exclusiones.

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

### Docker: Persistencia vs Eficiencia
Levantar un servidor con `docker run` en cada IDE consume recursos excesivos. La mejor práctica es usar un contenedor persistente y conectar los IDEs vía `exec -i`.

#### Ejemplo: Configuración Shared Container
```json
{
  "command": "docker",
  "args": ["exec", "-i", "github-mcp", "/server/github-mcp-server", "stdio"]
}
```

> [!WARNING]
> Si usas `docker run` (con `--rm`) en cada IDE, cada ventana levanta su propio contenedor. Siempre que puedas, usa el patrón `exec -i` con un contenedor con nombre compartido.

---

## 4. Colección de MCPs

### 4.1 MCPs Oficiales
Servidores publicados y mantenidos por los proveedores oficiales.

#### GitHub MCP
Permite operar sobre repositorios, pull requests e issues. Requiere un `GITHUB_PERSONAL_ACCESS_TOKEN`.

**Requisito:** Variable de entorno `GITHUB_PERSONAL_ACCESS_TOKEN` configurada en el sistema.

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

![[../attachments/git-hub-mcp-01.png]]

> [!TIP]
> Si no tienes Docker, usa `docker run -i --rm` en lugar de `exec -i`. Recuerda que eso levanta un contenedor nuevo por cada IDE abierto.

---

#### ClickUp MCP (Oficial)
Servidor oficial para gestionar tareas y documentos. Usa autenticación **OAuth**.

Servidor MCP oficial de ClickUp. La autenticación es por **OAuth** — al configurarlo, el agente abrirá una ventana del navegador para autorizar el acceso.

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

![[../attachments/clickup-oauth-01.jpg]]

**Configuración para Codex CLI (`config.toml`):**

```toml
[mcp_servers.clickup-mcp]
enabled = true
url = "https://mcp.clickup.com/mcp"
```

---

#### Figma MCP (Oficial)
Permite leer estilos, colores y componentes de archivos Figma. Requiere **Dev Mode** y OAuth.

Servidor MCP oficial de Figma. Permite al agente leer estilos, colores, tipografías y componentes de un archivo. La autenticación es por **OAuth**.

> [!WARNING]
> Antigravity solo soporta el MCP oficial de Figma a través del **Dev Mode**, que requiere una cuenta de pago (Pro o superior).

**Instalación en Gemini CLI (via Extension):**

```shell
gemini extensions install https://github.com/figma/figma-gemini-cli-extension
```

```shell
# Authenticate inside gemini:
/mcp auth figma
```

---

### 4.2 MCPs de Terceros (Community)
Servidores mantenidos por la comunidad que cubren casos no oficiales.

#### Figma Console MCP
Alternativa comunitaria que se comunica con Figma Desktop sin depender de cuenta Pro.

**Repositorio:** [github.com/southleft/figma-console-mcp](https://github.com/southleft/figma-console-mcp)

Alternativa community al MCP oficial de Figma. Se comunica con Figma Desktop a través de un plugin local, sin depender de servidor remoto ni de cuenta Pro.

> [!NOTE]
> Requiere la **aplicación desktop de Figma** instalada y activa. Ejecuta el siguiente comando para obtener la ruta del manifest del plugin: `npx figma-console-mcp@latest --print-path`

**Configuración con Access Token:**

#### Ejemplo: Configuración Figma Console (JSON)
```json
{
  "mcpServers": {
    "figma-console": {
      "command": "npx",
      "args": ["-y", "figma-console-mcp@latest"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "figd_TOKEN",
        "ENABLE_MCP_APPS": "true"
      }
    }
  }
}
```

---

#### Trello MCP
Gestión de tableros y tarjetas. Requiere `TRELLO_API_KEY` y `TRELLO_TOKEN`.

**Repositorio:** [npmjs.com/package/mcp-server-trello](https://www.npmjs.com/package/mcp-server-trello)

Permite al agente leer y gestionar tableros, listas y tarjetas de Trello.

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

## 5. Recursos Adicionales

### Directorios y Hubs
Recursos para descubrir y configurar nuevos servidores MCP.

| Recurso                                              | Descripción                                                       |
| :--------------------------------------------------- | :---------------------------------------------------------------- |
| [hub.docker.com/u/mcp](https://hub.docker.com/u/mcp) | Imágenes Docker oficiales de los MCPs más populares.             |
| [mcp.so](https://mcp.so)                             | Directorio comunitario de servidores MCP.                        |
| [geminicli.com/extensions](https://geminicli.com/extensions/) | Extensiones y MCPs específicos para Gemini CLI.         |
| [cursor.directory](https://cursor.directory)         | Marketplace de reglas, skills y MCPs para Cursor.                |

*Fuente: [Model Context Protocol — Specification](https://spec.modelcontextprotocol.io/)*
