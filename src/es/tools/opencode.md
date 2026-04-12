# OpenCode: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de OpenCode en cuanto a la gestión de contexto, habilidades y plugins.

## Gestión de Contexto (Rules)

OpenCode carga `AGENTS.md` y `opencode.json` automáticamente al iniciar una sesión. Lo que lo distingue del resto de herramientas es su mecanismo de **Lazy Loading**: en lugar de inyectar toda la documentación del proyecto en el contexto al arranque, el agente carga archivos de reglas adicionales de forma diferida, solo cuando el usuario o la tarea los referencia explícitamente. Esto reduce drásticamente el consumo de tokens en sesiones largas donde solo una fracción del conocimiento del proyecto es relevante.

### Lazy Loading y Referencias (@file)

Cualquier archivo o carpeta puede ser referenciado con la sintaxis `@ruta` directamente desde el chat. OpenCode inyecta el contenido de ese recurso en el contexto solo en el momento de la referencia, manteniendo el resto fuera de la ventana activa hasta que se necesite.

**Ejemplos de referencia:**

```text
@AGENTS.md                     Carga el archivo raíz de reglas
@src/backend                   Carga todos los archivos del directorio backend
@docs/api-conventions.md       Documento de convenciones especifico
@src/**/*.types.ts             Glob — carga todos los archivos de tipos del proyecto
```

> [!TIP]
> Usa `@carpeta/` en lugar de listar archivos individuales. OpenCode recorre el directorio y carga los archivos relevantes según el contexto de la tarea, ahorrando tokens al no tener que listar explícitamente cada archivo.

### Estructura de Directorios

```text
~/.config/opencode/
└── opencode.json              (Global — configuracion personal del usuario, todos los proyectos)

mi-proyecto/
├── AGENTS.md                  (Proyecto — reglas del repositorio, estándar universal)
└── opencode.json              (Proyecto — configuracion y reglas del proyecto, compartido via git)
```

### Configuración de Rules (`opencode.json`)

El campo `rules` acepta un arreglo mixto de tres tipos de fuentes: **rutas locales a archivos**, **rutas a carpetas** y **URLs remotas**. OpenCode los carga en el orden en que se declaran.

**Estructura del campo `rules`:**
```json
{
  "$schema": "https://opencode.ai/config.json",
  "rules": [
    "AGENTS.md",
    "docs/TYPESCRIPT.md",
    "@src/backend",
    "https://example.com/.well-known/opencode"
  ]
}
```

**Ejemplo completo funcional (`opencode.json`):**
```json
{
  "$schema": "https://opencode.ai/config.json",
  "rules": [
    "AGENTS.md",
    "docs/TYPESCRIPT.md",
    "docs/TESTING.md",
    "@src/backend",
    "https://standards.acme.com/.well-known/opencode"
  ],
  "model": "anthropic/claude-sonnet-4-20250514",
  "autoshare": false
}
```

### Remote Rules (.well-known/opencode)

OpenCode permite referenciar **reglas remotas** via URL. Cuando la URL apunta al endpoint `.well-known/opencode` de un servidor, OpenCode fetcha y carga esas reglas como si fueran locales. Esta característica permite que equipos distribuidos gestionen un conjunto centralizado de estándares de codificación sin duplicar archivos en cada repositorio.

**Casos de uso comunes:**
- Estándares de seguridad corporativos aplicados a todos los proyectos de la organización.
- Guías de estilo de código actualizadas en tiempo real sin necesidad de commits.
- Reglas diferenciadas por entorno (`staging` vs `production`) servidas desde el mismo host.

**Ejemplo de endpoint remoto (`opencode.json`):**
```json
{
  "rules": [
    "AGENTS.md",
    "https://standards.acme.com/.well-known/opencode",
    "https://security.acme.com/.well-known/opencode"
  ]
}
```

El servidor remoto debe servir un documento Markdown plano en esa ruta. OpenCode lo descargará al inicio de cada sesión, garantizando que los estándares siempre estén actualizados.

**Generación automática con CLI:**
```bash
opencode init
```
El comando `/init` analiza el repositorio y genera un `AGENTS.md` y `opencode.json` base con las reglas inferidas automáticamente desde el código existente.

*Fuente: [OpenCode: Rules](https://opencode.ai/docs/rules/)*


## Skills (Habilidades)

Una de las características más distintivas de OpenCode es que escanea **múltiples directorios de skills en paralelo**: `.opencode/skills/`, `.claude/skills/` y `.agents/skills/`. Esta compatibilidad cruzada permite que un equipo con repositorios que ya usan Claude Code o Antigravity aproveche sus skills existentes sin migración. OpenCode selecciona automáticamente la skill más relevante según la descripción semántica de la tarea.

El control de permisos de las skills es granular y se configura en `opencode.json`. Los tres niveles (`ask`, `allow`, `deny`) permiten definir exactamente qué acciones puede ejecutar una skill: desde pedir confirmación antes de modificar archivos hasta bloquear completamente el acceso a comandos bash destructivos.

### Estructura de Directorio

```text
mi-proyecto/
├── .opencode/
│   └── skills/
│       └── db-helper/          (Específico de OpenCode)
│           └── SKILL.md
├── .claude/
│   └── skills/                 (Skills heredadas de Claude Code)
│       └── api-reviewer/
│           └── SKILL.md
└── .agents/
    └── skills/                 (Skills del estándar universal)
        └── git-flow/
            └── SKILL.md
```

### Configuración de Permisos (`opencode.json`)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "db-helper": {
      "permission": {
        "bash": {
          "*": "deny",
          "prisma migrate status": "allow",
          "prisma migrate deploy": "ask"
        },
        "edit": "ask",
        "webfetch": "deny"
      }
    }
  }
}
```

### Ejemplo: Skill de Base de Datos (`db-helper/SKILL.md`)

```markdown
---
name: db-helper
description: Assists with Prisma database migrations and schema management. Use when working with database changes.
---
# Database Helper

This skill manages Prisma migrations safely.

Rules:
- Always run `prisma migrate status` before any migration to check pending changes.
- Use `prisma migrate deploy` for production. Never use `migrate reset` outside local dev.
- After schema changes, run `prisma generate` to update the client.
- All new models require a migration file — never modify the schema without a matching migration.
```

> [!TIP]
> OpenCode hereda las skills de directorios `.claude/` y `.agents/` automáticamente. Si tu equipo ya usa Claude Code, no necesitas migrar ni duplicar las skills para que OpenCode las reconozca.

*Fuente: [OpenCode: Skills Docs](https://opencode.ai/docs/skills/)*



## MCP (Model Context Protocol)

### Autenticación Dinámica y SSE/HTTP
Resuelve OAuth automáticamente vía `Dynamic Client Registration`. Soporta transportes locales (`Stdio`) y remotos.

### Remote Defaults (.well-known)
Permite configuraciones externas vía endpoints `.well-known/opencode` para gestión centralizada en organizaciones.

### Estructura de Directorio
```text
mi-proyecto/
└── opencode.json
```

#### Ejemplo: Servidor MCP SSE (`opencode.json`)
```json
{
  "mcp": {
    "servers": {
      "clickup": {
        "url": "https://mcp.clickup.com/sse",
        "tools": {"*": false, "list_tasks": true}
      }
    }
  }
}
```
*Fuente: [OpenCode: MCP Servers (ES)](https://opencode.ai/docs/es/mcp-servers/)*

## Plugins y Extensiones

### Arquitectura Event-Driven (Bun)
Basada en módulos nativos TS/JS ejecutados sobre Bun. Plugin interactivos vía PTY.

### Compaction Hooks
Permite personalizar cómo la IA resume sesiones largas mediante eventos como `session.compacted`.

### Estructura de Directorio
```text
mi-proyecto/
└── .opencode/
    └── plugins/
        └── my-plugin.ts
```

#### Ejemplo: Plugin TS (Compactación)
```typescript
export default {
  on: {
    "session.compacted": (context) => {
      console.log("Sesión compactada!");
    }
  }
}
```
*Fuentes: [OpenCode: Plugins (ES)](https://opencode.ai/docs/es/plugins/) | [OpenCode: Ecosystem (ES)](https://opencode.ai/docs/es/ecosystem/)*

## Subagentes y Orquestadores

OpenCode distingue dos tipos de agentes que operan en distintos roles. Los agentes primarios son los que el usuario controla directamente; los subagentes son especializados e invocados automáticamente o por mención `@nombre`.

> [!TIP]
> Consulta **[Subagentes: Arquitectura y Patrones](../concepts/subagentes.md)** para estrategias generales de orquestación, contratos de datos entre agentes y housekeeping antes de diseñar tu sistema.


### Tipos de Agentes

#### Agentes Primarios (Primary Agents)
Son el asistente principal de la sesión. Se cambia entre ellos con la tecla `Tab` o el keybind `switch_agent`. Su acceso a herramientas se controla mediante permisos.

#### Subagentes (Subagents)
Son asistentes especializados que los agentes primarios pueden invocar para tareas específicas. También pueden ser invocados manualmente con `@nombre` en el chat.

### Agentes Integrados (Built-in)

| Nombre | Modo | Propósito |
| :--- | :--- | :--- |
| `build` | `primary` | Agente por defecto. Acceso completo a todas las tools. |
| `plan` | `primary` | Solo análisis y planificación. Todas las writes/bash son `ask`. |
| `general` | `subagent` | Multi-propósito con acceso completo (excepto `todo`). |
| `explore` | `subagent` | Solo lectura. Búsqueda rápida de archivos y código. |
| `compaction` | `primary` *oculto* | Compacta contextos largos automáticamente. |
| `title` | `primary` *oculto* | Genera títulos de sesión automáticamente. |
| `summary` | `primary` *oculto* | Crea resúmenes de sesión automáticamente. |

### Uso e Invocación

*   **Agentes Primarios:** Cicla entre ellos con `Tab` o el keybind `switch_agent`.
*   **Subagentes (manual):** Menciónalos con `@nombre` en el chat.
    ```
    @general ayúdame a buscar esta función en el repo
    ```
*   **Navegación entre sesiones hijas:** Los subagentes crean sesiones hijas separadas.
    *   `session_child_first` (`<Leader>+Down`): Entrar a la primera sesión hija.
    *   `session_child_cycle` (`Right`): Ciclar a la siguiente sesión hija.
    *   `session_child_cycle_reverse` (`Left`): Ciclar a la sesión hija anterior.
    *   `session_parent` (`Up`): Regresar a la sesión padre.

### Métodos de Configuración

Los agentes pueden configurarse de **dos formas**: JSON (en `opencode.json`) o Markdown (en archivos `.md`).

#### Método 1: JSON (`opencode.json`)

Permite configurar agentes built-in y crear agentes personalizados directamente en el archivo de configuración del proyecto o global. El campo `tools` es deprecated; usar `permission` en su lugar.

**Estructura de Directorio:**
```text
~/.config/opencode/opencode.json  (Global — todos los proyectos)
mi-proyecto/
└── opencode.json                  (Proyecto — compartido con el equipo via git)
```

**Ejemplo de Configuración (`opencode.json`):**
```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "{file:./prompts/build.txt}",
      "permission": {
        "bash": { "*": "ask", "git status *": "allow" }
      }
    },
    "plan": {
      "mode": "primary",
      "model": "anthropic/claude-haiku-4-20250514",
      "temperature": 0.1,
      "permission": { "edit": "deny", "bash": "deny" }
    },
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.1,
      "steps": 10,
      "permission": {
        "edit": "deny",
        "bash": { "*": "ask", "git diff": "allow", "git log*": "allow" },
        "webfetch": "deny"
      }
    }
  }
}
```

#### Método 2: Markdown (archivos `.md`)

El nombre del archivo se convierte en el nombre del agente. Por ejemplo, `review.md` crea el agente `@review`. El frontmatter YAML define la configuración y el cuerpo del archivo es el system prompt.

**Estructura de Directorio:**
```text
~/.config/opencode/agents/       (Global — disponibles en todos los proyectos)
    ├── security-auditor.md      (Agente simple — archivo solo)
    └── code-reviewer/           (Agente con recursos — subdirectorio)
        ├── code-reviewer.md     (El .md raiz del directorio define el agente)
        └── prompts/             (Archivos de apoyo: prompts, docs, etc.)
            └── review-rules.md
mi-proyecto/
└── .opencode/
    └── agents/                  (Proyecto — compartidos con el equipo via git)
        ├── manager.md
        └── code-reviewer/
            ├── code-reviewer.md
            └── context/
                └── api-standards.md
```

> [!TIP]
> Los subdirectorios permiten agrupar el agente con sus archivos de apoyo (prompts externos, documentación de referencia, ejemplos). El archivo `.md` cuyo nombre coincide con el directorio padre define el agente; el resto son recursos de contexto.

**Ejemplo: Revisor de Código (`code-reviewer.md`):**
```markdown
---
description: Reviews code for quality and security. Use when validating changes before commit.
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
steps: 10
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
  webfetch: deny
---
You are in code review mode. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Security considerations

Provide feedback without making direct changes.
```

### Crear un Agente con CLI

OpenCode incluye un comando interactivo para crear agentes que pregunta la ubicación (global/proyecto), la descripción, genera el prompt, selecciona las tools y crea el archivo `.md` resultante.

```bash
opencode agent create
```

### Schema de Configuración (Opciones)

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `description` | `string` | **Requerido.** Descripción del propósito del agente. |
| `mode` | `primary` \| `subagent` \| `all` | Modo de uso. Default: `all`. |
| `model` | `string` | Modelo en formato `provider/model-id`. Heredado del invocador si no se especifica. |
| `prompt` | `string` | System prompt inline o referencia externa `{file:./path}`. |
| `temperature` | `number` | Controla la aleatoriedad de las respuestas. **0.0–0.2:** respuestas deterministas, ideal para análisis y revisión de código. **0.3–0.5:** balance entre creatividad y precisión, óptimo para desarrollo general. **0.6–1.0:** respuestas más creativas, útil para brainstorming. Default: `0` para la mayoría de modelos; `0.55` para modelos Qwen. |
| `top_p` | `number` | Diversidad de respuesta alternativa a `temperature` (0.0–1.0). |
| `steps` | `number` | Máximo de iteraciones antes de forzar resumen. Sin límite si no se define. |
| `disable` | `boolean` | Deshabilitar completamente el agente. |
| `hidden` | `boolean` | Ocultar del menú `@`. Solo invocable programáticamente via `Task` tool. Solo aplica a `mode: subagent`. |
| `color` | `string` | Color en la UI: hex (`#FF5733`) o tema (`primary`, `accent`, `error`...). |
| `permission` | `object` | Permisos granulares para `edit`, `bash` y `webfetch`. |
| `permission.task` | `object` | Qué subagentes puede invocar este agente. Usa glob patterns. |
| `tools` | `object` | **Deprecated.** Usar `permission` en su lugar. |

### Sistema de Permisos

Los valores son `"ask"`, `"allow"` o `"deny"`. Para `bash`, soporta glob patterns y se aplica la **última regla que coincida** (no la primera).

> [!TIP]
> La regla `*` debe ir primero y las reglas específicas después. La última que coincida gana.

```json
{
  "agent": {
    "build": {
      "permission": {
        "bash": { "*": "ask", "git status *": "allow" },
        "edit": "allow",
        "webfetch": "deny"
      },
      "permission": {
        "task": { "*": "deny", "code-reviewer": "ask", "explore": "allow" }
      }
    }
  }
}
```

> [!NOTE]
> Los usuarios siempre pueden invocar cualquier subagente directamente via `@nombre` incluso si `permission.task` lo tiene en `deny` para el agente primario.

*Fuentes: [OpenCode: Agents](https://opencode.ai/docs/agents/) | [OpenCode: Permissions](https://opencode.ai/docs/permissions/)*
