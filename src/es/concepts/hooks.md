# Hooks: Interceptación Determinista del Ciclo de Vida

Los Hooks son scripts externos que el orquestador ejecuta en momentos exactos del ciclo de vida del agente. No son instrucciones al modelo — son interrupciones del sistema que ocurren con independencia de lo que el LLM haya decidido hacer. Esta distinción es fundamental: mientras el agente es probabilístico, los Hooks son deterministas. Siempre se ejecutan, siempre en el mismo momento, siempre con el mismo resultado ante las mismas condiciones.

La analogía más cercana son los hooks de Git (`pre-commit`, `post-merge`): el desarrollador no le *pide* a Git que ejecute el linter — Git lo ejecuta obligatoriamente en cada commit, sin excepción. Los Hooks de agentes funcionan igual, pero en el nivel de las acciones del LLM.

---

## Eventos Disponibles por Herramienta

Cada herramienta expone un conjunto de eventos del ciclo de vida. Las diferencias entre tools son principalmente nominales — los momentos de disparo son equivalentes.

| Evento | Cuándo se dispara | Claude Code | Gemini CLI | Codex CLI | Cursor |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Antes de usar herramienta | Justo antes de ejecutar cualquier tool | `PreToolUse` | `BeforeTool` | `PreToolUse` | `preToolUse` |
| Después de usar herramienta | Justo después de que la tool retorna | `PostToolUse` | `AfterTool` | `PostToolUse` | `postToolUse` |
| Antes de ejecutar bash | Antes de correr un comando shell | `PreToolUse(Bash)` | `BeforeTool(bash)` | `PreToolUse(Bash)` | `beforeShellExecution` |
| Al recibir input del usuario | Cuando el usuario envía un mensaje | `UserPromptSubmit` | `BeforeInput` | — | `sessionStart` |
| Al terminar la respuesta | Cuando el agente completa su turno | `PostResponse` | `AfterResponse` | — | — |
| Al finalizar la sesión | Cuando el agente cierra la sesión | `Stop` | `SessionEnd` | — | `sessionEnd` |

---

## Protocolo de Comunicación (stdin/stdout)

Los Hooks se comunican con el orquestador mediante JSON estricto por stdin y stdout. El orquestador inyecta el contexto del evento como JSON en stdin del script; el script retorna su decisión via el código de salida y, opcionalmente, respuesta JSON en stdout.

### Input recibido por el Hook (stdin)

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

### Códigos de Salida

| Código | Efecto | Cuándo usar |
| :--- | :--- | :--- |
| `0` | Éxito — el orquestador continúa normalmente | La acción es segura, no hay nada que reportar |
| `1` (o `≠0` y `≠2`) | Error — el orquestador continúa, pero registra el error | Error del script en sí (bug, timeout) |
| `2` | **Bloqueo fail-closed** — la acción es ABORTADA | La acción viola una política y debe ser detenida |

> [!IMPORTANT]
> El código `2` es el mecanismo de seguridad principal. El orquestador no ejecuta la herramienta y retroalimenta el error al modelo para que el LLM entienda por qué fue bloqueado. Esto permite al agente reformular su acción o escalar al usuario.

---

## Configuración por Herramienta

### Claude Code

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

## Scripts de Hook: Ejemplos Reales

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

### Linter Automático Post-Edición (Node.js)

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

### Auditoría Completa de Sesión (Python)

```python
#!/usr/bin/env python3
# Logs every tool invocation to a JSONL file for security auditing.

import sys
import json
import datetime

input_data = json.loads(sys.stdin.read())

log_entry = {
    "timestamp": datetime.datetime.utcnow().isoformat(),
    "session_id": input_data.get("session_id"),
    "tool": input_data.get("tool_name"),
    "input": input_data.get("tool_input"),
    "cwd": input_data.get("cwd")
}

with open(".agent-audit.jsonl", "a") as f:
    f.write(json.dumps(log_entry) + "\n")

sys.exit(0)  # Always allow — this hook only observes
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

## Anti-patrones de Hooks

| Anti-patrón | Consecuencia | Corrección |
| :--- | :--- | :--- |
| Hook que llama a la API del LLM | Latencia extrema + coste adicional por cada acción | Usa lógica determinista (regex, grep, jq) |
| Hook sin timeout definido | Bloquea el agente indefinidamente si el script cuelga | Define `timeout: N` en la configuración |
| Exit `2` en todos los casos de error del script | Bloquea el agente cuando el bug es del propio hook | Usa exit `1` para errores del script, `2` solo para bloqueos intencionales |
| Lógica compleja en el hook | Scripts difíciles de testear, falsos positivos frecuentes | Mantén el hook simple; delega lógica compleja a scripts externos bien testeados |
| Hooks que modifican archivos | Efectos secundarios invisibles para el agente | Los hooks deben ser observadores o bloqueadores, nunca mutadores |

---

## Checklist de Producción

Antes de activar hooks en un repositorio:

- [ ] Los scripts tienen permisos de ejecución (`chmod +x`)
- [ ] Cada script tiene un timeout definido en la configuración
- [ ] Los scripts están testeados de forma independiente (sin el agente)
- [ ] Exit `2` solo se usa para bloqueos intencionales de política, no para bugs del script
- [ ] Los scripts no escriben archivos ni mutan estado del repositorio
- [ ] El equipo conoce qué acciones están bloqueadas y por qué

*Fuentes: [Claude Code: Hooks Guide](https://code.claude.com/docs/en/hooks-guide) | [Gemini CLI: Hooks Reference](https://geminicli.com/docs/hooks/reference/) | [Cursor: Hooks](https://cursor.com/docs/hooks) | [Codex CLI: Hooks](https://developers.openai.com/codex/hooks)*
