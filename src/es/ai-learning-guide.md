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

En el ecosistema de agentes de IA, el mayor desafío técnico es la **limitación de la ventana de contexto**. A medida que una conversación progresa, el modelo (como Claude 4.5 Haiku o GPT-5.4) consume "tokens" (palabras o fragmentos de código). Si las reglas del proyecto no están bien estructuradas, la IA comienza a "olvidar" las instrucciones iniciales, provocando alucinaciones o degradación en la calidad del código. La solución definitiva a esto es la **Memoria Persistente mediante `AGENTS.md`**.

---

### El Estándar: AGENTS.md

`AGENTS.md` es el estándar multiplataforma para guiar agentes de IA en un repositorio. Piensa en él como un `README` para el agente: un lugar predecible y dedicado que se inyecta automáticamente al inicio de cada sesión, antes de cualquier mensaje del usuario.

> [!IMPORTANT]
> **Compatibilidad multiplataforma:** Es soportado nativamente por **Codex**, **Gemini CLI**, **Claude Code** (como `CLAUDE.md`), **GitHub Copilot**, **OpenCode**, **Cursor** y **Antigravity**. Una sola fuente de verdad para todas las herramientas.

| Herramienta       | Archivo nativo       | Soporta `AGENTS.md` |
| :---------------- | :------------------- | :------------------ |
| **Codex CLI**     | `AGENTS.md`          | ✅ Nativo            |
| **Gemini CLI**    | `GEMINI.md`          | ✅ Sí                |
| **Claude Code**   | `CLAUDE.md`          | ✅ Sí (alias)        |
| **GitHub Copilot**| `copilot-instructions.md` | ✅ Sí           |
| **OpenCode**      | `AGENTS.md`          | ✅ Nativo            |
| **Cursor**        | `.cursor/rules/`     | ✅ Sí                |
| **Antigravity**   | `AGENTS.md`          | ✅ Nativo            |

> [!TIP]
> Para compatibilidad total, crea `AGENTS.md` en la raíz y crea un symlink: `ln -s AGENTS.md CLAUDE.md`. Esto garantiza que Claude Code y todas las demás herramientas lo lean sin duplicar contenido.

---

### Jerarquía de Alcance (Scope)

Los agentes aplican una jerarquía de tres niveles. Las instrucciones más específicas (subdirectorio) tienen prioridad sobre las más generales (global).

```text
~/.gemini/GEMINI.md          (Global — preferencias universales del usuario)
mi-proyecto/
├── AGENTS.md                (Proyecto — estándares del equipo y repositorio)
├── src/
│   └── auth/
│       └── AGENTS.md        (Módulo — instrucciones quirúrgicas para este modulo)
└── legacy/
    └── AGENTS.override.md   (Override — reemplaza TODAS las instrucciones padre, solo Codex)
```

| Nivel      | Alcance         | Propósito                                      |
| :--------- | :-------------- | :--------------------------------------------- |
| Global     | Usuario         | Idioma, estilo base, preferencias universales  |
| Proyecto   | Repositorio     | Stack, comandos, arquitectura, convenciones    |
| Módulo     | Subdirectorio   | Reglas específicas de un paquete o servicio    |
| Override   | Reemplazo total | Monorepos con convenciones radicalmente distintas (solo Codex) |

---

### El Presupuesto de Instrucciones

> [!WARNING]
> **Límite real de instrucciones:** Los LLMs de frontera pueden seguir ~150–200 instrucciones con consistencia razonable. Los modelos no-thinking siguen menos. El system prompt de Claude Code ya consume ~50 instrucciones antes de leer tu `AGENTS.md`. Cada instrucción que añades reduce la fiabilidad de *todas* las demás.

**Consecuencias directas:**
- Un archivo largo no hace que el agente ignore las instrucciones del final: las ignora de forma *uniforme* en todo el archivo.
- La documentación de rutas de archivos (`src/auth/handlers.ts`) se vuelve obsoleta cada vez que refactorizas. Prefiere describir *capacidades*, no rutas exactas.
- El contenido irrelevante para la tarea actual contamina el contexto. Usa **Progressive Disclosure**.

---

### Principio de Progressive Disclosure

En lugar de concentrar todo en un solo `AGENTS.md` monolítico, distribuye el conocimiento en archivos secundarios y referencia solo los relevantes.

```text
mi-proyecto/
├── AGENTS.md                        (raiz — minimo indispensable + punteros)
└── docs/
    ├── TYPESCRIPT.md                (convenciones de TypeScript)
    ├── TESTING.md                   (estrategia y comandos de test)
    ├── API_CONVENTIONS.md           (diseño de endpoints)
    ├── DATABASE_SCHEMA.md           (migraciones y modelos)
    └── SERVICE_ARCHITECTURE.md     (diagrama de servicios)
```

El `AGENTS.md` raíz solo referencia:

```markdown
This is a Node.js GraphQL API using Prisma and TypeScript.
Use pnpm workspaces. Build: `pnpm build`. Typecheck: `pnpm tsc --noEmit`.

For task-specific guidance, read only what is relevant:
- TypeScript conventions: docs/TYPESCRIPT.md
- Testing patterns: docs/TESTING.md
- API design: docs/API_CONVENTIONS.md
- Database schema: docs/DATABASE_SCHEMA.md
```

> [!TIP]
> Usa referencias conversacionales, no imperativas. En vez de `ALWAYS read docs/TYPESCRIPT.md`, escribe `For TypeScript conventions, see docs/TYPESCRIPT.md`. El agente evaluará si lo necesita y lo leerá solo cuando sea relevante.

---

### Estructura y Secciones del Archivo

#### Secciones Recomendadas

Según la especificación oficial de `agentsmd/agents.md`, estas son las secciones estándar:

| Sección                   | Propósito                                                     |
| :------------------------ | :------------------------------------------------------------ |
| **Project Overview**      | Una sola frase describiendo qué hace el proyecto              |
| **Tech Stack**            | Lenguajes, frameworks, gestores de paquetes                   |
| **Development Setup**     | Comandos de instalación y configuración inicial               |
| **Build & Test Commands** | Comandos exactos para construir, testear, lint y typecheck    |
| **Code Style Guidelines** | Convenciones del equipo (si no hay linter que lo maneje)      |
| **Architecture Notes**    | Estructura de carpetas, patrones de diseño clave              |
| **Security Practices**    | Variables de entorno, sanitización, autenticación             |
| **Common Tasks**          | Recetas paso a paso para tareas frecuentes                    |

#### Palabras Correctas para Instrucciones

| ❌ Evitar                                            | ✅ Preferir                                              |
| :-------------------------------------------------- | :------------------------------------------------------ |
| `ALWAYS use async/await`                            | `Use async/await over promise chains`                   |
| `NEVER commit without tests`                        | `Run tests before committing: npm test`                 |
| `Write clean code`                                  | `Use named exports. Prefer functional components.`      |
| `Be careful with the database`                      | `Validate all inputs server-side. Use Prisma for queries.` |
| Listar rutas exactas: `src/auth/handlers.ts`        | Describir capacidades: `Authentication logic lives in the auth module` |

---

### Reglas de Formato Markdown

1. **H1 (`#`)** — Solo para el título del archivo. Solo uno por archivo.
2. **H2 (`##`)** — Secciones principales (Tech Stack, Commands, Architecture).
3. **H3 (`###`)** — Subsecciones dentro de una sección principal.
4. **H4 (`####`)** — Ejemplos de código o detalles específicos dentro de una subsección.
5. **Listas** — Usa listas con guión (`-`) para instrucciones accionables.
6. **Bloques de código** — Siempre especifica el lenguaje: ` ```bash`, ` ```json`, ` ```text`.
7. **Negritas** — Para términos clave, nombres de herramientas y valores importantes.
8. **Sin emojis** en instrucciones técnicas. Solo en tablas ilustrativas si el contexto lo permite.

---

### Patrones de Referenciación entre Archivos

#### Referencia Simple (Markdown Link)
```markdown
For TypeScript conventions, see [docs/TYPESCRIPT.md](docs/TYPESCRIPT.md).
```

#### Referencia con Contexto
```markdown
Authentication logic is handled by the auth module.
For OAuth flows and JWT patterns, see [docs/AUTH.md](docs/AUTH.md).
```

#### Referencia Condicional (más efectiva)
```markdown
If working on database migrations, read docs/DATABASE_SCHEMA.md first.
If working on API endpoints, read docs/API_CONVENTIONS.md.
```

#### Referencia a Línea Específica en Código
```markdown
The base request handler is defined in src/lib/handler.ts:42.
```

> [!NOTE]
> Evita copiar snippets de código en el `AGENTS.md`. Los snippets se desactualizan rápidamente. En su lugar, apunta al archivo fuente con una referencia de línea: el agente leerá la versión actual del código directamente.

---

### Anti-Patrones a Evitar

| Anti-Patrón                            | Problema                                                     | Solución                                    |
| :------------------------------------- | :----------------------------------------------------------- | :------------------------------------------ |
| **Ball of mud** — crecer sin estructura | Cientos de reglas acumuladas que nadie revisa               | Auditoria regular. Si no aplica a TODAS las tareas, muévelo a un archivo secundario |
| **Auto-generado con `/init`**           | Genera archivos exhaustivos que saturan el contexto          | Escríbelo manualmente, con restraint         |
| **Reglas de estilo de código**          | El linter ya lo hace. Estos tokens son desperdiciados        | Usa ESLint/Biome con autofix. Usa un Hook para ejecutar el formatter |
| **Rutas absolutas de archivos**         | Se desactualizan en cada refactor                            | Describe capacidades, no rutas              |
| **Instrucciones contradictorias**       | Global dice "Tabs", proyecto dice "Spaces" → ruido           | El nivel más específico siempre tiene prioridad: no los mezcles |
| **Documentar lo obvio**                 | "Write clean code", "Be helpful"                            | Solo instrucciones específicas y accionables |

---

### Templates de AGENTS.md

Para facilitar la adopción de estas mejores prácticas, hemos creado una serie de plantillas listas para usar que ilustran tanto el modelo monolítico como el de **Progressive Disclosure**.

#### 1. Template Monolítico
Ideal para proyectos pequeños o medianos donde todas las reglas caben en un solo archivo sin saturar el presupuesto de instrucciones.
- 📄 [AGENTS.md Monolítico](../templates/agents/monolith/AGENTS.md)

#### 2. Template de Progressive Disclosure (Recomendado)
Diseñado para proyectos grandes, monorepos o equipos con múltiples preocupaciones técnicas. Los archivos secundarios pueden cubrir cualquier aspecto del proyecto: TypeScript, Testing, API, DB, estilos, componentes, arquitectura, tech stack, workflows de Deploy, etc. El agente solo lee los que son relevantes para la tarea actual.
- 📄 [AGENTS.md raíz](../templates/agents/progressive/AGENTS.md) — Mínimo indispensable + punteros
- 📄 [AGENTS.md de paquete](../templates/agents/progressive/packages/api/AGENTS.md) — Ejemplo de jerarquía en monorepo

  *Docs de Code & Language:*
  - 📄 [typescript.md](../templates/agents/progressive/docs/typescript.md) — Convenciones de lenguaje
  - 📄 [testing.md](../templates/agents/progressive/docs/testing.md) — Estrategia y comandos de tests

  *Docs de Frontend & UI:*
  - 📄 [components.md](../templates/agents/progressive/docs/components.md) — Estructura y reglas de componentes
  - 📄 [styles.md](../templates/agents/progressive/docs/styles.md) — CSS Modules, design tokens, dark mode

  *Docs de Arquitectura & Stack:*
  - 📄 [architecture.md](../templates/agents/progressive/docs/architecture.md) — Diagrama de sistema y decisiones de diseño
  - 📄 [tech-stack.md](../templates/agents/progressive/docs/tech-stack.md) — Stack, versiones y política de dependencias

---

### Comparativa de Gestión de Contexto

> [!WARNING]
> **Contaminación de Contexto:** Evita definir reglas contradictorias en diferentes niveles. El nivel más específico tiene prioridad — pero si ambos niveles definen lo mismo de forma distinta, el modelo puede confundirse e ignorar ambos.

> [!NOTE]
> Para conocer aspectos únicos y configuraciones avanzadas de cada herramienta, consulta su sección específica: [Cursor](tools/cursor.md#gestión-de-contexto-rules-agentsmd) | [Antigravity](tools/antigravity.md#gestión-de-contexto-rules-workflows) | [Gemini CLI](tools/gemini-cli.md#gestión-de-contexto-memory-management) | [OpenCode](tools/opencode.md#gestión-de-contexto-agentsmd) | [Claude Code](tools/claude-code.md#gestión-de-contexto-memory-agentsmd) | [Codex CLI](tools/codex-cli.md#gestión-de-contexto-agentsmd).


**Referencias y Documentación Oficial:**
- [AGENTS.md — Open Standard Spec](https://github.com/agentsmd/agents.md)
- [A Complete Guide to AGENTS.md — AIHero](https://www.aihero.dev/a-complete-guide-to-agents-md)
- [AGENTS.md Deep Dive — PRPM](https://prpm.dev/blog/agents-md-deep-dive)
- [Writing a Good CLAUDE.md — HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Cursor: Rules](https://cursor.com/docs/rules)
- [Gemini CLI: Memory Management](https://geminicli.com/docs/cli/tutorials/memory-management/)
- [OpenCode: Rules](https://opencode.ai/docs/rules/)
- [Claude: Memory & Agents.md](https://code.claude.com/docs/en/memory#agents-md)
- [Codex: Agents.md Guides](https://developers.openai.com/codex/guides/agents-md)

## Skills (Habilidades)

Dado que las **Skills** son un componente central y extenso (con reglas avanzadas de metadatos, evaluación y plantillas), hemos dedicado un documento completo para explicarlas a fondo.

👉 **[Ver Guía Completa de Skills (Habilidades)](concepts/skills.md)**

Aquí encontrarás:
- Mecanismos de Activación y Metadatos YAML.
- Árboles de estructura (Scripts, Templates, Monorepos).
- Reglas oficiales de **AgentSkills.io** (Optimización de Triggers, Evals, Scripts sin instalación).
- Recomendaciones de integración (ej. ClickUp, Vercel).
- Tablas de configuración global por herramienta.

## MCP (Model Context Protocol)

El **Model Context Protocol (MCP)** es el estándar de comunicación que permite a los modelos de IA interactuar con el mundo real. Actúa como un puente entre la lógica del LLM y herramientas externas (bases de datos, APIs, navegadores).

### Conceptos Base de MCP
Puente entre la IA y herramientas externas (Tools, Resources, Prompts).

### Comparativa de Configuración MCP
Lógica de exclusión por cada agente.

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
> Para conocer metadatos específicos, características únicas (como MCP Apps, Auth OAuth) y optimización de Docker por cada herramienta, consulta su sección específica: [Cursor](tools/cursor.md#mcp-model-context-protocol) | [Antigravity](tools/antigravity.md#mcp-model-context-protocol) | [Gemini CLI](tools/gemini-cli.md#mcp-model-context-protocol) | [OpenCode](tools/opencode.md#mcp-model-context-protocol) | [Claude Code](tools/claude-code.md#mcp-model-context-protocol) | [Codex CLI](tools/codex-cli.md#mcp-model-context-protocol).

## Plugins y Extensiones

### Comparativa de Ecosistemas
Resumen de arquitecturas y comandos de instalación.

| Agente | Arquitectura | Directorio/Comando |
| :--- | :--- | :--- |
| **Cursor** | Bundles con reglas, skills, MCP | `cursor.com/marketplace` |
| **Gemini CLI** | `gemini-extension.json` | `gemini extensions install` |
| **Claude Code** | `.claude-plugin/plugin.json` | `/plugin install` |
| **OpenCode** | Módulos JS/TS (Bun) | `.opencode/plugins/` |

> [!NOTE]
> Para detalles sobre desarrollo, eventos y arquitecturas de plugins específicos por herramienta, consulta su sección específica: [Cursor](tools/cursor.md#plugins-y-extensiones) | [Antigravity](tools/antigravity.md#skills-habilidades) | [Gemini CLI](tools/gemini-cli.md#extensions-extensiones) | [OpenCode](tools/opencode.md#plugins-y-extensiones) | [Claude Code](tools/claude-code.md#plugins-y-extensiones).

**Referencias y Documentación Oficial:**
- [Cursor: Plugins](https://cursor.com/docs/plugins)
- [Gemini CLI: Extensions Guide](https://geminicli.com/docs/extensions/) | [Writing](https://geminicli.com/docs/extensions/writing-extensions/) | [Best Practices](https://geminicli.com/docs/extensions/best-practices/) | [Reference](https://geminicli.com/docs/extensions/reference/)
- [OpenCode: Plugins](https://opencode.ai/docs/es/plugins/) | [Ecosystem](https://opencode.ai/docs/es/ecosystem/)
- [Claude: Discover Plugins](https://code.claude.com/docs/en/discover-plugins) | [Plugins Guide](https://code.claude.com/docs/en/plugins)

## Hooks (Disparadores)

### Protocolos Stdin/Stdout
Scripts deterministas que se ejecutan ante eventos del ciclo de vida.

### Bloqueo y Seguridad (Fail-Closed)
Mecanismos para abortar operaciones automáticas ante fallos de validación.

---

## Subagentes

### Arquitecturas de Equipos (Orquestadores)
Uso de agentes especializados (Manager, Coder, QA) para tareas complejas. Dividir tareas permite ahorrar contexto, pero requiere coordinación rigurosa.

### Patrones Avanzados Multi-Agente

Basado en la evolución de flujos orquestados en producción, se han consolidado cinco mejores prácticas para asegurar robustez al trabajar con múltiples subagentes:

1. **El Principio de "Housekeeping" (Limpieza Obligatoria):**
   Los subagentes que modifican estados (como escritura de código o manipulación en herramientas de diseño) deben ser instruidos expresamente para limpiar sus propios artefactos parciales si la tarea falla o necesita iterar. Esto evita los "cementerios de código" o estados rotos.
2. **Scripts Deterministas vs. Subagentes (LLMs):**
   Evita desperdiciar ciclos de inferencia asignando tareas puramente algorítmicas o de sistema a un subagente (ej. matar un puerto, hacer pull, mover carpetas). El orquestador debe usar directamente invocaciones de terminal a scripts locales (`.sh` o `.ps1`), reservando la invocación de subagentes exclusivamente para tareas cognitivas, argumentales o creativas.
3. **Contratos de Datos Estrictos (Patrón de Reportes Estáticos):**
   La comunicación entre subagentes no debe ser conversacional. Usa contratos estrictos (ej. bloques inmutables de TOML, JSON o Markdown estructurado). El orquestador actúa como transportista: capta el bloque del Lector y se lo pega íntegro en el prompt del Escritor, evitando tergiversaciones del lenguaje natural.
   > [!TIP]
   > **Estrategia de Modelos SOTA:** Utiliza modelos **Rápidos/Ligeros** (ej. Claude 4.5 Haiku, GPT-5.4 mini o Gemini 3.1 Flash) para estas tareas de formateo e invocación de MCP/APIs. Son más consistentes siguiendo esquemas JSON rígidos que los modelos de razonamiento pesado.

4. **Orquestadores con Rutinas de Recuperación (Fallbacks Automáticos):**
   Los flujos multi-agentes en cadena son frágiles por naturaleza. El orquestador debe poseer instrucciones claras de contingencia. (ej. "Si el Subagente X fracasa con un error de WebSocket ocupado, no te detengas; invoca el script de limpieza rápida y aplica un único reintento automatizado antes de rendirte y consultar al usuario").

5. **Lecturas Paralelas, Escrituras Secuenciales:**
   Minimiza la latencia despachando subagentes de sólo lectura de forma simultánea (ej. un *code-reader* inspeccionando arquitectura mientras un *design-reader* escanea mockups). Sin embargo, las fases destructivas o constructivas de los subagentes *writers* siempre deben ejecutarse lineal y rigurosamente.

### Beneficios del Aislamiento
Protección de tokens, prevención de alucinaciones por contexto cruzado y especialización de conocimientos técnicos.

> [!NOTE]
> Para conocer cómo se configuran estos equipos y ver **ejemplos de subagentes orquestadores** en cada herramienta, consulta su sección específica: [Cursor](tools/cursor.md#subagentes) | [Gemini CLI](tools/gemini-cli.md#subagentes) | [OpenCode](tools/opencode.md#subagentes) | [Claude Code](tools/claude-code.md#subagentes) | [Codex CLI](tools/codex-cli.md#subagentes).

---

## Automatización y Scripting

### Comparativa de Modos Headless
Ejecución en CI/CD, CRON y scripts no TTY.

### Seguridad en Modo Automático
Límites de aprobación y políticas de sandboxing.

> [!NOTE]
> Para detalles sobre códigos de salida, comandos específicos, formatos JSON y tareas programadas (CRON), consulta la sección de automatización de cada herramienta: [Gemini CLI](tools/gemini-cli.md#automatización-y-scripting) | [Claude Code](tools/claude-code.md#automatización-y-scripting) | [Codex CLI](tools/codex-cli.md#automatización-y-scripting).

**Referencias y Documentación Oficial:**
- [Gemini CLI: Headless Tutorial](https://geminicli.com/docs/cli/headless/)
- [Claude: Headless Mode](https://code.claude.com/docs/en/headless) | [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)

## Evaluación de Modelos (Benchmarks y Casos de Uso)

### Glosario de Términos para Humanos
*   **SOTA (State of the Art):** Se refiere a lo último en tecnología, los modelos que están en la "vanguardia" y lideran las capacidades actuales de la industria.
*   **NIAH (Needle In A Haystack):** Literalmente "aguja en un pajar". Es una prueba de estrés que mide la capacidad de un modelo para encontrar un dato específico dentro de una ventana de contexto masiva (ej. 1 millón de tokens).

### Tabla Comparativa de Idoneidad SOTA (Abril 2026)

La siguiente tabla resume el rendimiento de los modelos actuales de vanguardia.

| Familia | Modelo | Tipo / Velocidad | Razonamiento | Contexto (NIAH) | Tools / MCP | Mejor para... |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **OpenAI** | **GPT-5.4 Thinking** | Pesado (Razonativo) | ✅ | ✅ (1M+) | ⚠️ | Arquitectura y Computer Use |
| **OpenAI** | **GPT-5.3-Codex** | Pesado (Razonativo) | ✅ | ⚠️ (256K) | ✅ | Especialista en Código / Terminal |
| **Google** | **Gemini 3.1 Pro** | Pesado (Razonativo) | ✅ | ✅ (1M+) | ⚠️ | Arquitectura y Big Context |
| **Anthropic** | **Claude 5 Sonnet** | Equilibrado | ✅ | ⚠️ (200K) | ✅ | Desarrollo ágil y Production Code |
| **Anthropic** | **Claude 4.6 Opus** | Pesado (Razonativo) | ✅ | ⚠️ (200K) | ⚠️ | Lógica compleja multinivel |
| **OpenAI** | **GPT-5.4 mini** | Rápido (Ligero) | ✅ | ⚠️ (128K) | ✅ | **Consultas MCP**, JSON, Scripts |
| **Google** | **Gemini 3.1 Flash** | Rápido (Ligero) | ⚠️ | ✅ (1M+) | ✅ | **Búsqueda**, Lectura rápida |
| **Anthropic** | **Claude 4.5 Haiku** | Rápido (Ligero) | ⚠️ | ⚠️ (200K) | ✅ | **Subagentes de Búsqueda** |

> [!TIP]
> **Estrategia Pro:** Los modelos **Rápidos/Ligeros** (ej. GPT-5.4 mini, Gemini 3.1 Flash, Claude 4.5 Haiku) son excepcionales para subagentes de búsqueda, consultar MCPs y transformar salidas de APIs en formatos estructurados (JSON). Son más económicos y consistentes en tareas de formateo repetitivo.

---

### Guía de Perfiles: ¿Cuándo usar cada nivel?

La eficiencia de un agente depende de elegir el "combustible" adecuado para la tarea:

#### 1. Perfil "High Reasoning / MAX Effort"
*   **Modelos:** GPT-5.4 Thinking, GPT-5.3-Codex, Gemini 3.1 Pro, Claude 4.6 Opus.
*   **Cuándo conviene:** Cambios estructurales en la arquitectura, resolución de bugs complejos en múltiples archivos, o creación de planes iniciales.

#### 2. Perfil "Balanced / Logic-Efficient"
*   **Modelos:** Claude 5 Sonnet, GPT-5.4 Pro.
*   **Cuándo conviene:** Estándar para el desarrollo activo diario.

#### 3. Perfil "Utility / Low Effort / Search"
*   **Modelos:** GPT-5.4 mini, Gemini 3.1 Flash, Claude 4.5 Haiku.
*   **Cuándo conviene:** Subagentes de búsqueda, lectura de archivos masivos sin edición, generación de JSDoc, unit testing y mapeo de MCP/APIs a JSON.

---

### Advertencias sobre Modelos Legados (Deprecated)

Modelos que aún aparecen en configuraciones pero que **no se recomiendan** para uso profesional en 2026:

> [!WARNING]
> **Gemini 3.0 Pro:** Se ha observado un índice de **alucinación** significativamente mayor en comparación con la versión 3.1. Tiende a inventar rutas de archivos o herramientas inexistentes. Se recomienda migrar a **Gemini 3.1 Pro** inmediatamente.

> [!NOTE]
> **Gemini 3.0 Flash:** Aunque ya existe la versión 3.1, la 3.0 sigue siendo aceptable únicamente para **búsquedas muy rápidas** de texto plano o pre-procesamiento de datos no críticos. No se recomienda para codificación activa.

> [!CAUTION]
> **GPT-3.5-Turbo y Legacy Codex (code-davinci):** Estos modelos están técnicamente obsoletos para el desarrollo agentic moderno. 
> 
> **GPT-5.2 Thinking:** Aunque potente en su lanzamiento, OpenAI ha programado su **retiro para Junio de 2026**. Se recomienda migrar a la serie GPT-5.4 inmediatamente para evitar interrupciones.

#### Fuentes de Datos (Benchmarks 2026)
*   **Coding & Reasoning:** [LiveCodeBench](https://livecodebench.github.io/leaderboard.html)
*   **Real-World Software Engineering:** [SWE-bench Verified (Official)](https://www.swebench.com/)
*   **Tool Use Proficiency:** [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)

---
*Nota: Todos los términos técnicos y fragmentos de código se mantienen en inglés para mayor precisión técnica.*