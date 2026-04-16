# AI Agents Guide & Knowledge Base

<div align="center">
  <table>
    <tr>
      <td><img src="https://img.shields.io/badge/Obsidian-483699?logo=obsidian&logoColor=white" alt="Obsidian" /></td>
      <td><img src="https://img.shields.io/badge/Bash-4EAA25?logo=gnubash&logoColor=white" alt="Bash" /></td>
      <td><img src="https://img.shields.io/badge/PowerShell-5391FE?logo=microsoft&logoColor=white" alt="PowerShell" /></td>
      <td><img src="https://img.shields.io/badge/PRs_Welcome-10b981?logo=github&logoColor=white" alt="PRs Welcome" /></td>
      <td><img src="https://img.shields.io/badge/License-MIT-0284c7?logo=open-source-initiative&logoColor=white" alt="License" /></td>
    </tr>
  </table>
</div>

Welcome to my personal knowledge base and collection of best practices for working with AI coding agents. 

This repository started as a personal project to gather, organize, and structure everything I consider important to know about AI agents in general, and specifically about the CLI tools and IDEs I have tested. It serves as a centralized hub for technical documentation, configuration standards, and my personal approach to structuring agentic workflows.

## 🎯 What's in this repository?

This is primarily a curated collection of:
- **Technical Documentation & Guidelines**: Rules on how to instruct different agents efficiently.
- **Architectural Standards**: My preferred way of organizing contexts (e.g., Progressive Disclosure vs. Monolithic `AGENTS.md`).
- **Tool-Specific Deep Dives**: How-tos and configurations for tools like Cursor, Gemini CLI, Claude Code, OpenCode, and Codex CLI.
- **Templates**: Scaffoldings for `AGENTS.md` and secondary documentation files.

### 🚀 Upcoming Features
I am actively expanding this repository. Soon I will be adding:
- **My Personal Skills**: Reusable skill definitions for various agents.
- **Subagents**: Configurations for specialized orchestrator and worker agents.
- **Custom Commands**: Useful scripts and CLI commands that integrate with these tools.

## 📖 Where to start?

The main entry point for the Spanish-language theoretical concepts and high-level overviews is located here:
👉 [`src/es/index.md`](src/es/index.md)

For strict repository rules on how agents must operate within this guide, see:
👉 [`AGENTS.md`](AGENTS.md)

## 🔮 How to Read this Guide (Obsidian)

While you can read these markdown files natively on GitHub or in VSCode, this repository is architected as an **Obsidian Vault**. 

To get the best experience:
1. Download and install [Obsidian](https://obsidian.md/).
2. Select **"Open folder as vault"** and point it to the root of this cloned repository (`AI-Agents-Guide`).

**Why Obsidian?**
- **Native Callouts:** The documentation heavily relies on Obsidian-native callouts (e.g., `> [!NOTE]`, `> [!WARNING]`) to distinguish standard concepts from critical context-pollution warnings.
- **Cross-linking:** Files are heavily interlinked. Obsidian allows you to follow these links seamlessly or view the local graph of how agent concepts relate to each other.

## 🌐 How to Read this Guide (Web / MkDocs)

If you prefer to read this documentation as a standard, beautifully formatted technical website, this repository is fully configured with **MkDocs Material**.

### Running it locally
If you have Python installed, you can serve the entire website on your machine with live-reloading:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the local server
python -m mkdocs serve
```
Open `http://127.0.0.1:8000` in your browser. Any changes you make to the markdown files will instantly update on the web page.

### Deploying to GitHub Pages
To publish the current state of your documentation to the web:
```bash
python -m mkdocs gh-deploy
```
This automatically builds the site and pushes it to the `gh-pages` branch, activating GitHub Pages instantly.

## 🤝 Contributing

While this is a personal project, contributions are totally welcome if you have insights into new tools, better practices, or corrections to existing documentation!

To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a Pull Request (PR).

**Important:** All Pull Requests, commit messages, and issue descriptions **MUST** be in English. However, remember that the prose content inside the `src/` documentation files is generally written in Spanish (with English technical terms), as per the repository rules.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built to bring order to the chaos of AI agent configurations.*
