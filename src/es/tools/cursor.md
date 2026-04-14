# Cursor

Esta guía detalla las características exclusivas de Cursor en cuanto a la gestión de contexto, habilidades, subagentes, y más.

## Gestión de Contexto (Rules & AGENTS.md)

### Reglas MDC y AGENTS.md
Cursor gestiona su contexto mediante reglas granulares `.mdc` y el estándar universal `AGENTS.md`.

### Activación por Glob Patterns
El formato `MDC` usa YAML frontmatter para definir `globs` y la propiedad `alwaysApply`. Permite sincronizar reglas remotas desde GitHub (ej. `.cursor/rules/tech-stack.mdc`).

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

En Cursor, las Skills no existen como un sistema independiente — se implementan como **reglas `.mdc` con activación condicional**. Una skill en Cursor es un archivo `.mdc` cuyo frontmatter define el `glob` de los archivos que lo activan y el `alwaysApply: false`, garantizando que el contexto solo se inyecta cuando el agente trabaja con los archivos relevantes. Esto aplica el principio de Lazy Loading de forma nativa a nivel de IDE.

La herramienta `/migrate-to-skills` convierte automáticamente los comandos `@` y las reglas dinámicas del formato anterior al estándar `.mdc` actual, migrando el historial de conocimiento acumulado al nuevo sistema de activación por patrones.

### Estructura de Directorio

```text
~/.cursor/rules/
└── global-conventions.mdc     (Global — aplica a todos los proyectos)

mi-proyecto/
└── .cursor/
    └── rules/
        ├── react-components.mdc   (Proyecto — activada por glob en componentes)
        ├── api-patterns.mdc       (Proyecto — activada en archivos de rutas)
        └── always-on.mdc          (Proyecto — alwaysApply: true)
```

### Ejemplo: Skill para Componentes React (`.mdc`)

```yaml
---
description: Standards for React functional components and hooks.
globs: src/components/**/*.tsx
alwaysApply: false
---
# React Component Standards

- Use functional components exclusively. No class components.
- Extract logic into custom hooks under `src/hooks/`.
- Props interfaces must be named `[ComponentName]Props`.
- Use named exports. Never use default exports for components.
- Styling via CSS Modules only (`Component.module.css`).
```

> [!TIP]
> Mantén cada `.mdc` enfocado en un único dominio (ej. solo "React", solo "API routing"). Los archivos de reglas que cubren múltiples dominios se activan con más frecuencia de lo necesario, contaminando el contexto en tareas no relacionadas.

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

> [!TIP]
> Consulta **[Hooks: Interceptación Determinista](../concepts/hooks.md)** para la referencia completa de eventos, protocolo stdin/stdout, scripts de producción y anti-patrones.

En Cursor, los hooks se configuran en `.cursor/hooks.json`. A diferencia de otras herramientas, Cursor no usa el field `hooks` anidado dentro de un array de `hooks` — cada evento es una clave directa del objeto raíz con un array de reglas. El script del hook se comunica via stdin JSON y retorna decisiones via exit code.

### Eventos Disponibles

| Evento | Momento de Disparo |
| :--- | :--- |
| `sessionStart` | Al iniciar una nueva sesión del agente |
| `preToolUse` | Antes de ejecutar cualquier herramienta (filtrable por `matcher`) |
| `postToolUse` | Después de que la herramienta retorna su resultado |
| `beforeShellExecution` | Antes de ejecutar un comando bash/shell específicamente |
| `sessionEnd` | Cuando la sesión finaliza |

### Estructura de Directorio

```text
.cursor/
├── hooks.json
└── hooks/
    ├── audit-network.sh
    └── protect-env.sh
```

### Schema de Reglas (`hooks.json`)

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `command` | string | Script o binario a ejecutar |
| `matcher` | string | Regex para filtrar por nombre de tool o comando |
| `failClosed` | boolean | Si `true`, bloquea la acción cuando el exit code es `≠0` |

### Ejemplo: Bloqueo de Requests de Red (`hooks.json`)

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "./.cursor/hooks/audit-network.sh",
        "matcher": "curl|wget|fetch",
        "failClosed": true
      }
    ],
    "preToolUse": [
      {
        "command": "./.cursor/hooks/protect-env.sh",
        "matcher": "Read"
      }
    ]
  }
}
```

### Ejemplo: Bloqueo de Acceso a Archivos Sensibles (`protect-env.sh`)

```bash
#!/usr/bin/env bash
# Blocks the agent from reading .env and secret files.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

  if echo "$FILE" | grep -qE '\.(env|pem|key|p12|pfx)$' || echo "$FILE" | grep -q "secrets"; then
  echo "BLOCKED: Access to sensitive file '$FILE' not allowed." >&2
  exit 2
fi

exit 0
```

> [!NOTE]
> En Cursor, `failClosed: true` en el schema de la regla actúa equivalente al exit code `2`: bloquea la acción si el hook retorna cualquier código de salida distinto de `0`. Permite definir la política de bloqueo a nivel de configuración sin necesidad de codificarla en el script.

*Fuente: [Cursor Docs: Hooks](https://cursor.com/docs/hooks)*


## Subagentes

> [!TIP]
> Consulta **[Subagentes: Arquitectura y Patrones](../concepts/subagentes.md)** para estrategias generales de orquestación, contratos de datos entre agentes y housekeeping antes de diseñar tu sistema.

En Cursor, los subagentes son archivos `.md` con frontmatter YAML ubicados en `.cursor/agents/`. El agente principal detecta cuándo invocarlos leyendo su campo `description` y comparándolo semánticamente con la tarea actual. También pueden invocarse explícitamente con `@nombre` en el chat. Los subagentes heredan automáticamente los servidores MCP globales del proyecto, pero pueden restringir su propio conjunto de herramientas vía `readonly` o configuración de permisos del modelo.


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
