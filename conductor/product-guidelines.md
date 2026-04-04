# Product Guidelines: AI-Agents-Guide

## 1. Documentation Principles
- **Narrative & Contextual:** Explain the "why" before the "how". Every tutorial or guide should start with a brief context of the problem it solves.
- **Conversational & Educational:** The tone is helpful and engaging, like a senior engineer mentoring a peer.
- **Target Language (Spanish):** All generated content for the public guide (e.g., `AI-Agent Guide.md`, tool-specific files) MUST be in Spanish, as the target audience is Spanish-speaking.
- **English-Only Technical Content:** While the prose is in Spanish, all code snippets, technical comments, and technical identifiers MUST be in English. No emojis in comments.
- **Zero Hallucination Policy:** All information must be grounded in verified research and search results. Every external fact must include a source URL.

## 2. Visual Language
- **Callouts & Alerts:** Use Obsidian-style callouts (`> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`) to highlight critical information, best practices, and architectural warnings.
- **Diagrams & Visuals:** Incorporate screenshots and diagrams (using Mermaid or similar) to explain complex workflows, MCP architectures, and folder structures.
- **Code-Heavy Examples:** Provide comprehensive code snippets. Ensure snippets are syntactically correct and include comments explaining the "why" of specific implementation details.

## 3. Content Architecture (Hybrid)
The guide follows a hybrid organization to maximize discovery and depth:
- **Common Concepts:** General sections for shared concepts (Skills, MCP, Subagents) that define the "what" and "why" globally.
- **Tool-Specific Deep Dives:** Dedicated Markdown files for each major tool to provide exhaustive, tool-specific documentation:
    - `cursor.md`
    - `antigravity.md`
    - `gemini-cli.md`
    - `openCode.md`
    - `claude-code.md`
    - `codex-cli.md`

## 4. Mandatory Section Structure for Tool Files
To ensure consistency, every tool-specific `.md` file MUST contain:
1. **Overview:** What the tool is and its primary use case.
2. **Setup & Configuration:** Precise location of config files (using paths like `~/.gemini/settings.json`) and installation steps.
3. **Core Features:** Implementation details for Skills, MCP, and Hooks specific to that tool.
4. **Best Practices & Recommendations:** Practical tips for optimal usage.
5. **Warnings & Constraints:** Security considerations and known limitations.
6. **Reference Links:** All URLs used to gather the information.

## 5. Skills Template Standards
A dedicated `template/skills/` directory will store example skill structures.
- Each template must be self-contained and explain the anatomy of the skill (Goals, Steps, Output Formats, etc.).
- Examples should range from "Super Basic" to "Complete Environment" setups.