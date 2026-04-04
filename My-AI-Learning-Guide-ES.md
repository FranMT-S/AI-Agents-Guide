# Mi Guía de Aprendizaje de Agentes de IA

Esta guía es una referencia completa para el desarrollo de agentes potenciados por Inteligencia Artificial. Aquí encontrarás inmersiones profundas en herramientas, mejores prácticas para la gestión de contexto y evaluaciones detalladas de los modelos más avanzados.

---

## Índice
1. [Introducción y Conceptos Básicos](#introducción-y-conceptos-básicos)
2. [Skills (Habilidades)](#skills-habilidades)
3. [MCP (Model Context Protocol)](#mcp-model-context-protocol)
4. [Plugins y Extensiones](#plugins-y-extensiones)
5. [Hooks (Disparadores)](#hooks-disparadores)
6. [Subagentes](#subagentes)
7. [Automatización y Scripting](#automatización-y-scripting)
8. [Evaluación de Modelos](#evaluación-de-modelos)

---

## Introducción y Conceptos Básicos

En el desarrollo con Inteligencia Artificial, el mayor desafío no es solo escribir un buen *prompt*, sino evitar que la IA "olvide" las reglas a medida que la conversación se extiende. Este fenómeno, conocido como la limitación de la ventana de contexto, se resuelve mediante la **Memoria Persistente**.

### 1. El Concepto de Memoria Persistente y Alcance (Scope)

La memoria persistente permite que el asistente cargue automáticamente un "manual de identidad" antes de procesar tu primera palabra. Esto garantiza que el estilo, las herramientas y las restricciones de seguridad se mantengan constantes.

> [!NOTE]
> Un **archivo de contexto** (como `AGENTS.md`, `GEMINI.md` o `CLAUDE.md`) es un documento técnico donde se definen las instrucciones de comportamiento de la IA. Se denomina **memoria persistente** porque sobrevive al cierre de una sesión.

Para organizar estas instrucciones de forma eficiente, manejamos tres niveles de **Alcance (Scope)**:

1.  **Alcance Global (Capa de Usuario):** Instrucciones universales que la IA aplica siempre (ej. `~/.gemini/GEMINI.md`).
2.  **Alcance de Proyecto (Capa de Raíz):** Reglas específicas para un repositorio completo (ej. `AGENTS.md` en la raíz del proyecto).
3.  **Alcance de Módulo (Capa de Subdirectorio):** Instrucciones quirúrgicas para carpetas específicas (ej. `/src/auth/AGENTS.md`).

---

### 2. Comparativa de Archivos de Contexto

| Herramienta | Archivo Principal | Ubicación Global |
| :--- | :--- | :--- |
| **Cursor** | `.cursorrules` / `.cursor/rules/*.mdc` | Settings > Rules for AI |
| **Antigravity** | `GEMINI.md` | `~/.gemini/GEMINI.md` |
| **Gemini CLI** | `GEMINI.md` / `AGENTS.md` | `~/.gemini/GEMINI.md` |
| **Claude Code** | `CLAUDE.md` | `~/.claude/CLAUDE.md` |
| **Codex CLI** | `AGENTS.md` | `~/.codex/AGENTS.md` |

> [!WARNING]
> **Higiene de Contexto:** No satures cada carpeta con instrucciones. Si las reglas se contradicen en demasiados niveles, el comportamiento de la IA se vuelve errático. Usa siempre `.gitignore` para evitar que la IA lea carpetas innecesarias como `node_modules`.

## Skills (Habilidades)
Placeholder: Qué son las skills, consejos de construcción y metadatos.

## MCP (Model Context Protocol)
Placeholder: Configuración, seguridad y herramientas para cada CLI.

## Plugins y Extensiones
Placeholder: Resumen de integración para las distintas herramientas.

## Hooks (Disparadores)
Placeholder: Configuraciones y diferencias entre Gemini CLI, Claude Code y otros.

## Subagentes
Placeholder: Consejos, arquitectura y delegación de tareas.

## Automatización y Scripting
Placeholder: Headless mode y automatización de flujos.

## Evaluación de Modelos
Placeholder: Comparativa entre Gemini, Claude y GPT.

---
*Nota: Todos los términos técnicos y fragmentos de código se mantienen en inglés para mayor precisión técnica.*
