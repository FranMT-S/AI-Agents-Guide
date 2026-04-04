# Gemini CLI: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Gemini CLI en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Memory Management)
*   **Fuente:** [Gemini CLI: Memory Management](https://geminicli.com/docs/cli/tutorials/memory-management/)
*   **Archivos:** Usa la jerarquía de `GEMINI.md` y `AGENTS.md` (Global → Proyecto → Subdirectorio).
*   **Estructura de Directorio:**
    ```text
    ~/.gemini/GEMINI.md       (Global)
    mi-proyecto/
    ├── AGENTS.md             (Proyecto)
    └── src/
        └── auth/
            └── AGENTS.md     (Subdirectorio)
    ```
*   **Características Únicas:** Permite una modularización total escaneando recursivamente. Incluye un sistema de memoria global que se gestiona mediante la herramienta `save_memory` (ej. `/memory show`, `/memory reload`), persistiendo datos sin editar los archivos manualmente.

## Skills (Habilidades)
*   **Fuentes:** [Gemini CLI: Skills Getting Started](https://geminicli.com/docs/cli/tutorials/skills-getting-started/), [Gemini CLI: Skills](https://geminicli.com/docs/cli/skills/)
*   **Archivos:** Soporta tres niveles: Workspace (`.gemini/skills/`), User (`~/.gemini/skills/`) y Extension (empaquetado).
*   **Estructura de Directorio:**
    ```text
    mi-proyecto/
    └── .gemini/
        └── skills/
            └── my-skill/
                └── SKILL.md
    ```
*   **Características Únicas:** El orden de precedencia estricto es Workspace > User > Extension. Requiere aprobación manual del usuario (sandboxing) antes de que el agente pueda leer archivos dentro de la carpeta de la skill. Soporta ejecutar binarios empaquetados (ej. `node scripts/audit.js`).

## MCP (Model Context Protocol)
*   **Fuente:** [Gemini CLI: MCP Server Setup](https://geminicli.com/docs/tools/mcp-server/)
*   **Características Técnicas:** Soporta **Stdio**, **SSE** y **Streamable HTTP**. Implementa Tools, Resources y Prompts (invocados vía slash commands).
*   **Archivos:** Configuración global en `~/.gemini/settings.json` o local en `.gemini/settings.json`.
*   **Ejemplo de Configuración (`settings.json`):**
    ```json
    {
      "mcpServers": {
        "local-db": {
          "command": "node",
          "args": ["/path/to/server.js"],
          "excludeTools": ["drop_table", "truncate_db"]
        }
      }
    }
    ```
*   **Características Únicas:** **Sanitización de Entorno (Environment Sanitization)** censura automáticamente variables sensibles (ej. las que contienen `*TOKEN*`) por seguridad. Soporta **Service Account Impersonation** para servicios protegidos por IAP. Asigna **Fully Qualified Names (FQN)** a las herramientas automáticamente para evitar colisiones entre servidores MCP. Filtra herramientas usando `includeTools` y `excludeTools`.

## Plugins y Extensiones
*   **Fuentes:** [Gemini CLI: Extensions Guide](https://geminicli.com/docs/extensions/), [Writing Extensions](https://geminicli.com/docs/extensions/writing-extensions/), [Best Practices](https://geminicli.com/docs/extensions/best-practices/), [Reference](https://geminicli.com/docs/extensions/reference/)
*   **Arquitectura:** Las extensiones expanden el CLI mediante un manifiesto `gemini-extension.json` y se instalan directamente desde URLs de GitHub (`gemini extensions install <URL>`).
*   **Estructura de Directorio:**
    ```text
    mi-extension/
    ├── gemini-extension.json
    ├── commands/
    │   └── custom-cmd.toml
    └── skills/
    ```
*   **Características Únicas:** Pueden inyectar comandos personalizados (archivos TOML en la carpeta `commands/`), habilidades (Skills) e incluso aportar "Tier 2 security rules" al motor de políticas (Policy Engine) del agente. Soporta la gestión segura de credenciales en el keychain del sistema. Permite desarrollo iterativo mediante enlaces simbólicos con `gemini extensions link`.

## Automatización y Scripting (Headless Mode)
*   **Fuente:** [Gemini CLI: Headless Tutorial](https://geminicli.com/docs/cli/headless/)
*   **Comandos:** `gemini -p "query"` o `gemini --prompt "query"`.
*   **Ejemplo de Uso:**
    ```bash
    gemini -p "Resume git diff y devuelve JSON" --output-format json > report.json
    ```
*   **Características Únicas:** Retorna texto o JSON estructurado (`--output-format json` o `stream-json`) para scripts. Se activa automáticamente en entornos no-TTY. Genera eventos de salida específicos (`init`, `message`, `tool_use`, `tool_result`, `error`, `result`) y códigos de salida detallados (ej. `42` para errores de input, `53` para límite de turnos superado).
