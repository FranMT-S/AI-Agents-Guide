# Mi Guía de Aprendizaje de Agentes de IA

Esta guía es una referencia fundacional y completa para el desarrollo de agentes de software potenciados por Inteligencia Artificial. Aquí encontrarás inmersiones profundas en arquitecturas modernas, mejores prácticas de ingeniería para la gestión de contexto, y evaluaciones objetivas de los modelos (LLMs) más avanzados del mercado.

---

## Índice
1. [Introducción y Conceptos Básicos](#1-introduccion-y-conceptos-basicos)
2. [Gestión de Contexto (AGENTS.md)](#2-gestion-de-contexto-agentsmd)
3. [Skills (Habilidades)](#3-skills-habilidades)
4. [MCP (Model Context Protocol)](#4-mcp-model-context-protocol)
5. [Plugins y Extensiones](#5-plugins-y-extensiones)
6. [Hooks (Disparadores)](#6-hooks-disparadores)
7. [Subagentes y Orquestación](#7-subagentes-y-orquestacion)
8. [Automatización y Scripting](#8-automatizacion-y-scripting)
9. [Modelos de IA: Guía Completa](#9-modelos-de-ia-guia-completa)
10. [Metodologías de trabajo con AI](#10-metodologias-de-trabajo-con-ai)

> [!NOTE]
> **Mi Colección Personal:** Muchos de los recursos mencionados los tengo implementados y los iré actualizando periódicamente. Si deseas ver mis carpetas, puedes visitar:
> - 🧩 **[Mis Skills](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/skills/)**
> - 🤖 **[Mis Subagentes](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/subagents)**
> - 🏗️ **[Templates para Agentes](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/templates/agents)**
> - 📋 **[Templates para Skills](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/templates/skills)**

---

## 1. Introducción y Conceptos Básicos

En el ecosistema actual de agentes de IA aplicados a la ingeniería de software, el mayor desafío técnico no es la capacidad de código del modelo, sino la **limitación de la ventana de contexto**. 

A medida que una sesión de desarrollo o una conversación progresa, el modelo base (como Claude 4.5 Haiku o GPT-5.4) consume "tokens" (fragmentos semánticos de palabras o código). Si las reglas del proyecto no están estructuradas correctamente desde el inicio, la IA sufre una degradación de atención: comienza a "olvidar" las instrucciones críticas iniciales, provocando **alucinaciones** o generando código que ignora las convenciones del equipo. La solución arquitectónica definitiva a este problema es la implementación de **Memoria Persistente y Direccional** mediante estándares como `AGENTS.md`.

---

## 2. Gestión de Contexto (AGENTS.md)

A medida que una sesión de desarrollo avanza, el modelo base consume tokens para procesar el historial de conversación. Sin una fuente de verdad externa, el agente comienza cada sesión sin saber en qué proyecto trabaja, qué stack tecnológico usa el equipo, ni cómo compilar o testear la aplicación. La solución arquitectónica es `AGENTS.md`: un archivo Markdown que el orquestador lee e inyecta automáticamente en su *system prompt* al inicio de cada sesión, garantizando que el modelo opere con las convenciones del equipo antes de procesar el primer mensaje del usuario.

Su importancia va más allá de la comodidad. Los agentes sin contexto estructurado toman decisiones arquitectónicas incorrectas, generan código que viola las convenciones del proyecto e ignoran restricciones de seguridad que el equipo considera como reglas críticas. Un `AGENTS.md` bien redactado elimina esta varianza probabilística, convirtiendo el comportamiento del agente en algo predecible y repetible.

Lo que hace especialmente valioso este estándar es su **compatibilidad multiplataforma**. El mismo archivo que guía a Gemini CLI en la terminal guía a Cursor en el IDE. No necesitas sincronizar reglas entre herramientas; el archivo actúa como árbitro único.

| Herramienta | Archivo Nativo | Soporta `AGENTS.md` |
| :--- | :--- | :--- |
| **Codex CLI** | `AGENTS.md` | ✅ Nativo |
| **Gemini CLI** | `GEMINI.md` | ✅ Sí |
| **Claude Code** | `CLAUDE.md` | ✅ Sí (alias) |
| **GitHub Copilot** | `copilot-instructions.md` | ✅ Sí |
| **OpenCode** | `AGENTS.md` | ✅ Nativo |
| **Cursor** | `.cursor/rules/` | ✅ Sí |
| **Antigravity** | `AGENTS.md` | ✅ Nativo |

El archivo sigue una jerarquía de tres niveles (Global → Proyecto → Módulo) donde las instrucciones más específicas tienen prioridad absoluta. Existe además un patrón crítico llamado **Progressive Disclosure**: en lugar de concentrar todas las reglas en un `AGENTS.md` monolítico (lo que provoca que el agente ignore instrucciones aleatoriamente por fatiga de contexto), se distribuye el conocimiento en archivos secundarios referenciados bajo demanda.

> [!IMPORTANT]
> Los LLMs de frontera pueden mantener entre 150 y 200 instrucciones activas. Herramientas como Claude Code consumen ~50 instrucciones base en su *system prompt* interno. Cada regla que añades reduce la fiabilidad de todas las demás.

👉 **[Ver Guía Técnica Completa: AGENTS.md y Gestión de Contexto](concepts/agents.md)** — incluye jerarquía de alcance, secciones recomendadas, tabla de terminología correcta, malas prácticas y ejemplo de producción completo.

---



## 3. Skills (Habilidades)

### ¿Qué son las Skills?
Las **Skills** son herramientas modulares o capacidades encapsuladas que extienden drásticamente lo que un agente puede hacer. En lugar de depender de que el modelo base "sepa de memoria" cómo construir un diagrama UML o usar una API propietaria, una Skill agrupa instrucciones específicas y scripts auxiliares, dotando al agente de "músculo" especializado.

### Beneficios Clave
Proveen extensibilidad casi ilimitada sin comprometer el *context window* base. Una Skill permanece completamente inactiva y no satura los límites de tokens hasta que el agente evalúa su *trigger* (una descripción semántica de activación) y concluye que es la herramienta idónea para la tarea actual.

> [!IMPORTANT]
> Dado que las **Skills** son el pilar de la automatización avanzada (involucrando metadatos complejos, aislamiento en *sandboxes* y sistemas de evaluación o `Evals`), toda la documentación técnica sobre su arquitectura se ha movido a una guía especializada en favor del principio de Revelación Progresiva.

👉 **[Ver Guía Técnica Completa de Skills (Habilidades)](concepts/skills.md)**

En ese documento dedicado encontrarás el diseño de arquitecturas (Skills Simples, con Scripts, con Templates y *Few-Shot*), junto con las reglas del estándar oficial de **AgentSkills.io**.

---

## 4. MCP (Model Context Protocol)

### Introducción Técnica
El **Model Context Protocol (MCP)** es un protocolo asíncrono y universal, creado originalmente por Anthropic, que estandariza la comunicación bidireccional local/remota entre los modelos de IA (los "clientes") y las fuentes de datos (los "servidores"). 

### Sus Tres Pilares
1.  **Resources (Recursos):** Datos de solo lectura expuestos desde el servidor al cliente (ej. la IA solicita leer tu esquema de base de datos en tiempo real).
2.  **Tools (Herramientas):** Acciones ejecutables con estado que la IA puede invocar autónomamente (ej. un servidor MCP posee herramientas como `fetch_clickup_ticket` o `github_merge_pr`).
3.  **Prompts (Plantillas):** Estructuras de interacción controladas por el servidor para tareas parametrizadas que el LLM puede cargar para estandarizar procesos.

### El Riesgo del Server Sprawl
> [!WARNING]
> **Server Sprawl:** Instalar e invitar a múltiples servidores MCP indiscriminadamente contamina la experiencia del agente. Cada herramienta MCP disponible inyecta metadatos y descripciones en el *system prompt* central. Esto eleva dramáticamente el costo de inferencia por mensaje y diluye el raciocinio analítico de tu agente. 

Para mitigar el Server Sprawl, cada agente moderno incorpora un mecanismo de listas blancas y negras que permite deshabilitar comandos específicos.

| Agente | Archivo de Configuración | Método de Exclusión (Blacklist) |
| :--- | :--- | :--- |
| **Cursor** | `~/.cursor/mcp.json` | Desactivación Manual vía UI |
| **Antigravity** | `mcp_config.json` | Clave JSON: `"disabledTools": []` |
| **Gemini CLI** | `settings.json` | Clave JSON: `"excludeTools": []` |
| **Claude Code** | `settings.json` | Políticas vía `hooks: PreToolUse` |
| **Codex CLI** | `config.toml` | Variable TOML: `disabled_tools` |
| **OpenCode** | `opencode.json` | JSON Config: `"tools": {"*": false}` |

👉 **[Ver Guía Técnica Completa de Configuración MCP](concepts/mcp.md)** (Incluye configuraciones detalladas para GitHub, ClickUp, Figma y Trello).

---

## 5. Plugins y Extensiones

Un desarrollador nuevo llega a un equipo. Para tener al agente de IA funcionando con las mismas capacidades que el resto del equipo — las Skills de revisión de API, los Hooks de seguridad, los servidores MCP conectados al gestor de tareas, las reglas de estilo del `AGENTS.md` del proyecto — necesita replicar manualmente toda esa configuración. Clonar repositorios, copiar JSONs de configuración, instalar dependencias de scripts, actualizar rutas. Un proceso frágil que tarda horas y termina inevitablemente en inconsistencias entre máquinas.

Los **Plugins** resuelven exactamente esto: empaquetan todo ese ecosistema en una unidad instalable. Un solo comando instala el conjunto completo — Skills, Hooks, servidores MCP, configuración de subagentes, reglas de contexto — sin intervención manual. La analogía directa son las extensiones de VS Code: no configuras cada extensión a mano, las instalas y funcionan.

### Qué puede contener un Plugin

Un plugin no tiene un contenido fijo — es un contenedor que agrupa lo que el equipo o el autor del plugin decida distribuir de forma coherente:

- **Skills**: capacidades especializadas (revisor de APIs REST, generador de tests, documentador de funciones)
- **Hooks**: scripts de seguridad y calidad preconfigurados (protección de archivos, linter automático)
- **Servidores MCP**: integraciones con servicios externos (GitHub, Jira, Slack, Supabase)
- **Configuración de subagentes**: roles y permisos predefinidos para un tipo de proyecto
- **Reglas de contexto**: fragmentos de `AGENTS.md` con convenciones del stack

La diferencia con instalar cada uno por separado es la **cohesión**: el plugin garantiza que todas las piezas son compatibles entre sí, están versionadas juntas y se pueden desinstalar completamente sin dejar fragmentos huérfanos.

### Cuándo tiene sentido crear un Plugin

Un plugin es la elección correcta cuando el conjunto de configuraciones que necesitas es lo suficientemente estable para distribuir y lo suficientemente complejo para que replicarlo manualmente sea un problema real. Para experimentos personales basta con Skills individuales. Un plugin es para equipos, proyectos a largo plazo o para publicar en un marketplace.

### Sistemas por herramienta

Cada orquestador tiene su propio sistema de plugins con arquitecturas técnicas diferentes, pero el propósito es el mismo:

| Herramienta | Arquitectura | Instalación |
| :--- | :--- | :--- |
| **Cursor** | Bundles con `plugin.json` (reglas + skills + agents + MCP) | Marketplace UI o `cursor.com/marketplace` |
| **Gemini CLI** | Manifiestos `gemini-extension.json` con comandos TOML y skills | `gemini extensions install <URL>` |
| **Claude Code** | `.claude-plugin/plugin.json` con skills, subagentes, hooks y MCP | `/plugin install @scope/nombre` |
| **OpenCode** | Módulos TypeScript nativos ejecutados en Bun con API de eventos | Archivo `.ts` en `.opencode/plugins/` |

> [!NOTE]
> Antigravity y Codex CLI no tienen un sistema de plugins formal — sus capacidades equivalentes se distribuyen como Skills individuales o configuraciones de Skills con dependencias explícitas.

👉 **[Ver Guía Técnica Completa: Plugins y Extensiones](concepts/plugins.md)** — incluye estructuras de directorios, schemas de `plugin.json`, ejemplos de extensiones para cada herramienta y guía de publicación en marketplace.

---



## 6. Hooks (Disparadores)

Pedirle a un modelo de lenguaje "no olvides ejecutar el linter antes de hacer commit" es un error arquitectónico. Los LLMs son sistemas probabilísticos — la misma instrucción puede cumplirse, ignorarse o confundirse dependiendo del contexto de la sesión, el orden del historial o la longitud de la ventana. Para las validaciones que no pueden fallar ni una sola vez, la respuesta es **determinismo programático**, no confianza estadística.

Los **Hooks** son scripts externos que el orquestador ejecuta en momentos exactos del ciclo de vida del agente: antes de usar una herramienta (`PreToolUse`), después de que el agente termina (`PostResponse`), al recibir input del usuario (`UserPromptSubmit`), o antes de ejecutar un comando bash (`beforeShellExecution`). No son sugerencias al modelo — son interrupciones del sistema que ocurren independientemente de lo que el LLM haya decidido hacer.

### El principio Fail-Closed

La característica más importante de los Hooks es el comportamiento **fail-closed**: si el script del Hook retorna un código de salida distinto de `0` (o `2` en algunas herramientas), el orquestador **aborta la acción** antes de ejecutarla. El error se retroalimenta al modelo como contexto, pero la acción nunca ocurre. Esto convierte a los Hooks en barandas de seguridad que ninguna instrucción del modelo puede saltarse.

```text
Usuario: "Borra todos los logs de errores"
Agente:   → Intenta ejecutar bash: rm -rf logs/
Hook:     → pre_bash_execution.sh evalúa el comando
          → Detecta "rm -rf" sobre path protegido
          → exit 2 → BLOQUEADO
Agente:   → Recibe el error, informa al usuario
```

### Qué se puede hacer con un Hook

Los casos de uso más comunes se dividen en dos categorías:

**Seguridad y protección**:
- Bloquear comandos bash destructivos (`rm -rf`, `DROP TABLE`, `git push --force`)
- Impedir escritura en archivos fuera del workspace del proyecto
- Detectar y rechazar prompts que contengan credenciales o tokens

**Calidad y observabilidad**:
- Ejecutar el linter automáticamente antes de cualquier commit (`PostToolUse: git commit`)
- Registrar en un log cada herramienta que el agente invoca (auditoría completa)
- Ejecutar tests unitarios después de cada modificación de archivo, interrumpiendo si fallan

### Qué NO son los Hooks

Los Hooks no son subagentes ni Skills. No tienen acceso al LLM ni pueden generar texto. Son scripts de shell, Python o cualquier binario que reciben contexto via stdin y responden via stdout/exit code. Su fortaleza es exactamente esa simplicidad determinista — no fallan por alucinación ni por contexto confuso.

> [!WARNING]
> Un Hook que consume demasiado tiempo de CPU o que tiene bugs propios puede bloquear el flujo del agente indefinidamente o generar falsos positivos que frustran al desarrollador. Mantén los scripts de Hook simples, rápidos y bien testeados de forma independiente al agente.

👉 **[Ver Guía Técnica Completa: Hooks](concepts/hooks.md)** — incluye tabla de eventos por herramienta, protocolo stdin/stdout, ejemplos de scripts de protección, auditoría y calidad, y la tabla de códigos de salida.

---



## 7. Subagentes y Orquestación

La imagen del asistente de IA como un único agente resolviendo todo — leyendo el proyecto, diseñando la arquitectura, escribiendo el código, revisando la calidad y ejecutando los tests — es el antipatrón más costoso del ecosistema actual. La orquestación con **Subagentes** invierte ese enfoque: el agente primario actúa como manager y delega cada parte del trabajo a especialistas con roles y permisos acotados. No es un monólogo; es un equipo coordinado.

La analogía es directa: un manager competente no redacta los contratos, implementa el código, audita la seguridad y entrega el proyecto al cliente al mismo tiempo. Convoca al especialista correcto para cada tarea, recibe su output y coordina la síntesis final. Los subagentes funcionan exactamente igual.

### Por qué existen

Cuando un modelo de lenguaje intenta resolver simultáneamente una tarea compleja — diseñar, implementar, revisar y testear una feature — su atención se divide entre contextos que compiten entre sí. El resultado es trabajo de calidad inconsistente: el diseño es sólido pero la implementación omite casos borde, o la revisión es superficial porque el modelo ya está "pensando" en los tests.

La especialización resuelve esto. Un subagente `reviewer` cuyo único contexto activo sea revisar un diff de código específico produce una revisión mucho más profunda que el agente primario que acaba de escribir ese mismo código y ahora intenta autocorregirse. Además, los subagentes permiten **paralelismo real**: mientras `builder` escribe el código, `tester` puede preparar los fixtures y el plan de pruebas de forma simultánea.

### El flujo real

Un usuario pide: *"Crea una API REST para gestionar tareas."* El flujo con subagentes se ve así:

1. **Agente primario** analiza el requerimiento y decide que necesita estructurar el trabajo antes de codificar.
2. Delega a `architect`: *"Diseña las rutas, modelos y esquema de base de datos para esta API."*
3. `architect` devuelve: un plan de arquitectura en Markdown con rutas, modelos Prisma y decisiones técnicas justificadas.
4. Agente primario delega a `builder`: *"Implementa esta API basándote en el plan adjunto."*
5. `builder` devuelve: los archivos implementados según el plan.
6. Agente primario delega a `reviewer`: *"Valida la seguridad y calidad de esta implementación."*
7. `reviewer` devuelve: lista de observaciones con severidad y sugerencias de remediación.
8. Agente primario consolida todo, aplica feedback crítico y devuelve el resultado al usuario.

El output final no es el producto de un modelo intentando hacer todo a la vez — es el resultado de tres especialistas trabajando en secuencia con contextos limpios.

### Tipos de subagentes

Los subagentes se dividen en tres categorías prácticas:

- **Especializados personalizados**: los que tú creas para tu workflow particular — un auditor de seguridad, un traductor de documentación, un generador de tests unitarios. Tienen el system prompt, modelo y permisos que tú defines.
- **Integrados (built-in)**: vienen preconfigurados con la herramienta. OpenCode incluye `build`, `plan`, `explore` y `general`. Cursor incluye `Explore` y `Bash`. Gemini CLI incluye `codebase_investigator` y `browser_agent`. Están disponibles sin ninguna configuración adicional.
- **Híbridos**: subagentes personalizados que extienden el comportamiento de uno built-in, añadiendo instrucciones específicas del proyecto al system prompt base.

### Impacto real: sin vs. con subagentes

| Escenario | Sin subagentes | Con subagentes |
| :--- | :--- | :--- |
| "Crea una feature completa" | El agente intenta todo a la vez | Architect diseña → Builder implementa → Reviewer valida |
| Calidad del output | Inconsistente (contexto dividido) | Consistente (especialización por rol) |
| Permisos en acción | El agente tiene acceso completo a todo | Cada subagente solo accede a lo que necesita |
| Tiempo total | Rápido pero impredecible | A veces mayor (coordinación), mejor en paralelo |
| Confiabilidad | Variable | Alta (cada especialista falla en su dominio acotado) |

### La configuración varía, el concepto no

El concepto de subagente es universal, pero cada herramienta tiene su sintaxis propia. El mismo `code-reviewer` se define de estas formas:

| Herramienta | Formato | Directorio |
| :--- | :--- | :--- |
| **OpenCode** | JSON en `opencode.json` o archivo `.md` | `.opencode/agents/` |
| **Cursor** | Archivo `.md` con frontmatter YAML | `.cursor/agents/` |
| **Codex CLI** | Archivo `.toml` | `.codex/agents/` |
| **Gemini CLI** | Archivo `.md` con frontmatter YAML | `.gemini/agents/` |
| **Claude Code** | Archivo `.md` con frontmatter YAML | `.claude/agents/` |

### Control de acceso granular

Los subagentes no son simplemente "copias" del agente principal con un nombre diferente — tienen permisos propios que limitan exactamente qué pueden hacer:

- **`reviewer`**: lectura únicamente. No puede modificar archivos, solo leerlos y reportar.
- **`builder`**: lectura y escritura. Puede crear y editar archivos, pero no ejecutar comandos de red.
- **`tester`**: ejecución de comandos bash limitada y lectura. Puede correr `npm test`, no puede modificar código.

Este modelo de permisos proporciona una protección real: si un subagente recibe instrucciones maliciosas o alucina de forma destructiva, el daño queda contenido a su dominio de permisos. Un `reviewer` que alucina no puede borrar archivos aunque lo intente.

### Cuándo crear un subagente (y cuándo no)

**Crea un subagente si:**
- La tarea requiere especialización real que justifique tener un modelo con contexto aislado.
- Necesitas restringir los permisos de una fase del trabajo (auditoría de solo lectura, revisión sin escritura).
- El modelo del subagente debe ser diferente al principal (usar Haiku para búsqueda, Sonnet para codificación).

**No crees un subagente si:**
- El beneficio de la especialización no supera el overhead de comunicación entre agentes.
- La tarea es simple y el agente principal puede resolverla en una sola respuesta.
- Estarías creando un subagente que simplemente "ayuda a pensar" — eso ya lo hace el agente principal.

La regla práctica: si no puedes describir en una frase clara y restrictiva qué hace el subagente y qué NO hace, probablemente no necesitas crearlo.

### Anti-patrones comunes

- **Subagente para todo**: no todo problema se resuelve con más agentes. El overhead de coordinación tiene un coste real en tokens y tiempo.
- **System prompts vagos**: un `description` que dice "helps with coding" no le dice al orquestador cuándo invocar al subagente ni qué esperar de él.
- **Sin límite de iteraciones**: los flujos multi-agente pueden entrar en bucles recursivos infinitamente costosos si no se define un `max_turns` o `steps` explícito.
- **Escrituras paralelas**: múltiples subagentes escribiendo en los mismos archivos sin coordinación secuencial genera condiciones de carrera y código corrupto.

👉 **[Ver Configuración Técnica, Patrones y Ejemplos de Subagentes](concepts/subagentes.md)**
Para configuraciones específicas por herramienta, consulta **[Cursor](tools/cursor.md)** | **[Gemini CLI](tools/gemini-cli.md)** | **[OpenCode](tools/opencode.md)** | **[Claude Code](tools/claude-code.md)** | **[Codex CLI](tools/codex-cli.md)**

---


## 8. Automatización y Scripting

Los agentes de IA no están limitados a responder en un chat. Cuando se elimina al humano del bucle interactivo, el agente se convierte en un proceso autónomo: recibe un prompt inicial, ejecuta herramientas, toma decisiones y termina retornando un código de salida estándar (`0` éxito, `1+` error). Este es el **modo headless** — el mismo agente que usas en el IDE corriendo desatendido en un servidor, un pipeline de CI/CD o un cronjob nocturno.

El cambio de paradigma es significativo. En modo interactivo el humano supervisa cada acción. En modo headless el agente opera en ciclos completos sin intervención: lee los logs de un pipeline fallido, entiende el error, escribe el fix, abre el Pull Request y notifica por Slack — todo mientras el equipo duerme. La diferencia entre "asistente de código" y "colaborador autónomo" es exactamente esta capacidad.

### Cuándo tiene sentido automatizar

No toda tarea justifica un flujo headless. Los casos donde aporta valor real son aquellos con tres características: son repetitivos, tienen criterios de éxito medibles y no requieren juicio humano en cada iteración.

**CI/CD reactivo**: en lugar de que un pipeline falle pasivamente y el desarrollador reciba una notificación de error a revisar manualmente, el agente intercepta el output del compilador o los tests fallidos, analiza la causa raíz, aplica el fix en una rama aislada y abre un PR con la corrección y una explicación. El humano solo aprueba; no diagnostica.

**Cron jobs cognitivos**: un cronjob que se ejecuta cada madrugada puede invocar al agente para que escanee los tickets `good-first-issue` en Jira, seleccione los más urgentes, codifique en ramas independientes, ejecute los tests y deje los PRs listos para revisión a primera hora. Las tareas que antes tomaban horas de ramp-up de un contribuidor ocurren mientras el equipo no está trabajando.

**Pre-merge automatizado**: antes de que cualquier rama llegue a `main`, un agente puede ejecutar una suite de auditoría — revisión de seguridad, validación de contratos de API, verificación de cobertura de tests — y bloquear el merge si detecta problemas críticos, sin intervención humana en el proceso de validación.

### El riesgo que no es opcional ignorar

Un agente en modo headless con permisos de escritura irrestrictos sobre un repositorio de producción es un riesgo arquitectónico severo. Los tres vectores de fallo más comunes son:

- **Bucle de facturación infinita**: el agente no converge en una solución, reintenta indefinidamente y consume miles de dólares en llamadas a la API sin producir output útil.
- **Borrado accidental de estado**: un `rm -rf` hallucinated en el contexto equivocado, ejecutado sin sandbox, puede ser irreversible.
- **Filtración de secretos**: el agente lee un `.env` con credenciales y las incluye en un log, un PR o un mensaje de Slack.

La respuesta no es evitar la automatización — es implementarla con los controles correctos: sandboxing en contenedores efímeros, `max_turns` explícitos, permisos de bash con allowlists, y variables de entorno nunca en el contexto del agente.

> [!IMPORTANT]
> Nunca ejecutes modo headless contra producción directamente. Usa contenedores Docker efímeros, permisos de solo lectura para las fases de análisis, y aprobación humana obligatoria para writes que afecten ramas protegidas.

👉 **[Ver Guía Técnica Completa: Automatización y Headless Mode](concepts/automatizacion.md)** — incluye comandos por herramienta, ejemplos reales de GitHub Actions, configuración de sandboxing, cost caps y patrones de integración CI/CD.

---



## 9. Modelos de IA: Guía Completa

Elegir el modelo incorrecto no solo desperdicia presupuesto — produce outputs de baja calidad, latencias inaceptables o facturas inesperadas. Un desarrollador que usa `claude-opus-4-6` para parsear 10,000 archivos de JSON está pagando el precio de un neurocirujano para hacer trabajo de administrativo. Un desarrollador que usa `gpt-5.4-nano` para diseñar la arquitectura de un sistema distribuido está confiando ese diseño al asistente más económico del equipo.

La diferencia entre un workflow de agentes eficiente y uno costoso no suele ser el código — suele ser el modelo asignado a cada paso.

Esta sección tiene dos propósitos: primero, darte el vocabulario completo para entender cualquier tabla de modelos que encuentres (tokens, context window, temperatura, thinking, naming de versiones). Segundo, organizar el catálogo actual de los tres proveedores principales por caso de uso real, no por familia de marketing.

| Concepto | Qué aprenderás |
| :--- | :--- |
| **Tokens** | La moneda de cambio de los LLMs — qué son, cómo se cuentan, por qué importan al costo |
| **Context Window** | Cuánta información puede ver el modelo simultáneamente y qué cambia con 1M tokens |
| **Temperatura** | Cómo controlar la aleatoriedad de las respuestas en tareas de código vs. creativas |
| **Thinking / Reasoning** | Qué significa activar el razonamiento profundo y cuándo tiene sentido pagarlo |
| **Naming** | Qué significan Pro, Flash, mini, nano, Lite, Haiku, Sonnet, Codex y todos los demás sufijos |
| **Catálogo por proveedor** | Los modelos activos de OpenAI, Anthropic y Google con sus context windows confirmados |
| **Modelos por caso de uso** | Qué modelo usar para arquitectura, codificación, subagentes, investigación y documentos masivos |

👉 **[Ver Guía Completa de Modelos de IA](concepts/models.md)** — incluye glosario técnico, nomenclatura de versiones, catálogo de modelos activos por proveedor, categorías de uso, guía de selección rápida y advertencias sobre modelos deprecados.

---
## 10. Metodologías de trabajo con AI

En esta sección exploramos cómo estructurar el desarrollo de software cuando se integra IA, pasando de la experimentación aleatoria a flujos de trabajo deterministas y escalables.

👉 **[Ver Guía Técnica Completa: Metodologías de trabajo con AI](Metodologías%20de%20Ingeniería%20AI-Native.md)** — incluye comparativas entre SDD, CDD, TDD+AI y workflows de agentes.
