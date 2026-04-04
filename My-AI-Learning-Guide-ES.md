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
> **Compatibilidad:** Actualmente es soportado de forma nativa por **Codex**, **Gemini CLI**, **Claude Code**, **OpenCode** y recientemente se añadió soporte oficial en **Antigravity**. Esto permite mantener una única "fuente de verdad" para las reglas de tu proyecto que funcione en cualquier IDE o CLI.

---

### 3. Comparativa Técnica de Gestión de Contexto

| Herramienta | Archivos Soportados | Lógica de Precedencia | Capacidad de Modularización |
| :--- | :--- | :--- | :--- |
| **Cursor** | `.cursor/rules/*.mdc`, `AGENTS.md` | Los archivos `.mdc` se activan por patrones `glob` (archivos específicos). | Alta: Permite reglas granulares por tipo de archivo. |
| **Antigravity** | `GEMINI.md`, `AGENTS.md` | Combina las reglas globales con las del workspace. | Media: Permite referenciar otros archivos usando `@filename`. |
| **Gemini CLI** | `GEMINI.md`, `AGENTS.md`, `CONTEXT.md` | Escanea recursivamente hacia arriba hasta la raíz del repo. | Alta: Soporta modularización total con la sintaxis `@./path/to/rules.md`. |
| **Claude Code** | `CLAUDE.md`, `AGENTS.md` | Detecta e importa automáticamente archivos de subdirectorios. | Alta: Tiene **Auto Memory** (aprende preferencias sin editarlas manualmente). |
| **Codex CLI** | `AGENTS.md`, `AGENTS.override.md` | Concatenación por líneas en blanco; el contenido final tiene prioridad. | Baja: Se basa principalmente en la jerarquía de carpetas. |
| **OpenCode** | `AGENTS.md`, `opencode.json` | Comienza por la configuración global y luego la del proyecto. | Alta: Soporta **Lazy Loading** referenciando `@archivos` e inicialización automática. |

> [!WARNING]
> **Contaminación de Contexto:** Evita definir reglas contradictorias en diferentes niveles. Si el global dice "Usa Tabs" y el proyecto dice "Usa Spaces", el modelo puede confundirse y generar código inconsistente. Prioriza siempre el archivo `AGENTS.md` en la raíz para reglas críticas del proyecto.

> [!NOTE]
> Para conocer aspectos únicos y configuraciones avanzadas de cada herramienta, consulta su archivo específico: [Cursor](./cursor.md) | [Antigravity](./antigravity.md) | [Gemini CLI](./gemini-cli.md) | [OpenCode](./openCode.md) | [Claude Code](./claude-code.md) | [Codex CLI](./codex-cli.md).

**Referencias y Documentación Oficial:**
- [Cursor: Rules](https://cursor.com/docs/rules)
- [Antigravity: Rules & Workflows](https://antigravity.google/docs/rules-workflows)
- [Gemini CLI: Memory Management](https://geminicli.com/docs/cli/tutorials/memory-management/)
- [OpenCode: Rules](https://opencode.ai/docs/rules/)
- [Claude: Memory & Agents.md](https://code.claude.com/docs/en/memory#agents-md)
- [Codex: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)

## Skills (Habilidades)

Las **Skills** son paquetes de **experiencia bajo demanda**. A diferencia del contexto general (`AGENTS.md`) que siempre está activo, las habilidades contienen instrucciones, scripts auxiliares, plantillas (templates) y recursos que el agente solo carga mediante **progressive disclosure** (revelación progresiva). 

¿Qué significa esto? El agente solo inyectará esta información en su contexto cuando detecte que la tarea actual coincide con la descripción de la skill. Esto evita saturar la memoria con información irrelevante y permite dotar al agente de roles técnicos muy específicos.

### 1. Consejos: Cómo Construir Skills Correctamente

Para que una skill sea efectiva, debe estar diseñada con precisión:
- **Un solo propósito:** Una skill debe resolver un solo problema (ej. "Revisar código de Python", no "Revisar código y hacer despliegues").
- **Metadata clara:** El agente decide usar la skill basándose *exclusivamente* en la descripción y los "triggers" (disparadores). Si son vagos, el agente nunca la usará o la usará mal.
- **Usa el principio de Caja Negra (Black-Box):** Si necesitas procesar datos complejos, no le pidas al agente que escriba un script al vuelo. Crea un script en Python o Node, guárdalo dentro de la carpeta de la skill, y dile al agente: *"Ejecuta este script y usa el resultado"*.

---

### 2. Metadatos de una Skill (Frontmatter en `SKILL.md`)

El archivo `SKILL.md` es el cerebro de la habilidad. Utiliza un bloque de metadatos (YAML frontmatter) en la parte superior para controlar el comportamiento y descubrimiento del modelo. 

Aquí tienes un **desglose exhaustivo** de los metadatos disponibles (combinando estándares de Claude, OpenCode, Codex y Gemini):

- `name` *(Requerido)*: Identificador único. Debe ser corto, en minúsculas y sin espacios (ej. `api-auditor`).
- `description` *(Requerido)*: Explicación detallada de lo que hace la skill. Es la señal principal que usa la IA para decidir si debe activarla.
- `trigger`: Palabras clave o frases exactas que le dicen al agente cuándo activarla (ej. `"auditar api"`, `"seguridad endpoint"`).
- `allowed-tools` (Claude): Lista estricta de herramientas permitidas mientras la skill está activa (ej. `["read_file", "run_shell_command"]`). Bloquea el resto por seguridad.
- `context` (Claude): Puede configurarse como `fork` para aislar la ejecución de la skill en un subagente, protegiendo la memoria principal de logs basura.
- `dependencies` (Codex): Servidores MCP que deben estar activos obligatoriamente para poder usar la skill (ej. `["github-mcp"]`).
- `metadata` (OpenCode): Diccionario libre para atributos personalizados (ej. `metadata: { "audience": "maintainers", "tier": "backend" }`).
- `disable-model-invocation` / `allow_implicit_invocation`: Si se configuran, la IA no puede invocar la skill por su cuenta; el usuario debe pedirlo explícitamente con un comando (ej. `/auditar`).

**Ejemplo completo de Frontmatter Avanzado:**
```yaml
---
name: auditor-seguridad
description: Experto en auditoría de seguridad para APIs REST. Actívalo para buscar vulnerabilidades OWASP.
trigger: "auditar api", "seguridad endpoint", "revisar vulnerabilidades"
allowed-tools: ["read_file", "run_shell_command"]
context: fork
dependencies: ["github-mcp"]
allow_implicit_invocation: false
---
```

---

### 3. Árbol de Ejemplos: Estructuras y Templates

Una de las mejores prácticas es tener una carpeta de referencia (como `template/skills/`) en tu proyecto para estandarizar la creación de skills. A continuación, mostramos cómo se ve un árbol de directorios avanzado con múltiples tipos de skills:

```text
📁 mi-proyecto/
├── 📁 .agents/                 (O .gemini/ o .claude/)
│   └── 📁 skills/
│       ├── 📁 python-reviewer/ (Skill Simple)
│       │   └── 📄 SKILL.md
│       │
│       ├── 📁 video-optimizer/ (Skill + Scripts)
│       │   ├── 📄 SKILL.md
│       │   └── 📁 scripts/
│       │       ├── 📄 optimizer.js
│       │       └── 📄 validate.py
│       │
│       └── 📁 tech-reporter/   (Skill + Templates)
│           ├── 📄 SKILL.md
│           └── 📁 templates/
│               └── 📄 design-record.md
│
└── 📁 template/                (Carpeta de plantillas generadas para ti)
    └── 📁 skills/
        ├── 📄 basic-skill.md
        ├── 📄 skill-with-scripts.md
        └── 📄 skill-with-templates.md
```

#### Ejemplo Interno A: Skill + Scripts (Lógica Compleja)
Ideal cuando la skill necesita procesar datos antes de dar una respuesta.
**Instrucción Clave dentro de `video-optimizer/SKILL.md`:**
> [!NOTE]
> Para optimizar archivos de video, debes ejecutar el script adjunto: `node $SKILL_DIR/scripts/optimizer.js <input>`. No intentes escribir el comando `ffmpeg` tú mismo. Analiza el `stdout` del script para dar la respuesta final.

#### Ejemplo Interno B: Skill + Templates (Generación de Documentos)
Ideal para asegurar que el agente siempre responda con un formato estandarizado.

**Contenido del archivo `templates/design-record.md`:**
```markdown
# Reporte de Arquitectura: {{title}}
**Fecha:** {{date}}
**Autor:** AI Agent

## Hallazgos
{{findings}}
```

**Instrucción Clave dentro de `tech-reporter/SKILL.md`:**
> [!TIP]
> Al generar el reporte, debes leer obligatoriamente el archivo `$SKILL_DIR/templates/design-record.md`. Copia su estructura exacta y rellena las variables `{{title}}`, `{{date}}` y `{{findings}}`. Nunca inventes un formato nuevo.

---

### 4. Mejores Prácticas y Reglas Oficiales (AgentSkills.io)

Basado en la especificación oficial de AgentSkills, aquí tienes las reglas de oro para crear skills robustas:

#### Optimización de Descripciones (Triggers)
La descripción es el **único** mecanismo para que el agente descubra la skill.
- ✅ **Fraseo Imperativo:** Usa `"Úsalo cuando..."` o `"Usa esta skill para..."` en lugar de descripciones pasivas como `"Esta skill hace..."`.
- ✅ **Enfoque en la Intención:** Describe qué quiere lograr el usuario, no los mecanismos internos.
- ✅ **Sé Asertivo ("Pushy"):** Lista contextos explícitos incluso si el usuario no usa palabras clave exactas (ej. *"incluso si no mencionan la palabra CSV"*).
- ❌ **Triggers Genéricos:** Evita `"ayuda"`, `"código"` o `"revisar"`. Usa Evals (ver abajo) para crear un ratio 60/40 de queries que *deben* activarlo vs queries que *no deben* activarlo (near-misses).

#### Creación de Instrucciones (SKILL.md)
- **"Añade lo que el agente no sabe, omite lo que ya sabe":** No le enseñes cómo funciona HTTP. Enfócate en las convenciones únicas de tu proyecto.
- **Gotchas y Checklists:** Usa listas explícitas para hechos que el modelo suele ignorar (ej. *"La tabla users usa soft deletes, NUNCA hagas DELETE FROM"*). Para procesos largos, obliga al agente a seguir un checklist paso a paso.
- **Loops de Validación:** Instruye al agente a ejecutar un script de test/linting y arreglar los errores en un bucle hasta que pase (ej. `Plan-Validate-Execute`).

#### Uso de Scripts en Skills
- **Dependencias al vuelo:** Usa `uvx`, `npx` o `bunx` para ejecutar scripts sin necesidad de instalaciones manuales previas (ej. `npx eslint@9`).
- **Scripts Autocontenidos:** Para Python, usa la sintaxis PEP 723 (`# /// script`) para incrustar las dependencias dentro del mismo archivo.
- **Diseño para Agentes:** Los scripts **NO deben ser interactivos** (nada de prompts tipo "Presiona Y para continuar"). Deben emitir mensajes de error muy claros explicando al agente cómo solucionarlo y usar salidas estructuradas (JSON/CSV) preferiblemente.

#### Evaluación de Calidad (Evals)
Nunca lances una skill sin probarla. Usa herramientas de evaluación para medir el **Delta** (lo que cuesta ejecutar la skill en tokens/tiempo vs lo que aporta).
- **Test Cases:** Deben incluir el Prompt, Output Esperado y Archivos de Entrada.
- **Aserciones Verificables:** No uses métricas vagas como *"El output es bueno"*. Usa aserciones medibles como *"El archivo final es un JSON válido"*.
- **Rastreo:** Revisa las transcripciones de ejecución para entender *por qué* el agente ignoró una regla y ajusta el `SKILL.md` en consecuencia.

---

### 5. Configuración y Rutas Globales (Scopes)

| Herramienta | Alcance Proyecto | Alcance Global | Comando de Gestión |
| :--- | :--- | :--- | :--- |
| **Cursor** | `.cursor/rules/*.mdc` | Settings > Rules | `/migrate-to-skills` |
| **Antigravity** | `.agent/skills/` | `~/.agents/skills/` | Automático por trigger |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` | `gemini skills list` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | `/skills` |
| **Codex** | `.agents/skills/` | `~/.agents/skills/` | Automático por triggers |
| **OpenCode** | `.opencode/skills/` | `~/.config/opencode/skills/` | Automático por triggers |

> [!NOTE]
> Para conocer metadatos específicos, control de permisos y características avanzadas de las skills en cada herramienta, consulta su archivo específico: [Cursor](./cursor.md) | [Antigravity](./antigravity.md) | [Gemini CLI](./gemini-cli.md) | [OpenCode](./openCode.md) | [Claude Code](./claude-code.md) | [Codex CLI](./codex-cli.md).

### 6. Seguridad y Aislamiento (Sandboxing)

- **Permisos de Archivos:** En **Gemini CLI**, al activar una skill, el usuario recibe una solicitud de aprobación para que el agente pueda leer los archivos *dentro* de la carpeta de esa skill específica.
- **Variables de Entorno:** Puedes usar variables como `$SKILL_DIR` (o `${CLAUDE_SKILL_DIR}`) para referenciar scripts locales sin importar la ruta actual del proyecto.
- **Invocación Implícita vs Explícita:** Para tareas críticas (como despliegues a producción), se recomienda configurar `allow_implicit_invocation: false` (Codex) o `disable-model-invocation: true` (Claude) para que solo el usuario pueda disparar la acción manualmente.

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

### 2. Tabla Comparativa de Configuración MCP

Cada agente permite habilitar o deshabilitar herramientas específicas para evitar la degradación del contexto.

| Agente | Archivo de Configuración | Clave de Exclusión |
| :--- | :--- | :--- |
| **Cursor** | `~/.cursor/mcp.json` | N/A (Manual en UI) |
| **Antigravity** | `mcp_config.json` | `"disabledTools": []` |
| **Gemini CLI** | `settings.json` | `"excludeTools": []` |
| **Claude Code** | `settings.json` | `hooks: PreToolUse` |
| **Codex CLI** | `config.toml` | `disabled_tools` |
| **OpenCode** | `opencode.json` | `"tools": {"*": false}` |

> [!NOTE]
> Para conocer metadatos específicos, características únicas (como MCP Apps, Auth OAuth) y optimización de Docker por cada herramienta, consulta su archivo específico: [Cursor](./cursor.md) | [Antigravity](./antigravity.md) | [Gemini CLI](./gemini-cli.md) | [OpenCode](./openCode.md) | [Claude Code](./claude-code.md) | [Codex CLI](./codex-cli.md).

## Plugins y Extensiones

Las extensiones permiten añadir funcionalidades específicas a los agentes, como integración con bases de datos, APIs de terceros o capacidades de renderizado.

### 1. Tabla Comparativa de Ecosistemas

| Agente | Arquitectura | Directorio/Comando |
| :--- | :--- | :--- |
| **Cursor** | Bundles con reglas, skills, MCP | `cursor.com/marketplace` |
| **Gemini CLI** | `gemini-extension.json` | `gemini extensions install` |
| **Claude Code** | `.claude-plugin/plugin.json` | `/plugin install` |
| **OpenCode** | Módulos JS/TS (Bun) | `.opencode/plugins/` |

> [!NOTE]
> Para detalles sobre desarrollo, eventos y arquitecturas de plugins específicos por herramienta, consulta su archivo específico: [Cursor](./cursor.md) | [Antigravity](./antigravity.md) | [Gemini CLI](./gemini-cli.md) | [OpenCode](./openCode.md) | [Claude Code](./claude-code.md) | [Codex CLI](./codex-cli.md).

**Referencias y Documentación Oficial:**
- [Cursor: Plugins](https://cursor.com/docs/plugins)
- [Gemini CLI: Extensions Guide](https://geminicli.com/docs/extensions/) | [Writing](https://geminicli.com/docs/extensions/writing-extensions/) | [Best Practices](https://geminicli.com/docs/extensions/best-practices/) | [Reference](https://geminicli.com/docs/extensions/reference/)
- [OpenCode: Plugins](https://opencode.ai/docs/es/plugins/) | [Ecosystem](https://opencode.ai/docs/es/ecosystem/)
- [Claude: Discover Plugins](https://code.claude.com/docs/en/discover-plugins) | [Plugins Guide](https://code.claude.com/docs/en/plugins)

## Hooks (Disparadores)

Los **Hooks** son la capa de ejecución determinista de los agentes. A diferencia de las reglas en `AGENTS.md`, que son sugerencias para el LLM, los hooks son scripts del sistema que **siempre se ejecutan** ante eventos específicos del ciclo de vida.

### 1. Protocolos de Comunicación (Gemini CLI)

En **Gemini CLI**, los hooks se comunican con el agente principal mediante un protocolo estricto de **stdin/stdout** utilizando JSON.

> [!IMPORTANT]
> Cualquier texto enviado a `stdout` que no sea un JSON válido provocará un error de parseo. Para logs de depuración, utiliza siempre `stderr`.

**Ejemplo de flujo:**
1. El agente dispara el evento `BeforeTool`.
2. El hook recibe el contexto de la herramienta por `stdin`.
3. El hook valida y devuelve un JSON por `stdout` para permitir o modificar la acción.

### 2. Bloqueo de Acciones (Claude Code)

En **Claude Code**, un hook puede abortar una operación si detecta una violación de seguridad o estilo.
- **Acción:** El script debe salir con un código de salida `exit 2`.
- **Feedback:** El mensaje de error escrito en `stderr` se mostrará directamente al usuario y al modelo.

---

## Subagentes

Un **Subagente** no es solo un prompt diferente; es una instancia del modelo con un contexto **aislado** y un conjunto de herramientas limitado para una tarea específica.

### 1. Arquitectura de "Agent Teams"

Para proyectos complejos, herramientas como **Claude Code** permiten crear equipos de agentes que trabajan en paralelo:
- **Agente Planificador:** Diseña la estrategia sin tocar código.
- **Agente Programador:** Implementa cambios quirúrgicos basados en el plan.
- **Agente de QA:** Ejecuta tests y audita la calidad sin acceso a las herramientas de escritura.

### 2. Ventajas del Aislamiento
- **Protección de Contexto:** Evita que el historial de chat se llene de logs de tests o búsquedas repetitivas de archivos.
- **Especialización:** Permite definir un **expertise** único (ej. "Eres un experto en Rust") que no afecte el comportamiento del agente principal en otras áreas del proyecto.

---

## Automatización y Scripting

El modo **Headless** (sin interfaz) permite integrar agentes en flujos de CI/CD, tareas programadas o scripts donde no hay un usuario humano para interactuar con la terminal.

### 1. Tabla Comparativa de Automatización

Ejecutar un agente de forma programática requiere comandos y flags específicos para evitar solicitudes de aprobación constantes y estructurar la salida (ej. a JSON).

| Agente | Comando Principal | Enfoque Principal |
| :--- | :--- | :--- |
| **Gemini CLI** | `gemini -p "query"` | Retorna texto o JSON estructurado para scripts. Usa la herramienta nativa en entornos no TTY. |
| **Claude Code** | `claude -p "prompt"` | Soporta `Agent SDK` y ejecución mediante `--bare` para aislar contextos en CI. |
| **Codex CLI** | `codex exec "prompt"` | Ejecución robusta en pipelines con `--full-auto` y validación de schemas JSON. |

> [!WARNING]
> El modo automatizado debe usarse con extrema precaución. Asegúrate de tener guardrails definidos en los **Hooks** o usar modos de *sandboxing* estrictos (como `--sandbox` en Codex o `--allowedTools` en Claude) para evitar que el agente ejecute comandos destructivos sin supervisión.

> [!NOTE]
> Para detalles sobre códigos de salida, comandos específicos, formatos JSON y tareas programadas (CRON), consulta el archivo específico de cada herramienta: [Gemini CLI](./gemini-cli.md) | [Claude Code](./claude-code.md) | [Codex CLI](./codex-cli.md).

**Referencias y Documentación Oficial:**
- [Gemini CLI: Headless Tutorial](https://geminicli.com/docs/cli/headless/)
- [Claude: Headless Mode](https://code.claude.com/docs/en/headless) | [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)
- [Codex: Non-interactive Usage](https://developers.openai.com/codex/noninteractive)

## Evaluación de Modelos

En el ecosistema actual, no existe un modelo único para todas las tareas. La arquitectura de los agentes requiere el uso de diferentes modelos según el volumen de datos, la complejidad del razonamiento o la velocidad necesaria.

A continuación, se categorizan los modelos principales por su idoneidad en tareas específicas:

### 1. Modelos de Razonamiento Profundo y Arquitectura (Los Pesos Pesados)
Diseñados para generación de código complejo, entender el contexto de código a gran escala y orquestar MCPs con instrucciones ambiguas.

#### Gemini 3.1 PRO / Gemini 3.0 Pro
- **Análisis multi-repo:** Excelente para la ingesta masiva de contexto (ventana de 1M-10M tokens).
- **Entender contexto a gran escala:** Imbatible para encontrar dependencias ocultas (RAG interno).
- **Evitar en:** Generación de JSON simples o consultas aisladas de API, debido al mayor tiempo de inferencia comparado con modelos más pequeños.

#### Claude Opus 4.6
- **Tareas de arquitectura:** Superior en diseño de sistemas y razonamiento lógico profundo.
- **Generar documentación:** Destaca redactando manuales técnicos extensos y estructurados.
- **Evitar en:** Lectura rápida de archivos o ejecución de comandos repetitivos.

#### GPT-5.3 Codex
- **Ejecución en Terminal:** Excelente para comandos autónomos y refactorización masiva (generación de código puro).
- **Consultar MCPs avanzados:** Muy efectivo integrando recursos MCP que requieran acciones de escritura y scripts.
- **Evitar en:** Tareas puramente semánticas o generación de informes largos de negocio.

### 2. Modelos de Flujo de Trabajo Diario (El Equilibrio)
Optimizados para desarrollo interactivo, generación de código del día a día y consultar APIs.

#### Claude Sonnet 4.6
- **Refactorización de UI/Frontend:** Gran precisión para el trabajo iterativo de código.
- **Consultar APIs y MCPs:** Organiza lógicamente las peticiones gracias a su *Adaptive Thinking*.
- **Leer Skills:** Excelente capacidad de aplicar directivas y plantillas de forma estricta.
- **Evitar en:** Ingesta de bases de código completas de millones de líneas.

#### GPT-4o
- **Generación de código:** Sólido rendimiento de uso general y multimodalidad.
- **Generar estructuras como JSON:** Muy predecible y consistente para el manejo de esquemas y datos.
- **Evitar en:** Proyectos masivos que superen su ventana de contexto estándar sin el uso de compactación de historial.

### 3. Modelos Rápidos y de Soporte (Los Especialistas)
Pensados para lectura de archivos, resúmenes rápidos, consultar MCP (solo lectura) y extracción de datos.

#### Gemini 3.1 Flash / Gemini 3.0 Flash
- **Lectura de archivos:** Procesamiento a altísima velocidad de grandes volúmenes de texto.
- **Generación de informes:** Eficiente extrayendo datos rápidamente (tareas de aguja en el pajar).
- **Evitar en:** Generación de código arquitectónico complejo o resolución de bugs lógicos difíciles.

#### Claude Haiku 4.6
- **Consultar MCP:** Ideal para obtener contexto veloz y ligero.
- **Análisis de logs:** Extracción rápida de JSON y resúmenes a partir de texto plano o consola.
- **Evitar en:** Tareas que requieran mantener un contexto de código enorme o generar scripts desde cero.

---

### Tabla Comparativa de Idoneidad

La siguiente tabla resume qué tan adecuado es cada modelo para diferentes tareas técnicas.

| Categoría Técnica | Gemini Pro | Claude Opus | GPT Codex | Claude Sonnet | GPT-4o | Gemini Flash | Claude Haiku |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Generación de código** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Lectura de archivos** | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ |
| **Generación de informes** | ✅ | ✅ | ❌ | ⚠️ | ⚠️ | ✅ | ⚠️ |
| **Generar documentación** | ⚠️ | ✅ | ❌ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| **Generar JSON / Estructuras** | ❌ | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ | ⚠️ |
| **Consultar APIs** | ⚠️ | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| **Consultar MCP** | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| **Leer skills** | ⚠️ | ✅ | ⚠️ | ✅ | ⚠️ | ❌ | ⚠️ |
| **Entender contexto de código** | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ❌ |

**Leyenda:**
- ✅ **Recomendado:** El modelo sobresale, es rápido o está diseñado específicamente para esta tarea.
- ⚠️ **Posible:** Funciona, pero existen opciones mejores, más eficientes en tokens o más rápidas.
- ❌ **Evitar:** No usar. Puede fallar, ser muy costoso o tener una latencia que no justifica la tarea.

---
*Nota: Todos los términos técnicos y fragmentos de código se mantienen en inglés para mayor precisión técnica.*
 