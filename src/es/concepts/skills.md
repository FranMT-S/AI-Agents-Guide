# Skill: No escribas código, inyecta capacidades

Las **Skills** son el motor de extensión modular de nuestros agentes. Mientras que el `AGENTS.md` define la identidad base y las reglas de convivencia del proyecto, las *Skills* actúan como **paquetes de ejecución especializada**. Su función es inyectar conocimientos, scripts, *templates* y recursos técnicos en la memoria de trabajo del agente **exclusivamente cuando la tarea lo requiere**.

Esta es la forma definitiva de implementar la **Revelación Progresiva (Progressive Disclosure)**: el agente permanece ágil y eficiente porque mantiene su "ventana de atención" limpia de información irrelevante hasta que el contexto específico de la tarea activa la habilidad correspondiente.

---

## ¡Vamos a construir tu primera Skill!

No te limites a entender cómo funcionan; crea tu propia capacidad especializada. Cada habilidad que diseñes debe ser una "caja negra" autónoma. Si tu agente necesita ejecutar tareas complejas, no debe improvisar: debe invocar la infraestructura predefinida (scripts y plantillas) que tú mismo vas a definir en la estructura de su carpeta.

### Ejemplo: Una Skill Simple (saludo-agente)
Para crear una skill básica, solo necesitas el archivo de especificación `SKILL.md`:

```text
src/skills/
└── saludo-agente/
    └── SKILL.md
```

**Definición de `SKILL.md`:**
```markdown
---
name: saludo-agente
description: Skill simple para saludar al usuario usando un formato corporativo.
trigger: "saludar usuario", "bienvenida"
allow_implicit_invocation: true
---

# Goal
Cuando el usuario pida saludar, responde siempre con el siguiente formato:
"Hola, soy el agente [NOMBRE] y estoy listo para procesar tu solicitud."

# Steps
1. Identifica el nombre del agente en el contexto.
2. Responde con el saludo estándar.
```

### Principios de Diseño
1. **Unicidad de Dominio:** Cada *skill* debe resolver un problema concreto (ej. auditoría de seguridad, gestión de tareas o generación de reportes). Evita agrupar funcionalidades dispares.
2. **Activadores Deterministas:** La activación de la *skill* depende de la precisión de sus `triggers`. Reglas ambiguas causan activaciones erráticas; definiciones claras garantizan una carga de contexto infalible.
3. **Máxima Resiliencia:** El agente debe actuar como un orquestador, no como un improvisador. Si tu skill requiere lógica compleja, externalízala a recursos predefinidos (scripts o plantillas) en lugar de pedirle al agente que invente la lógica en cada ejecución.

---

## El Cerebro de la Skill: Metadatos y Frontmatter

El bloque de `YAML Frontmatter` no es una simple configuración; es la **interfaz de control** que dicta cómo, cuándo y bajo qué privilegios se despierta tu habilidad. Definir este bloque con precisión es lo que separa a una herramienta versátil de un agente que dispara comandos al azar.

### A. Metadatos Obligatorios (Activación)
Sin estos campos, la skill es invisible o no puede ser identificada por el orquestador.

| Atributo | Función Técnica |
| :--- | :--- |
| `name` | Identificador único del paquete. |
| `description` | **Motor de Inferencia:** Es la señal principal que usa el orquestador para decidir si tu skill es relevante. |

### B. Metadatos Opcionales (Control y Seguridad)
Utiliza estos campos para ajustar la autonomía, el aislamiento y los privilegios de tu skill.

| Atributo | Función Técnica |
| :--- | :--- |
| `trigger` | **Disparador Semántico:** Define los *keywords* exactos para una activación inmediata. |
| `allowed-tools` | **Sandboxing:** Reduce la superficie de ataque limitando las capacidades del agente. |
| `context` | **Aislamiento:** Decide si la skill corre en el contexto principal o en un *sandbox* paralelo (fork). |
| `dependencies` | **Infraestructura:** Servidores MCP externos necesarios para operar. |
| `allow_implicit_invocation` | **Autonomía:** Política de ejecución manual o automática. |

### Ejemplo: Configuración avanzada con todos los campos
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


---

##  Mejores Prácticas (Estándar AgentSkills.io)

El diseño de una Skill determina directamente su tasa de éxito y eficiencia en costos. Siguiendo las normativas del estándar AgentSkills, aquí tienes las heurísticas de diseño para una arquitectura robusta:

### Optimización del Motor de Descubrimiento (Triggers)
El atributo `description` y los `triggers` no son comentarios pasivos; representan el **motor semántico** mediante el cual un orquestador decide inyectar o ignorar la habilidad en su contexto.

- **Firma Accionable:** Utiliza verbos imperativos exactos (ej. "Valida", "Transforma", "Despliega") en lugar de sustantivos abstractos.
- **Señales Negativas:** Especifica explícitamente **cuándo NO** usar la skill dentro de la propia descripción (ej. *"No la actives para revisiones de sintaxis frontend"*). Esto previene que el agente se distraiga en tareas superpuestas.

### Diseño de Instrucciones Resilientes
Los modelos de lenguaje son sistemas probabilísticos. Para forzar resultados deterministas dentro de tu Skill, debes guiar su raciocinio algorítmicamente.

- **Control de Flujo Numérico:** Para procesos delicados (ej. publicación de paquetes NPM, migraciones de base de datos), desglosa las acciones en checklists secuenciales estrictos.
- **El Bucle Plan-Validate-Execute:** Obliga al agente a documentar su plan, validarlo contra una regla de negocio y solo entonces ejecutar comandos potencialmente destructivos o escrituras finales.

### Implementación de Confirmation Feedback Loops
En tareas críticas (escritura de archivos, despliegues, llamadas a APIs externas), no confíes en la ejecución automática. Implementa un bucle de confirmación explícito donde el agente deba presentar su propuesta y esperar un comando específico del usuario.

- **Comando de Validación:** Define un disparador inmutable (ej. `CONFIRMAR_EJECUCION`) que el usuario deba escribir para proceder.
- **Estado de Espera:** Instruye al agente para que **no realice ninguna escritura** hasta recibir dicho comando. Esto evita el ASR (Automatic Speech Recognition) o alucinaciones de confirmación donde el agente asume que el usuario está de acuerdo.
- **Prevención de Errores:** Si el usuario solicita cambios, el agente debe presentar una versión actualizada y solicitar nuevamente el comando de validación.

> [!IMPORTANT]
> El ciclo de confirmación es obligatorio para cualquier script o comando que modifique el estado del repositorio o infraestructura externa.


---

## Errores Comunes (Antipatrones)

La creación de Skills puede fallar si no se respeta el diseño de **Revelación Progresiva (Progressive Disclosure)** o si se confunde el propósito de una Skill con el contexto global de todo el repositorio. Evita los siguientes antipatrones críticos para mantener a tus agentes rápidos y eficaces:

### Triggers Genéricos o Ambiguos
Configurar triggers demasiado comunes provoca **falsos positivos** (la skill se inyecta en la memoria del agente cuando no hace falta, consumiendo valiosos tokens de contexto y robando la atención del modelo).
* **Incorrecto:** `trigger: "ayuda", "revisar código", "json"`
* **Correcto:** `trigger: "auditar api rest", "generar reporte arquitectura", "análisis owasp"`

### El `SKILL.md` Monolítico
Una skill nunca debe contener 500 líneas de reglas ni enormes JSONs incrustados en su archivo principal. Si obligas al agente a leer todo eso, se quedará sin ventana de contexto antes de empezar.
* **La Solución:** Utiliza estructuras multi-archivo. Si requieres que el agente entienda una gran estructura de datos, usa referencias: *"Lee estrictamente el esquema de referencia ubicado en `$SKILL_DIR/templates/schema.json` y basa tu trabajo en él"*.

### Reglas Globales dentro de una Skill
Una skill no es el lugar para definir el stack tecnológico de todo el equipo. 
* **Incorrecto:** Escribir en un `SKILL.md`: *"En este proyecto programamos usando TypeScript Estricto y TailwindCSS"*.
* **La Solución:** Las directrices a nivel repositorio pertenecen única y exclusivamente al archivo `AGENTS.md`. Las Skills son herramientas especializadas; su función es ejecutar tareas, no definir el marco de desarrollo.

> [!WARNING]
> **Consecuencia letal:** Si pones la regla de usar TypeScript dentro de la skill `"auditar api"`, el agente perderá esa instrucción y volverá a escribir código inseguro en cuanto la skill se descargue de su memoria activa al terminar la auditoría.

### Automatización Crítica sin Manejo de Errores (Infinite Loops)
Dejar que el agente ejecute un script (ej. `$SKILL_DIR/scripts/deploy.js`) sin darle instrucciones de qué hacer si falla, provoca un antipatrón donde el agente entra en pánico y reintenta la orden en bucle hasta agotar sus *max turns* o el saldo de la API.
* **La Solución:** Instruye resiliencia determinista: *"Si el script falla (exit code != 0), lee los errores de `stdout`, diseña una propuesta de solución y **ESPERA** confirmación humana antes de volver a ejecutarlo"*.

## Plantillas: No te compliques en pensar como organizarlo

### Estructura de Directorios (Proyecto)

Un Skill puede tener diferenets formas de organizarse y aqui estan las mas comunes

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
```

---
### Templates: no pierdas tiempo en formularios aburridos 
Asegura que el agente siempre responda con un formato estandarizado, eliminando el riesgo de que el agente improvise.

#### Estructura de Directorios
```text
skills/arch-doc/
├── SKILL.md
└── templates/
    └── design-record.md
```

#### Ejemplo de Template (`templates/design-record.md`)
```markdown
# Reporte de Arquitectura: {{title}}
**Fecha:** {{date}}
**Autor:** AI Agent

## Hallazgos
{{findings}}
```

#### Ejemplo de Definición (`SKILL.md`)
```markdown
---
name: arch-reporter
description: Usa esta skill para generar reportes técnicos estandarizados siguiendo las plantillas del equipo.
trigger: "generar reporte", "resumen técnico", "informe de arquitectura"
---

# Goal
Crear un documento Markdown siguiendo estrictamente la estructura definida en nuestras plantillas internas.

# Output Format (Templates)
Para generar el reporte, debes leer obligatoriamente el archivo `$SKILL_DIR/templates/design-record.md`. Copia su estructura exacta y rellena las variables `{{title}}`, `{{date}}` y `{{findings}}` con la información obtenida. Nunca inventes un formato nuevo.

# Steps
1. Recopila datos del contexto actual usando las herramientas de lectura.
2. Inyecta la información recolectada en el template.
3. **Confirmation Feedback Loop:** Presenta el reporte generado en el chat. Solicita explícitamente al usuario que revise el contenido para evitar alucinaciones o errores de formato.
4. **Comando de Validación:** El usuario debe responder estrictamente con `CONFIRMAR_REPORTE` para autorizar el guardado.
5. Si recibes la confirmación, guarda el resultado en `/reports` del proyecto. Si no, ajusta el contenido según las observaciones del usuario.

# Gestión de Fallas
- Si el template no existe, detén la ejecución y solicita su creación.
- Si no recibes el comando `CONFIRMAR_REPORTE`, **NO** realices ninguna escritura en disco.
```


---
### Superpoderes: Skill con Scripts
Convierte cualquier herramienta corporativa en una extensión de tu agente. Ideal para integrar el ciclo de vida completo mediante sus respectivas CLIs: Git/GitHub (`git`, `gh`), gestión de tareas (`clickup-cli`), comunicación (`slack-cli`), diseño (`figma-cli`) o despliegue (`vercel`, `docker`). Esta capacidad permite que tu agente ejecute flujos cross-platform con precisión, automatizando desde la gestión de Pull Requests hasta la actualización de variables de diseño o el envío de notificaciones críticas, todo desde la terminal.

#### Estructura de Directorios
```text
skills/video-tool/
├── SKILL.md
└── scripts/
    └── optimizer.js
```

#### Ejemplo: Automatización de PR con GitHub CLI y Templates (`SKILL.md`)
```markdown
---
name: github-pr-automation
description: Automatiza la creación de PRs utilizando plantillas estandarizadas para el cuerpo del mensaje.
trigger: "crear pr", "abrir pull request"
allowed-tools: ["run_shell_command", "read_file"]
---

# Goal
Agilizar el flujo de desarrollo mediante la apertura automática de Pull Requests, asegurando que la descripción siga el estándar del equipo.

# Workflow & Logic
1. **Análisis:** Extrae info de la rama y últimos commits.
2. **Template:** Lee el cuerpo del mensaje desde `$SKILL_DIR/templates/pr-body.md`.
3. **CLI:** Usa `gh pr create` inyectando el contenido de la plantilla.

# Steps
1. **Cargar Template:** Lee el archivo `$SKILL_DIR/templates/pr-body.md` y reemplaza las variables `{{feature}}` y `{{task_id}}` con la información del contexto actual.
2. **Ejecución:** Ejecuta:
   `gh pr create --title "feat: {{feature}}" --body "$(cat $SKILL_DIR/templates/pr-body.md)" --head <rama>`
3. **Verificación:** Confirma la URL generada y notifica al usuario.

# Resiliencia
- Si falta el template, detén la ejecución y solicita la creación del archivo en `templates/`.
- Ante errores de `gh`, verifica si el token está activo con `gh auth status`.
```

#### Estructura de Directorios
```text
skills/github-pr-automation/
├── SKILL.md
└── templates/
    └── pr-body.md
```

#### Ejemplo de Template (`templates/pr-body.md`)
```markdown
## Descripción
Resumen de los cambios para la tarea: {{task_id}}.

## Cambios Realizados
- {{feature}}

## Checklist
- [ ] Pruebas unitarias añadidas.
- [ ] Documentación actualizada.
```


---
### MCP Server, no es tan caro con una buena SKILL

Los servidores MCP exponen las **capacidades técnicas** (tools), pero una Skill es el **manual de instrucciones** que le enseña al agente a dominarlas. Sin una Skill, el agente puede ver una lista de 50 herramientas y no saber cuál elegir, cómo formatear los argumentos o qué pasos seguir para completar un flujo corporativo.

La Skill define:
1. **Selección Precisa:** Qué herramienta MCP invocar según el contexto.
2. **Orquestación:** El orden lógico de llamadas.
3. **Formateo y Validación:** Cómo estructurar los parámetros para evitar errores de ejecución.

> [!TIP]
> **Optimización de Costos:** Al proporcionar reglas detalladas y deterministas en tu `SKILL.md`, puedes lograr resultados de alta calidad incluso con modelos rápidos y económicos. Si dependieras de un modelo pesado (como Claude 3 Opus) para deducir el uso de una tool, el costo en tokens sería ineficiente y la latencia aumentaría drásticamente.

#### Ejemplo: Referencia a MCP (`SKILL.md`)
```markdown
---
name: doc-search-helper
description: Usa esta skill para buscar APIs en la documentación oficial. Sabe qué tool del servidor MCP llamar y cómo interpretar el resultado.
dependencies: ["mi-mcp-server"]
---

# Goal
Responder dudas técnicas consultando el servidor MCP "mi-mcp-server".

# Instrucciones de uso
1. **Identificación:** Debes llamar específicamente a la tool `search_docs` del servidor `mi-mcp-server`.
2. **Formateo:** El servidor requiere el parámetro `query` en formato string. Nunca pases objetos JSON complejos si el esquema espera un string plano.
3. **Validación:** Si la herramienta devuelve un resultado vacío, no inventes una respuesta. Indica al usuario que la documentación no cubre su consulta y cita la fuente oficial.
```


---

## Few-Shot Learning: Optimización vía Ejemplos

El **Few-Shot Learning** es una técnica de *Prompt Engineering* que consiste en proporcionar al agente ejemplos concretos (pares de *input* y *output*) para ilustrar el comportamiento esperado. Es la forma más efectiva de transmitir patrones, formatos y tonos sin necesidad de escribir instrucciones complejas y propensas a errores.

### ¿Por qué implementar Few-Shot?
1. **Reducción de Alucinaciones:** El modelo imita la estructura proporcionada en lugar de intentar "adivinar" el formato.
2. **Determinismo:** Garantiza una salida idéntica ante entradas similares, crucial para automatizaciones que alimentan bases de datos o sistemas de CI/CD.
3. **Eficiencia (Token cost-saving):** Un ejemplo bien estructurado sustituye párrafos de explicaciones abstractas, lo que reduce drásticamente el consumo de tokens y acelera el tiempo de inferencia.

#### Estructura de Directorios
```text
skills/data-extractor/
├── SKILL.md
└── examples/
    ├── input-1.txt     # Caso de prueba A (Input)
    ├── output-1.txt    # Resultado esperado A (Output)
    ├── input-2.txt     # Caso de prueba B (Input)
    └── output-2.txt    # Resultado esperado B (Output)
```

#### Ejemplo de Implementación (`SKILL.md`)
```markdown
---
name: data-extractor
description: Extrae información de logs crudos y los estructura en JSON.
trigger: "extraer datos", "parsear logs"
---

# Objetivo
Convertir texto crudo en un JSON válido según el esquema interno del proyecto.

# Few-Shot Examples
Para entender el formato exacto que debes devolver, consulta los archivos en `$SKILL_DIR/examples/`:
- **Ejemplo 1:** Compara `input-1.txt` vs `output-1.txt` para ver la estructura básica.
- **Ejemplo 2:** Compara `input-2.txt` vs `output-2.txt` para manejar casos de error.

# Instrucciones de ejecución
1. Recibe el texto del usuario.
2. Basándote ESTRICTAMENTE en los patrones de los `examples/`, genera el JSON correspondiente.
3. Devuelve **únicamente** el JSON resultante; no añadas texto explicativo ni comentarios fuera del bloque de código.
```

---


## Rutas Globales y Scopes

### Tabla de Rutas por Herramienta
A continuación se detalla dónde cada agente busca y descubre las skills instaladas, tanto a nivel global (disponibles en cualquier terminal/proyecto) como a nivel local (restringidas al repositorio actual).

| Herramienta | Ruta Global (Usuario) | Ruta Local (Proyecto) | Notas |
| :--- | :--- | :--- | :--- |
| **Antigravity** | `~/.agents/skills/` | `.agents/skills/` | Usa el directorio estándar `.agents` (agnóstico). |
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` | Soporta configuración a nivel *Enterprise* vía entorno. |
| **Codex CLI** | `~/.agents/skills/` | `.agents/skills/` | Requiere manifiesto `openai.yaml` además del directorio. |
| **Gemini CLI** | `~/.gemini/skills/` | `.gemini/skills/` | Soporta skills empaquetadas en extensiones NPM/GitHub. |
| **OpenCode** | `~/.opencode/skills/` | `.opencode/skills/` | Escanea automáticamente `.claude/` y `.agents/` heredando sus skills. |

### Seguridad y Sandboxing
Protege el contexto mediante aislamiento de variables (`$SKILL_DIR`) e invocaciones explícitas para tareas críticas.

- **Permisos de Archivos:** En **Gemini CLI**, al activar una skill, el usuario recibe una solicitud de aprobación para que el agente pueda leer los archivos *dentro* de la carpeta de esa skill específica.
- **Variables de Entorno:** Puedes usar variables como `$SKILL_DIR` (o `${CLAUDE_SKILL_DIR}`) para referenciar scripts locales sin importar la ruta actual del proyecto.
- **Invocación Implícita vs Explícita:** Para tareas críticas (como despliegues a producción), se recomienda configurar `allow_implicit_invocation: false` (Codex) o `disable-model-invocation: true` (Claude) para que solo el usuario pueda disparar la acción manualmente.

---

## Recursos y Discovery (Exploración)


### Colección Personal (FranMT-S)
El directorio central de Skills mantenido en este repositorio. Úsalo como referencia para crear tus propias habilidades.

> [!NOTE]
> Colección de directorios:
> - 🧩 **[Directorio de Skills](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/skills/)**
> - 📋 **[Templates para Skills](https://github.com/FranMT-S/AI-Agents-Guide/tree/main/src/templates/skills)**

### Marketplaces ([Skills.sh](https://skills.sh/))
Skill.sh es una pagina donde puedes descargar e instalar skill en tu proyecto o a nivel del sistema, tambien puedes compartir tus propias skills con la comunidad.

- **Auditoría:** Siempre revisa el código de los scripts antes de ejecutar comandos o permitir permisos de escritura en tu sistema.
- **Instalación:** Utiliza el comando centralizado para integrar cualquier skill:
  ```bash
  npx skills add <url-del-repositorio> --skill <nombre-skill>
  ```

#### Skills Corporativas Destacadas

Skills optimizadas para flujos de trabajo profesionales, descargables desde el marketplace:

#####  Vrcel React Best Practices
Enforza normativas oficiales de Next.js y React directamente en el flujo del agente.

##### Integración ClickUp (API Based)
Automatiza la gestión de tareas.
  * *Configuración:* Requiere añadir tu `CLICKUP_API_TOKEN` en el archivo `.env` local.
  * *Instalación:* `npx skills add <repo-url> --skill clickup`
  * *Definición de Dependencias:* Si la skill carece de `package.json`, puedes definir uno básico:
    ```json
    {
      "name": "clickup-skill",
      "version": "1.0.0",
      "description": "ClickUp skill for Agents",
      "type": "module",
      "dependencies": {
        "unified": "^11.0.4",
        "remark-parse": "^11.0.0",
        "dotenv": "^16.3.1",
        "node-fetch": "^3.3.2"
      }
    }
    ```
