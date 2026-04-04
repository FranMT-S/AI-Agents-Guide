# Skills (Habilidades)

Las **Skills** son paquetes de **experiencia bajo demanda**. A diferencia del contexto general (`AGENTS.md`) que siempre está activo, las habilidades contienen instrucciones, scripts auxiliares, plantillas (templates) y recursos que el agente solo carga mediante **progressive disclosure** (revelación progresiva). 

¿Qué significa esto? El agente solo inyectará esta información en su contexto cuando detecte que la tarea actual coincide con la descripción de la skill. Esto evita saturar la memoria con información irrelevante y permite dotar al agente de roles técnicos muy específicos.

## 1. Consejos: Cómo Construir Skills Correctamente

Para que una skill sea efectiva, debe estar diseñada con precisión:
- **Un solo propósito:** Una skill debe resolver un solo problema (ej. "Revisar código de Python", no "Revisar código y hacer despliegues").
- **Metadata clara:** El agente decide usar la skill basándose *exclusivamente* en la descripción y los "triggers" (disparadores). Si son vagos, el agente nunca la usará o la usará mal.
- **Usa el principio de Caja Negra (Black-Box):** Si necesitas procesar datos complejos, no le pidas al agente que escriba un script al vuelo. Crea un script en Python o Node, guárdalo dentro de la carpeta de la skill, y dile al agente: *"Ejecuta este script y usa el resultado"*.

---

## 2. Metadatos de una Skill (Frontmatter en `SKILL.md`)

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

## 3. Árbol de Ejemplos: Estructuras y Templates

Una de las mejores prácticas es tener una carpeta de referencia en tu proyecto para estandarizar la creación de skills. 

### Estructura Básica y Scripts/Templates
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

### Estructuras Avanzadas

#### Múltiples Skills en un mismo repositorio
Cuando tienes varias skills relacionadas que comparten recursos comunes.

```text
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

#### Skill + Ejemplos de Referencia (Few-Shot)
Los ejemplos le muestran al agente qué output se espera.

```text
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
**Cuándo usarla:** La skill produce outputs complejos o con formato muy específico. Los ejemplos prácticos (few-shot) son mucho más efectivos que describirlo en palabras.

---

## 4. Mejores Prácticas y Reglas Oficiales (AgentSkills.io)

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

## 5. Malas Prácticas (Qué NO hacer)

- ❌ **Triggers Genéricos:** Usar triggers como `"ayuda"`, `"código"` o `"revisar"`. Esto causará que la skill se active accidentalmente en tareas rutinarias, gastando tokens innecesariamente.
- ❌ **Exceso de Texto en SKILL.md:** Un archivo `SKILL.md` de 1000 líneas anula el propósito de la revelación progresiva. Mantén el archivo corto y delega la lógica pesada a scripts dentro de la carpeta de la skill.
- ❌ **Reglas Globales en Skills:** No pongas reglas como "Habla en español" o "Usa CamelCase" en una skill. Esas reglas pertenecen al contexto global de `AGENTS.md`.

---

## 6. Descubrimiento, Descargas y Recomendaciones

Existen plataformas donde la comunidad comparte skills listas para usarse.

### Marketplaces (Ej. Skills.sh)
Se pueden buscar y descargar Skills desde repositorios y plataformas como [Skills.sh](https://skills.sh/). 
> [!WARNING]
> Hay que asegurarse de revisar las auditorías antes de instalar. Algunas advertencias pueden deberse a que la skill usa servidores externos (como servicios SaaS que integran MCPs), por lo que siempre verifica los permisos.

### Recomendaciones Comunes

#### Vercel React Best Practices
Skill ideal para equipos de Frontend que deseen enforzar las normativas oficiales de Vercel y Next.js.

#### Integración ClickUp (Ejemplo: Civitai)
Si el servidor MCP estándar de ClickUp falla o es insuficiente, puedes usar esta skill basada en API con tokens de autenticación:
1. Copia `.env.template` a `.env` en la ruta de la skill (usualmente `~/.agents/skills/clickup`) y añade tu `CLICKUP_API_TOKEN`.
2. Instala dependencias internamente:
```bash
cd ~/.agents/skills/clickup && npm install
```
3. O instálala vía CLI:
```bash
npx skills add https://github.com/civitai/civitai --skill clickup
```
Si falta el `package.json`, puedes definir uno básico (o pedirle a la IA que lo deduzca):
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

---

## 7. Configuración y Rutas Globales (Scopes)

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

### Seguridad y Aislamiento (Sandboxing)

- **Permisos de Archivos:** En **Gemini CLI**, al activar una skill, el usuario recibe una solicitud de aprobación para que el agente pueda leer los archivos *dentro* de la carpeta de esa skill específica.
- **Variables de Entorno:** Puedes usar variables como `$SKILL_DIR` (o `${CLAUDE_SKILL_DIR}`) para referenciar scripts locales sin importar la ruta actual del proyecto.
- **Invocación Implícita vs Explícita:** Para tareas críticas (como despliegues a producción), se recomienda configurar `allow_implicit_invocation: false` (Codex) o `disable-model-invocation: true` (Claude) para que solo el usuario pueda disparar la acción manualmente.