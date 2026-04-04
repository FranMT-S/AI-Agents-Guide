---
name: python-pep8-reviewer
description: Usa esta skill para revisar código Python buscando violaciones de PEP8 y errores comunes. Ideal para PR reviews.
trigger: "revisar python", "pep8 check", "analizar script"
compatibility: "Requiere Python 3.10+"
allowed-tools: ["read_file", "run_shell_command"]
---

# Goal
El agente debe identificar errores de sintaxis, falta de docstrings y violaciones de estilo en archivos .py.

# Context
- **Gotcha:** Este proyecto usa Type Hints obligatorios en TODAS las funciones.
- **Regla:** No sugieras cambios que rompan la compatibilidad con Python 3.10.

# Steps
1. Leer el archivo proporcionado.
2. Comparar con las reglas de PEP8 y Type Hints.
3. Generar sugerencias usando bloques diff.

# Constraints
- NO reescribir el archivo completo.
- Solo enfocarse en lógica y estilo, no en lógica de negocio a menos que sea un error evidente.
