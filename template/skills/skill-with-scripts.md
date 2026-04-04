---
name: video-optimizer
description: Experto en el uso de FFmpeg para comprimir y convertir videos.
trigger: "optimizar video", "ffmpeg", "convertir mp4"
allowed-tools: ["run_shell_command"]
---

# Goal
Generar comandos exactos de FFmpeg y ejecutarlos para cumplir con los requisitos de tamaño del usuario.

# Logic (Scripts)
Esta skill depende de scripts externos para validar el bitrate.
Ruta: `$SKILL_DIR/scripts/validate_bitrate.py`

# Steps
1. Verificar si `ffmpeg` está instalado: `ffmpeg -version`.
2. Analizar el archivo de entrada: `ffprobe <input>`.
3. Ejecutar el script de validación.
4. Generar y ejecutar el comando de optimización.

# Examples
Input: "Optimiza video.mp4 para web"
Output: `ffmpeg -i video.mp4 -vcodec libx264 -crf 28 output.mp4`
