# Contexto: La Base del Agente Senior

La base de cualquier flujo de trabajo con agentes de IA es la **persistencia del contexto**. ***Sin un mecanismo de memoria externa, cada sesión comienza desde cero***: el agente no sabe en qué proyecto trabaja, qué convenciones sigue el equipo, ni qué comandos usar para compilar y testear. 

Los archivos de reglas —  `AGENTS.md` — resuelven este problema fundacional inyectando conocimiento estructurado en el sistema del agente antes de procesar cualquier petición.

---

> [!NOTE]
> **Mi Colección Personal:** Muchos de los *templates* para contextualizar agentes los tengo ya estructurados. Si deseas ver mis carpetas para inspirarte o reutilizarlas, puedes visitar:
> 🏗️ **[Templates para Agentes](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/templates/agents)**

---

## Menos alucinación y más dirección

`AGENTS.md` no es solo un archivo de texto; es el contrato que garantiza que tu agente y tú habléis el mismo idioma desde el primer segundo. Actúa como el *System Prompt* dinámico que elimina las conjeturas del agente antes de que empiecen.

Al definir claramente este documento, logramos tres pilares clave para la eficiencia:

1. **Eliminación de la adivinación:** Sin reglas claras, el agente intenta "adivinar" tu stack, las convenciones de nombres o qué comando ejecutar para compilar. Con este archivo, transformas la incertidumbre en instrucciones blindadas.
2. **Contexto On-Demand:** El agente no pierde tiempo (ni tokens) explorando el repositorio a ciegas. El conocimiento crítico está pre-cargado, marcando el camino óptimo desde el inicio.
3. **Estándar Universal:** Ya sea que uses Cursor, Claude Code o Gemini CLI, este archivo actúa como un lenguaje común. Tus directrices son portables y se respetan en cualquier herramienta, evitando que el proyecto se fragmente.

> [!IMPORTANT]
> `AGENTS.md` es el estándar multiplataforma soportado nativamente por **Codex**, **Gemini CLI**, **Claude Code** (vía `CLAUDE.md`), **GitHub Copilot**, **OpenCode**, **Cursor** y **Antigravity**. Un solo archivo en tu raíz garantiza coherencia operativa en todo tu flujo de trabajo.

---



## Jerarquía de Autoridad: ¿Quién manda aquí?

Los agentes resuelven conflictos de información mediante una jerarquía de **"especificidad creciente"**. Las reglas definidas en subdirectorios profundos tienen autoridad absoluta sobre las globales.

```text
~/.gemini/      (Nivel Global: Tus preferencias universales)
└── mi-proyecto/
    ├── AGENTS.md        (Nivel Proyecto: Estándares compartidos)
    └── src/auth/
        └── AGENTS.md    (Nivel Módulo: Instrucciones de máxima prioridad aquí)
```

| Prioridad | Alcance | Cuándo usarlo |
| :--- | :--- | :--- |
| **Alta** | Módulo local | Aislamiento de código legacy o microservicios únicos. |
| **Media** | Proyecto | Stack tecnológico, arquitectura y convenciones de equipo. |
| **Baja** | Global | Estilo personal, idioma y preferencias de formato del usuario. |

> [!TIP]
> **No te compliques:** En el 90% de los casos, un único `AGENTS.md` en la raíz es suficiente. Utiliza archivos locales solo cuando un módulo requiera una convención que rompa radicalmente con el resto del proyecto.

---

## Si quieres un agente tonto, ponle un AGENTS.md gigante

Un `AGENTS.md` inflado no es una ventaja competitiva; es un **sabotaje arquitectónico**. Al saturar al modelo con datos innecesarios, no estás "dándole más información", estás provocando una atrofia cognitiva: el agente pierde la capacidad de distinguir la señal del ruido, diluyendo su atención y convirtiendo una inteligencia capaz en un sistema errático y perezoso. La IA no sabe filtrar lo obsoleto; si se lo das, lo procesa con el mismo costo de recursos que la instrucción crítica.

La solución es el **Principio de Revelación Progresiva**. El `AGENTS.md` raíz debe actuar como un "filtro de alta densidad" que contenga exclusivamente el ADN fundacional del proyecto. Todo lo demás —especificaciones técnicas, guías de estilo, o pruebas— debe residir en archivos secundarios. Estos solo se activan mediante una arquitectura de inyección bajo demanda, garantizando que el agente opere siempre con una **atención quirúrgica**: máxima precisión, cero carga basura.

### Ejemplo de Estructura Desacoplada

```text
mi-proyecto/
├── AGENTS.md                        (Raíz — mínimo indispensable + descriptores semánticos)
└── docs/
    ├── TYPESCRIPT.md                (Convenciones estrictas del lenguaje y linter)
    ├── TESTING.md                   (Estrategia, fixtures y comandos de pruebas)
    └── DATABASE_SCHEMA.md           (Diseño relacional y convenciones de Prisma)
```

### Sintaxis de Referenciación Dinámica

Para encadenar estos sub-archivos de forma eficiente, redacta tu AGENTS.md referenciándolos con descriptores claros, delegando al agente la decisión autónoma de si requiere su lectura o no.

**Formato recomendado en la raíz:**
```markdown
This is a Node.js GraphQL API using Prisma and TypeScript.
Build: `pnpm build`. Typecheck: `pnpm tsc --noEmit`.

For task-specific guidance, read only the documents meaningfully related to your current task:
- TypeScript conventions and types: docs/TYPESCRIPT.md
- Integration testing patterns: docs/TESTING.md
- Relational schema structure: docs/DATABASE_SCHEMA.md
```

> [!TIP]
> Usa referencias descriptivas, nunca imperativas. En vez de gritarle a la máquina: `ALWAYS read docs/TYPESCRIPT.md`, escribe `For TypeScript conventions, see docs/TYPESCRIPT.md`. El agente evaluará inteligentemente la semántica del problema; ahorrándote miles de tokens cuando, por ejemplo, le pides editar un simple archivo Markdown.

> [!WARNING]
> **El Límite de Atención: Por qué tu agente ignora tus reglas**
> Los modelos de IA tienen un límite en la cantidad de instrucciones que pueden mantener activas en su "memoria de trabajo". Si le das 5 directrices, las cumplirá a la perfección. Si le das 200 reglas de golpe, se saturará y empezará a ignorar muchas de ellas (especialmente las que están en medio del documento).
> 
> Ten en cuenta que herramientas como Cursor o Claude ya consumen parte de este límite con sus propias instrucciones internas (el *System Prompt* base). Cada regla innecesaria o redundante que añadas a tu `AGENTS.md` compite por la atención del modelo, aumentando la probabilidad de que pase por alto las instrucciones de seguridad verdaderamente críticas.


---

## Anatomía de un `AGENTS.md` de Alto Rendimiento

Un `AGENTS.md` no es un manual de usuario, es un **contrato de comportamiento**. Si el Linter o el Compilador ya pueden detectar un error, no lo escribas aquí. Este archivo debe restringirse exclusivamente a las **decisiones de diseño** que el código, por sí solo, no puede explicar.

| Capa de Conocimiento | ¿Por qué es vital? | Directriz Estratégica |
| :--- | :--- | :--- |
| **Identidad del Proyecto** | Evita que el agente asuma un contexto erróneo. | Define qué es el proyecto y qué problema resuelve. |
| **Stack y Runtime** | Bloquea al agente para que no use librerías obsoletas. | Versiones exactas de Node, framework y gestor de paquetes. |
| **Macros de Ejecución** | Garantiza que el agente ejecute los comandos correctos. | Alias o comandos únicos de build, test y linting. |
| **Criterios de Estilo** | Captura la "filosofía" que el linter ignora. | Ej: "Preferir Early Returns", "Order imports". |
| **Fronteras (Guards)** | Impide que el agente cree una arquitectura espagueti. | Define qué carpetas tienen prohibido hablar entre sí. |
| **Seguridad Innegociable** | Evita vulnerabilidades por defecto. | "Never write raw SQL", "All secrets in `.env`". |

---

## Ingeniería de Instrucciones: El Arte de la Precisión

La forma en que redactas tus reglas determina si el agente actuará como un ingeniero senior o como un becario confundido. Olvida las sugerencias abstractas; el LLM necesita **macros accionables** que reduzcan su espacio de búsqueda de soluciones.

| ❌ El Error (Ambigüedad) | ✅ La Solución (Acción) | ¿Por qué funciona? |
| :--- | :--- | :--- |
| `ALWAYS use async/await` | `Prefer async/await over Promises` | Elimina la ambigüedad en el encadenamiento. |
| `NEVER commit without tests` | `Run: pnpm test` | Fuerza la ejecución inmediata de la verificación. |
| `Write clean code` | `Use named exports; functional components only.` | Dicta una estructura sintáctica innegociable. |
| `Be careful with the database` | `Validate inputs via Zod; use Prisma ORM.` | Define la herramienta y el método de seguridad. |

---

## Plantilla de Referencia para Configuración a Producción

La plantilla a continuación ejemplifica un proyecto *Backend de Express robusto*, destiladando progresividad y agudeza técnica.

```markdown
# Project Context

This is a Node.js REST API using Express, Prisma, and TypeScript.
Package manager: pnpm. Runtime: Node.js 22.

## Commands

- Build: `pnpm build`
- Dev server: `pnpm dev`
- Tests: `pnpm test` (Vitest)
- Typecheck: `pnpm tsc --noEmit`
- Lint: `pnpm lint` (ESLint + Prettier)

## Architecture

- `src/routes/` — Express route handlers (one file per resource)
- `src/services/` — Business logic (no DB access here)
- `src/db/` — Prisma client and query helpers
- `src/types/` — Shared TypeScript interfaces and enums

## Code Conventions

- Strict TypeScript. Never use `any`.
- Named exports only. No default exports.
- All async functions must handle errors with try/catch.
- Use Zod for request validation in all routes.

## Security

- Never log secrets or tokens.
- All environment variables are in `.env.example`. Use `process.env.VAR`.
- DB queries must use Prisma — no raw SQL.

## Task-Specific Guidance

- TypeScript conventions: docs/TYPESCRIPT.md
- Testing patterns: docs/TESTING.md
- Database schema: docs/DATABASE_SCHEMA.md
```


---

## Antipatrones: Lo que bloquea tu escalabilidad

La arquitectura de contexto no es estática. Si cometes estos errores, tu `AGENTS.md` dejará de ser una ventaja y se convertirá en un cuello de botella.

| Antipatrón | El Impacto Real | La Estrategia Correcta |
| :--- | :--- | :--- |
| **Hardcoding de rutas** | Fragilidad total si mueves un archivo. | Define **fronteras lógicas** (ej. "Toda la lógica de negocio vive en `src/core/`"). |
| **Contexto Monolítico** | Saturación y pérdida de prioridad (Attention Decay). | **Revelación Progresiva:** externaliza guías a `/docs/*.md`. |
| **Conflictos de Jerarquía** | Comportamiento impredecible del agente. | **Override explícito:** aisla reglas en módulos específicos. |
| **Ignorar el Control de Versiones** | Incoherencia entre miembros del equipo/agentes. | **`git commit` obligatorio:** el `AGENTS.md` es código crítico. |

---

## Soporte y Equivalencias por Ecosistema

| Proveedor Integrado | Fichero Base Localizado   | Soporte al Estándar | Rasgos y Particularidades del Entorno                  |
| :----------------- | :------------------------ | :------------------ | :----------------------------------------------------- |
| **Codex CLI**      | `AGENTS.md`               | ✅ Nativo            | Despliega soporte singular sobre `AGENTS.override.md`. |
| **Gemini CLI**     | `GEMINI.md`               | ✅ Sí                | Barrido iterativo hacia carpetas de mayor altitud hasta topar con un nodo `.git`. |
| **Claude Code**    | `CLAUDE.md`               | ✅ Sí (Mediante Alias)| Destaca por engendrar `MEMORY.md` orgánicamente desde logs conversacionales. |
| **GitHub Copilot** | `copilot-instructions.md` | ✅ Sí                | Requiere estar estacionado estrictamente dentro el folder oculto de la organización (`.github/`). |
| **OpenCode**       | `AGENTS.md`               | ✅ Nativo            | Permite anclar `URLs` perimetrales inyectadas directamente. |
| **Cursor IDE**     | `.cursor/rules/*.mdc`     | ✅ Sí                | Sistema regido bajo activadores cruzados referenciando `Glob Patterns`. |
| **Antigravity**    | `AGENTS.md`               | ✅ Nativo            | Suma soporte híbrido permitiendo encastrar con `.agents/rules/`. |


*Fuentes Oficiales Adicionales: [AGENTS.md Open Standard](https://github.com/agentsmd/agents.md) | [A Complete Guide to AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md) | [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)*
