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
