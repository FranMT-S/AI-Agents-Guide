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

En el ecosistema de agentes de IA, el mayor desafío técnico es la **limitación de la ventana de contexto**. A medida que una conversación progresa, el modelo consume "tokens" (palabras o fragmentos de código). Si las reglas del proyecto no están bien estructuradas, la IA comienza a "olvidar" las instrucciones iniciales, provocando alucinaciones o degradación en la calidad del código. La solución definitiva a esto es la **Memoria Persistente**.

### 1. Memoria Persistente y la Jerarquía de Contexto (Scope)

La memoria persistente permite inyectar un "manual de identidad" técnico antes de que el modelo procese el primer mensaje del usuario. Esto garantiza consistencia en el estilo de codificación, herramientas autorizadas y restricciones de seguridad.

Para optimizar el uso de tokens, los agentes modernos utilizan un sistema de **Alcance (Scope)** jerárquico:

1.  **Alcance Global (Capa de Usuario):**
    - **Ubicación:** Generalmente en el directorio home del usuario (ej. `~/.gemini/GEMINI.md` o `~/.claude/CLAUDE.md`).
    - **Propósito:** Define tu "ADN" como desarrollador. Preferencias universales como "Habla siempre en español", "Usa indentación de 2 espacios" o "No uses emojis en comentarios".
2.  **Alcance de Proyecto (Capa de Raíz):**
    - **Ubicación:** Raíz del repositorio (donde reside el archivo `.git`).
    - **Propósito:** Reglas específicas para el equipo o el repo. Estándares como "Usa React con TypeScript", "Tests obligatorios con Vitest" o "Comandos de build: `npm run build`".
3.  **Alcance de Módulo (Capa de Subdirectorio):**
    - **Ubicación:** Cualquier subcarpeta dentro del proyecto.
    - **Propósito:** Instrucciones quirúrgicas. Por ejemplo, en `/src/auth/`, una regla puede prohibir rotar llaves API sin permiso explícito, o en `/legacy/` prohibir refactorizaciones sin una tarea asignada.

---

### 2. El Estándar Emergente: AGENTS.md

Históricamente, cada herramienta tenía su propio archivo (`.cursorrules`, `GEMINI.md`, `CLAUDE.md`). Sin embargo, **`AGENTS.md` se ha consolidado como el estándar multiplataforma**. 

> [!IMPORTANT]
> **Compatibilidad:** Actualmente es soportado de forma nativa por **Codex**, **Gemini CLI**, **Claude Code** y recientemente se añadió soporte oficial en **Antigravity**. Esto permite mantener una única "fuente de verdad" para las reglas de tu proyecto que funcione en cualquier IDE o CLI.

---

### 3. Comparativa Técnica de Gestión de Contexto

| Herramienta | Archivos Soportados | Lógica de Precedencia | Capacidad de Modularización |
| :--- | :--- | :--- | :--- |
| **Cursor** | `.cursor/rules/*.mdc`, `AGENTS.md` | Los archivos `.mdc` se activan por patrones `glob` (archivos específicos). | Alta: Permite reglas granulares por tipo de archivo. |
| **Antigravity** | `GEMINI.md`, `AGENTS.md` | Combina las reglas globales con las del workspace. | Media: Permite referenciar otros archivos usando `@filename`. |
| **Gemini CLI** | `GEMINI.md`, `AGENTS.md`, `CONTEXT.md` | Escanea recursivamente hacia arriba hasta la raíz del repo. | Alta: Soporta modularización total con la sintaxis `@./path/to/rules.md`. |
| **Claude Code** | `CLAUDE.md`, `AGENTS.md` | Detecta e importa automáticamente archivos de subdirectorios. | Alta: Tiene **Auto Memory** (aprende preferencias sin editarlas manualmente). |
| **Codex CLI** | `AGENTS.md`, `AGENTS.override.md` | Concatenación por líneas en blanco; el contenido final tiene prioridad. | Baja: Se basa principalmente en la jerarquía de carpetas. |

> [!WARNING]
> **Contaminación de Contexto:** Evita definir reglas contradictorias en diferentes niveles. Si el global dice "Usa Tabs" y el proyecto dice "Usa Spaces", el modelo puede confundirse y generar código inconsistente. Prioriza siempre el archivo `AGENTS.md` en la raíz para reglas críticas del proyecto.

**Referencias y Documentación:**
- [Cursor Docs: Rules & AGENTS.md](https://cursor.com/docs/rules#agentsmd)
- [Antigravity Docs: Rules & Workflows](https://antigravity.google/docs/rules-workflows)
- [Gemini CLI: Memory Management](https://geminicli.com/docs/cli/tutorials/memory-management/)
- [Claude Code: Memory & Agents.md](https://code.claude.com/docs/en/memory#agents-md)
- [Codex CLI: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)

## Skills (Habilidades)

Las **Skills** son paquetes de **experiencia bajo demanda**. A diferencia del contexto general, las habilidades contienen instrucciones, scripts y recursos que el agente solo carga mediante **progressive disclosure** (revelación progresiva) cuando detecta que la tarea actual coincide con la descripción de la skill. Esto evita saturar la ventana de contexto con información irrelevante.

### 1. Mecanismos de Activación y Revelación Progresiva

Para optimizar el uso de tokens, los agentes siguen un patrón de "Metadata-First":
1.  **Descubrimiento:** Al iniciar la sesión, solo se inyectan los **nombres y descripciones** de las skills disponibles en el prompt del sistema.
2.  **Activación:** El contenido completo del archivo `SKILL.md` y sus archivos adjuntos solo se cargan cuando el agente llama a la herramienta `activate_skill` o cuando el usuario invoca el comando explícitamente (ej. `/skill-name`).

---

### 2. Anatomía Avanzada de una Skill (SKILL.md)

El archivo `SKILL.md` es el cerebro de la habilidad. Utiliza metadatos técnicos para controlar el comportamiento del modelo.

#### Metadatos en Frontmatter (Ejemplo Claude/Gemini)
```markdown
---
name: api-auditor
description: Experto en auditoría de seguridad para APIs REST. Actívalo para buscar vulnerabilidades OWASP.
trigger: "auditar api", "seguridad endpoint", "revisar vulnerabilidades"
allowed-tools: ["read_file", "run_shell_command", "grep_search"]
context: fork
---
```
- **`allowed-tools` (Claude):** Restringe al agente a usar solo ciertas herramientas mientras la skill está activa (Principio de Menor Privilegio).
- **`context: fork`:** Ejecuta la skill en un subagente aislado para no contaminar el historial principal.

---

### 3. Ejemplos Prácticos de Implementación

#### Ejemplo A: Skill + Scripts (Ejecución de lógica compleja)
Ideal cuando la skill necesita procesar datos antes de dar una respuesta.

**Estructura:**
```text
skills/video-tool/
├── SKILL.md
└── scripts/
    └── optimizer.js
```

**Instrucción en `SKILL.md`:**
> [!NOTE]
> Eres un experto en optimización de video. Para procesar archivos, debes ejecutar el script bundleado: `node $SKILL_DIR/scripts/optimizer.js <input>`.

#### Ejemplo B: Skill + Templates (Generación de documentos estructurados)
Ideal para reportes técnicos, PR summaries o documentación de arquitectura.

**Estructura:**
```text
skills/arch-doc/
├── SKILL.md
└── templates/
    └── design-record.md
```

**Instrucción en `SKILL.md`:**
> [!TIP]
> Al documentar una decisión de arquitectura, usa SIEMPRE el formato de `templates/design-record.md`. Rellena cada campo marcado con `{{placeholder}}`.

---

### 4. Configuración y Rutas Globales

| Herramienta | Alcance Proyecto | Alcance Global | Comando de Gestión |
| :--- | :--- | :--- | :--- |
| **Cursor** | `.cursor/rules/*.mdc` | Settings > Rules | `/migrate-to-skills` |
| **Antigravity** | `.agent/skills/` | `~/.agents/skills/` | Automático por trigger |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` | `gemini skills list` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | `/skills` |
| **Codex** | `.agents/skills/` | `~/.agents/skills/` | Automático por triggers |

### 5. Seguridad y Aislamiento (Sandboxing)

- **Permisos de Archivos:** En **Gemini CLI**, al activar una skill, el usuario recibe una solicitud de aprobación para que el agente pueda leer los archivos *dentro* de la carpeta de esa skill específica.
- **Variables de Entorno:** Puedes usar variables como `$SKILL_DIR` para referenciar scripts locales sin importar la ruta actual del proyecto.
- **Invocación Implícita vs Explícita:** Para tareas críticas (como despliegues a producción), se recomienda configurar `allow_implicit_invocation: false` (Codex) o `disable-model-invocation: true` (Claude) para que solo el usuario pueda disparar la acción manualmente.

**Referencias y Documentación:**
- [Cursor: Skills Migration](https://cursor.com/help/customization/skills#how-do-i-migrate-commands-to-skills)
- [Antigravity: Skills Docs](https://antigravity.google/docs/skills)
- [Gemini CLI: Skills Getting Started](https://geminicli.com/docs/cli/tutorials/skills-getting-started/)
- [OpenCode: Skills Docs](https://opencode.ai/docs/skills/)
- [Claude: Skills Guide](https://code.claude.com/docs/en/skills)
- [Codex: Developers Skills](https://developers.openai.com/codex/skills)

## MCP (Model Context Protocol)

El **Model Context Protocol (MCP)** es el estándar de comunicación que permite a los modelos de IA interactuar con el mundo real. Actúa como un puente entre la lógica del LLM y herramientas externas (bases de datos, APIs, navegadores).

### 1. Arquitectura y Componentes

- **MCP Client:** El agente (Cursor, Gemini CLI, etc.) que consume las herramientas.
- **MCP Server:** El servidor que expone las funcionalidades.
- **Tools (Herramientas):** Funciones que el modelo puede "llamar" (ej. `read_github_repo`).
- **Resources (Recursos):** Datos estáticos o dinámicos que el modelo puede leer (ej. logs en tiempo real).

> [!WARNING]
> **Sandboxing y Seguridad:** Al usar servidores MCP, el agente obtiene permisos para ejecutar acciones en tu nombre. Siempre revisa el código fuente de los servidores de terceros y utiliza tokens con permisos mínimos (Principio de Menor Privilegio).

---

### 2. Configuración y Gestión de Herramientas

Cada agente permite habilitar o deshabilitar herramientas específicas para evitar la degradación del contexto.

| Agente | Archivo de Configuración | Clave de Exclusión |
| :--- | :--- | :--- |
| **Cursor** | `~/.cursor/mcp.json` | N/A (Manual en UI) |
| **Antigravity** | `mcp_config.json` | `"disabledTools": []` |
| **Gemini CLI** | `settings.json` | `"excludeTools": []` |
| **Claude Code** | `settings.json` | `hooks: PreToolUse` |

---

### 3. Deep Dive: GitHub MCP y Docker Optimization

Muchos servidores MCP se distribuyen como imágenes de Docker. El error común es levantar una instancia nueva por cada sesión, lo que consume memoria y CPU excesivamente.

#### Optimización con `docker exec`
En lugar de usar `--rm` y `run` (que crea y destruye contenedores), es más eficiente mantener un contenedor persistente y conectarse vía `exec`.

**Comando para el servidor:**
```bash
docker run -d -i --name github-mcp -e GITHUB_PERSONAL_ACCESS_TOKEN=xxx ghcr.io/github/github-mcp-server
```

**Configuración en `settings.json`:**
```json
"github-mcp-server": {
  "command": "docker",
  "args": ["exec", "-i", "github-mcp", "/server/github-mcp-server", "stdio"]
}
```

---

### 4. Solución de Problemas Comunes

- **Reseteo de Oauth (ClickUp/Figma):** Si la autenticación se corrompe, elimina la carpeta de sesión del MCP. En Antigravity/Gemini suele estar en `~/.mcp-auth`.
- **Errores de Stdio:** Asegúrate de que el servidor MCP no imprima nada a `stdout` que no sea JSON válido. Usa `stderr` para depuración.
- **Timeout:** Servidores lentos pueden causar que el agente aborte la tarea. Ajusta los límites de tiempo en la configuración del cliente si el agente lo permite.

**Referencias y Documentación:**
- [Cursor: MCP Overview](https://cursor.com/docs/mcp)
- [Antigravity: MCP Docs](https://antigravity.google/docs/mcp)
- [Gemini CLI: MCP Server Setup](https://geminicli.com/docs/tools/mcp-server/)
- [OpenCode: Servidores MCP (ES)](https://opencode.ai/docs/es/mcp-servers/)
- [Claude Code: MCP Guide](https://code.claude.com/docs/en/mcp)
- [Codex CLI: MCP Developers](https://developers.openai.com/codex/mcp)
- [GitHub MCP Server Repo](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- [ClickUp MCP Server Docs](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server-1)

## Plugins y Extensiones

Las extensiones permiten añadir funcionalidades específicas a los agentes, como integración con bases de datos, APIs de terceros o capacidades de renderizado.

- **Cursor:** Soporta extensiones de VSCode y plugins específicos de IA.
- **Gemini CLI:** Utiliza un ecosistema de extensiones instalables vía URL de GitHub.
- **Claude Code:** Se expande mediante herramientas y hooks configurables.

**Referencias y Documentación:**
- [Cursor: Plugins](https://cursor.com/docs/plugins)
- [Gemini CLI: Extensions Guide](https://geminicli.com/docs/extensions/)
- [OpenCode: Ecosystem (ES)](https://opencode.ai/docs/es/ecosystem/)
- [Claude Code: Discover Plugins](https://code.claude.com/docs/en/discover-plugins)

## Hooks (Disparadores)

Los **Hooks** son scripts deterministas que se ejecutan automáticamente en respuesta a eventos del ciclo de vida del agente. A diferencia del contexto, los hooks son garantías de ejecución.

### Eventos Comunes

| Evento | Cuándo se dispara | Uso Típico |
| :--- | :--- | :--- |
| **PreToolUse** | Antes de ejecutar una herramienta | Validaciones de seguridad, guardrails. |
| **PostToolUse** | Después de que una herramienta completa | Formateo de código (Prettier), tests. |
| **BeforeSession** | Al iniciar la sesión | Carga de variables de entorno. |

> [!IMPORTANT]
> Los hooks deben ser scripts rápidos. Si un hook falla (por ejemplo, con un `exit 2` en Claude Code), puede bloquear la acción del agente para proteger la integridad del sistema.

**Referencias y Documentación:**
- [Cursor Docs: Hooks](https://cursor.com/docs/hooks)
- [Gemini CLI: Hooks Reference](https://geminicli.com/docs/hooks/reference/)
- [Claude Code: Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Codex CLI: Hooks](https://developers.openai.com/codex/hooks)

## Subagentes

Un **Subagente** es un agente especializado con su propio contexto aislado y **expertise** definida que el agente principal puede invocar para delegar tareas complejas.

### ¿Cuándo usar un Subagente?

- **Delegación de Expertise:** Cuando necesitas un especialista (ej. un experto en seguridad para auditar código).
- **Aislamiento de Contexto:** Para evitar que la ventana de contexto del agente principal se sature con detalles irrelevantes de una sub-tarea.
- **Tareas Paralelas:** Equipos de agentes trabajando en diferentes módulos simultáneamente.

> [!NOTE]
> En herramientas como **Gemini CLI**, los subagentes se definen en la carpeta `.gemini/agents/` mediante archivos `.md` que describen sus herramientas y rol.

**Referencias y Documentación:**
- [Cursor Docs: Subagents](https://cursor.com/docs/subagents)
- [Gemini CLI: Subagents Tutorial](https://geminicli.com/docs/core/subagents/)
- [OpenCode: Agents (ES)](https://opencode.ai/docs/es/agents/)
- [Claude Code: Sub-agents & Teams](https://code.claude.com/docs/en/sub-agents)
- [Codex CLI: Subagents Guide](https://developers.openai.com/codex/subagents)

## Automatización y Scripting
Placeholder: Headless mode y automatización de flujos.

## Evaluación de Modelos
Placeholder: Comparativa entre Gemini, Claude y GPT.

---
*Nota: Todos los términos técnicos y fragmentos de código se mantienen en inglés para mayor precisión técnica.*
