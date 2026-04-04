---
name: video-optimizer
description: Usa esta skill cuando el usuario necesite comprimir o convertir archivos de video MP4 usando herramientas CLI.
trigger: "optimizar video", "ffmpeg", "convertir mp4"
allowed-tools: ["run_shell_command"]
license: "MIT"
---

# Goal
Ejecutar el script de validación incluido para procesar videos según los parámetros del proyecto.

# Logic (Scripts)
Esta skill depende de un script en Python contenido en la carpeta de la skill. El script utiliza PEP 723 inline metadata para instalar sus dependencias al vuelo usando `uvx`.
Ruta: `$SKILL_DIR/scripts/validate_bitrate.py`

# Steps
1. **Plan:** Analiza la petición del usuario y determina los parámetros de compresión.
2. **Validate:** Ejecuta el script de validación usando `uvx`: `uvx run $SKILL_DIR/scripts/validate_bitrate.py <input>`.
3. **Execute:** Si el script falla (exit code != 0), lee el mensaje de error y ajusta los parámetros en un bucle hasta que pase la validación. NO hagas preguntas interactivas.

# Constraints
- Usa SIEMPRE salidas JSON o CSV cuando parsees la respuesta del script.
- Asegúrate de que tus comandos sean idempotentes (ej. verifica si el archivo de salida ya existe antes de sobreescribirlo).
