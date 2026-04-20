# Automatización y Headless Mode: Cuando el Agente Trabaja Solo Mientras Tú Duermes

El modo headless es la capacidad de un agente de IA para ejecutarse como proceso autónomo sin interfaz de usuario interactiva. En lugar de responder a mensajes en un chat, el agente recibe un prompt inicial por stdin o como argumento de CLI, ejecuta todas las herramientas necesarias y termina con un código de salida estándar (`0` éxito, `1+` error). Esta característica lo convierte en un componente legítimo dentro de pipelines de CI/CD, cronjobs y workflows de automatización empresarial.

---

## Cómo Invocar Cada Herramienta en Modo No Interactivo

Cada orquestador expone el modo headless con una sintaxis ligeramente diferente. El principio es el mismo en todos: el prompt inicial va como argumento o stdin, y el agente opera sin esperar confirmaciones del usuario.

| Herramienta | Comando Headless | Flag Autónomo |
| :--- | :--- | :--- |
| **Claude Code** | `claude -p "prompt"` | `--allowedTools` |
| **Gemini CLI** | `gemini -p "prompt"` | `--yolo` (sin confirmaciones) |
| **Codex CLI** | `codex exec "prompt"` | `--full-auto` |
| **OpenCode** | `opencode run "prompt"` | `--non-interactive` |
| **Cursor** | No soporta headless nativo | Usar API directamente |

### Ejemplos de Invocación

**Claude Code — CI/CD básico:**
```bash
claude -p "Review the failing tests in the last commit and fix them. Open a PR with the fix." \
  --allowedTools "Bash,Read,Write,Glob" \
  --max-turns 20
```

**Codex CLI — Refactorización masiva:**
```bash
codex exec "Migrate all Promise.then() chains to async/await across src/" \
  --full-auto \
  --sandbox workspace-write \
  --output-schema ./schemas/refactor-output.json
```

**Gemini CLI — Auditoría de seguridad:**
```bash
echo "Audit all API endpoints in src/routes/ for missing authentication middleware. Report findings as JSON." \
  | gemini -p - \
  --yolo \
  --model gemini-3.1-flash
```

---

## Patrones de Integración CI/CD: Los Tres Escenarios que Justifican la Automatización

### Patrón 1: Auto-corrección Reactiva (GitHub Actions)

El pipeline detecta un fallo, invoca al agente con el log del error y el agente aplica el fix en una PR automáticamente.

```yaml
name: AI Auto-Fix on Failure

on:
  workflow_run:
    workflows: ["CI Tests"]
    types: [completed]

jobs:
  auto-fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Get failed test output
        id: test-output
        run: |
          # Fetch the logs from the failed run
          gh run view ${{ github.event.workflow_run.id }} --log-failed > failed-tests.log
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Run AI agent to fix failures
        run: |
          claude -p "$(cat failed-tests.log)" \
            --allowedTools "Bash,Read,Write,Edit,Glob" \
            --max-turns 15
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Open PR with fix
        run: |
          git config user.name "AI Bot"
          git config user.email "bot@yourcompany.com"
          git checkout -b auto-fix/test-failures-${{ github.run_id }}
          git add -A
          git commit -m "fix: auto-correct failing tests [AI]"
          gh pr create \
            --title "Auto-fix: Failing tests from run ${{ github.event.workflow_run.id }}" \
            --body "This PR was generated automatically by the AI agent." \
            --base main
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Patrón 2: Auditoría Pre-Merge

El agente se ejecuta como check obligatorio en cada PR para validar seguridad y calidad antes de que el código llegue a `main`.

```yaml
name: AI Security Audit

on:
  pull_request:
    branches: [main]
    paths: ['src/**']

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run security audit
        id: audit
        run: |
          git diff origin/main...HEAD -- src/ > changes.diff
          
          RESULT=$(claude -p "$(cat changes.diff)" \
            --allowedTools "Read,Grep,Glob" \
            --max-turns 10 \
            --output-format json)
          
          echo "result=$RESULT" >> $GITHUB_OUTPUT
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Block PR on critical findings
        run: |
          CRITICAL=$(echo '${{ steps.audit.outputs.result }}' | jq '.findings[] | select(.severity == "critical")' | wc -l)
          if [ "$CRITICAL" -gt "0" ]; then
            echo "Critical security issues found. Blocking merge."
            exit 1
          fi
```

### Patrón 3: Cron Job Cognitivo

Un agente que trabaja de madrugada procesando tareas repetitivas que no requieren supervisión humana.

```yaml
name: Nightly Task Processor

on:
  schedule:
    - cron: '0 3 * * 1-5'  # Monday-Friday at 3am UTC

jobs:
  process-tasks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Process good-first-issues
        run: |
          gemini -p "
            1. Use the GitHub MCP to list open issues tagged 'good-first-issue'.
            2. For each issue under 4 hours estimated effort, create a feature branch.
            3. Implement the fix based on the issue description.
            4. Run npm test to validate.
            5. Open a draft PR for human review.
            Limit to 3 issues maximum.
          " --yolo
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Operación Segura en Producción: Las Tres Capas que Separan un Pipeline Robusto de uno Peligroso

Un agente headless que funciona en local no es lo mismo que uno que corre desatendido en producción. Sin supervisión humana, tres vectores de riesgo se vuelven críticos: el acceso sin restricciones al sistema de archivos y a la red, el consumo ilimitado de tokens cuando el agente no converge, y la exposición accidental de credenciales que están en el contexto del agente. Cada una de las siguientes secciones aborda una de estas capas.

### Sandboxing: Por Qué un Agente con `bash: "*"` en Producción Es un Accidente Esperando Ocurrir

Un agente headless con acceso irrestricto puede ejecutar cualquier comando bash que el modelo genere. Los LLMs, incluso los más avanzados, pueden alucinar comandos destructivos al razonar bajo presión de contexto largo. Sin sandboxing, un `rm -rf /` alucinado no tiene freno.

**Contenedor efímero (máxima seguridad):**
```bash
docker run --rm \
  --memory=512m \
  --cpus=1 \
  --network=none \
  --read-only \
  --tmpfs /tmp \
  -v $PWD:/workspace:ro \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  claude-headless:latest \
  claude -p "Analyze the codebase and generate a dependency report." \
    --allowedTools "Read,Glob,Grep" \
    --max-turns 10
```

**Sandbox de workspace (escritura limitada al proyecto):**
```bash
codex exec "Implement the feature described in TASK.md" \
  --full-auto \
  --sandbox workspace-write
```

**Tabla de riesgos por nivel de acceso:**

| Acceso | Riesgo | Mitigación |
| :--- | :--- | :--- |
| `bash: "*": allow` | Crítico — borrado, exfiltración, loops | Nunca en producción |
| `bash` con allowlist | Medio — limitado a comandos declarados | Aceptable con revisión |
| Solo `read_file, grep` | Bajo — solo lee, no modifica | Ideal para auditorías |
| Sin bash | Mínimo | Análisis y generación de código únicamente |

### Control de Costes: Cómo Poner un Techo al Gasto Cuando el Agente No Converge

El mayor riesgo económico del modo headless es el bucle infinito: el agente no converge, reintenta indefinidamente y consume miles de dólares en llamadas a la API. Todas las herramientas exponen un campo de límite de iteraciones — definirlo no es opcional.

**Claude Code:**
```bash
claude -p "prompt" --max-turns 20
```

**Gemini CLI (`settings.json`):**
```json
{
  "headless": {
    "maxTurns": 15,
    "timeoutMins": 30
  }
}
```

**Codex CLI:**
```bash
codex exec "prompt" --full-auto --max-steps 25
```

**OpenCode (`opencode.json`):**
```json
{
  "run": {
    "steps": 20,
    "timeout": "30m"
  }
}
```

> [!WARNING]
> Define siempre `max_turns` entre 10 y 30 dependiendo de la complejidad de la tarea. Tareas simples (análisis, reportes) → 5-10. Tareas de implementación → 15-25. Nunca dejes el campo sin definir en modo headless.

### Secretos y Variables de Entorno: Lo Que el Agente No Debe Ver Nunca en Su Contexto

El agente puede incluir en su output cualquier información que esté en su ventana de contexto. Si un archivo `.env` se carga en el contexto (via `@.env` o `Read`), las credenciales pueden aparecer en un PR, un log o un comentario generado automáticamente. La regla es simple: los secretos van como variables de entorno del proceso, nunca como texto dentro del prompt.

```bash
# INCORRECT: The agent reads the directory and .env can enter its context
claude -p "Review all files in ./" --allowedTools "Read"

# CORRECT: Restrict scope to source files only and exclude sensitive files
claude -p "Review all TypeScript files in src/" \
  --allowedTools "Read,Glob" \
  --ignore ".env,.env.*,*.key,*.pem"
```

**Patrón de inyección segura de secretos en CI/CD:**

```yaml
- name: Run agent
  run: |
    # API keys as environment variables, never as text in the prompt
    claude -p "Deploy the staging environment using the configured credentials." \
      --allowedTools "Bash" \
      --max-turns 10
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    # The agent accesses these via process.env in scripts,
    # but they are never injected as text into the prompt
```

---

## Checklist de Producción: Lo Que Debes Verificar Antes de Ejecutar un Agente Sin Supervisión

Antes de desplegar cualquier flujo headless, verifica:

- [ ] `max_turns` o `steps` definido explícitamente (nunca ilimitado)
- [ ] El agente corre en contenedor efímero o con sandbox de workspace
- [ ] Permisos de bash configurados con allowlist, no con wildcard `*`
- [ ] Archivos `.env` y secretos excluidos del scope de lectura del agente
- [ ] El pipeline tiene un mecanismo de notificación cuando el agente falla
- [ ] Cost caps activados en la cuenta de la API (budget alerts)
- [ ] Las ramas que el agente puede abrir PRs nunca incluyen `main` directamente

*Fuentes: [Claude Code: Non-interactive Usage](https://code.claude.com/docs/en/automation) | [Codex: Non-interactive Usage](https://developers.openai.com/codex/noninteractive) | [Gemini CLI: Automation](https://geminicli.com/docs/automation/) | [OpenCode: CLI Reference](https://opencode.ai/docs/cli/)*
