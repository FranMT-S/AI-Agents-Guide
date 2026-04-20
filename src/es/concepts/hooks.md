# Hooks: La Diferencia Entre Sugerirle a tu Agente y Obligarlo a Cumplir

Imagina que tienes un desarrollador junior muy rápido pero algo impulsivo. Le pides que escriba código, pero a veces olvida correr el linter o, peor aún, intenta ejecutar comandos destructivos en la terminal. Puedes añadir reglas en su prompt, pero los modelos de lenguaje son probabilísticos: a veces simplemente ignoran o "alucinan" por encima de sus propias restricciones. 

Los Hooks resuelven esto actuando como guardias de seguridad invisibles. No son instrucciones al modelo — son scripts externos que el orquestador ejecuta en momentos exactos del ciclo de vida del agente. Mientras el agente es probabilístico, los Hooks son **completamente deterministas**. Siempre se ejecutan, siempre en el mismo momento, y siempre pueden bloquear una acción antes de que ocurra. 

La analogía más cercana son los hooks de Git (`pre-commit`, `post-merge`): el desarrollador no le *pide* a Git que ejecute el linter — Git lo ejecuta obligatoriamente en cada commit, sin excepción. Los Hooks de agentes funcionan igual, pero controlando cada paso y herramienta que el LLM intenta usar.

---

## Eventos Disponibles: El Mapa Exacto de Cuándo Puedes Interrumpir al Agente

Cada orquestador expone un conjunto de eventos del ciclo de vida. Aunque los nombres varían entre herramientas, los momentos de disparo son conceptualmente idénticos en todo el ecosistema.

| Evento | Cuándo se dispara | Claude Code | Gemini CLI | Codex CLI | Cursor |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Antes de usar herramienta | Justo antes de ejecutar cualquier tool | `PreToolUse` | `BeforeTool` | `PreToolUse` | `preToolUse` |
| Después de usar herramienta | Justo después de que la tool retorna | `PostToolUse` | `AfterTool` | `PostToolUse` | `postToolUse` |
| Antes de ejecutar bash | Antes de correr un comando shell | `PreToolUse(Bash)` | `BeforeTool(bash)` | `PreToolUse(Bash)` | `beforeShellExecution` |
| Al recibir input del usuario | Cuando el usuario envía un mensaje | `UserPromptSubmit` | `BeforeInput` | — | `sessionStart` |
| Al terminar la respuesta | Cuando el agente completa su turno | `PostResponse` | `AfterResponse` | — | — |
| Al finalizar la sesión | Cuando el agente cierra la sesión | `Stop` | `SessionEnd` | — | `sessionEnd` |

---

## Protocolo de Comunicación: Cómo Entender el Mensaje del Orquestador

Los Hooks se comunican con el orquestador mediante JSON estricto por `stdin` y devuelven su veredicto por `stdout` o código de salida (`exit code`). El orquestador pausa al modelo, inyecta el contexto del evento como JSON en tu script, y espera a que tu script decida si la acción procede o se bloquea.

### Input recibido por el Hook (`stdin`)

```json
{
  "session_id": "abc-123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf logs/errors/"
  },
  "cwd": "/home/user/mi-proyecto",
  "transcript_path": "/tmp/claude-transcript-abc123.json",
  "timestamp": "2026-04-11T17:00:00Z"
}
```

### Códigos de Salida: El Verdadero Poder del Hook

| Código | Efecto | Cuándo usar |
| :--- | :--- | :--- |
| `0` | Éxito — el orquestador continúa normalmente | La acción es segura, no hay nada que reportar |
| `1` (o `≠0` y `≠2`) | Error — el orquestador continúa, pero registra el error | Error del script en sí (bug, timeout) |
| `2` | **Bloqueo fail-closed** — la acción es ABORTADA | La acción viola una política y debe ser detenida |

> [!IMPORTANT]
> El código `2` es el mecanismo de seguridad definitivo. Al devolver `exit 2`, el orquestador cancela la ejecución de la herramienta e inyecta el error de vuelta al modelo. Esto permite que el LLM lea por qué fue bloqueado, repiense su plan, y lo intente de otra forma.

---

## Configuración por Herramienta

Aunque el concepto de Hook es universal, cada herramienta decide dónde colocar estos interceptores y cómo declararlos en su archivo de configuración.

### Claude Code

Claude Code permite definir hooks anidados basados en expresiones regulares que hacen match con nombres de herramientas (como `Bash` o `Edit`). Su principal ventaja es que inyecta variables de entorno listas para usar directamente en el contexto del script.

**Directorio y archivo de configuración:**
```text
mi-proyecto/
└── .claude/
    ├── settings.json
    └── hooks/
        ├── protect-files.sh
        └── run-linter.sh
```

**`settings.json` — Schema de hooks:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-linter.sh"
          }
        ]
      }
    ]
  }
}
```

**Variables de entorno disponibles en scripts:**
- `$CLAUDE_PROJECT_DIR` — Raíz del proyecto
- `$CLAUDE_TOOL_NAME` — Nombre de la herramienta que disparó el hook
- `$CLAUDE_SESSION_ID` — ID de la sesión activa

*Fuente: [Claude Code: Hooks Guide](https://code.claude.com/docs/en/hooks-guide)*

---

### Gemini CLI

En Gemini CLI, los hooks se configuran de manera consolidada en `settings.json`. El orquestador se destaca por pasar toda la información contextual vía `stdin` en forma de un objeto JSON rico y estructurado, lo que hace trivial escribir validadores en Python o Node.js.

**Directorio y archivo de configuración:**
```text
mi-proyecto/
└── .gemini/
    └── settings.json
```

**`settings.json` — Schema de hooks:**
```json
{
  "hooks": {
    "BeforeTool": [
      {
        "command": "./scripts/validate-tool.sh",
        "timeout": 15,
        "matcher": {
          "toolName": ["bash", "write_file"]
        }
      }
    ],
    "AfterResponse": [
      {
        "command": "./scripts/log-session.sh"
      }
    ]
  }
}
```

**Input via stdin (objeto completo):**
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "BeforeTool",
  "tool_name": "bash",
  "tool_input": {},
  "timestamp": "2026-04-11T00:00:00Z"
}
```

*Fuente: [Gemini CLI: Hooks Reference](https://geminicli.com/docs/hooks/reference/)*

---

### Cursor

Cursor utiliza un archivo `hooks.json` separado de las configuraciones primarias y permite un bloqueo rígido mediante la propiedad booleana explícita `failClosed`, dejando claro si el hook detiene en seco al agente o solo enciende una alarma pasiva.

**Directorio y archivo de configuración:**
```text
.cursor/
├── hooks.json
└── hooks/
    ├── audit-network.sh
    └── protect-env.sh
```

**`hooks.json` — Schema:**
```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "./.cursor/hooks/audit-network.sh",
        "matcher": "curl|wget|fetch",
        "failClosed": true
      }
    ],
    "preToolUse": [
      {
        "command": "./.cursor/hooks/protect-env.sh",
        "matcher": "Read"
      }
    ]
  }
}
```

*Fuente: [Cursor Docs: Hooks](https://cursor.com/docs/hooks)*

---

### Codex CLI

Codex CLI usa un schema `hooks.json` que soporta configuración de mensajes de estado visuales (`statusMessage`). Esto permite darle retroalimentación explícita al usuario humano en su terminal mientras el script de hook retiene al modelo en segundo plano.

**Directorio y archivo de configuración:**
```text
mi-proyecto/
└── .codex/
    ├── hooks.json
    └── hooks/
        └── pre_tool_use_policy.py
```

**`hooks.json` — Schema:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \".codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking Bash command policy"
          }
        ]
      }
    ]
  }
}
```

*Fuente: [Codex CLI: Hooks](https://developers.openai.com/codex/hooks)*

---

## Scripts de Hook: Ejemplos Reales de Protección y Auditoría

La teoría es simple, pero el código es lo que protege al proyecto. Aquí hay implementaciones reales que puedes copiar directamente a tu repositorio para dotar a tu agente de barreras irrompibles.

### Protección contra Comandos Destructivos (Bash)

```bash
#!/usr/bin/env bash
# Reads the tool input from stdin and blocks destructive bash commands.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

BLOCKED_PATTERNS=("rm -rf /" "rm -rf ~" "DROP TABLE" "git push --force" "format" "> /dev/sd")

for PATTERN in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$PATTERN"; then
    echo "BLOCKED: Command matches restricted pattern: '$PATTERN'" >&2
    exit 2
  fi
done

exit 0
```

### Linter Automático Post-Edición (Node.js/Bash)

```bash
#!/usr/bin/env bash
# Runs ESLint on the edited file after every write/edit action.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if echo "$FILE" | grep -qE '\.(ts|tsx|js)$'; then
  npx eslint "$FILE" --fix --quiet
  if [ $? -ne 0 ]; then
    echo "Linting failed on $FILE. Resolve ESLint errors before continuing." >&2
    exit 2
  fi
fi

exit 0
```

### Bloqueo de Archivos Sensibles (Bash)

```bash
#!/usr/bin/env bash
# Prevents the agent from reading files containing secrets.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

PROTECTED_FILES=(".env" ".env.local" ".env.production" "*.pem" "*.key" "secrets.json")

for PATTERN in "${PROTECTED_FILES[@]}"; do
  if echo "$FILE" | grep -q "$PATTERN"; then
    echo "BLOCKED: Access to sensitive file '$FILE' is not allowed." >&2
    exit 2
  fi
done

exit 0
```

---

## Anti-patrones: Errores Comunes que Rompen tu Pipeline

Incluso la mejor intención puede arruinar la experiencia si un Hook está mal diseñado. Estos son los errores que paralizan a un agente:

| Anti-patrón | Consecuencia | Corrección |
| :--- | :--- | :--- |
| **Hook que llama a la API del LLM** | Latencia extrema y coste adicional masivo que se multiplica por cada simple acción del agente. | Usa la magia aburrida pero determinista (regex, `grep`, `jq`, linter rules). |
| **Hook sin timeout definido** | Bloquea el agente de manera infinita en la terminal si el script de validación se cuelga. | Define siempre la propiedad `timeout: N` en la configuración JSON respectiva. |
| **Exit `2` en todos los casos** | Engaña al agente diciéndole "lo que intentaste es ilegal" cuando en realidad el script crashó por un typo. | Usa exit `1` para bugs del script, reserva el exit `2` solo para abortos intencionales. |
| **Hooks que mutan o reescriben archivos en silencio** | El agente cree que su herramienta modificó X, pero tu hook de repente transformó el resultado a Y a sus espaldas, causándole confusión general. | Los hooks deben ser guardianes observadores o bloqueadores. Para formater mutaciones visibles, haz que el propio agente corra herramientas pre-escritas. |

---

## Checklist de Producción: Lo Que Debes Verificar Antes de Habilitar Tus Hooks

Antes de confiar ciegamente en tus nuevos guardianes dentro de un repositorio real:

- [ ] Los scripts tienen permisos de ejecución obligatorios (`chmod +x`).
- [ ] Cada script en el archivo JSON tiene un timeout máximo en segundos asignado expresamente.
- [ ] Los scripts individuales de barrera han sido testeados manualmente pasando un payload por stdin sin lanzar el orquestador.
- [ ] Exit `2` realmente frena y no reintenta. Las excepciones de uso son transparentes.
- [ ] Los scripts analíticos de auditoría fallan de manera segura (Exit `0` o `1`, nunca bloqueando con `2` si no son políticas restrictivas de seguridad).

*Fuentes generales: [Claude Code: Hooks Guide](https://code.claude.com/docs/en/hooks-guide) | [Gemini CLI: Hooks Reference](https://geminicli.com/docs/hooks/reference/) | [Cursor: Hooks](https://cursor.com/docs/hooks) | [Codex CLI: Hooks](https://developers.openai.com/codex/hooks)*
