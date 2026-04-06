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

Los **Workflows** permiten automatizar tareas repetitivas mediante secuencias de prompts preguardados. Se invocan mediante slash commands (ej. `/deploy`) y se estructuran como archivos Markdown (.md) que combinan instrucciones con ejecución de herramientas.

**Estructura de Directorios:**
```text
~/.gemini/antigravity/global_workflows/ (Global — disponibles en todos los proyectos)
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

### Progressive Disclosure y Scripts
Las skills se cargan bajo demanda cuando el agente detecta que su descripción coincide con la tarea. Se recomienda tratar los scripts internos como "caja negra" pasándoles el flag `--help` para optimizar el contexto.

### Estructura de Directorio
```text
mi-proyecto/
└── .agents/
    └── skills/
        └── my-skill/
            └── SKILL.md
```
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
