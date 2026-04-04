# Project Context: AI-Agents-Guide

This file defines the strict consistency and formatting rules for any AI agent working within this repository, ensuring that the documentation remains uniform, professional, and accurate as sections are added or modified.

---

## 0. Repository Map

Before making any change, understand the full layout of this repository:

```text
AI-Agents-Guide/
├── AGENTS.md                      <- This file. Rules for all agents.
├── .gitignore
├── src/                           <- All documentation files live here.
│   ├── ai-learning-guide-es.md   <- Main guide. Overview tables and concept intro only.
│   │                                 No dense technical details, no massive JSONs here.
│   ├── skills.md                  <- Deep-dive: Skills system (all tools).
│   ├── antigravity.md             <- Deep-dive: Antigravity-specific config.
│   ├── claude-code.md             <- Deep-dive: Claude Code-specific config.
│   ├── codex-cli.md               <- Deep-dive: Codex CLI-specific config.
│   ├── cursor.md                  <- Deep-dive: Cursor-specific config.
│   ├── gemini-cli.md              <- Deep-dive: Gemini CLI-specific config.
│   ├── openCode.md                <- Deep-dive: OpenCode-specific config.
│   ├── attachments/               <- Images embedded in docs.
│   ├── brain/                     <- Agent session notes. Do not edit manually.
│   └── template/                  <- File templates for new tool docs.
├── conductor/                     <- PERSONAL ONLY. Workflow notes and product specs.
│                                     Git-ignored. Do not reference or modify in PRs.
└── spec/                          <- PERSONAL ONLY. Style guides and technical specs.
                                      Git-ignored. Do not reference or modify in PRs.
```

> [!IMPORTANT]
> Never add dense technical content to `src/ai-learning-guide-es.md`. That file only contains summary tables and links to specific tool files in `src/`. All detailed configurations go in the tool-specific file.

> [!WARNING]
> The `conductor/` and `spec/` folders are **personal working directories** excluded from version control via `.gitignore`. They exist only on the local machine for the owner's reference.
> - You MAY read them to understand context or intentions when explicitly asked.
> - You MUST NOT suggest committing, publishing, or referencing them in any documentation under `src/`.
> - Do NOT treat their content as project requirements unless the owner explicitly confirms so.

---

## 1. Language and Tone Rules

- **Spanish Prose:** All descriptive and narrative content directed at the end-user MUST be in Spanish.
- **English Technical Terms:** Code snippets, terminal commands, file names, configuration keys (JSON/YAML), and industry terms (e.g., *Hooks*, *Skills*, *Headless Mode*, *Subagents*) MUST remain in English.
- **Code Comments:** Comments inside any code block (including configuration examples) MUST be in English.
- **No Emojis:** Never use emojis in code comments or serious technical writing, unless they are specific visual indicators requested for tables (e.g., ✅, ⚠️, ❌).
- **Educational and Objective Tone:** The tone must be direct, conversational, yet highly technical and objective. Avoid excessive praise or promotional language. Be specific about what each tool or model excels at.

---

## 2. Visual Format and Architecture

### Callouts (Obsidian Style)

Always use native Obsidian callouts to highlight information:

```markdown
> [!NOTE]
> For general notes or links to related files.

> [!TIP]
> For best practice advice (e.g., resetting OAuth, using symlinks).

> [!WARNING]
> For security risks (e.g., sandboxing, context pollution) or breaking behaviors.

> [!IMPORTANT]
> For critical framework rules that must not be ignored.
```

### Tables

Use **Comparative Tables** to show differences between agents or models. Example:

| Herramienta    | Archivo de Contexto            | Lógica de Precedencia                         |
| :------------- | :----------------------------- | :-------------------------------------------- |
| **Cursor**     | `.cursor/rules/*.mdc`          | Activación por patrones `glob`.               |
| **Gemini CLI** | `GEMINI.md`, `AGENTS.md`       | Escaneo recursivo hacia arriba hasta `.git`.  |
| **Claude Code**| `CLAUDE.md`, `AGENTS.md`       | Importa automáticamente archivos de `src/`.   |

### Role of the Main Guide vs. Tool Files

- `src/ai-learning-guide-es.md` → Only overview tables, concept explanations, and links to tool files.
- `src/<tool>.md` → All detailed config structures, directory trees, JSON examples, and sources.

---

## 3. Standards for Tool Technical Documentation

When modifying or creating any file in `src/` (e.g., `src/gemini-cli.md`, `src/claude-code.md`), **every concept section** (Context, Skills, MCP, Plugins, Hooks, Subagents, Automation) MUST follow this exact pattern:

### Pattern: Text → Directory Tree → Config Block → Source

**1. One paragraph** describing the concept and what makes this tool unique in that area.

**2. A `text` Directory Tree** showing exactly where the configuration file lives:

```text
mi-proyecto/
└── .gemini/
    └── settings.json
```

**3. A configuration block** in the correct format (`json`, `yaml`, `toml`, `bash`, or `markdown`):

```json
{
  "mcpServers": {
    "local-db": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "excludeTools": ["drop_table"]
    }
  }
}
```

**4. An italic source line** with the official documentation link:

```markdown
*Fuente: [Gemini CLI: MCP Server Setup](https://geminicli.com/docs/tools/mcp-server/)*
```

---

### Complete Section Example (Hooks in a tool file)

The following is a well-formed section. Use it as the gold standard when writing or reviewing any concept in `src/`:

```markdown
## Hooks (Disparadores)

Los hooks permiten ejecutar scripts en respuesta a eventos del ciclo de vida del agente.
Se configuran en el objeto `hooks` dentro de `settings.json` y se comunican
via `stdin`/`stdout` con JSON estricto.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .gemini/
    └── settings.json
```

**Ejemplo de Configuración (`settings.json`):**
```json
{
  "hooks": {
    "BeforeTool": [
      {
        "command": "./scripts/validate-tool.sh"
      }
    ]
  }
}
```

**Ejemplo de Input recibido por el hook (`stdin`):**
```json
{
  "session_id": "string",
  "hook_event_name": "BeforeTool",
  "cwd": "/path/to/project",
  "timestamp": "2026-04-03T12:00:00Z"
}
```

*Fuente: [Gemini CLI: Hooks Reference](https://geminicli.com/docs/hooks/reference/)*
```

---

## 4. File-to-Tool Mapping

Each tool has a dedicated file in `src/`. Never duplicate content across files. If a concept is shared (e.g., the AGENTS.md standard), document it in `src/ai-learning-guide-es.md` and link to it from the tool file.

| Tool File                   | Covers                                                      |
| :-------------------------- | :---------------------------------------------------------- |
| `src/antigravity.md`        | Antigravity (Gemini in VSCode): Rules, Workflows, Plugins   |
| `src/claude-code.md`        | Claude Code CLI: CLAUDE.md, Hooks, Sub-agents, Headless     |
| `src/codex-cli.md`          | Codex CLI: AGENTS.md, `config.toml`, `--full-auto`          |
| `src/cursor.md`             | Cursor IDE: `.mdc` rules, MCP Apps, Hooks, Subagents        |
| `src/gemini-cli.md`         | Gemini CLI: GEMINI.md, Extensions, Hooks, Orchestrators     |
| `src/openCode.md`           | OpenCode: `opencode.json`, Lazy Loading, `@file` refs       |
| `src/skills.md`             | Skills system (all tools): SKILL.md anatomy, templates      |

---

## 5. "Zero Hallucination" Policy

- **Source of Truth:** Only extract technical information, terminal flags, or architectures if they explicitly come from the tool's official documentation.
- **Do not invent:** Never assume behavior based on older versions of an agent. If you do not know a fact, state it and request the official documentation link.
- **Reference URLs:** At the end of each major concept or section, add the official source using this exact format:

```markdown
*Fuente: [Tool Name: Section Title](https://official.url/path)*
```

Multiple sources:
```markdown
*Fuentes: [Title One](https://url1) | [Title Two](https://url2)*
```