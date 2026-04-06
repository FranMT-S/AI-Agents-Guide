---
name: tech-reporter
description: Usa esta skill para generar reportes técnicos estandarizados, resúmenes de PR o informes de arquitectura.
trigger: "generar reporte", "resumen técnico", "informe de arquitectura"
metadata:
  audience: "maintainers"
  tier: "frontend"
---

# Goal
Crear un documento Markdown siguiendo estrictamente la estructura definida en nuestras plantillas internas.

# Output Format (Templates)
Usa siempre el archivo en `$SKILL_DIR/templates/report_v1.md`.

# Placeholders
- `{{title}}`: Título del reporte.
- `{{date}}`: Fecha actual.
- `{{findings}}`: Lista concreta de hallazgos técnicos.

# Steps
1. Recopilar datos del contexto actual usando las herramientas disponibles.
2. Rellenar el template sin alterar su estructura base.
3. Validar: Asegúrate de que el documento generado reemplazó todos los placeholders `{{}}`.
4. Guardar el resultado en la carpeta `/reports`.
