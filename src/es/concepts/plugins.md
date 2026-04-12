# Plugins y Extensiones: Empaquetado y Distribución de Ecosistemas

Un plugin es la unidad de distribución más completa del ecosistema de agentes de IA. A diferencia de las Skills (que proveen capacidades específicas) o los Hooks (que interceptan eventos), un plugin empaqueta el conjunto completo de lo que un agente necesita para trabajar en un contexto determinado: Skills, Hooks, servidores MCP, configuración de subagentes y reglas de contexto — todo versionado junto y con una sola instalación.

La analogía práctica es la de las extensiones de editor de código: cuando un nuevo miembro del equipo instala VS Code, puede reproducir el entorno de trabajo completo instalando un pack de extensiones preconfigurado en lugar de configurar cada herramienta por separado. Los plugins de agentes cumplen este mismo rol en el ecosistema de IA.

---

## Comparativa entre Sistemas de Plugins

Cada herramienta tiene una arquitectura de plugins técnicamente distinta, pero el propósito es idéntico: distribuir ecosistemas completos de forma reproducible.

| Herramienta | Formato | Instalación | Capacidades empaquetables |
| :--- | :--- | :--- | :--- |
| **Claude Code** | `.claude-plugin/plugin.json` | `/plugin install <nombre>@<marketplace>` | Skills, agents, hooks, MCP (`.mcp.json`), LSP (`.lsp.json`) |
| **Gemini CLI** | `gemini-extension.json` | `gemini extensions install <URL>` | Commands TOML, skills, policy rules, credentials |
| **Cursor** | `.cursor-plugin/plugin.json` | Marketplace UI / private team registry | Reglas MDC, skills, agents, MCP servers |
| **OpenCode** | Módulo TypeScript (`.ts`) | Archivo en `.opencode/plugins/` | Event handlers, PTY interactivos, session hooks |

---

## Claude Code: Plugins

### Arquitectura

En Claude Code, un plugin es esencialmente **una estructura de directorios** con un manifiesto mínimo de metadata. Claude Code carga automáticamente los componentes basándose en la convención de carpetas: skills desde `skills/`, subagentes desde `agents/`, hooks desde `hooks/`, MCP desde `.mcp.json` y servidores LSP desde `.lsp.json`. El archivo `plugin.json` solo declara metadata de identificación, no los componentes.

**Estructura de Directorio:**
```text
mi-plugin/
├── .claude-plugin/
│   └── plugin.json          (Solo metadata: name, version, description, author)
├── skills/
│   └── code-review/
│       └── SKILL.md         (Skill cargada por convención de directorio)
├── agents/
│   └── reviewer.md          (Subagente cargado por convención de directorio)
├── hooks/
│   └── hooks.json           (Hooks cargados por convención de directorio)
├── .mcp.json                (Servidores MCP del plugin)
└── .lsp.json                (Servidores LSP para code intelligence)
```

**`plugin.json` — Metadata y Component Path Fields:**
El manifiesto soporta sobreescribir las rutas por defecto indicando qué directorios o archivos usar para cada capacidad:
```json
{
  "name": "@myteam/fullstack-plugin",
  "version": "1.2.0",
  "description": "Complete environment for fullstack TypeScript development.",
  "author": { "name": "Team" },
  "skills": "./custom/skills/",
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/"
}
```

> [!TIP]
> **Convención vs. Configuración:** Si no defines los campos `skills`, `agents`, etc., Claude Code buscará automáticamente en los directorios `skills/`, `agents/`, `hooks/hooks.json`, y `.mcp.json`.

**Ejemplo de `.lsp.json` (Code Intelligence):**
```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

**Comandos de gestión:**
```bash
# Añadir marketplace (repositorio GitHub de Anthropic)
/plugin marketplace add anthropics/claude-code

# Instalar un plugin desde el marketplace
/plugin install commit-commands@anthropics-claude-code

# Desarrollo local — cargar sin instalar
claude --plugin-dir ./mi-plugin

# Recargar plugins sin reiniciar
/reload-plugins

# Deshabilitar/habilitar plugin instalado
/plugin disable plugin-name@marketplace-name
/plugin enable plugin-name@marketplace-name

# Desinstalar
/plugin uninstall plugin-name@marketplace-name
```

*Fuentes: [Claude Code: Create Plugins](https://code.claude.com/docs/en/plugins) | [Claude Code: Discover Plugins](https://code.claude.com/docs/en/discover-plugins) | [Claude Code: Plugins Reference](https://code.claude.com/docs/en/plugins-reference)*

---

## Gemini CLI: Extensions

### Arquitectura

Las extensiones de Gemini CLI se distribuyen como repositorios Git. El archivo `gemini-extension.json` declara los comandos personalizados que se agregan a la CLI, las skills incluidas y las reglas del Policy Engine.

**Estructura de Directorio:**
```text
mi-extension/
├── gemini-extension.json    (Manifiesto de la extensión)
├── commands/
│   ├── deploy.toml          (Comando personalizado)
│   └── audit.toml           (Otro comando personalizado)
├── skills/
│   └── api-reviewer.md      (Skill incluida)
└── policies/
    └── security.yaml        (Reglas del Policy Engine)
```

**Ejemplo de `gemini-extension.json`:**
```json
{
  "name": "myteam-devtools",
  "version": "2.0.0",
  "description": "Development tools and security policies for our stack.",
  "commands": ["./commands/deploy.toml", "./commands/audit.toml"],
  "skills": ["./skills/api-reviewer.md"],
  "policies": ["./policies/security.yaml"],
  "credentials": {
    "DEPLOY_TOKEN": { "keychain": true }
  }
}
```

**Ejemplo de Comando Personalizado (`deploy.toml`):**
```toml
name = "deploy"
description = "Deploy the current branch to staging environment"
prompt = """
Deploy the current branch to staging:
1. Run the pre-deploy checks
2. Build the Docker image
3. Push to the staging registry
4. Notify #deployments on Slack
"""
```

**Instalación y desarrollo:**
```bash
# Instalar desde GitHub
gemini extensions install https://github.com/myteam/gemini-devtools

# Desarrollo local — instala desde directorio sin copiar
gemini extensions link ./mi-extension/

# Listar extensiones instaladas
gemini extensions list

# Desinstalar
gemini extensions uninstall myteam-devtools
```

*Fuentes: [Gemini CLI: Extensions Guide](https://geminicli.com/docs/extensions/) | [Writing Extensions](https://geminicli.com/docs/extensions/writing-extensions/) | [Reference](https://geminicli.com/docs/extensions/reference/)*

---

## Cursor: Plugins y Team Marketplaces

### Arquitectura

Cursor usa un sistema de "bundles" que empaquetan reglas MDC, skills, subagentes y configuraciones MCP en un `plugin.json`. Los plugins se distribuyen a través del Marketplace público (`cursor.com/marketplace`) o mediante un Team Marketplace privado (disponible en plan Business).

**Estructura de Directorio:**
```text
mi-cursor-plugin/
├── .cursor-plugin/
│   └── plugin.json          (Manifiesto del bundle)
├── rules/
│   └── typescript-style.mdc (Reglas MDC incluidas)
├── agents/
│   └── reviewer.md          (Subagente incluido)
└── mcp/
    └── config.json          (Servidores MCP del plugin)
```

**Ejemplo de `plugin.json`:**
```json
{
  "name": "typescript-fullstack",
  "version": "1.0.0",
  "description": "TypeScript + React + Prisma development environment.",
  "rules": ["./rules/typescript-style.mdc"],
  "agents": ["./agents/reviewer.md"],
  "mcpServers": {
    "github": { "command": "npx", "args": ["-y", "@cursor/mcp-github"] }
  }
}
```

**Team Marketplaces (Plan Business):**

Los Team Marketplaces permiten publicar plugins privados accesibles únicamente para miembros del equipo. Soportan sincronización de grupos via SCIM desde el Identity Provider (Okta, Azure AD).

```bash
# Publicar al team marketplace (desde la UI de cursor.com)
# Settings → Team → Marketplace → Publish Plugin

# Los miembros del equipo lo ven directamente en su Marketplace
# cursor.com/marketplace?team=myorg
```

*Fuente: [Cursor Docs: Plugins](https://cursor.com/docs/plugins)*

---

## OpenCode: Plugins (TypeScript Nativos)

### Arquitectura

OpenCode es la herramienta con el sistema de plugins más diferente del ecosistema. Los plugins son **módulos TypeScript** ejecutados directamente en el runtime Bun del propio OpenCode. No hay un manifiesto JSON — el plugin es código que se suscribe a eventos via una API de eventos tipada.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .opencode/
    └── plugins/
        ├── audit-logger.ts    (Plugin de auditoría)
        └── custom-commands.ts (Plugin de comandos)
```

**API de Eventos Disponibles:**

| Evento | Cuándo se dispara |
| :--- | :--- |
| `session.start` | Al iniciar una nueva sesión |
| `session.end` | Al finalizar la sesión |
| `session.compacted` | Cuando el contexto es compactado por longitud |
| `tool.before` | Antes de ejecutar cualquier herramienta |
| `tool.after` | Después de que la herramienta retorna |
| `message.user` | Cuando el usuario envía un mensaje |
| `message.assistant` | Cuando el agente termina de responder |

**Ejemplo: Plugin de Auditoría Completa (`audit-logger.ts`):**
```typescript
import type { Plugin } from "opencode/plugin"
import fs from "fs"

const auditPlugin: Plugin = {
  name: "audit-logger",
  version: "1.0.0",
  on: {
    "tool.before": (ctx) => {
      const entry = {
        timestamp: new Date().toISOString(),
        tool: ctx.tool.name,
        input: ctx.tool.input,
        session: ctx.session.id,
      }
      fs.appendFileSync(".opencode/audit.jsonl", JSON.stringify(entry) + "\n")
    },
    "session.compacted": (ctx) => {
      console.log(`Session ${ctx.session.id} compacted at ${ctx.stats.tokenCount} tokens`)
    },
  },
}

export default auditPlugin
```

**Ejemplo: Plugin con PTY Interactivo (`custom-commands.ts`):**
```typescript
import type { Plugin } from "opencode/plugin"

const commandsPlugin: Plugin = {
  name: "custom-commands",
  on: {
    "message.user": async (ctx) => {
      if (ctx.message.content.startsWith("/deploy")) {
        const target = ctx.message.content.replace("/deploy ", "").trim()
        await ctx.pty.run(`./scripts/deploy.sh ${target}`)
      }
    },
  },
}

export default commandsPlugin
```

*Fuentes: [OpenCode: Plugins](https://opencode.ai/docs/plugins/) | [OpenCode: Ecosystem](https://opencode.ai/docs/ecosystem/)*

---

## Cuándo Crear un Plugin vs. una Skill

| Criterio | Skill | Plugin |
| :--- | :--- | :--- |
| **Alcance** | Una capacidad específica | Ecosistema completo para un contexto |
| **Distribución** | Archivo `.md` copiado o referenciado | Instalación con un solo comando |
| **Versionado** | Manual | Declarado en el manifiesto |
| **Dependencias** | No tiene | Puede declarar skills, hooks, MCP |
| **Audiencia** | Uso personal o en el proyecto | Equipo, empresa o comunidad |
| **Cuándo usar** | Experimentando, uso local | Stack estable, equipo distribuido |

*Fuentes generales: [Claude Code: Plugins](https://code.claude.com/docs/en/plugins) | [Gemini CLI: Extensions](https://geminicli.com/docs/extensions/) | [Cursor: Plugins](https://cursor.com/docs/plugins) | [OpenCode: Plugins](https://opencode.ai/docs/plugins/)*
