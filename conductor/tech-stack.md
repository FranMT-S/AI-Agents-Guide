# Tech Stack: AI-Agents-Guide

## 1. Documentation Format
- **Markdown:** The core documentation format for all guides, ensuring broad compatibility and ease of reading.
- **Obsidian Flavor:** We utilize Obsidian-specific markdown features such as callouts (`> [!NOTE]`, `> [!WARNING]`) to create rich, visually structured documents that draw attention to important details.

## 2. Diagramming & Visuals
- **Mermaid:** Used within markdown files to dynamically generate diagrams, flowcharts, and architectural overviews (e.g., explaining MCP interactions or Subagent structures).
- **Static Assets:** PNG and JPG files stored in the `attachments/` directory for screenshots and complex graphics that cannot be easily rendered via text.

## 3. Version Control & Workspace
- **Git:** Standard version control for tracking changes to the guides, skills templates, and configuration files.
- **Local Filesystem:** All tools (Gemini CLI, Cursor, Claude Code, etc.) will interact with these files directly through the local workspace.