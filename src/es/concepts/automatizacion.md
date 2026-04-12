# Automatización y Headless Mode

El modo headless es la capacidad de un agente de IA para ejecutarse como proceso autónomo sin interfaz de usuario interactiva. En lugar de responder a mensajes en un chat, el agente recibe un prompt inicial por stdin o como argumento de CLI, ejecuta todas las herramientas necesarias y termina con un código de salida estándar (`0` éxito, `1+` error). Esta característica lo convierte en un componente legítimo dentro de pipelines de CI/CD, cronjobs y workflows de automatización empresarial.

---

## Comandos por Herramienta

Cada orquestador expone el modo headless con una sintaxis ligeramente diferente. El principio es el mismo en todos: el prompt inicial va como argumento o stdin, y el agente opera en modo no interactivo.

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

## Patrones de Integración CI/CD

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

## Sandboxing y Permisos

### Por qué el Sandboxing No Es Opcional

Un agente headless con acceso irrestricto puede ejecutar cualquier comando bash que el modelo genere. Los LLMs, incluso los más avanzados, pueden alucinar comandos destructivos al razonar bajo presión de contexto largo. Sin sandboxing, un `rm -rf /` hallucinated no tiene freno.

### Niveles de Sandboxing

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

**Sandbox de workspace (escritura limitada):**
```bash
# Codex CLI con sandbox de escritura solo en el workspace
codex exec "Implement the feature described in TASK.md" \
  --full-auto \
  --sandbox workspace-write  # Solo puede escribir dentro del proyecto
```

### Tabla de Riesgos por Nivel de Acceso

| Acceso | Riesgo | Mitigación |
| :--- | :--- | :--- |
| `bash: "*": allow` | Crítico — borrado, exfiltración, loops | Nunca en producción |
| `bash` con allowlist | Medio — limitado a comandos declarados | Aceptable con revisión |
| Solo `read_file, grep` | Bajo — solo lee, no modifica | Ideal para auditorías |
| Sin bash | Mínimo | Análisis y generación de código únicamente |

---

## Control de Costes (Cost Caps)

El mayor riesgo económico del modo headless es el bucle infinito: el agente no converge, reintenta indefinidamente y consume miles de dólares en llamadas a la API.

### Campos de Límite por Herramienta

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

---

## Variables de Entorno y Secretos

### Lo que Nunca Debe Estar en el Contexto del Agente

El agente puede incluir en su output cualquier información que esté en su ventana de contexto. Si un archivo `.env` se carga en el contexto (via `@.env` o `Read`), las credenciales pueden aparecer en un PR, un log o un comentario.

```bash
# INCORRECTO: El .env puede entrar al contexto si el agente lee el directorio
claude -p "Review all files in ./" --allowedTools "Read"

# CORRECTO: Excluye explícitamente archivos sensibles del scope
claude -p "Review all TypeScript files in src/" \
  --allowedTools "Read,Glob" \
  --ignore ".env,.env.*,*.key,*.pem"
```

### Patrón de Inyección Segura de Secretos

```yaml
- name: Run agent
  run: |
    # API keys como variables de entorno, no como texto en el prompt
    claude -p "Deploy the staging environment using the configured credentials." \
      --allowedTools "Bash" \
      --max-turns 10
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    # The agent can use these via process.env in scripts,
    # but they are never injected as text into the prompt
```

---

## Checklist de Producción

Antes de desplegar cualquier flujo headless, verifica:

- [ ] `max_turns` o `steps` definido explícitamente (nunca ilimitado)
- [ ] El agente corre en contenedor efímero o con sandbox de workspace
- [ ] Permisos de bash configurados con allowlist, no con wildcard `*`
- [ ] Archivos `.env` y secretos excluidos del scope de lectura del agente
- [ ] El pipeline tiene un mecanismo de notificación cuando el agente falla
- [ ] Cost caps activados en la cuenta de la API (budget alerts)
- [ ] Las ramas que el agente puede abrir PRs nunca incluyen `main` directamente

*Fuentes: [Claude Code: Non-interactive Usage](https://code.claude.com/docs/en/automation) | [Codex: Non-interactive Usage](https://developers.openai.com/codex/noninteractive) | [Gemini CLI: Automation](https://geminicli.com/docs/automation/) | [OpenCode: CLI Reference](https://opencode.ai/docs/cli/)*
