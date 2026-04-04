---
name: tech-reporter
description: Genera reportes técnicos estandarizados.
trigger: "generar reporte", "resumen técnico", "informe de arquitectura"
---

# Goal
Crear un documento Markdown siguiendo una estructura fija.

# Output Format (Templates)
Usa siempre el archivo en `$SKILL_DIR/templates/report_v1.md`.

# Placeholders
- `{{title}}`: Título del reporte.
- `{{date}}`: Fecha actual.
- `{{findings}}`: Lista de hallazgos técnicos.

# Steps
1. Recopilar datos del contexto actual.
2. Rellenar el template.
3. Guardar el resultado en la carpeta `/reports`.
