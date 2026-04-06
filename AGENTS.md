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
│   ├── es/                        <- Spanish documentation.
│   │   ├── ai-learning-guide.md   <- Main guide. Overview tables and concept intro only.
│   │   │                                 No dense technical details, no massive JSONs here.
│   │   ├── concepts/                  <- Core infrastructure (Shared).
│   │   │   ├── mcp.md                 <- Architecture, best practices, and configs.
│   │   │   └── skills.md              <- Skills system (all tools) & SKILL.md.
│   │   ├── tools/                     <- Individual Agent deep-dives.
│   │   │   ├── antigravity.md         <- VSCode integration & workflows.
│   │   │   ├── claude-code.md         <- CLAUDE.md & Subagents.
│   │   │   ├── codex-cli.md           <- config.toml & Headless mode.
│   │   │   ├── cursor.md              <- .mdc rules & MCP Apps.
│   │   │   ├── gemini-cli.md          <- GEMINI.md & Extensions.
│   │   │   └── opencode.md            <- opencode.json & Lazy loading.
│   │   └── attachments/               <- Localized images (Spanish).
│   ├── templates/                 <- Neutral file templates (shared across languages).
│   │   ├── skills/                <- Skill file templates.
│   │   └── agents/
│   │       ├── monolith/
│   │       │   └── AGENTS.md      <- Single-file AGENTS.md template (small/medium projects).
│   │       └── progressive/
│   │           ├── AGENTS.md      <- Root file: minimal + pointers to secondary docs.
│   │           ├── packages/
│   │           │   └── api/
│   │               └── AGENTS.md      <- Package-level AGENTS.md example (monorepo).
│   │           └── docs/          <- Secondary docs loaded on demand (all lowercase).
│   │               ├── typescript.md
│   │               ├── testing.md
│   │               ├── components.md
│   │               ├── styles.md
│   │               ├── architecture.md
│   │               └── tech-stack.md
│   └── brain/                     <- Agent session notes. Do not edit manually.
├── conductor/                     <- PERSONAL ONLY. Workflow notes and product specs.
│                                     Git-ignored. Do not reference or modify in PRs.
└── spec/                          <- PERSONAL ONLY. Style guides and technical specs.
                                      Git-ignored. Do not reference or modify in PRs.
```

> [!IMPORTANT]
> Never add dense technical content to `src/es/ai-learning-guide.md`. That file only contains summary tables and links to specific tool files in `src/es/`. All detailed configurations go in the tool-specific file.

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

- `src/es/ai-learning-guide.md` → Only overview tables, concept explanations, and links to tool files.
- `src/es/<tool>.md` → All detailed config structures, directory trees, JSON examples, and sources.

---

## 3. Standards for Tool Technical Documentation

When modifying or creating any file in `src/es/` (e.g., `src/es/gemini-cli.md`, `src/es/claude-code.md`), **every concept section** (Context, Skills, MCP, Plugins, Hooks, Subagents, Automation) MUST follow this exact pattern:

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

Each tool has a dedicated file in `src/es/`. Never duplicate content across files. If a concept is shared (e.g., the AGENTS.md standard), document it in `src/es/ai-learning-guide.md` and link to it from the tool file.

| File                        | Covers                                                       |
| :-------------------------- | :----------------------------------------------------------- |
| `src/es/tools/antigravity.md` | Antigravity (Gemini in VSCode): Rules, Workflows, Plugins    |
| `src/es/tools/claude-code.md` | Claude Code CLI: CLAUDE.md, Hooks, Sub-agents, Headless      |
| `src/es/tools/codex-cli.md`   | Codex CLI: AGENTS.md, `config.toml`, `--full-auto`           |
| `src/es/tools/cursor.md`      | Cursor IDE: `.mdc` rules, MCP Apps, Hooks, Subagents         |
| `src/es/tools/gemini-cli.md`  | Gemini CLI: GEMINI.md, Extensions, Hooks, Orchestrators      |
| `src/es/tools/opencode.md`    | OpenCode: `opencode.json`, Lazy Loading, `@file` refs        |
| `src/es/concepts/mcp.md`      | MCP architecture, best practices, and curated configs.       |
| `src/es/concepts/skills.md`   | Skills system (all tools): SKILL.md anatomy, templates       |

### Template Files

Templates live in `src/templates/agents/`. Secondary doc files (inside `docs/`) use **lowercase kebab-case**. Only root agent instructions (`AGENTS.md`, `CLAUDE.md`) use uppercase.

| Template                                          | Purpose                                                           |
| :------------------------------------------------ | :---------------------------------------------------------------- |
| `src/templates/agents/monolith/AGENTS.md`         | Single-file layout for small/medium projects                      |
| `src/templates/agents/progressive/AGENTS.md`      | Root file (minimal) for projects using Progressive Disclosure     |
| `src/templates/agents/progressive/packages/api/AGENTS.md` | Package-level AGENTS.md in a monorepo                         |
| `src/templates/agents/progressive/docs/typescript.md`  | TypeScript conventions (loaded on demand)                        |
| `src/templates/agents/progressive/docs/testing.md`     | Testing strategy and commands (loaded on demand)                  |
| `src/templates/agents/progressive/docs/components.md`  | React component structure and rules (loaded on demand)            |
| `src/templates/agents/progressive/docs/styles.md`      | CSS Modules, design tokens, dark mode (loaded on demand)          |
| `src/templates/agents/progressive/docs/architecture.md`| System architecture and directory tree (loaded on demand)         |
| `src/templates/agents/progressive/docs/tech-stack.md`  | Tech stack, versions, dependency policy (loaded on demand)        |

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