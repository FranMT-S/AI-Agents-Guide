# Cursor: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Cursor en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Rules & AGENTS.md)
*   **Fuente:** [Cursor Docs: Rules](https://cursor.com/docs/rules)
*   **Archivos:** Usa `.cursor/rules/*.mdc` para reglas granulares y `AGENTS.md` como alternativa sencilla. Soporta reglas a nivel global, de proyecto y de equipo.
*   **Características Únicas:** El formato MDC soporta "frontmatter" YAML para definir `globs` (qué archivos activan la regla) y `alwaysApply`. Además, permite sincronizar reglas remotas directamente desde repositorios de GitHub.

## Skills (Habilidades)
*   **Fuente:** [Cursor: Skills Migration](https://cursor.com/help/customization/skills#how-do-i-migrate-commands-to-skills)
*   **Archivos:** Usa `.cursor/rules/*.mdc` y la UI de Settings.
*   **Características Únicas:** Proporciona el comando `/migrate-to-skills` para convertir "Slash Commands" y reglas dinámicas antiguas (aquellas con `alwaysApply: false`) al nuevo formato de Skills.

## MCP (Model Context Protocol)
*   **Fuente:** [Cursor: MCP](https://cursor.com/docs/mcp)
*   **Características Técnicas:** Soporta transportes **Stdio**, **SSE** y **Streamable HTTP**. Implementa Tools, Prompts, Resources y Roots.
*   **Archivos:** Configuración en `~/.cursor/mcp.json` o `.cursor/mcp.json` en el proyecto. Permisos en `~/.cursor/permissions.json`.
*   **Características Únicas:** **MCP Apps** permite que las herramientas devuelvan vistas interactivas en la UI. Instalación rápida (One-click) mediante `cursor.directory` o el Marketplace. Soporta interpolación de variables de entorno (`${env:NAME}`) por seguridad.

## Plugins y Extensiones
*   **Fuente:** [Cursor: Plugins](https://cursor.com/docs/plugins)
*   **Arquitectura:** Los plugins son "bundles" (paquetes) que pueden contener reglas, skills, agentes, comandos, servidores MCP y hooks en un solo archivo, definidos por un `.cursor-plugin/plugin.json`.
*   **Características Únicas:** **Team Marketplaces** permite a las organizaciones distribuir plugins privados a grupos específicos vía repositorios de GitHub, soportando sincronización de grupos mediante SCIM.
