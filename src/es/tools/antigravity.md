# Google Antigravity: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Google Antigravity en cuanto a la gestión de contexto, habilidades y flujos de trabajo (workflows).

## Gestión de Contexto (Rules)

### Reglas Globales y de Espacio de Trabajo
Combina `AGENTS.md` y `GEMINI.md` con reglas locales en `.agents/rules/`. Soporta menciones `@filename` para inyección dinámica de contexto adicional durante la sesión.

### Estructura de Directorios
```text
~/.gemini/GEMINI.md              (Global — ADN del desarrollador)
mi-proyecto/
├── AGENTS.md                    (Proyecto — reglas base del repositorio)
├── GEMINI.md                    (Proyecto — reglas base del repositorio)
└── .agents/
    └── rules/
        └── tech-stack.md        (Modulo — reglas adicionales por contexto)
```
*Fuente: [Antigravity Docs: Rules & Workflows](https://antigravity.google/docs/rules-workflows)*

## Workflows (Flujos de Trabajo)

Los **Workflows** permiten automatizar tareas repetitivas mediante secuencias de prompts preguardados. Se invocan mediante slash commands (ej. `/deploy`) y se estructuran como archivos Markdown (`.md`) que combinan instrucciones con ejecución de herramientas.

**Estructura de Directorios:**
```text
`~/.gemini/antigravity/global_workflows/` (Global — disponibles en todos los proyectos)
    └── my-command.md
mi-proyecto/
└── .agents/
    └── workflows/                      (Proyecto — específicos para el repositorio)
        └── build-app.md
```

**Ejemplo de Workflow (`build-app.md`):**
```markdown
---
description: Pipeline de build y validación estática local.
---
# Objetivo
Ejecutar el ciclo completo de validación y generación de artefactos.

# Pasos
1. Ejecuta `npm run test` para validar lógica.
2. Si los tests pasan, ejecuta `npm run build`.
3. Notifica el resultado final en el chat.
```

*Fuente: [Antigravity Docs: Rules & Workflows](https://antigravity.google/docs/rules-workflows)*

## Skills (Habilidades)

Las Skills de Antigravity se descubren siguiendo una jerarquía de dos niveles: primero las del **Workspace** activo (`.agents/skills/`), y luego las del **Usuario** (`~/.agents/skills/`). El agente evalúa semánticamente la `description` de cada skill al recibir una petición y la activa automáticamente si el contexto coincide. El cuerpo del archivo `SKILL.md` se inyecta en el contexto del agente únicamente cuando la skill es invocada, manteniendo el resto fuera de la ventana activa.

Una característica específica de Antigravity es su integración con el sistema de **Workflows**: una skill puede referenciar workflows internos del agente, permitiendo que una habilidad no solo provea contexto sino que orqueste secuencias de acciones preguardadas.

### Estructura de Directorio

```text
~/.agents/
└── skills/
    └── my-global-skill/         (Global — disponible en todos los proyectos)
        └── SKILL.md

mi-proyecto/
└── .agents/
    └── skills/
        └── api-style-guide/     (Proyecto — específico de este repositorio)
            ├── SKILL.md
            └── templates/
                └── endpoint.md
```

### Anatomía de SKILL.md

```markdown
---
name: api-style-guide
description: Enforces REST API conventions. Use when creating or modifying API endpoints.
---
# API Style Guide

All endpoints must follow these conventions:
- Use kebab-case for URL paths: `/user-profiles`, not `/userProfiles`
- Return standard error objects: `{ error: string, code: number }`
- Version prefix required: `/api/v1/`

For new endpoint templates, see {file:./templates/endpoint.md}
```

> [!TIP]
> Trata los scripts internos de la skill como "cajas negras". Si la skill invoca un binario externo, pásale el flag `--help` en el prompt de la skill para que el agente sepa qué argumentos acepta sin necesidad de inferirlos.

*Fuente: [Antigravity: Skills Docs](https://antigravity.google/docs/skills)*



## MCP (Model Context Protocol)

### Google ADC (Application Default Credentials)
Soporta `STDIO` y `Streamable HTTP`. El modo `authProviderType: "google_credentials"` facilita integraciones seguras con los servicios de Google Cloud (GCP) utilizando las credenciales del sistema.

### MCP Store Integrado
Interfaz visual para descubrir e instalar servidores (Supabase, Linear, Docker, etc.) con un clic. Permite la gestión de herramientas permitidas mediante el campo `disabledTools` en el archivo de configuración.

### Estructura de Directorio
```text
~/.gemini/
└── antigravity/
    ├── mcp_config.json
    └── mcp_oauth_tokens.json
```

**Ejemplo de Configuración (`mcp_config.json`):**
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp"],
      "disabledTools": ["delete_table"]
    }
  },
  "authProviderType": "google_credentials"
}
```
*Fuente: [Antigravity: MCP Docs](https://antigravity.google/docs/mcp)*
