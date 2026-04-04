# Introducion

![[summary_02.png]]

--- 
# Contexto/Rules/Memoria

En el desarrollo con Inteligencia Artificial, el mayor desafío no es solo escribir un buen _prompt_, sino evitar que la IA "olvide" las reglas a medida que la conversación se extiende. Este fenómeno, conocido como la limitación de la ventana de contexto, se resuelve mediante la **Memoria Persistente**.

### 1. El Concepto de Memoria Persistente y Alcance (Scope)

La memoria persistente permite que el asistente cargue automáticamente un "manual de identidad" antes de procesar tu primera palabra. Esto garantiza que el estilo, las herramientas y las restricciones de seguridad se mantengan constantes.

**Definición:** Un **archivo de contexto** (como `AGENTS.md` o `GEMINI.md`) es un documento técnico donde se definen las instrucciones de comportamiento de la IA. Se denomina **memoria persistente** porque sobrevive al cierre de una sesión; es una "arquitectura de pensamiento" que reside en tu sistema de archivos.

Para organizar estas instrucciones de forma eficiente, manejamos tres niveles de **Alcance (Scope)**:

1.  **Alcance Global (Capa de Usuario):** Instrucciones universales que la IA aplica siempre (ej. "Habla siempre en español", "No uses emojis", "escribe todos los comentarios en ingles").
2. **Alcance de Proyecto (Capa de Raíz):** Reglas específicas para un repositorio completo (ej. "Usa React con TypeScript", "El estándar de indentación son 2 espacios").
3. **Alcance de Módulo (Capa de Subdirectorio):** Instrucciones quirúrgicas para carpetas específicas (ej. "En esta carpeta de /pagos, usa solo la API de Stripe y nunca rotar llaves sin permiso").


--------------------------------------------------------------------------------
### 2. Antigravity: Rules

Antigravity obtiene su contexto de dos fuentes la global y las rules que viven a nivel de proyecto la global vive en ~/.gemini/GEMINI.md`

#### Rules (Reglas)
Las **Rules** son instrucciones manuales que el Agente sigue de forma persistente para garantizar consistencia, los archivos de contexto de antigravity pueden referenciar a otros usando `@filename`

* **Niveles de Aplicación**:
    * **Global**: Ubicadas en `~/.gemini/GEMINI.md`, aplican a todos los proyectos.
    * **Workspace**: Ubicadas en `.agent/rules/` dentro del proyecto.
* **Activación**: Se aplican basándose en descripciones de lenguaje natural o patrones **Glob** (ej. `src/**/*.ts`).
* **Referencias**: Permiten usar `@mentions` para incluir otros archivos como contexto dentro de la regla.



---
### 3. Gemini CLI: Flexibilidad con `GEMINI.md`

Gemini CLI no solo mira hacia "arriba" (padres), sino que también escanea "hacia abajo". Para evitar el caos o la lectura de archivos sensibles, esta herramienta **respeta estrictamente los archivos** `**.gitignore**` **y** `**.geminiignore**` durante su escaneo.

``

#### Niveles de Contexto en Gemini CLI

|                    |                                         |                                                                      |
| ------------------ | --------------------------------------- | -------------------------------------------------------------------- |
| Nivel              | Ubicación                               | Impacto Arquitectónico                                               |
| **Global**         | `~/.gemini/GEMINI.md`                   | Tu ADN como desarrollador (preferencias universales).                |
| **Ancestros**      | Desde el actual hasta la raíz `.git`.   | Contexto heredado del proyecto y sus padres.                         |
| **Subdirectorios** | Carpetas debajo de la ubicación actual. | Permite que la IA entienda el impacto de tu código en otros módulos. |
```Markdown

mi-organizacion/
├── .gemini/
│   └── GEMINI.md     mi-organizacion/
├── .gemini/
│   └── GEMINI.md   <-- [Global] ADN: "Escribe siempre en TS, usa estilo funcional"
├── proyecto-mcp/
│   ├── .gitignore    <-- Gemini CLI no leerá lo que esté aquí
│   ├── AGENTS.md     <-- [Ancestro] Regla base: "Tests con Vitest"
│   ├── apps/
│   │   ├── frontend/
│   │   │   └── AGENTS.md <-- [Subdirectorio] Regla específica: "componentes Shcn"
│   │   └── api-go/
│   │       └── AGENTS.override.md  <-- [Anula] "Aquí no uses Vitest, usa 'go test'. No uses TS."
│   └── shared-utils/
│       └── .geminiignore     <-- Bloquea archivos de logs o datos sensibles
```
#### Modularización y Comandos

A diferencia de Codex, Gemini permite **Modularizar** la memoria. Puedes usar la sintaxis `@nombre-archivo.md` dentro de un `GEMINI.md` para importar instrucciones de otros archivos, facilitando la creación de guías de estilo compartidas.

```
# Main GEMINI.md file

This is the main content.

@./components/instructions.md

More content here.

@../shared/style-guide.md
```

Se puede editar el archivo `settings.json` de gemini cli en ![[#^gemini-path]]
para extender los archivos de los que buscara el contexto 

```json
{
  "context": {
    "fileName": ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]
  }
}
```

--------------------------------------------------------------------------------

### 4. Codex: El Poder de `AGENTS.md`

Codex construye una "cadena de instrucciones" cada vez que inicias una sesión. Su lógica se basa en la **concatenación por líneas en blanco**, donde lo que se lee al final tiene prioridad sobre lo que se leyó al principio.

#### Orden de Precedencia (Descubrimiento)

1. **Directorio Global:** Busca en `~/.codex`. Lee **solo el primer archivo no vacío** que encuentre, priorizando `AGENTS.override.md` sobre `AGENTS.md`.
2. **Raíz del Proyecto:** Localiza el origen (usualmente donde está el archivo `.git`) y busca instrucciones base.
3. **Camino al Directorio Actual:** Codex camina desde la raíz hacia tu carpeta de trabajo. En cada carpeta intermedia, busca un archivo de instrucciones. Si encuentra un `.override.md`, lo usa y descarta el `.md` de esa carpeta específica.

**Visualización de la Cadena de Instrucciones:**

```text
Global: ~/.codex/AGENTS.md 
 
Proyecto: raiz/AGENTS.md
    
Módulo: raiz/servicios/pagos/AGENTS.override.md
```

**Ejemplo de estructura con anulación:**

```markdown
mi-proyecto/
├── AGENTS.md (Regla: "Usa npm test")
└── apps/
    └── api/
        └── AGENTS.override.md (Regla: "Usa make test-api" -> Anula la anterior para esta carpeta)
```

__

--------------------------------------------------------------------------------



### 5. Personalización y Reglas de Oro

Como especialista en arquitectura, te recomiendo no saturar cada carpeta con instrucciones (fenómeno de **Contaminación de Contexto**). Si las reglas se contradicen en demasiados niveles, el comportamiento de la IA se vuelve errático.

**Personalización de nombres:**

- **Codex:** Configura `project_doc_fallback_filenames` en tu `config.toml`.
- **Gemini CLI:** Ajusta `context.fileName` en tu `settings.json`.

**¡Advertencia de Arquitectura! Lista de Verificación:**

-  **Archivos Vacíos:** Las herramientas ignoran archivos sin texto. Asegúrate de que tus guías tengan contenido real.
-  **Límite de Tamaño (Cap):** Codex tiene un límite por defecto de **32 KiB** (`project_doc_max_bytes`). Si lo superas, las instrucciones se cortarán y la IA "perderá el hilo".
-  **Nomenclatura:** Un error común es escribir `AGENT.md` (singular). El estándar es plural: `AGENTS.md`.
- **Higiene de Contexto:** Usa `.gitignore` para evitar que la IA intente leer instrucciones dentro de `node_modules` o carpetas temporales.

## Resumen

![[summary_memo.png]]

--------------------------------------------------------------------------------

# Skills

Las skills son habilidades que le damos a nuestros modelos ***representan una expertise***
a diferencia de los contextos que le dan al modelo contexto general del workspace, y si tiene un alcance global le da ideas generales de como comportarse, las skills le dicen al modelo "Eres Experto en" o "Eres capaz de utilizar la herramitan Y" en una skill definimos profesiones, experiencia, habilidaeds, y herramientas que sera capaz de usar, es una manera de extender la funcionalidad de los modelos.

Con las Skills podemos:

 - **Definir Roles Técnicos Específicos:** Transformar al modelo en un experto de nicho (ej. "Arquitecto de infraestructura en AWS" o "Especialista en ciberseguridad ofensiva"), lo que refina la precisión de sus sugerencias técnicas.
    
- **Integrar Herramientas de Terceros:** Habilitar la capacidad de interactuar con APIs, bases de datos o terminales (como el CLI de Gemini) para que el modelo no solo "diga", sino que "haga".

	 ```
	 Eres un experto en edicion de videos e imagenes, por lo que eres capaz de usar la herramienta de consola: ffmpeg
	 ```

- **Estandarizar el Formato de Salida:** Forzar al modelo a que siempre responda siguiendo un esquema estricto (JSON, documentación bajo norma ISO, o estructuras de código específicas del proyecto).
    
- **Reducir Alucinaciones Técnicas:** Al limitar el alcance de la "experticia" a una Skill documentada, el modelo se ciñe a los parámetros de esa habilidad en lugar de intentar adivinar basándose en conocimiento general.
    
- **Automatizar Flujos de Trabajo Complejos:** Crear secuencias de comandos o "recetas" de refactorización que se activan bajo demanda (muy útil en Cursor o Codex para mantener la coherencia del código).
    
- **Inyectar "Know-how" Propietario:** Darle al modelo acceso a metodologías internas de trabajo o patrones de diseño que no están en su entrenamiento base de internet.
    
- **Modularizar la Inteligencia:** En lugar de tener un modelo "sabelotodo" pesado, puedes activar o desactivar Skills específicas según la tarea, optimizando el rendimiento y la relevancia de la respuesta.



## ¿Qué son las Skills?

Son paquetes de **experiencia bajo demanda**. A diferencia del contexto general, las skills contienen instrucciones, scripts y recursos específicos que el agente solo carga ("progressive disclosure") cuando detecta que tu tarea coincide con la descripción de la skill. Esto evita saturar la ventana de contexto.

>[!Note] Las skills se invocan solas cuando el agente lo detecta o pueden ser invocadas por nosotros mismos diciendole que use la skill

### ¿Que pueden invocar?
Pueden invocar cualquier cosa que le definamos dentro del markdown, podemos decirle que invoque otras skill, que siga reglas definidas en otras carpetas, podemos dejarles scripts en lengaujes listos para que las ejecute, python, node, golang etc, se pueden dejar proyectos enteros que se ejecuten con npm e incluso algunas deben ser configuradas con un .env
## Configuración y Rutas

Para instalar o crear skills manualmente, debes colocar los archivos en las siguientes rutas según el alcance deseado:

| Herramienta    | Alcance Proyecto (Workspace/Repo) | Alcance Global (Usuario)                          |
| :------------- | :-------------------------------- | :------------------------------------------------ |
| Antigravity    | .agent/skills                     | ~/.agents/skills/<br>~/.gemini/antigravity/skills |
| **Gemini CLI** | `.gemini/skills/`                 | `~/.gemini/skills/`                               |
| **Codex**      | `.agents/skills/`                 | `~/.agents/skills`                                |

> [!Note] En ambas herramientas, una Skill es un directorio que **debe** contener al menos un archivo `SKILL.md`.

![[summary-skill.png]]

### Anatomia de una skill

Este es un ejemplo de como se estructura una skill, el nombre debe ser igual que la carpeta que lo contiene, `la descripcion debe decir que hace y cuando se activa`, los pasos pueden variar y muchos ser opcionales pero el uso de titulos en markdown ayuda a al agente a no alucinar

La skill puede referenciar carpetas dentro de su workspace y archivos.

```markdown
---
name: nombre-de-la-skill
description: Una línea que explique qué hace y cuándo usarla.
Trigger: Disparador de cando se activa (es mejor aqui que en la descripcion)
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
El tono y estructura de ese output es el estándar a seguir.

## Constraints
Qué NO debe hacer el agente.
```

### Anatomia de un template
se usa {{param}} para decir que variables usar, y se usa `---` para separar secciones lo cual ayuda al agente a entender el documento

``` markdown
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

### Folder Estructura de ejemplos

#### Ejemplo 1

```
my-project/ 
├── SKILL.md ← instrucciones principales de la skill 
└── README.md
```

---
#### Ejemplo 2 - Skill + Scripts

La skill describe el _qué_, los scripts hacen el _cómo_ técnico.

**Cuándo usarla:** La skill necesita que el agente ejecute código auxiliar (parsers, transformadores, validadores).

```
my-project/
├── skill/
│   └── SKILL.md
├── scripts/
│   ├── generate.ts
│   └── validate.ts
└── README.md
```

```markdown
<!--skill.md-->
## Tools
Run `scripts/generate.ts` to produce the output file before returning results.
```

---
#### Ejemplo 3 - Skill + Templates
La skill describe el proceso; los templates son los artefactos que el agente debe producir o completar.

**Cuándo usarla:** El agente debe generar documentos con una estructura fija y consistente.

```
my-project/
├── skill/
│   └── SKILL.md
├── templates/
│   ├── report.md
│   └── email.md
└── README.md
```

```markdown
<!--skill.md-->

## Output Format
Use `templates/report.md` as base. Fill in every section marked with `{{placeholder}}`.
```

---

#### Estructura 4 — Skill con entorno completo

Para skills que viven dentro de un proyecto real con configuración de entorno.

**Cuándo usarla:** La skill necesita acceder a APIs, bases de datos o servicios externos con credenciales.

```markdown
my-project/
├── .env.example
├── .env                  ← valores reales (no commitear)
├── skill/
│   └── SKILL.md
├── src/
│   └── index.ts
├── package.json
└── tsconfig.json
```

```markdown
## Environment
This skill requires environment variables set by the user before running.
See `.env.example` for the full list of required variables.
Do NOT attempt to generate, guess, or fill in values for `.env`.
```

---
### Estructura 5 — Múltiples Skills en un mismo repo

Cuando tienes varias skills relacionadas que comparten recursos.

```
my-project/
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

**Cuándo usarla:** Proyecto de skills reutilizables, tipo librería interna o monorepo de agentes.

--- 
### Estructura 6 — Skill + ejemplos de referencia

Los ejemplos le muestran al agente qué output se espera (few-shot en archivos).

```
my-project/
├── skill/
│   └── SKILL.md
├── examples/
│   ├── input-1.txt
│   ├── output-1.txt
│   ├── input-2.txt
│   └── output-2.txt
└── README.md
```

**Cuándo usarla:** La skill produce outputs complejos o con formato muy específico. Los ejemplos son más efectivos que describirlo en palabras.

**Referencia en SKILL.md:**

## Descargas Y Recomendaciones

![[skillsh.png]]

Se pueden descargar Skills en la pagina [Skill.sh](https://skills.sh/)

Hay que asegurarse que las auditorias que muestran en la pagina no sean fallos graves, algunos advertencias son debido a que la skill usa servidores externos que pueden ser otros SAS que integran muchos MCP en uno solo. 

Las recomendaciones de skills son:
### Vercel-react-best-practices
Esta skill ayuda al agente a crear mejores componentes usando react, evita sobrerenderizado, crea mejores componentes atomicos, documenta mejor y evita smell code de react/next

### Clickup de [civitai](https://skills.sh/civitai/civitai)

Si en algun caso el mcp de clickup no funciona, este Skill permite ejecutar comandos a clickup via API usando un token de autentificacion, solo que se deben hacer 2 pasos para configurar la skill y que el agente lo pueda usar:

1. ir a la carpeta donde se instalo la skill y copiar el .env.template a .env y rellenar las variables de entorno, usualmente es en  `~/.agents/skills/clickup` tambien puedes probar a exportarlo en variables de entorno con el ID
   `CLICKUP_API_TOKEN=<TOKEN>`

2. dentro de la carpeta de la skill ejecutar npm install para instalar las dependencias.

```
npx skills add https://github.com/civitai/civitai --skill clickup
```

si falta el package.json podria servir este o la misma IA puede deducirlo.****

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

---

## Ejemplos
### 1. Ejemplo Super Básico: Code Reviewer

Estructura de carpetas: `my-skills/python-reviewer/SKILL.md`

**Archivo: `SKILL.md`**

```
---
name: python-reviewer
description: Úsalo cuando el usuario pida revisar código Python buscando errores comunes y PEP8.
---

# Instrucciones de Revisión Python

1.  Analiza el código proporcionado buscando violaciones de PEP8.
2.  Verifica si hay manejo de excepciones (try/except) en operaciones I/O.
3.  Si encuentras funciones sin docstrings, sugiere añadirlos.
4.  No reescribas todo el código, solo muestra los diffs sugeridos.
```

---

### 2. Ejemplo Integrando CLI de Terceros (FFmpeg)

Las skills no ejecutan binarios por sí mismas "mágicamente"; instruyen al agente sobre **cómo** usar su capacidad de terminal para operar herramientas complejas.

Estructura: `my-skills/video-optimizer/SKILL.md`

**Archivo: `SKILL.md`**

```
---
name: video-optimizer
description: Activa esto cuando el usuario quiera comprimir, convertir o extraer audio de videos usando FFmpeg.
---

# Experto en FFmpeg

Eres un experto en el uso de la línea de comandos FFmpeg. Tu objetivo es construir el comando exacto y ejecutarlo usando tu herramienta de terminal.

### Reglas de Operación:
1.  **Detección**: Verifica si `ffmpeg` está instalado ejecutando `ffmpeg -version`.
2.  **Compresión Web**: Si el usuario pide "optimizar para web", usa:
    `ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4`
3.  **Extracción de Audio**: Para extraer MP3, usa:
    `ffmpeg -i input.mp4 -q:a 0 -map a output.mp3`

### Ejecución:
- Siempre muestra el comando al usuario antes de ejecutarlo.
- Si el comando falla, analiza el error del stderr y propón una corrección.
```

---

### 3. Ejemplo Skill llamando a una Tool de MCP

Para conectar una Skill explícitamente a un servidor MCP (Model Context Protocol), se utiliza un archivo de configuración adicional. En Codex, esto se define en `agents/openai.yaml`.

Estructura:

- `my-skills/doc-search/SKILL.md`
- `my-skills/doc-search/agents/openai.yaml`

**Archivo: `SKILL.md`**

```
---
name: doc-search-helper
description: Úsalo para buscar información en la documentación técnica oficial cuando el usuario pregunte sobre APIs.
---

# Asistente de Documentación

Utiliza la herramienta disponible del servidor MCP para buscar en la documentación.
1.  No inventes APIs.
2.  Usa la herramienta `search_docs` proporcionada por el servidor MCP.
3.  Cita la URL fuente devuelta por la herramienta.
```

**Archivo: `agents/openai.yaml`** (Configuración específica para Codex)

```
interface:
  display_name: "Buscador de Docs Oficiales"
  icon_small: "./assets/docs-icon.svg"

dependencies:
  tools:
    - type: "mcp"
      value: "documentation-server" # Nombre del servidor MCP
      description: "Servidor MCP de documentación técnica"
      transport: "stdio" # O "streamable_http" según tu config MCP
      # Si fuera HTTP, añadirías: url: "http://localhost:8080"
```


 4. Descargar Skills

---





# **MCP**

El Protocolo de contexto de modelo (MCP) conecta los modelos con las herramientas y el contexto. Se usan para dar acceso a documentación de terceros o para permitirle interactuar con herramientas de desarrollo como su navegador o Figma.


Los archivos de configuración de los MCP de las diferentes herramientas en caso de preferir o requerir una instalacion manual son:

-  Codex:  

  ` C:\Users\<USER>\.codex\config.toml `  ^codex-path

-  Antigravity:  

  `C:\Users\<USER>\\.gemini\antigravity\mcp_config.json`  ^antigravity-path
  
-  Gemini Cli: 

  ` C:\Users\<USER>\.gemini\settings.json `  ^gemini-path





![[mcp_01.png  | 500]] 






## Tools

Cuando te conectas a un MCP se habilitan las “Tools” estos son nada más y nada menos que las funciones o acciones que el MCP le habilita a nuestro modelo, los podemos ver como simples funciones o llamadas HTTP (Endpoints), 

**Seguridad**

Los MCP pueden habilitar muchas tools por lo general es mejor solo activar las que necesitemos, por lo general las herramientas en su documentación incluye una forma de habilitar o deshabilitar una tool.

**Importante**

Procurar tener activado solo las tools que ocupemos ayuda a que nuestro modelo no comience a alucinar al tener que elegir entre todas las herramientas que puede usar.

## Nota

Si se bugea el Oauth de `Antigravity` en los mcp se puede resetear eliminado los archivos de `~/.mcp-auth`

## GitHub MCP

Documentacion para instalar el MCP de github es [aqui](https://github.com/github/github-mcp-server/tree/23fa0dd1a821d1346c1de2abafe7327d26981606?tab=readme-ov-file) 

Primero se deben hacer algunas configuraciones debemos configurar la variable de entorno en nuestro sistema. se puede hacer de dos maneras.

La configuracion que yo suelo usar con tools desactivadas y una version especifica del repo es:

```json
   "github-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server:v0.30.3"
      ],
      "disabledTools": [
        "sub_issue_write",
        "request_copilot_review",
        "merge_pull_request",
        "issue_read",
        "issue_write",
        "get_team_members",
        "get_teams",
        "get_release_by_tag",
        "get_tag",
        "delete_file",
        "fork_repository",
        "assign_copilot_to_issue",
        "add_issue_comment",
        "create_repository",
        "list_issue_types",
        "list_issues",
        "list_releases",
        "list_tags",
        "list_pull_requests",
        "create_or_update_file",
        "search_issues",
        "get_latest_release",
        "add_comment_to_pending_review"
      ],
      "disabled": false
    }
```

### Problema con docker

> [!WARNING]
> El problelma de configurar MCP con docker es que levantan instancias nuevas por cada ventana del ide que usa mcp y gasta muchos recursos asi que hay otra solucion

Podemos correr un solo server en docker y que todos los IDE se conecten a ese server pero hay que correr un contenedor de docker manualmente y sustituir `-rm` y `run` por `exec -i`.

`Configura la variable de entorno configurada en el sistema`

```shell
docker run -d -i --name github-mcp --restart unless-stopped -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server:v0.30.3 stdio
```

y la configuracion 
```json
   "github-mcp-server": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "github-mcp",
        "/server/github-mcp-server",
        "stdio"
      ],
      "disabledTools": [
        "sub_issue_write",
        "request_copilot_review",
        "merge_pull_request",
        "issue_read",
        "issue_write",
        "get_team_members",
        "get_teams",
        "get_release_by_tag",
        "get_tag",
        "delete_file",
        "fork_repository",
        "assign_copilot_to_issue",
        "add_issue_comment",
        "create_repository",
        "list_issue_types",
        "list_issues",
        "list_releases",
        "list_tags",
        "list_pull_requests",
        "create_or_update_file",
        "search_issues",
        "get_latest_release",
        "add_comment_to_pending_review"
      ],
```


### Antigravity

Ir al archivo de configuracion de antigravity  ![[#^antigravity-path]]
```json
"mcpServers": {
      "github-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server:v0.30.3"
      ],
      "disabledTools": [
      "sub_issue_write",
        "request_copilot_review",
        "merge_pull_request",
        "issue_read",
        "issue_write",
        "get_team_members",
        "get_teams",
        "get_release_by_tag",
        "get_tag",
        "delete_file",
        "fork_repository",
        "assign_copilot_to_issue",
        "add_issue_comment",
        "create_repository",
        "list_issue_types",
        "list_issues",
        "list_releases",
        "list_tags",
        "list_pull_requests",
        "create_or_update_file",
        "search_issues",
        "get_latest_release",
        "add_comment_to_pending_review"
      ]
    },
}
```


O si no funciona este

```json
"mcpServers": {
    "github-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
}
```


### Gemini CLI
Para configurarlo en gemini cli hay que ir al archivo de configuracion de gemini ![[#^gemini-path]]

```json
"mcpServers": {
      "github-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server:v0.30.3"
      ],
      "disabledTools": [
        "sub_issue_write",
        "request_copilot_review",
        "merge_pull_request",
        "issue_read",
        "issue_write",
        "get_team_members",
        "get_teams",
        "get_release_by_tag",
        "get_tag",
        "delete_file",
        "fork_repository",
        "assign_copilot_to_issue",
        "add_issue_comment",
        "create_repository",
        "list_issue_types",
        "list_issues",
        "list_releases",
        "list_tags",
        "list_pull_requests",
        "create_or_update_file",
        "search_issues",
        "get_latest_release",
        "add_comment_to_pending_review"
      ]
    },
}
```


O si no funciona este

```json
"mcpServers": {
    "github-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    },
}
```



### Codex
Ir al administrador mcp y configurar los siguientes campos
![[git-hub-mcp-01.png]]

manualmente es 

```toml
[mcp_servers.github-mcp-server]
args = ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"]
command = "docker"
enabled = true

[mcp_servers.github-mcp-server.env]
GITHUB_PERSONAL_ACCESS_TOKEN = "<YOUR_TOKEN>"
```

## ClickUp MCP

La documentación oficial para instalar el MCP de clicks está [aqui](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server-1)

> [!warning] Si no funciona su agente luego de activar Clickup MCP 
>  Entonces deben desactivar la tool <font color="yellow">clickup_get_workspace_hierarchy</font>

La autentificación se realiza mediante Oauth 

  ![[clickup-oauth-01.jpg|500]]

La configuracion general que prefiero usar con tools desactivadas y solo las necesarias es:

```json
   "clickup": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.clickup.com/mcp"
      ],
      "disabledTools": [
        "clickup_get_workspace_hierarchy",
        "clickup_start_time_tracking",
        "clickup_stop_time_tracking",
        "clickup_add_time_entry",
        "clickup_get_current_time_entry",
        "clickup_create_document",
        "clickup_create_document_page",
        "clickup_update_document_page",
        "clickup_get_chat_channels",
        "clickup_send_chat_message",
        "clickup_get_task_time_entries",
        "clickup_attach_task_file",
        "clickup_find_member_by_name"
      ]
    }
```


### Antigravity

Ir al archivo de configuracion de antigravity  ![[#^antigravity-path]]

```json
"mcpServers": {
	"clickup": { 
		"command": "npx", 
		"args": ["-y", "mcp-remote", "https://mcp.clickup.com/mcp"] 
	}
}
```

Luego se autentifican por Oauth les aparecera una ventana para hacerlo.
### Gemini CLI
Para configurarlo en gemini cli hay que ir al archivo de configuracion de gemini ![[#^gemini-path]]


```json
"mcpServers": {
	"clickup": { 
		"command": "npx", 
		"args": ["-y", "mcp-remote", "https://mcp.clickup.com/mcp"] 
	}
}
```

luego entrar a gemini cli y escribir el comando /mcp auth clickup

![[clickup_gemini_01.png]]

Luego se autentifican por Oauth les aparecera una ventana para hacerlo.
`
Para excluir los tools debemos ir a![[#^gemini-path]] y podemos excluir las tools en las siguientes configuraciones

```json
"mcpServers": {
	"clickup": {
	  "excludeTools": [
		"clickup_get_workspace_hierarchy"
	  ]
	}
}
```

o  

```json
"mcpServers":{},
"tools":{
	"exclude":[
	  "clickup_get_workspace_hierarchy"
	]
}
```
### Codex

Se puede usando la interfaz y configurando los datos, buscar settings->Open MCP Settings, luego en Add Server

![[clickup-codex-01.0.png |600]]

  

Luego le damos click en Autentificar

  

![[clickup-codex-02.jpg|600]]

Aparecera la ventana Oauth y solo debemos proseguir con los pasos
   
#### Desde Config File 
![[#^codex-path]]

```toml
[mcp_servers.clickup-mcp]
enabled = true
url = "https://mcp.clickup.com/mcp"
```

  
## Figma MCP

La documentacion oficial para instalar el MCP de figma esta [aqui](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)


### Antigravity

> [!warning]  Antigravity solo soporta el MCP de figma a traves del Dev Mode por lo que es necesario tener una cuenta PRO

### Gemini

Se logra desde el buscador de [extensiones](https://geminicli.com/extensions/) de la pagina de Gemini CLI, justo [aqui](https://geminicli.com/extensions/?name=figmafigma-gemini-cli-extension)
hay que ejecutar el suguiente comando

```shell
gemini extensions install https://github.com/figma/figma-gemini-cli-extension
```

luego usar el siguiente comando dentro de gemini y realizar la autentificacion Oauth

```
/mcp auth figma
```

![[figma-gemini.png]]
### Codex

Codex puede instalaro desde su ventana de configuracion de mcp solo se le da instalar y autentificar 

![[code-git-hub.png]]
##  [Figma Console](https://github.com/southleft/figma-console-mcp)

> [!INFO]
> Se necesita la  aplicacion desktop de figma para que funcione

Configurar el settings.json


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

Hay que instalar el plugin en figma desktop y abrir un archivo para poder editar, ejecutar el siguiente comando para obtener la ruta del manifest.

```shell
npx figma-console-mcp@latest --print-path
```



Tools no necesarias para edicion y obtension de data:

```json
	"disabledTools": [
        "ds_dashboard_refresh",
        "token_browser_refresh",
        "figma_audit_design_system",
        "figma_browse_tokens",
        "figma_check_design_parity",
        "figma_generate_component_doc",
        "figma_get_design_changes",
        "figma_get_file_for_plugin",
        "figma_reconnect",
        "figma_get_comments",
        "figma_delete_comment",
        "figma_rename_mode",
        "figma_add_mode",
        "figma_arrange_component_set",
        "figma_add_component_property",
        "figma_edit_component_property",
        "figma_delete_component_property",
        "figma_setup_design_tokens",
        "figma_batch_create_variables",
        "figma_batch_update_variables",
        "figma_create_variable_collection",
        "figma_rename_variable",
        "figma_delete_variable",
        "figma_delete_variable_collection",
        "figma_get_console_logs",
        "figma_take_screenshot",
        "figma_watch_console",
        "figma_reload_plugin",
        "figma_clear_console",
        "figma_navigate",
        "figma_get_status"
      ]
    }
```

## Figma MCP de [Antonytm](https://github.com/Antonytm/figma-mcp-server)

La version oficial del mcp de figma tiene muchas limitantes hay algunas alternativas, la version de Antonytm es un mcp de codigo abierto, bastante seguro que utiliza un sandbox para comunicarse con el plugin de figma asi que no hay servidores de terceros, aqui una explicacion de como funciona, [ver](https://exdst.com/posts/20251222-figma-mcp-server).

### Instrucciones

> [!INFO]
> Se necesita la  aplicacion desktop de figma para que funcione

1. Clonar repositorio

	```
	https://github.com/Antonytm/figma-mcp-server
	```

2. Entrar en la carpeta `plugin` y ejecutar 

	```shell
	npm install
	npm run build
	```

3. Entrar a figma desktop, abrir el proyecto que quieres leer o editar, `click derecho> plugins > development > import plugins` y seleccionar el manifest.json de la carpeta plugins del cp ese plugin debe iniciarse en la app desktop cada vez que se quiera usar

4. buscar la carpeta `mcp` del proyecto clonado, y ejecutar, para servir el server, ejecutar esto cada vez que se quiera usar el mcp.

```shell
npm install
npm run start
```


5.  luego hay que configurar el mcp pero usando el atributo de url, dependera de su agente como el nombre que tendra este key del json

```json
"mcpServers": {
    "figma-antony": {
      "serverUrl": "http://localhost:38450/mcp"
    }
}
```


## Trello MCP

Configurar variables de entorno 
- `TRELLO_API_KEY`  
- `TRELLO_TOKEN` 

Se deben generar el Trello api key y el token en la pagina de trello.

```json
"trello": {
  "command": "npx",
  "args": [
	"-y",
	"mcp-server-trello"
  ]
}
```

O

```json
"trello": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-server-trello"
      ],
      "env": {
        "TRELLO_API_KEY": "<TRELLO_API_KEY>",
        "TRELLO_TOKEN": ">input:TRELLO_TOKEN>"
      }
    }
```

## Docker recursos para buscar MCP

Docker ofrece una pagina para instalar mcp de diferentes servicios y correrlos en el contenedor local

[https://hub.docker.com/r/mcp/github](https://hub.docker.com/r/mcp/github)

---
# Workflows/Commands (Flujos de trabajo)

### Antigravity
Los **Workflows** son secuencias de pasos o prompts que el usuario activa manualmente. aqui podemos especificar como ejecutara los pasos.

Lo ideal seria diseñar una lista de pasos, y especificar que use una skill, la skill deberia tener definido que tools y mcp puede llamar, aunque se puede especificar usar el mcp directamente.

* **Ubicación**: Archivos Markdown guardados en `.agent/workflows/`.
* **Ejecución**: Se activan mediante el comando **`/`** en el chat.
* **Estructura**: Deben incluir título, descripción y pasos, con un límite de 12,000 caracteres.
* **Generación**: El Agente puede crear Workflows automáticamente a partir del historial de chat.

se llaman desde el chat usando /workflow y pueden llamar a otro workflot tipo

`/search-ticket-assigned-to-me y luego  /create-new-feature`

![[work-flow-01.png]]

Ejemplo:

```markdown
# Workflow: Sync ClickUp Ticket
# ID: sync-clickup-branch

Este workflow extrae el ID del ticket desde el nombre del branch actual y busca los detalles en ClickUp.

## Pasos del Workflow

1. **Identificar Branch**: Revisa el nombre del branch actual en el que estás trabajando.
2. **Extraer ID**: Busca el patrón `-ticket` al final del nombre del branch para obtener el ID de ClickUp.
3. **Consultar ClickUp**: Usa el mcp de clickup para encontrar el ID extraído.
4. **Resumir**: Muestra el estado del ticket, el nombre de la tarea y cualquier dependencia bloqueante encontrada.

## Instrucciones para el Agente

- Si el branch no termina en un ID válido tras el guion (ejemplo: `feature/login-abc1234`), detén el proceso e informa al usuario.
- Una vez encontrado el ticket, verifica si la descripción coincide con los cambios realizados en el código actual.
```

---

# Skill vs MCP

Los MCP es una forma de extender nuestro agente para usar  <u>herramientas externas</u>, mientras que las skills nos permiten extender nuestro agente con <u>nuestras herramientas</u> --> `pero parte de nuestras herramientas incluyen a los mcp`  entonces los mcp pueden ser parte de la utilidad que las skills pueden manejar ademas de comandos `cli` de nuestras aplicaciones instaladas.

En resumen las Skills le pueden enseñar a nuestro agente como usar el MCP de manera correcta en lugar de mapear todas las tools del mcp le podes dejar explicito cual usar.

>[!important]  Las skills son los elementos que proporcionan mas extension por que funcionan con todo lo demas MCP, contexto, subagentes, hooks.

---
# Subagentes

---

# Resumen

![[summary_03.png]]


Orden en que se cargan los recursos

![[session-agent.png]]

---
# Instalación/Registro

## Antigravity

Descargar desde la [pagina oficial](https://antigravity.google/)

###  Nota

Si se bugea el Oauth de `Antigravity` en los mcp se puede resetear eliminado los archivos de `~/.mcp-auth`

## Gemini CLI

Seguir los pasos de instalacion desde la (pagina oficial)[https://geminicli.com/docs/get-started/installation/]

```bash
npm install -g @google/gemini-cli
```

Lanzar desde la consola usando el comando gemini

```shell
gemini
```

### Modos de arranque
Esto se encuentra [aqui](https://geminicli.com/docs/get-started/configuration/#security)

#### Yolo
el modo yolo arranca gemini en modo autonomo, no pregunta si quieres ejecutar cierto comando, es completamente autonomo
``
dentro de gemini se puede cambiar usando `ctrl + y`, a la derecha dira modo yolo

```shell
gemini --yolo
```

> [!warning] Usarlo con cuidado ya que si no se tiene validado los comandos que no puede usar podria eliminar archivos o lanzar comandos peligrosos 

### approval-mode

**`--approval-mode <mode>`**


Establece el modo de aprobación para las llamadas de herramienta. Modos disponibles:
- **`default`**: Solicitar aprobación en cada llamada de herramienta (comportamiento predeterminado)
- **`auto_edit`**: Aprobar automáticamente las herramientas de edición (replace, write_file) y solicitar las demás
- **`yolo`**: Aprobar automáticamente todas las llamadas de herramienta (equivalente a --yolo)

Si configuras `auto_edit` a la derecha dira  `accepting edits`  
### Configuraciones extras

Todas las configuraciones se hacen en la ruta ![[#^gemini-path]]


```json
  "experimental": {
    "skills": true, // habiilta las skill
    "enableAgents": true, // habilita subagentes, si piensan usarlo
  },
  "ide": {
    "enabled": true // comunicacion con antigravity
  },
```

## Codex

Crear un api key en [en su pagina](https://platform.openai.com/api-keys)

Y usarlo para autentificarse en la extensión de codex en VS Code, Antigravity o cursor.

