# AI-Agent Guide

![[summary_02.png]]

---

# 1. Instalación y Registro

## Antigravity (Google)

Descargar desde la [pagina oficial](https://antigravity.google/).

> [!tip] Si se bugea el OAuth de Antigravity en los MCP, se puede resetear eliminando los archivos de `~/.mcp-auth`

## Gemini CLI

Seguir los pasos desde la [pagina oficial](https://geminicli.com/docs/get-started/installation/).

```bash
npm install -g @google/gemini-cli
```

Lanzar desde la consola:

```shell
gemini
```

### Modos de Aprobación

Documentación completa [aqui](https://geminicli.com/docs/get-started/configuration/#security).

| Modo | Flag | Descripción |
|:-----|:-----|:------------|
| **Default** | *(ninguno)* | Solicita aprobación en cada llamada de herramienta |
| **Auto Edit** | `--approval-mode auto_edit` | Aprueba ediciones automáticamente, pregunta las demás |
| **Yolo** | `--yolo` o `Ctrl + Y` | Aprueba todo automáticamente (modo autónomo) |

> [!warning] El modo Yolo ejecuta todo sin confirmación. Si no se han validado los comandos permitidos, podria eliminar archivos o lanzar comandos peligrosos.

### Configuraciones Extras

Todas las configuraciones se hacen en: `~/.gemini/settings.json` ^gemini-path

```json
{
  "experimental": {
    "skills": true,
    "enableAgents": true
  },
  "ide": {
    "enabled": true
  }
}
```

| Clave | Descripción |
|:------|:------------|
| `experimental.skills` | Habilita las Skills |
| `experimental.enableAgents` | Habilita subagentes |
| `ide.enabled` | Comunicación con Antigravity |

## Extensiones

Nano Banana
Stich
Compositor
ralph

## Codex (OpenAI)

Codex es el agente de codificación de OpenAI. Disponible como **App de escritorio** (macOS/Windows), **extensión IDE** (VS Code, Cursor, Windsurf), **CLI**, y en la **nube** vía [chatgpt.com/codex](https://chatgpt.com/codex).

### Instalación

| Método | Comando / Acción |
|:-------|:-----------------|
| **App de escritorio** | Descargar desde [developers.openai.com/codex/quickstart](https://developers.openai.com/codex/quickstart) |
| **Extensión IDE** | Buscar `openai.chatgpt` en VS Code / Cursor / Windsurf |
| **CLI (npm)** | `npm install -g @openai/codex` |
| **CLI (Homebrew)** | `brew install codex` |
| **Cloud** | [chatgpt.com/codex](https://chatgpt.com/codex) |

**Autenticación:** Crear un API key en [platform.openai.com/api-keys](https://platform.openai.com/api-keys), o autenticarse con cuenta de ChatGPT (Plus, Pro, Business, Edu o Enterprise).

**Archivo de configuración:** `~/.codex/config.toml` ^codex-path

> [!tip] Codex CLI y la extensión IDE comparten la misma configuración. Una vez configurado, puedes cambiar entre ambos sin reconfigurar.

## Claude Code (Anthropic)

Claude Code es una herramienta de codificación agéntica. Disponible en **terminal**, **VS Code**, **Cursor**, **JetBrains**, **App de escritorio** (macOS/Windows), y en la **web** vía [claude.ai/code](https://claude.ai/code).

Documentación oficial: [docs.anthropic.com/en/docs/claude-code/overview](https://docs.anthropic.com/en/docs/claude-code/overview)

### Instalación

| Plataforma | Comando / Acción |
|:-----------|:-----------------|
| **macOS / Linux** | `curl -fsSL https://claude.ai/install.sh \| bash` |
| **Windows** | `irm https://claude.ai/install.ps1 \| iex` |
| **Homebrew** | `brew install --cask claude-code` |
| **WinGet** | `winget install Anthropic.ClaudeCode` |
| **VS Code / Cursor** | Extensión `anthropic.claude-code` |
| **JetBrains** | [Claude Code plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) |
| **Web** | [claude.ai/code](https://claude.ai/code) |

**Autenticación:** Suscripción de [Claude](https://claude.com/pricing) o via [Anthropic Console](https://console.anthropic.com/).

**Archivo de configuración:** `~/.claude.json` y `.claude/settings.local.json` (proyecto)

---

# 2. Contexto, Rules y Memoria Persistente

En el desarrollo con IA, el mayor desafío es evitar que el agente "olvide" las reglas a medida que la conversación se extiende. Esto se resuelve mediante **archivos de contexto** — documentos técnicos que definen el comportamiento del agente y persisten entre sesiones.

## Alcance (Scope)

Los archivos de contexto se organizan en tres niveles:

| Nivel | Descripción | Ejemplo |
|:------|:------------|:--------|
| **Global (Usuario)** | Instrucciones universales para todos los proyectos | "Escribe comentarios en inglés", "No uses emojis" |
| **Proyecto (Raíz)** | Reglas específicas para un repositorio | "Usa React con TypeScript", "Indentación de 2 espacios" |
| **Módulo (Subdirectorio)** | Instrucciones quirúrgicas para carpetas específicas | "En `/pagos`, usa solo la API de Stripe" |

## Archivos de Contexto por Herramienta

| Herramienta     | Archivo                   | Global                | Proyecto                              | Subdirectorio                                   |
| :-------------- | :------------------------ | :-------------------- | :------------------------------------ | :---------------------------------------------- |
| **Antigravity** | `GEMINI.md`               | `~/.gemini/GEMINI.md` | `.agent/rules/`                       | N/A                                             |
| **Gemini CLI**  | `GEMINI.md` / `AGENTS.md` | `~/.gemini/GEMINI.md` | Raíz del proyecto                     | Subdirectorios (escaneo descendente)            |
| **Codex**       | `AGENTS.md`               | `~/.codex/AGENTS.md`  | Raíz del proyecto (`.git`)            | Carpetas intermedias hasta el directorio actual |
| **Claude Code** | `CLAUDE.md`               | `~/.claude/CLAUDE.md` | `./CLAUDE.md` o `./.claude/CLAUDE.md` | Cualquier subdirectorio con `CLAUDE.md`         |

### Antigravity: Rules

Las **Rules** son instrucciones persistentes que el agente sigue para garantizar consistencia. Pueden referenciar otros archivos usando `@filename`.

- **Global**: `~/.gemini/GEMINI.md`
- **Workspace**: `.agent/rules/` dentro del proyecto
- **Activación**: Por descripciones en lenguaje natural o patrones **Glob** (ej. `src/**/*.ts`)

### Gemini CLI

Gemini CLI escanea tanto hacia arriba (ancestros) como hacia abajo (subdirectorios). Respeta estrictamente `.gitignore` y `.geminiignore`.

| Nivel | Ubicación | Impacto |
|:------|:----------|:--------|
| **Global** | `~/.gemini/GEMINI.md` | Preferencias universales del desarrollador |
| **Ancestros** | Desde el actual hasta la raíz `.git` | Contexto heredado del proyecto |
| **Subdirectorios** | Carpetas debajo de la ubicación actual | Impacto del código en otros módulos |

```
mi-organizacion/
├── .gemini/
│   └── GEMINI.md         <-- [Global] "Escribe siempre en TS, usa estilo funcional"
├── proyecto-mcp/
│   ├── .gitignore         <-- Gemini CLI no leerá lo que esté aquí
│   ├── AGENTS.md          <-- [Ancestro] "Tests con Vitest"
│   ├── apps/
│   │   ├── frontend/
│   │   │   └── AGENTS.md  <-- [Subdirectorio] "componentes Shcn"
│   │   └── api-go/
│   │       └── AGENTS.override.md  <-- [Anula] "Usa 'go test', no Vitest"
│   └── shared-utils/
│       └── .geminiignore   <-- Bloquea archivos sensibles
```

**Modularización:** Gemini permite importar instrucciones de otros archivos usando `@nombre-archivo.md`:

```
# Main GEMINI.md file
@./components/instructions.md
@../shared/style-guide.md
```

**Personalizar nombres de archivo de contexto** en ![[#^gemini-path]]:

```json
{
  "context": {
    "fileName": ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]
  }
}
```

### Codex

Codex construye una "cadena de instrucciones" por concatenación, donde **lo que se lee al final tiene prioridad**.

**Orden de precedencia:**

1. **Global:** `~/.codex/AGENTS.md` (prioriza `AGENTS.override.md` sobre `AGENTS.md`)
2. **Raíz del proyecto:** Donde está `.git`
3. **Camino al directorio actual:** En cada carpeta intermedia busca un archivo de instrucciones

```
mi-proyecto/
├── AGENTS.md                (Regla: "Usa npm test")
└── apps/
    └── api/
        └── AGENTS.override.md  (Regla: "Usa make test-api" → Anula la anterior)
```

> [!NOTE] Personaliza los nombres con `project_doc_fallback_filenames` en `config.toml`.

### Claude Code

Claude Code usa archivos `CLAUDE.md` con una lógica similar de herencia. Soporta **auto memoria** — el agente aprende y guarda conocimiento automáticamente entre sesiones.

**Ubicaciones de `CLAUDE.md`:**

| Alcance | Ubicación |
|:--------|:----------|
| **Sistema** | `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows) |
| **Global (Usuario)** | `~/.claude/CLAUDE.md` |
| **Proyecto** | `./CLAUDE.md` o `./.claude/CLAUDE.md` |
| **Subdirectorio** | Cualquier carpeta con `CLAUDE.md` |

**Importar archivos adicionales:**

```markdown
See @README for project overview and @package.json for available npm commands.
# Additional Instructions
- git workflow @docs/git-instructions.md
```

**Reglas por carpeta:** Se pueden organizar reglas modulares en `.claude/rules/*.md` para mayor control.

**Comandos útiles:**

| Comando | Descripción |
|:--------|:------------|
| `/init` | Crea un `CLAUDE.md` inicial para el proyecto |
| `/memory` | Ver y editar la memoria auto-guardada |

## Reglas de Oro

> [!caution] Contaminación de Contexto
> No satures cada carpeta con instrucciones. Si las reglas se contradicen en demasiados niveles, el comportamiento del agente se vuelve errático.

**Lista de verificación:**

- **Archivos vacíos:** Las herramientas ignoran archivos sin texto
- **Límite de tamaño:** Codex tiene un límite de **32 KiB** (`project_doc_max_bytes`)
- **Nomenclatura:** El estándar es plural: `AGENTS.md` (no `AGENT.md`)
- **Higiene de contexto:** Usa `.gitignore` / `.geminiignore` para excluir `node_modules` y carpetas temporales

## Resumen

![[summary_memo.png]]

---

# 3. Skills

Las Skills son paquetes de **experiencia bajo demanda** que extienden las capacidades del agente. A diferencia del contexto general (que define *cómo comportarse*), las Skills definen *en qué es experto* y *qué herramientas puede usar*.

El agente solo carga una Skill cuando detecta que la tarea coincide con su descripción (**progressive disclosure**), evitando saturar la ventana de contexto.

> [!note] Las Skills se invocan automáticamente cuando el agente lo detecta, o manualmente diciéndole que use una Skill específica.

### Capacidades de las Skills

- **Definir roles técnicos** (ej. "Arquitecto AWS", "Especialista en ciberseguridad")
- **Integrar herramientas de terceros** (APIs, CLIs como FFmpeg, bases de datos)
- **Estandarizar formatos de salida** (JSON, documentación ISO, código estructurado)
- **Reducir alucinaciones** al limitar el alcance de la experticia
- **Automatizar flujos complejos** (refactorizaciones, migraciones)
- **Inyectar know-how propietario** (metodologías internas, patrones de diseño)
- **Modularizar la inteligencia** (activar/desactivar Skills según la tarea)

### ¿Qué pueden invocar?

Cualquier cosa definida en el markdown: otras Skills, reglas de otras carpetas, scripts en Python/Node/Go, proyectos completos con `npm`, e incluso Skills que requieren `.env`.

## Configuración y Rutas

| Herramienta | Alcance Proyecto | Alcance Global |
|:------------|:-----------------|:---------------|
| **Antigravity** | `.agent/skills/` | `~/.agents/skills/` o `~/.gemini/antigravity/skills/` |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` |
| **Codex** | `.agents/skills/` | `~/.agents/skills/` |
| **Claude Code** | `.claude/skills/<skill>/SKILL.md` | `~/.claude/skills/<skill>/SKILL.md` |

> [!note] En todas las herramientas, una Skill es un directorio que **debe** contener al menos un archivo `SKILL.md`.

![[summary-skill.png]]

## Anatomía de una Skill

El nombre de la carpeta debe coincidir con el nombre de la Skill. La descripción debe indicar **qué hace y cuándo se activa**.

```markdown
---
name: nombre-de-la-skill
description: Una línea que explique qué hace y cuándo usarla.
Trigger: Disparador de cuando se activa (es mejor aqui que en la descripcion)
---

## Goal
Qué debe lograr el agente con esta skill.

## Context
Información de fondo que el agente necesita saber.

## Steps
1. Paso uno
2. Paso dos — ver `scripts/transform.ts` para la lógica de transformación
3. Paso tres

## Output Format
Usa `templates/report.md` como base.
Respeta cada sección del template sin omitir ni reordenar bloques.

## Examples
Revisa `examples/input-1.txt` y su resultado esperado en `examples/output-1.txt`.

## Constraints
Qué NO debe hacer el agente.
```

## Metadata del Frontmatter

La metadata vive en el frontmatter YAML al inicio del `SKILL.md`, entre los `---`. Es lo **único que el agente siempre lee** — el resto del archivo se carga solo cuando la Skill es activada.

```markdown
---
← AQUI va la metadata (siempre en contexto)
---

# El resto del skill... (se carga al activarse)
```

Cada Skill tiene **3 capas de carga progresiva**:

```
skill-name/
├── SKILL.md              ← Siempre en contexto (metadata + instrucciones)
├── scripts/              ← Codigo ejecutable determinístico
├── references/           ← Docs técnicos cargados bajo demanda
└── assets/               ← Templates, fonts, iconos
```

### Campos de Metadata Explicados

#### `name` — Identificador único

```yaml
name: sql-query-optimizer
```

Nombre interno de la Skill. Debe ser en **minúsculas con guiones**, descriptivo del **qué hace** (no del cómo), y único en tu colección.

#### `description` — El campo más importante

```yaml
description: >
  Analiza y optimiza queries SQL lentos. Úsalo cuando el usuario mencione
  queries lentos, índices, EXPLAIN ANALYZE, N+1 problems, o cualquier
  problema de performance en base de datos. Aplica aunque el usuario
  solo diga "mi query está lento" sin dar más contexto.
```

> [!important] La `description` es literalmente el mecanismo de trigger
> El agente lee solo `name` + `description` de todas las Skills disponibles, y decide cuál usar basándose en esto. Debe tener dos partes:
> 1. **Qué hace:** Una oración clara del propósito
> 2. **Cuándo usarla:** Ejemplos de frases del usuario que deben activarla

El `>` en YAML significa "string multilínea sin saltos de línea literales". Es el formato recomendado para descriptions largas.

#### `trigger` — Disparador explícito

```yaml
trigger: >
  Cuando el usuario mencione "query lento", "EXPLAIN ANALYZE",
  "N+1", "índices", o cualquier variación de performance en SQL.
```

Separa el **cuándo activar** la Skill del **qué hace**. Mientras `description` explica el propósito general, `trigger` lista las frases y palabras clave exactas que deben activar la Skill. Es más preciso ponerlo aquí que mezclarlo en la descripción.

> [!tip] Usar `trigger` separado del `description` evita que la descripción se vuelva demasiado larga y mantiene clara la intención de cada campo.

#### `compatibility` — Dependencias técnicas

```yaml
compatibility:
  tools: [bash, file_create, present_files]
  python_packages: [pandas, polars]
  node_packages: [tsx, zod]
  required_env: [AWS_REGION, PROJECT_NAME]
  optional_env: [TERRAFORM_VERSION]
  min_python: "3.11"
```

Le dice al agente (y al usuario) qué necesita tener instalado. Si falta un tool requerido, el agente debería avisar al usuario antes de intentar ejecutar.

#### `version` y `author` — Control de cambios

```yaml
version: "2.1"
author: platform-team
created: "2025-01"
updated: "2025-11"
```

Útil cuando varias personas trabajan en las mismas Skills. No afecta el comportamiento del agente, pero ayuda a saber qué versión está instalada.

#### `tags` — Organización y búsqueda

```yaml
tags: [infrastructure, cloud, terraform, devops, aws]
```

Para categorizar Skills en repositorios grandes (50+ skills). El agente no los usa para decidir si activar la Skill, pero los sistemas de gestión sí los usan.

### Campos Custom — Lo más poderoso

Puedes definir cualquier campo que tenga sentido para tu Skill. El agente los lee como contexto adicional.

**Para Skills de contenido:**

```yaml
style:
  tone: technical-but-approachable
  length: 1500-3000 words
  audience: mid-senior engineers
  code_blocks: always
output_formats: [markdown, mdx, html]
```

**Para Skills de review/análisis:**

```yaml
review_dimensions:
  - security
  - performance
  - maintainability
severity_levels: [critical, warning, suggestion, nitpick]
```

**Para Skills de generación de código:**

```yaml
output_structure:
  always_include: [error_handling, types, tests]
  language_default: typescript
  framework_detection: automatic
```

**Para Skills con múltiples modos:**

```yaml
modes:
  quick: "Respuesta en <2 minutos, sin archivos"
  full: "Análisis completo con archivos descargables"
default_mode: quick
```

### Comparativa de Campos de Metadata

| Campo | Cuándo usarlo |
|:------|:-------------|
| `name` | **Siempre.** Identificador único |
| `description` | **Siempre.** Explica qué hace la Skill |
| `trigger` | Cuando quieres separar el **cuándo activar** del **qué hace** |
| `compatibility` | Cuando requieres tools específicos o env vars |
| `version` + `author` | Skills de equipos o con historial de cambios |
| `tags` | Skills en repositorios grandes para búsqueda |
| `style` | Skills de generación de contenido |
| `output_formats` | Cuando el output puede variar |
| `review_dimensions` | Skills de evaluación/análisis estructurado |
| `severity_levels` | Skills que clasifican o priorizan |

### Resumen Visual de Metadata

```
metadata
├── name          → ID único de la skill
├── description   → Qué hace la skill (lo más importante)
├── trigger       → Cuándo activarla (frases y keywords exactas)
├── version       → Control de cambios
├── author        → Quién la mantiene
├── tags          → Categorización para repositorios grandes
├── compatibility → Qué tools/packages necesita para funcionar
└── [custom]      → Cualquier campo relevante para tu skill:
    ├── style     → Tono, longitud, audiencia (skills de contenido)
    ├── modes     → Modos de operación
    ├── output    → Formato y estructura del output
    └── ...       → Lo que necesites
```

> [!tip] Solo `name` y `description` son técnicamente requeridos. Todo lo demás es contexto adicional que ayuda al agente a tomar mejores decisiones. Entre más específica y rica sea la metadata, más predecible y consistente será el comportamiento.

## Anatomía de un Template

Se usa `{{param}}` para variables y `---` para separar secciones:

```markdown
<!-- templates/report.md -->
# {{title}}

**Date:** {{date}}
**Author:** {{author}}

---

## Summary
{{summary}}

## Findings
{{findings}}

## Recommendations
{{recommendations}}

---
_Report generated by: {{skill_name}}_
```

## Estructuras de Carpeta

#### 1. Skill Básica

```
my-skill/
├── SKILL.md
└── README.md
```

---

#### 2. Skill + Scripts

La Skill describe el *qué*, los scripts hacen el *cómo* técnico. Ideal cuando la Skill necesita ejecutar código auxiliar (parsers, validadores).

```
my-skill/
├── skill/
│   └── SKILL.md
├── scripts/
│   ├── generate.ts
│   └── validate.ts
└── README.md
```

---

#### 3. Skill + Templates

El agente debe generar documentos con estructura fija y consistente.

```
my-skill/
├── skill/
│   └── SKILL.md
├── templates/
│   ├── report.md
│   └── email.md
└── README.md
```

---

#### 4. Skill con Entorno Completo

Para Skills que necesitan acceder a APIs o servicios externos con credenciales.

```
my-skill/
├── .env.example
├── .env                  ← valores reales (no commitear)
├── skill/
│   └── SKILL.md
├── src/
│   └── index.ts
├── package.json
└── tsconfig.json
```

---

#### 5. Múltiples Skills en un Mismo Repo

```
my-skills/
├── skills/
│   ├── summarize/
│   │   └── SKILL.md
│   ├── translate/
│   │   └── SKILL.md
│   └── extract/
│       └── SKILL.md
├── shared/
│   └── utils.ts
└── README.md
```

---

#### 6. Skill + Ejemplos de Referencia (Few-Shot)

Los ejemplos muestran al agente qué output se espera — más efectivos que describirlo en palabras.

```
my-skill/
├── skill/
│   └── SKILL.md
├── examples/
│   ├── input-1.txt
│   ├── output-1.txt
│   ├── input-2.txt
│   └── output-2.txt
└── README.md
```

## Descargas y Recomendaciones

![[skillsh.png]]

Se pueden descargar Skills en [skills.sh](https://skills.sh/).

> [!important] Revisar las auditorías de seguridad antes de instalar. Algunas advertencias son porque la Skill usa servidores SaaS externos que integran varios MCP.

### Skills Recomendadas

#### Vercel-react-best-practices
Ayuda al agente a crear mejores componentes React: evita sobrerenderizado, crea componentes atómicos, documenta mejor y evita smell code de React/Next.

#### ClickUp de [civitai](https://skills.sh/civitai/civitai)

Alternativa si el MCP de ClickUp no funciona. Ejecuta comandos a ClickUp vía API con token de autenticación.

**Configuración:**

1. Copiar `.env.template` a `.env` en la carpeta de la skill (`~/.agents/skills/clickup`) y rellenar las variables (o exportar `CLICKUP_API_TOKEN=<TOKEN>`)
2. Ejecutar `npm install` dentro de la carpeta de la skill

```shell
npx skills add https://github.com/civitai/civitai --skill clickup
```

Si falta `package.json`, usar este:

```json
{
  "name": "clickup-skill",
  "version": "1.0.0",
  "description": "ClickUp skill for Antigravity",
  "type": "module",
  "dependencies": {
    "unified": "^11.0.4",
    "remark-parse": "^11.0.0",
    "dotenv": "^16.3.1",
    "node-fetch": "^3.3.2"
  }
}
```

## Tipos de Skills — Ejemplos Avanzados

### 1. Skill Simple — Tarea específica

Un solo archivo, sin dependencias. Ideal para tareas enfocadas.

```markdown
---
name: sql-query-optimizer
description: >
  Analiza y optimiza queries SQL lentos. Úsalo cuando el usuario mencione
  queries lentos, índices, EXPLAIN ANALYZE, N+1 problems, o cualquier
  problema de performance en base de datos. Aplica aunque el usuario
  solo diga "mi query está lento" sin dar más contexto.
---

# SQL Query Optimizer

## Tu rol
Eres un experto en optimización de bases de datos. Analiza el query dado,
identifica el problema y propón una versión optimizada con explicación.

## Proceso
1. Detecta el motor (PostgreSQL, MySQL, SQLite, etc.)
2. Identifica anti-patterns: SELECT *, N+1, missing indexes, full table scans
3. Propón el query optimizado
4. Explica el cambio con métricas esperadas

## Output format
-- ANTES (problema identificado: X)
SELECT ...

-- DESPUÉS (optimización: índice compuesto en col_a, col_b)
SELECT ...

Estimado de mejora: ~10x en tablas >100k rows.
```

---

### 2. Skill con Recursos Bundleados — Multi-archivo

Incluye scripts ejecutables, referencias técnicas y templates.

```markdown
---
name: api-documentation-generator
description: >
  Genera documentación completa de APIs REST o GraphQL en formato OpenAPI 3.0,
  Markdown o Postman Collection. Úsalo cuando el usuario quiera documentar
  endpoints, generar swagger, o crear colecciones de Postman desde código.
compatibility:
  tools: [bash, file_create, present_files]
  python_packages: [pyyaml]
---

# API Documentation Generator

## Recursos disponibles
- `references/openapi-3.0-spec.md` — Spec completa de OpenAPI
- `references/postman-schema.md` — Schema de Postman Collections v2.1
- `scripts/parse_routes.py` — Extrae rutas de Express/FastAPI/Django
- `assets/openapi-template.yaml` — Template base con autenticación

## Flujo principal
1. **Detectar framework** — Express, FastAPI, Django REST, NestJS, etc.
2. **Extraer endpoints** — `python scripts/parse_routes.py --file <path> --framework <fw>`
3. **Generar docs** — Usar `assets/openapi-template.yaml` como base
4. **Output** — Siempre generar archivo descargable, nunca solo texto en chat
```

---

### 3. Skill Avanzado con Metadata Extendida

Metadata rica para Skills multi-dominio con checklists de seguridad.

```markdown
---
name: cloud-infrastructure-deployer
description: >
  Genera Infrastructure as Code (IaC) para AWS, GCP o Azure: Terraform,
  Pulumi o CDK. Úsalo para cualquier tarea de deploy, configuración de
  recursos cloud, redes VPC, IAM roles, o arquitecturas serverless.
compatibility:
  tools: [bash, file_create, present_files]
  required_env: [AWS_REGION, PROJECT_NAME]
  optional_env: [TERRAFORM_VERSION]
version: "2.1"
author: platform-team
tags: [infrastructure, cloud, terraform, devops]
---

# Cloud Infrastructure Deployer

## Selección de dominio

| Cloud | Archivo de referencia |
|:------|:---------------------|
| AWS   | `references/aws.md`  |
| GCP   | `references/gcp.md`  |
| Azure | `references/azure.md`|

## Checklist de seguridad (siempre aplicar)
- [ ] No hay credenciales hardcodeadas
- [ ] IAM roles siguen principio de mínimo privilegio
- [ ] Recursos en VPC privada cuando aplique
- [ ] Encryption at rest habilitada en storage
- [ ] Logs habilitados
```

---

### 4. Skill con Scripts Ejecutables — Data Pipeline

Scripts que el agente ejecuta directamente como parte del flujo.

```markdown
---
name: data-pipeline-builder
description: >
  Construye pipelines de datos en Python (pandas, polars, dbt, o PySpark)
  con validación, tests y documentación. Úsalo cuando el usuario quiera
  transformar datos, limpiar CSVs, construir ETLs, o procesar datasets.
compatibility:
  tools: [bash, file_create, present_files]
  python_packages: [pandas, polars, great_expectations, pytest]
---

# Data Pipeline Builder

## Scripts disponibles (ejecutar directamente)
- `scripts/profile_data.py` — Genera perfil estadístico del dataset
- `scripts/detect_schema.py` — Infiere schema y tipos de datos
- `scripts/run_quality_checks.py` — Ejecuta validaciones

## Selección de engine según tamaño
| Tamaño | Engine recomendado |
|:-------|:-------------------|
| < 1M rows | pandas |
| 1M–100M rows | polars |
| > 100M rows | PySpark |
```

---

### 5. Skill de Contenido con Metadata de Estilo

Controla tono, longitud, audiencia y formato del output.

```markdown
---
name: technical-blog-writer
description: >
  Escribe artículos técnicos de alta calidad para blogs de ingeniería.
  Úsalo cuando el usuario quiera escribir un blog post técnico, artículo
  para Medium/Dev.to/Hashnode, o documentación narrativa.
style:
  tone: technical-but-approachable
  code_blocks: always
  diagrams: mermaid-preferred
  length: 1500-3000 words
  audience: mid-senior engineers
output_formats: [markdown, mdx, html]
---

# Technical Blog Writer

## Estructura obligatoria
1. **Título** (problema real, no clickbait)
2. **TL;DR** — Una oración con el valor del post
3. **El problema** — Historia real o pain point
4. **Por qué las soluciones comunes fallan** — Contexto crítico
5. **La solución** — Con código real y ejecutable
6. **Tradeoffs** — Honestidad técnica = credibilidad
7. **Conclusión** — Qué aprendió el lector, próximos pasos
```

---

### 6. Skill de Workflow Complejo — Code Review

Skill con dimensiones de evaluación y niveles de severidad.

```markdown
---
name: code-review-assistant
description: >
  Realiza code reviews exhaustivos: seguridad, performance, mantenibilidad,
  tests, y adherencia a patrones del proyecto. Úsalo para cualquier PR review
  o revisión de código antes de merge.
review_dimensions:
  - security
  - performance
  - maintainability
  - test_coverage
  - patterns
severity_levels: [critical, warning, suggestion, nitpick]
---

# Code Review Assistant

## Proceso de review (siempre en este orden)

### 1. Pass de seguridad (SIEMPRE primero)
- Injection vulnerabilities (SQL, command, SSTI)
- Secrets hardcodeados
- Auth/authz incorrectos
- Inputs no sanitizados

### 2. Pass de performance
- Queries N+1
- Loops anidados innecesarios O(n²)
- Async/await mal usado (await en loops)

### 3. Pass de mantenibilidad
- Funciones >50 líneas (candidatas a extraer)
- Duplicación de código
- Magic numbers/strings

### 4. Resumen ejecutivo al final
- Critical: N issues (MUST fix before merge)
- Warnings: N issues (should fix)
- Suggestions: N issues (nice to have)
- Overall: Approved / Changes Requested / Blocked
```

---

### 7. Integración con CLI (FFmpeg)

Las Skills instruyen al agente sobre **cómo** usar su capacidad de terminal para operar herramientas complejas.

```markdown
---
name: video-optimizer
description: >
  Activa cuando el usuario quiera comprimir, convertir o extraer audio
  de videos usando FFmpeg. Aplica aunque solo diga "comprimir video".
---

# Experto en FFmpeg

### Reglas de Operación:
1. **Detección**: Verifica si `ffmpeg` está instalado ejecutando `ffmpeg -version`.
2. **Compresión Web**: `ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4`
3. **Extracción de Audio**: `ffmpeg -i input.mp4 -q:a 0 -map a output.mp3`

### Ejecución:
- Siempre muestra el comando al usuario antes de ejecutarlo.
- Si falla, analiza el stderr y propón una corrección.
```

---

### 8. Skill con Tool de MCP (Codex)

```markdown
---
name: doc-search-helper
description: >
  Úsalo para buscar en la documentación técnica oficial cuando el usuario
  pregunte sobre APIs. No inventar, solo citar fuentes reales.
---

# Asistente de Documentación

1. No inventes APIs.
2. Usa la herramienta `search_docs` proporcionada por el servidor MCP.
3. Cita la URL fuente devuelta por la herramienta.
```

Configuración adicional para Codex (`agents/openai.yaml`):

```yaml
interface:
  display_name: "Buscador de Docs Oficiales"

dependencies:
  tools:
    - type: "mcp"
      value: "documentation-server"
      description: "Servidor MCP de documentación técnica"
      transport: "stdio"
```

---

### 9. Skill Real Completa — Ejemplo consolidado

Ejemplo que muestra todos los campos de metadata juntos en una Skill funcional:

```markdown
---
name: typescript-refactor-assistant
description: >
  Refactoriza código TypeScript legacy: mejora tipos, elimina any, aplica
  patrones modernos (Result types, Zod validation, fp-ts). Úsalo cuando
  el usuario quiera mejorar código TypeScript existente, eliminar any,
  agregar validación de runtime, o modernizar código viejo. Aplica aunque
  solo diga "mejorar este código" o "esto está feo".
version: "1.3"
author: dev-tools-team
tags: [typescript, refactoring, types, quality]
compatibility:
  tools: [bash, file_create, present_files]
  node_packages: [typescript, zod, tsx]
  min_node: "18"
style:
  always_generate_types: true
  prefer_functional: true
  error_handling: result-type
output:
  format: typescript
  always_include: [types, validation, tests]
  file_structure: single-file-unless-asked
---

# TypeScript Refactor Assistant
...
```

---

# 4. MCP (Model Context Protocol)

El MCP conecta los agentes con herramientas externas y contexto. Permite acceso a documentación de terceros e interacción con herramientas como GitHub, Figma, ClickUp, etc.

![[mcp_01.png | 500]]

## Archivos de Configuración

| Herramienta | Ruta | Formato |
|:------------|:-----|:--------|
| **Antigravity** | `~/.gemini/antigravity/mcp_config.json` | JSON |
| **Gemini CLI** | `~/.gemini/settings.json` | JSON |
| **Codex** | `~/.codex/config.toml` | TOML |
| **Claude Code** | `~/.claude.json` (user) / `.mcp.json` (proyecto) | JSON |

^config-paths

## Tools

Las **Tools** son las funciones/acciones que el MCP habilita para el agente.

> [!important] Seguridad de Tools
> Los MCP pueden habilitar muchas tools. Es **mejor activar solo las necesarias** para evitar que el agente alucine al tener que elegir entre demasiadas opciones. Cada herramienta suele incluir documentación para habilitar/deshabilitar tools individuales.

### Deshabilitar Tools por Herramienta

| Herramienta     | Propiedad                                                                        | Ejemplo              |
| :-------------- | :------------------------------------------------------------------------------- | :------------------- |
| **Antigravity** | `"disabledTools": [...]` en el JSON del MCP                                      | Ver ejemplos abajo   |
| **Gemini CLI**  | `"excludeTools": [...]` dentro del MCP, o `"tools": { "exclude": [...] }` global | Ver sección ClickUp  |
| **Codex**       | `disabled_tools = [...]` o `enabled_tools = [...]` en `config.toml`              | Ver Codex MCP docs   |
| **Claude Code** | Via CLI: opciones al agregar el server                                           | `claude mcp add ...` |

## GitHub MCP

Documentación oficial: [github.com/github/github-mcp-server](https://github.com/github/github-mcp-server)

**Requisito previo:** Configurar la variable de entorno `GITHUB_PERSONAL_ACCESS_TOKEN` en el sistema.

### Configuración Preferida (con tools desactivadas)

**JSON** (Antigravity / Gemini CLI):

> ![Note]
> En antigravity hay que colocar las variables en .env usando los expansores en linus $

```json
"github-mcp-server": {
  "command": "docker",
  "args": [
    "run", "-i", "--rm", "-e",
    "GITHUB_PERSONAL_ACCESS_TOKEN",
    "ghcr.io/github/github-mcp-server:v0.30.3"
  ],
}
```

**Alternativa con `.env` explícito** (si la variable de entorno del sistema no funciona):

```json
"github-mcp-server": {
  "command": "docker",
  "args": [
    "run", "-i", "--rm", "-e",
    "GITHUB_PERSONAL_ACCESS_TOKEN",
    "ghcr.io/github/github-mcp-server"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
  }
}
```



**TOML** (Codex):

```toml
[mcp_servers.github-mcp-server]
command = "docker"
args = ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"]
enabled = true

[mcp_servers.github-mcp-server.env]
GITHUB_PERSONAL_ACCESS_TOKEN = "<YOUR_TOKEN>"
```

![[git-hub-mcp-01.png]]

**Claude Code:**

```shell
claude mcp add --transport stdio github -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
```

### Tools para excluir

| Herramienta | Json Key      |
| ----------- | ------------- |
| Antigravity | disabledTools |
| Gemini Cli  | excludeTools  |


```json
  [
    "sub_issue_write", "request_copilot_review", "merge_pull_request",
    "issue_read", "issue_write", "get_team_members", "get_teams",
    "get_release_by_tag", "get_tag", "delete_file", "fork_repository",
    "assign_copilot_to_issue", "add_issue_comment", "create_repository",
    "list_issue_types", "list_issues", "list_releases", "list_tags",
    "list_pull_requests", "create_or_update_file", "search_issues",
    "get_latest_release", "add_comment_to_pending_review"
  ]
```

### Problema con Docker: Múltiples Instancias

> [!warning] Docker levanta instancias nuevas por cada ventana del IDE, consumiendo muchos recursos.

**Solución:** Correr un solo contenedor persistente y conectar todos los IDEs:

```shell
docker run -d -i --name github-mcp --restart unless-stopped -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server:v0.30.3 stdio
```

Configuración usando `exec` en lugar de `run`:

```json
"github-mcp-server": {
  "command": "docker",
  "args": [
    "exec", "-i", "github-mcp",
    "/server/github-mcp-server", "stdio"
  ],
  "disabledTools": [
    "sub_issue_write", "request_copilot_review", "merge_pull_request",
    "issue_read", "issue_write", "get_team_members", "get_teams",
    "get_release_by_tag", "get_tag", "delete_file", "fork_repository",
    "assign_copilot_to_issue", "add_issue_comment", "create_repository",
    "list_issue_types", "list_issues", "list_releases", "list_tags",
    "list_pull_requests", "create_or_update_file", "search_issues",
    "get_latest_release", "add_comment_to_pending_review"
  ]
}
```

>[!Warning]
>Si el token se vence o se cambia se debe eliminar el contenedor y volverlo a correr para que se inyecten de nuevo las nuevas variables de entorno

## ClickUp MCP

Documentación oficial: [developer.clickup.com](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server-1)

Autenticación mediante **OAuth**.

![[clickup-oauth-01.jpg|500]]

> [!warning] Si el agente no funciona luego de activar ClickUp MCP, deshabilitar la tool `clickup_get_workspace_hierarchy`.

### Configuración Preferida (con tools desactivadas)

**JSON** (Antigravity / Gemini CLI):

```json
"clickup": {
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://mcp.clickup.com/mcp"],
}
```

### Tools para excluir

| Herramienta | Json Key      |
| ----------- | ------------- |
| Antigravity | disabledTools |
| Gemini Cli  | excludeTools  |

```json
[
    "clickup_get_workspace_hierarchy",
    "clickup_start_time_tracking", "clickup_stop_time_tracking",
    "clickup_add_time_entry", "clickup_get_current_time_entry",
    "clickup_create_document", "clickup_create_document_page",
    "clickup_update_document_page", "clickup_get_chat_channels",
    "clickup_send_chat_message", "clickup_get_task_time_entries",
    "clickup_attach_task_file", "clickup_find_member_by_name"
  ]
```

**TOML** (Codex):

```toml
[mcp_servers.clickup-mcp]
enabled = true
url = "https://mcp.clickup.com/mcp"
```

![[clickup-codex-01.0.png |600]]
![[clickup-codex-02.jpg|600]]

**Claude Code:**

```shell
claude mcp add --transport http clickup https://mcp.clickup.com/mcp
```

### Autenticación por Herramienta

| Herramienta | Procedimiento |
|:------------|:-------------|
| **Antigravity** | Se abre ventana OAuth automáticamente |
| **Gemini CLI** | Ejecutar `/mcp auth clickup` dentro de Gemini CLI |
| **Codex** | Settings → Open MCP Settings → Autentificar |
| **Claude Code** | `claude mcp login clickup` |

![[clickup_gemini_01.png]]

### Excluir Tools en Gemini CLI

Opción 1 — dentro del MCP:
```json
"mcpServers": {
  "clickup": {
    "excludeTools": ["clickup_get_workspace_hierarchy"]
  }
}
```

Opción 2 — exclusión global:
```json
"tools": {
  "exclude": ["clickup_get_workspace_hierarchy"]
}
```

## Figma MCP (Oficial)

Documentación: [developers.figma.com](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)

| Herramienta | Método |
|:------------|:-------|
| **Antigravity** | Solo via Dev Mode (requiere cuenta **PRO**) |
| **Gemini CLI** | `gemini extensions install https://github.com/figma/figma-gemini-cli-extension` → `/mcp auth figma` |
| **Codex** | Desde ventana de configuración MCP → Instalar y autentificar |
| **Claude Code** | `claude mcp add --transport http figma https://mcp.figma.com/mcp` |

![[figma-gemini.png]]
![[code-git-hub.png]]

## Figma Console MCP

Repositorio: [github.com/southleft/figma-console-mcp](https://github.com/southleft/figma-console-mcp)

> [!note] Requiere la aplicación **desktop** de Figma para funcionar.

**Configuración JSON:**

```json
"figma-console": {
  "command": "npx",
  "args": ["-y", "figma-console-mcp@latest"],
  "env": {
    "FIGMA_ACCESS_TOKEN": "figd_YOUR_TOKEN_HERE",
    "ENABLE_MCP_APPS": "true"
  }
}
```

**Pasos adicionales:**

1. Instalar el plugin en Figma Desktop y abrir un archivo
2. Obtener la ruta del manifest: `npx figma-console-mcp@latest --print-path`

**Tools recomendadas para deshabilitar** (edición y obtención de data):

```json
"disabledTools": [
  "ds_dashboard_refresh", "token_browser_refresh",
  "figma_audit_design_system", "figma_browse_tokens",
  "figma_check_design_parity", "figma_generate_component_doc",
  "figma_get_design_changes", "figma_get_file_for_plugin",
  "figma_reconnect", "figma_get_comments", "figma_delete_comment",
  "figma_rename_mode", "figma_add_mode",
  "figma_arrange_component_set", "figma_add_component_property",
  "figma_edit_component_property", "figma_delete_component_property",
  "figma_setup_design_tokens", "figma_batch_create_variables",
  "figma_batch_update_variables", "figma_create_variable_collection",
  "figma_rename_variable", "figma_delete_variable",
  "figma_delete_variable_collection", "figma_get_console_logs",
  "figma_take_screenshot", "figma_watch_console",
  "figma_reload_plugin", "figma_clear_console",
  "figma_navigate", "figma_get_status"
]
```

## Figma MCP de [Antonytm](https://github.com/Antonytm/figma-mcp-server) (Open Source)

Alternativa de código abierto que usa un sandbox local (sin servidores de terceros). Explicación: [ver](https://exdst.com/posts/20251222-figma-mcp-server).

> [!note] Requiere la aplicación **desktop** de Figma.

**Instrucciones:**

1. Clonar el repositorio: `https://github.com/Antonytm/figma-mcp-server`
2. En la carpeta `plugin`: `npm install && npm run build`
3. En Figma Desktop: *click derecho → plugins → development → import plugins* → seleccionar `manifest.json` de la carpeta plugins
4. En la carpeta `mcp` del proyecto clonado: `npm install && npm run start`
5. Configurar el MCP:

```json
"figma-antony": {
  "serverUrl": "http://localhost:38450/mcp"
}
```

> [!important] El plugin y el servidor deben iniciarse cada vez que se quiera usar el MCP.

## Trello MCP

**Variables de entorno requeridas:** `TRELLO_API_KEY` y `TRELLO_TOKEN` (generar en la página de Trello).

**Sin `.env` en el JSON** (variable de entorno del sistema):

```json
"trello": {
  "command": "npx",
  "args": ["-y", "mcp-server-trello"]
}
```

**Con `.env` en el JSON:**

```json
"trello": {
  "command": "npx",
  "args": ["-y", "mcp-server-trello"],
  "env": {
    "TRELLO_API_KEY": "<TRELLO_API_KEY>",
    "TRELLO_TOKEN": "<TRELLO_TOKEN>"
  }
}
```

## Recursos para buscar MCP

Docker Hub ofrece una página para instalar MCPs de diferentes servicios: [hub.docker.com/r/mcp/github](https://hub.docker.com/r/mcp/github)

---

# 5. Workflows / Commands

Los Workflows son secuencias de pasos que el usuario activa manualmente para automatizar procesos.

## Por Herramienta

| Herramienta | Ubicación | Invocación | Notas |
|:------------|:----------|:-----------|:------|
| **Antigravity** | `.agent/workflows/` | Comando `/` en el chat | Límite de 12,000 caracteres. El agente puede crearlos automáticamente |
| **Codex** | `.agents/skills/` (integrado con Skills) | Comando `/` | Se integran con las Skills via `agents/openai.yaml` |
| **Claude Code** | `.claude/skills/<skill>/SKILL.md` (custom commands) | Comando `/skill-name` | Skills con `name` en frontmatter se convierten en comandos |

Lo ideal es diseñar una lista de pasos y especificar que use una Skill que define qué tools y MCP puede llamar.

![[work-flow-01.png]]

### Ejemplo de Workflow (Antigravity)

```markdown
---
description: Este workflow extrae el ID del ticket desde el branch y busca detalles en ClickUp.
---

## Pasos del Workflow

1. **Identificar Branch**: Revisa el nombre del branch actual.
2. **Extraer ID**: Busca el patrón `-ticket` al final del nombre del branch.
3. **Consultar ClickUp**: Usa el MCP de ClickUp para encontrar el ID extraído.
4. **Resumir**: Muestra el estado del ticket, nombre de la tarea y dependencias bloqueantes.

## Instrucciones para el Agente

- Si el branch no termina en un ID válido (ej: `feature/login-abc1234`), detén el proceso e informa al usuario.
- Una vez encontrado el ticket, verifica si la descripción coincide con los cambios del código actual.
```

### Skills Integradas en Claude Code

Claude Code incluye **skills integradas** que se invocan con `/`:

| Comando | Descripción |
|:--------|:------------|
| `/simplify` | Revisa archivos recientes buscando mejoras de calidad, reuso y eficiencia |
| `/batch <instrucción>` | Orquesta cambios a gran escala en paralelo usando subagentes |
| `/debug [descripción]` | Diagnostica problemas en la sesión actual |
| `/loop [intervalo] <prompt>` | Ejecuta un prompt repetidamente en intervalos |
| `/claude-api` | Carga referencia de la API de Claude para tu lenguaje |

---

# 6. Skill vs MCP

Los MCP extienden al agente con **herramientas externas**, mientras que las Skills lo extienden con **nuestras herramientas** — pero las Skills pueden incluir a los MCP como parte de su utilidad.

En resumen: las Skills le enseñan al agente **cómo usar** el MCP correctamente. En lugar de exponer todas las tools, puedes dejar explícito cuáles usar.

> [!important] Las Skills son los elementos con mayor poder de extensión, ya que funcionan con todo lo demás: MCP, contexto, subagentes y hooks.

---

# 7. Subagentes

Los **subagentes** (subagents) son “especialistas” que trabajan **dentro de tu sesión principal** pero con:

- **Contexto separado** (no ensucian el historial/context window del agente principal).
- **Prompt/sistema propio** (persona y foco distintos).
- **Tooling acotado** (puedes limitar qué herramientas pueden usar).

> [!warning] En Gemini CLI son una feature **experimental** y pueden operar en “YOLO mode” (pueden ejecutar tools sin confirmación por cada paso). Ten cuidado si les das herramientas potentes como ejecución de shell o escritura.

## Qué son y por qué sirven

- **Delegación limpia**: el agente principal “contrata” un subagente para tareas pesadas (análisis profundo, lookup de docs, etc.) y luego el subagente devuelve **hallazgos**.
- **Ahorro de tokens**: el trabajo ocurre en un bucle aislado; el principal recibe un resumen.

## Cómo se usan (en prompts)

- **Delegación automática**: el agente principal puede decidir usar un subagente si encaja con la tarea.
- **Forzar un subagente con `@`**: escribe `@<nombre_del_agente> <tarea>` al inicio del prompt para ir directo al especialista.

Ejemplo:

```text
@codebase_investigator Map out the relationship between the AgentRegistry and the LocalAgentExecutor.
```

## Subagentes integrados (built-in)

- **`codebase_investigator`**: investiga y “reverse engineer” del código (dependencias, flujos, arquitectura).
- **`cli_help`**: experto en el propio Gemini CLI (comandos, configuración, troubleshooting).
- **`generalist_agent`**: enrutador interno (normalmente no lo invocas).
- **`browser_agent`** (preview/experimental): automatiza navegación web (clicks, formularios, extracción).  
  - **Requisitos**: Chrome (reciente; la doc menciona v144+), Node.js con `npx`.  
  - **Restricciones de seguridad**: bloquea `file://`, `javascript:`, `data:text/html`, y varias páginas sensibles de Chrome; acciones sensibles (rellenar/subir/enviar) suelen requerir confirmación por política.

## Crear subagentes personalizados

### 1) Habilitar agentes experimentales

Para usar **agentes personalizados**, activa la feature en tu `settings.json`:

```json
{
  "experimental": { "enableAgents": true }
}
```

### 2) Dónde colocar los agentes (archivos `.md`)

Los agentes personalizados se definen como **Markdown (`.md`) con YAML frontmatter** y puedes ponerlos en:

- **Nivel proyecto (compartible con equipo)**: `.gemini/agents/*.md`
- **Nivel usuario (personal)**: `~/.gemini/agents/*.md`

El **cuerpo** del `.md` (debajo del frontmatter) es el **System Prompt** del subagente.

### 3) Formato del archivo (YAML frontmatter) y qué hace cada campo

Ejemplo (estructura):

```text
---
name: security-auditor
description: Especialista en detectar vulnerabilidades.
kind: local
tools:
  - read_file
  - grep_search
model: gemini-3-flash-preview
temperature: 0.2
max_turns: 10
timeout_mins: 10
---

<system prompt del agente aquí>
```

Campos importantes:

- **`name`** *(obligatorio)*: identificador único (solo minúsculas, números, guiones/underscores). Es el “nombre de tool” del agente.
- **`description`** *(obligatorio)*: describe **cuándo** debe usarse; esto afecta si el agente principal lo elige automáticamente.
- **`kind`**: `local` (por defecto) o `remote` (para Agent2Agent, experimental).
- **`tools`**: lista de herramientas permitidas.  
  - Si **se omite**, el subagente **hereda** todas las tools del contexto padre.  
  - **Wildcards** útiles:
    - `*` = todas las tools disponibles (built-in + descubiertas)
    - `mcp_*` = todas las tools de todos los MCP
    - `mcp_<servidor>_*` = todas las tools de un servidor MCP concreto
- **`model`**: modelo específico (si no, hereda el de la sesión principal).
- **`temperature`**: creatividad/variación (0.0–2.0).
- **`max_turns`**: máximo de “turnos internos” del subagente antes de devolver resultados.
- **`timeout_mins`**: tiempo máximo de ejecución del subagente.

> [!note] Aislamiento y recursión: los subagentes corren en un contexto separado y **no pueden invocar otros subagentes** (protección contra loops), incluso si les das `tools: ["*"]`.

## Gestionar subagentes y overrides

### Gestión interactiva

- Usa el comando **`/agents`** para habilitar/deshabilitar y reconfigurar agentes sin editar archivos (recomendado para iteración rápida).

### Configuración persistente (`settings.json`)

Puedes aplicar overrides globales sin tocar el `.md` del agente:

- **`agents.overrides`**: activar/desactivar agentes y ajustar límites de ejecución.

```json
{
  "agents": {
    "overrides": {
      "security-auditor": {
        "enabled": false,
        "runConfig": {
          "maxTurns": 20,
          "maxTimeMinutes": 10
        }
      }
    }
  }
}
```

- **`modelConfigs.overrides`**: aplicar configuración de modelo (por ejemplo, temperatura) a un agente específico usando `overrideScope`.

```json
{
  "modelConfigs": {
    "overrides": [
      {
        "match": { "overrideScope": "security-auditor" },
        "modelConfig": {
          "generateContentConfig": { "temperature": 0.1 }
        }
      }
    ]
  }
}
```

## Configuración del `browser_agent` (si lo habilitas)

Está deshabilitado por defecto; se habilita con overrides:

```json
{
  "agents": {
    "overrides": {
      "browser_agent": { "enabled": true }
    }
  }
}
```

Opciones típicas bajo `agents.browser`:

- **`sessionMode`**: cómo se gestiona Chrome
  - `persistent` (default): perfil persistente (cookies/historial se guardan)
  - `isolated`: perfil temporal (se borra al terminar)
  - `existing`: se adjunta a un Chrome ya abierto (requiere remote debugging habilitado)
- **`headless`**: ejecuta Chrome sin ventana (true/false).
- **`profilePath`**: ruta de perfil personalizada.
- **`visualModel`**: habilita “modo visual” (análisis por screenshot + clicks por coordenadas) para tareas donde el árbol de accesibilidad no basta.

> Fuente: [Subagents (experimental) | Gemini CLI](https://geminicli.com/docs/core/subagents/)

---

# Resumen

![[summary_03.png]]

**Orden en que se cargan los recursos:**

![[session-agent.png]]
