# Cursor: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Cursor en cuanto a la gestión de contexto, habilidades, subagentes, y más.

## Gestión de Contexto (Rules & AGENTS.md)

### Reglas MDC y AGENTS.md
Cursor gestiona su contexto mediante reglas granulares `.mdc` y el estándar universal `AGENTS.md`.

### Activación por Glob Patterns
El formato `MDC` usa YAML frontmatter para definir `globs` y la propiedad `alwaysApply`. Permite sincronizar reglas remotas desde GitHub.

### Estructura de Directorios
```text
~/.cursor/rules/global.mdc       (Global — reglas que aplican a todos los proyectos)
mi-proyecto/
├── AGENTS.md                    (Proyecto — estándar multiplataforma)
└── .cursor/
    └── rules/
        └── mi-regla.mdc         (Proyecto — regla con activación por glob o always)
```

#### Ejemplo: Reglas para React (`.mdc`)
```yaml
---
description: Reglas para componentes React
globs: src/components/**/*.tsx
alwaysApply: false
---
```
*Fuente: [Cursor Docs: Rules](https://cursor.com/docs/rules)*

## Skills (Habilidades)

### Migración de Comandos
Las habilidades se manejan vía reglas `.mdc`. El comando `/migrate-to-skills` convierte antiguos comandos y reglas dinámicas al nuevo formato optimizado.

### Estructura de Directorio
```text
mi-proyecto/
└── .cursor/
    └── rules/
        └── my-skill.mdc
```
*Fuente: [Cursor: Skills Migration](https://cursor.com/help/customization/skills#how-do-i-migrate-commands-to-skills)*

## MCP (Model Context Protocol)

### Transportes y Roots
Soporta `Stdio`, `SSE` y `Streamable HTTP`. Implementa `Tools`, `Prompts`, `Resources` y `Roots`.

### MCP Apps y Marketplace
Las `MCP Apps` devuelven vistas interactivas. Soporta instalación rápida vía `cursor.directory` y variables de entorno (`${env:NAME}`).

### Estructura de Directorio
```text
mi-proyecto/
└── .cursor/
    └── mcp.json
```

#### Ejemplo de Configuración (`mcp.json`)
```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["exec", "-i", "github-mcp", "/server/github-mcp-server", "stdio"]
    }
  }
}
```
*Fuente: [Cursor: MCP](https://cursor.com/docs/mcp)*

## Plugins y Extensiones

### Bundles y Marketplace
Arquitectura basada en "bundles" que encapsulan reglas, skills y agentes en un `plugin.json`.

### Team Marketplaces
Permiten distribuir plugins privados vía GitHub, soportando sincronización de grupos mediante SCIM.

### Estructura de Directorio
```text
mi-proyecto/
└── .cursor-plugin/
    └── plugin.json
```
*Fuente: [Cursor: Plugins](https://cursor.com/docs/plugins)*

## Hooks (Disparadores)

### Comunicación vía Stdio
Scripts externos que observan y controlan el bucle del agente mediante JSON.

### Eventos y Bloqueo (Fail-Closed)
Eventos como `sessionStart`, `preToolUse` y `beforeShellExecution`. El código `2` bloquea la acción.

### Estructura de Directorio
```text
.cursor/
├── hooks.json
└── hooks/
    └── script.sh
```

#### Ejemplo de Configuración (`hooks.json`)
```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [{
      "command": "./hooks/audit.sh",
      "matcher": "curl|wget",
      "failClosed": true
    }]
  }
}
```
*Fuente: [Cursor Docs: Hooks](https://cursor.com/docs/hooks)*

## Subagentes

### Aislamiento y Delegación
Asistentes especializados en contextos aislados. El agente principal los invoca automáticamente o vía `@nombre`.

### Herencia y Recursión
Soportan cadenas de orquestación anidadas. Heredan MCP globales y pueden usar skills locales del proyecto.

### Agentes Integrados

| Nombre | Proposito | Modo |
|---|---|---|
| `Explore` | Busqueda y analisis de codigo en el repositorio | Solo lectura |
| `Bash` | Ejecucion de comandos de terminal | Escritura |
| `Browser` | Navegacion y extraccion de contenido web | Solo lectura |

**Estructura de Directorio:**
```text
~/.cursor/agents/                (Global — disponibles en todos los proyectos)
    └── researcher.md
mi-proyecto/
├── AGENTS.md                    (Proyecto — contexto del repositorio)
├── .cursor/
│   ├── agents/                  (Proyecto — subagentes personalizados)
│   │   ├── architect.md
│   │   └── code-reviewer.md
│   ├── skills/                  (Proyecto — skills que los subagentes pueden usar)
│   │   └── api-style-guide/
│   │       └── SKILL.md
│   └── mcp.json                 (Global — heredado por todos los subagentes)
└── src/
    └── api/
        └── AGENTS.md            (Subdirectorio — contexto especifico del modulo)
```

### Campos del Frontmatter

| Campo | Descripcion | Valores |
|---|---|---|
| `name` | Identificador del subagente | string |
| `description` | Cuando invocarlo (el orquestador lo lee para decidir la delegacion) | string |
| `model` | Modelo a usar | `fast`, `inherit`, o ID completo (ej. `gpt-4o`) |
| `readonly` | Impide modificaciones al sistema de archivos | `true` / `false` |
| `is_background` | Ejecutar de forma asincrona en segundo plano | `true` / `false` |

#### Ejemplo: Orquestador de Arquitectura (`architect.md`)
```markdown
---
name: architect
description: Plans and delegates implementation work. Use when the user asks to build a new feature end-to-end.
model: inherit
is_background: false
readonly: true
---
You are a software architect. Your job is to plan, NOT to code.
1. Analyze the request and break it into tasks.
2. For each task, delegate to @code-reviewer or the Bash agent.
3. Do not write code yourself. Only produce the plan and coordinate.
```

#### Ejemplo: Revisor de Código (`code-reviewer.md`)
```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and performance issues.
model: fast
readonly: true
---
You are a skeptical code reviewer. Analyze the files provided and list specific issues.
Apply the conventions from the AGENTS.md in the relevant directory.
```
*Fuente: [Cursor Docs: Subagents](https://cursor.com/docs/agent/subagents)*
