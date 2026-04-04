import os
import re

GUIDE_PATH = "My-AI-Learning-Guide-ES.md"

def test_file_exists():
    assert os.path.exists(GUIDE_PATH), f"Error: {GUIDE_PATH} not found."

def test_spanish_headers():
    required_headers = [
        r"# Mi Guía de Aprendizaje de Agentes de IA",
        r"## Índice",
        r"## Introducción y Conceptos Básicos",
        r"## Skills \(Habilidades\)",
        r"## MCP \(Model Context Protocol\)",
        r"## Plugins y Extensiones",
        r"## Hooks \(Disparadores\)",
        r"## Subagentes",
        r"## Automatización y Scripting",
        r"## Evaluación de Modelos"
    ]
    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    for header in required_headers:
        assert re.search(header, content, re.IGNORECASE), f"Error: Header '{header}' not found."

def test_obsidian_callouts_placeholders():
    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Placeholder:" in content, "Error: Placeholders not found."

if __name__ == "__main__":
    try:
        test_file_exists()
        test_spanish_headers()
        test_obsidian_callouts_placeholders()
        print("Success: All tests passed.")
    except AssertionError as e:
        print(e)
        exit(1)
