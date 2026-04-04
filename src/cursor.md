# Cursor: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Cursor en cuanto a la gestión de contexto, habilidades, subagentes, y más.

## Gestión de Contexto (Rules & AGENTS.md)

Cursor gestiona su contexto principalmente a través de reglas granulares, pero también soporta estándares universales. Usa archivos `.mdc` para reglas específicas y `AGENTS.md` como una alternativa sencilla para reglas a nivel global, de proyecto y de equipo.

El formato `MDC` destaca por usar un `frontmatter` en YAML para definir `globs` (qué archivos activan la regla) y la propiedad `alwaysApply`. Además, permite sincronizar reglas remotas directamente desde repositorios de GitHub.

**Estructura de Directorio:**
```text
mi-proyecto/
├── AGENTS.md
└── .cursor/
    └── rules/
        └── mi-regla.mdc
```

**Ejemplo de Configuración (Frontmatter en `.mdc`):**
```yaml
---
description: Reglas para componentes React
globs: src/components/**/*.tsx
alwaysApply: false
---
```
*Fuente: [Cursor Docs: Rules](https://cursor.com/docs/rules)*

## Skills (Habilidades)

Las habilidades en Cursor se manejan a través de sus reglas `.mdc` y la interfaz de configuración (Settings). Proporciona un comando especial `/migrate-to-skills` para convertir los antiguos "Slash Commands" y reglas dinámicas (aquellas configuradas con `alwaysApply: false`) al nuevo formato de Skills, optimizando así el contexto.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .cursor/
    └── rules/
        └── my-skill.mdc
```
*Fuente: [Cursor: Skills Migration](https://cursor.com/help/customization/skills#how-do-i-migrate-commands-to-skills)*

## MCP (Model Context Protocol)

Cursor soporta conexiones MCP utilizando los transportes `Stdio`, `SSE` y `Streamable HTTP`. Implementa capacidades completas para `Tools`, `Prompts`, `Resources` y `Roots`.

Una característica única son las `MCP Apps`, que permiten que las herramientas devuelvan vistas interactivas directamente en la interfaz de usuario. Además, soporta instalación rápida (One-click) mediante `cursor.directory` o el Marketplace, y permite la interpolación de variables de entorno (como `${env:NAME}`) por seguridad.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .cursor/
    └── mcp.json
```

**Ejemplo de Configuración (`mcp.json`):**
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

La arquitectura de plugins de Cursor se basa en "bundles" (paquetes). Estos pueden contener reglas, skills, agentes, comandos, servidores MCP y hooks, todo encapsulado en un solo archivo definido por `plugin.json`.

Los `Team Marketplaces` permiten a las organizaciones distribuir estos plugins privados a grupos específicos vía repositorios de GitHub, soportando además la sincronización de grupos mediante SCIM.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .cursor-plugin/
    └── plugin.json
```
*Fuente: [Cursor: Plugins](https://cursor.com/docs/plugins)*

## Hooks (Disparadores)

Los hooks en Cursor permiten que scripts externos observen, controlen y extiendan el bucle del agente mediante comunicación JSON sobre `stdio`. Se configuran en un archivo dedicado `hooks.json`.

Los eventos clave del agente incluyen `sessionStart`, `preToolUse`, `postToolUse`, y `beforeShellExecution`. Si un script de hook retorna un exit code de `2`, la acción se bloquea o deniega.

**Estructura de Directorio:**
```text
.cursor/
├── hooks.json
└── hooks/
    └── script.sh
```

**Ejemplo de Configuración (`hooks.json`):**
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

Los subagentes son asistentes de IA especializados que operan en ventanas de contexto aisladas para manejar tareas delegadas. En Cursor, se definen mediante archivos Markdown con `frontmatter` YAML.

Los metadatos incluyen `name`, `description`, `model` (puede ser `inherit`, `fast`, o un ID específico), y propiedades como `readonly` e `is_background`. Cursor incluye agentes integrados como `Explore` (para búsqueda de código), `Bash` (para terminal), y `Browser` (para web). Además, soporta recursión, permitiendo subagentes anidados.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .cursor/
    └── agents/
        └── verifier.md
```

**Ejemplo de Configuración (Frontmatter en `.md`):**
```markdown
---
name: verifier
description: Validates completed work.
model: fast
---
You are a skeptical validator...
```
*Fuente: [Cursor Docs: Subagents](https://cursor.com/docs/subagents)*
