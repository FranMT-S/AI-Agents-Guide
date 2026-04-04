# Google Antigravity: Aspectos Únicos y Configuraciones

Esta guía detalla las características exclusivas de Google Antigravity en cuanto a la gestión de contexto y habilidades.

## Gestión de Contexto (Rules & Workflows)

Antigravity gestiona el contexto combinando las reglas globales con las del espacio de trabajo. Soporta explícitamente `AGENTS.md` y `GEMINI.md`, además de archivos Markdown dentro del directorio `.agents/rules/` (con un límite de 12k caracteres).

Soporta menciones de contexto usando `@filename` dentro de las reglas para inyectar contenido dinámico. Los `Workflows` se definen como secuencias de pasos que se pueden invocar con slash commands (por ejemplo, `/deploy`).

**Estructura de Directorio:**
```text
mi-proyecto/
├── AGENTS.md
├── GEMINI.md
└── .agents/
    └── rules/
        └── tech-stack.md
```
*Fuente: [Antigravity Docs: Rules & Workflows](https://antigravity.google/docs/rules-workflows)*

## Skills (Habilidades)

Las skills en Antigravity se buscan en `.agents/skills/<name>/` a nivel de proyecto o en `~/.gemini/antigravity/skills/<name>/` a nivel global.

Se activan mediante una herramienta nativa usando la sintaxis `skill({ name: "..." })`. La documentación recomienda incluir scripts en una carpeta `/scripts` y pedirle al agente que ejecute el script pasándole `--help` (tratándolo como una "caja negra") en lugar de leer todo el código fuente, ahorrando así espacio valioso en la ventana de contexto.

**Estructura de Directorio:**
```text
mi-proyecto/
└── .agents/
    └── skills/
        └── my-skill/
            └── SKILL.md
```
*Fuente: [Antigravity: Skills Docs](https://antigravity.google/docs/skills)*

## MCP (Model Context Protocol)

Antigravity soporta los transportes `Stdio` y `Streamable HTTP`, estando enfocado primariamente en proveer contexto en tiempo real como schemas y logs.

Ofrece soporte nativo para `Google Application Default Credentials (ADC)` configurando `authProviderType: "google_credentials"`. Posee un `MCP Store` integrado en la interfaz para descubrir e instalar servidores populares (como Supabase o Linear) con un solo clic. Permite controlar y restringir herramientas deshabilitadas mediante la propiedad `"disabledTools": []`.

**Estructura de Directorio:**
```text
~/.gemini/
└── antigravity/
    ├── mcp_config.json
    └── mcp_oauth_tokens.json
```

**Ejemplo de Configuración (`mcp_config.json`):**
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp"],
      "disabledTools": ["delete_table"]
    }
  },
  "authProviderType": "google_credentials"
}
```
*Fuente: [Antigravity: MCP Docs](https://antigravity.google/docs/mcp)*
