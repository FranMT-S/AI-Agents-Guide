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
> 
> **`AGENTS.md` se está convirtiendo en el estándar multiplataforma**, siendo compatible actualmente con la mayoría de las herramientas (Codex, Gemini CLI, Claude Code y recientemente Antigravity).

Para organizar estas instrucciones de forma eficiente, manejamos tres niveles de **Alcance (Scope)**:

1.  **Alcance Global (Capa de Usuario):** Instrucciones universales que la IA aplica siempre (ej. `~/.gemini/GEMINI.md`).
2.  **Alcance de Proyecto (Capa de Raíz):** Reglas específicas para un repositorio completo (ej. `AGENTS.md` en la raíz del proyecto).
3.  **Alcance de Módulo (Capa de Subdirectorio):** Instrucciones quirúrgicas para carpetas específicas (ej. `/src/auth/AGENTS.md`).

---

### 2. Comparativa de Archivos de Contexto

| Herramienta | Archivos Principales | Ubicación Global |
| :--- | :--- | :--- |
| **Cursor** | `.cursor/rules/*.mdc` / `AGENTS.md` | Settings > Rules for AI |
| **Antigravity** | `GEMINI.md` / `AGENTS.md` | `~/.gemini/GEMINI.md` |
| **Gemini CLI** | `GEMINI.md` / `AGENTS.md` | `~/.gemini/GEMINI.md` |
| **Claude Code** | `CLAUDE.md` / `AGENTS.md` | `~/.claude/CLAUDE.md` |
| **Codex CLI** | `AGENTS.md` | `~/.codex/AGENTS.md` |

> [!WARNING]
> **Higiene de Contexto:** No satures cada carpeta con instrucciones. Si las reglas se contradicen en demasiados niveles, el comportamiento de la IA se vuelve errático. Usa siempre `.gitignore` para evitar que la IA lea carpetas innecesarias como `node_modules`.

**Referencias y Documentación:**
- [Cursor Docs: Rules & AGENTS.md](https://cursor.com/docs/rules#agentsmd)
- [Antigravity Docs: Rules & Workflows](https://antigravity.google/docs/rules-workflows)
- [Gemini CLI: Memory Management](https://geminicli.com/docs/cli/tutorials/memory-management/)
- [Claude Code: Memory & Agents.md](https://code.claude.com/docs/en/memory#agents-md)
- [Codex CLI: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)

## Skills (Habilidades)

Las **Skills** representan una experticia específica bajo demanda. A diferencia del contexto general, las habilidades contienen instrucciones, scripts y recursos que el agente solo carga mediante **progressive disclosure** (revelación progresiva) cuando detecta que la tarea actual coincide con la descripción de la skill.

### 1. ¿Qué podemos lograr con las Skills?

- **Definir Roles Técnicos:** Transformar al modelo en un experto de nicho (ej. "Arquitecto de AWS").
- **Integrar Herramientas:** Enseñar al agente a usar binarios de terminal como `ffmpeg` o `git`.
- **Estandarizar Formatos:** Asegurar que el output siempre siga un esquema (JSON, ISO, templates).
- **Reducir Alucinaciones:** Limitar el alcance del conocimiento a los parámetros definidos en la skill.

### 2. Anatomía de una Skill (SKILL.md)

Cada habilidad reside en una carpeta que **debe** contener un archivo `SKILL.md`. Los metadatos en el frontmatter son cruciales para que el agente sepa cuándo activarla.

> [!TIP]
> **Metadatos Clave:** El campo `description` o `trigger` es el disparador. Debe ser claro sobre *qué* hace la skill y *cuándo* debe usarse.

```markdown
---
name: nombre-de-la-skill
description: Úsalo cuando necesites [acción específica].
trigger: Palabras clave o intención del usuario.
---

# Goal
Qué debe lograr el agente.

# Steps
1. Paso técnico uno.
2. Paso técnico dos (ver `scripts/logic.ts`).

# Output Format
Usa el template en `templates/report.md`.
```

### 3. Configuración y Rutas

| Herramienta     | Alcance de Proyecto | Alcance Global      |
| :-------------- | :------------------ | :------------------ |
| **Antigravity** | `.agent/skills/`    | `~/.agents/skills/` |
| **Gemini CLI**  | `.gemini/skills/`   | `~/.gemini/skills/` |
| **Codex**       | `.agents/skills/`   | `~/.agents/skills/` |

### 4. Buenas Prácticas y Metadatos

- **Modularidad:** No crees una skill "sabelotodo". Divide la inteligencia en módulos pequeños.
- **Uso de Templates:** Define variables con `{{variable}}` en archivos dentro de una carpeta `templates/` para que el agente genere documentos consistentes.
- **Ejemplos Few-Shot:** Incluye una carpeta `examples/` con inputs y outputs esperados; es más efectivo que las instrucciones largas.
- **Metadatos de Activación:** Asegúrate de que el `trigger` no sea demasiado genérico para evitar activaciones accidentales que consuman tokens innecesariamente.

**Referencias y Documentación:**
- [Cursor: Skills Migration](https://cursor.com/help/customization/skills#how-do-i-migrate-commands-to-skills)
- [Antigravity: Skills Docs](https://antigravity.google/docs/skills)
- [Gemini CLI: Skills Getting Started](https://geminicli.com/docs/cli/tutorials/skills-getting-started/)
- [OpenCode: Skills Docs](https://opencode.ai/docs/skills/)
- [Claude: Skills Guide](https://code.claude.com/docs/en/skills)
- [Codex: Developers Skills](https://developers.openai.com/codex/skills)

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
