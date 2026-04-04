# Contexto del Proyecto: AI-Agents-Guide

Este archivo define las reglas estrictas de consistencia y formato para cualquier agente de IA que trabaje en este repositorio, asegurando que la documentación se mantenga uniforme, profesional y precisa a medida que se agregan o modifican secciones.

## 1. Reglas de Idioma y Tono
- **Prosa en Español:** Todo el contenido descriptivo y narrativo dirigido al usuario final debe estar en español.
- **Términos Técnicos en Inglés:** Los fragmentos de código, comandos de terminal, nombres de archivos, claves de configuración (JSON/YAML) y términos de la industria (ej. *Hooks*, *Skills*, *Headless Mode*, *Subagents*) deben mantenerse en inglés.
- **Comentarios en Código:** Los comentarios dentro de cualquier bloque de código (incluyendo ejemplos de configuración) DEBEN estar en inglés.
- **Sin Emojis:** Nunca uses emojis en los comentarios del código o en la redacción técnica seria, a menos que sean indicadores visuales específicos solicitados (ej. ✅, ⚠️, ❌ en tablas).
- **Tono Educativo y Objetivo:** El tono debe ser directo, conversacional pero altamente técnico y objetivo. Evita halagos excesivos o lenguaje promocional (ej. no digas "precisión quirúrgica", "el rey del contexto"). Sé específico en qué destaca cada herramienta o modelo.

## 2. Formato Visual y Arquitectura
- **Callouts (Obsidian Style):** Usa siempre los callouts nativos de Obsidian para resaltar información:
  - `> [!NOTE]` para notas generales o indicaciones de dónde encontrar más detalles.
  - `> [!TIP]` para consejos de mejores prácticas (ej. reseteo de OAuth).
  - `> [!WARNING]` para riesgos de seguridad (ej. sandboxing) o problemas de contexto.
  - `> [!IMPORTANT]` para reglas críticas del framework.
- **Tablas en la Guía Principal:** El archivo principal (`src/ai-learning-guide-es.md`) debe mantenerse limpio y fácil de leer. Usa **Tablas Comparativas** para mostrar diferencias entre agentes/modelos.
- **Detalles en Archivos Específicos:** Nunca pongas explicaciones técnicas densas, árboles de directorios o JSONs masivos en la guía principal. Si una herramienta tiene características únicas, documéntalas en su archivo específico en `src/` (ej. `src/cursor.md`, `src/gemini-cli.md`). La guía principal solo debe enlazar a estos archivos.

## 3. Estándares para Documentación Técnica de Herramientas
Al modificar o crear archivos específicos de herramientas (`src/gemini-cli.md`, `src/claude-code.md`, etc.), DEBES incluir siempre los siguientes elementos visuales para cada concepto (Contexto, MCP, Skills, Plugins, Hooks, Subagentes, Automatización):
1.  **Árbol de Directorios (`text`):** Usa un bloque de código `text` para ilustrar la ruta exacta donde reside el archivo de configuración o la skill (ej. `mi-proyecto/ -> .gemini/ -> settings.json`).
2.  **Bloque de Configuración:** Muestra el contenido exacto esperado (en formato `json`, `yaml`, `toml`, `bash`, etc.) basado en la documentación oficial.
3.  **Fuentes Reales:** No inventes configuraciones ni asumas el comportamiento basándote en versiones antiguas de los agentes. Si no sabes un dato, exige el link oficial de la documentación para investigar.

## 4. Política de "Zero Hallucination"
- **Fuente de Verdad:** Solo extrae información técnica, banderas de terminal (flags), o arquitecturas si provienen explícitamente de la documentación oficial de la herramienta.
- **Urls de Referencia:** Al final de cada sección importante o archivo específico, añade una lista de enlaces oficiales usados para investigar el tema bajo el título `*Fuente:* [Nombre](url)`.