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
        # Using a more flexible check for encoding issues if necessary, 
        # but let's try direct first with proper encoding.
        assert re.search(header, content, re.IGNORECASE), f"Error: Header '{header}' not found."

def test_core_concepts_content():
    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    required_keywords = [
        "Memoria Persistente",
        "AGENTS.md",
        "GEMINI.md",
        "CLAUDE.md",
        "Scope",
        "Global",
        "Proyecto",
        "Subdirectorio"
    ]
    for keyword in required_keywords:
        assert keyword in content, f"Error: Keyword '{keyword}' not found in Core Concepts."

def test_skills_content():
    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Check for presence of substrings to avoid encoding issues with 'í' or '¿'
    required_substrings = [
        "Skills (Habilidades)",
        "Metadatos",
        "templates",
        "de una Skill", # Anatomy of a Skill
        "progressive disclosure"
    ]
    for substring in required_substrings:
        assert substring in content, f"Error: Substring '{substring}' not found in Skills section."

def test_mcp_advanced_content():
    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    required_keywords = [
        "MCP (Model Context Protocol)",
        "Sandboxing",
        "docker exec",
        "disabledTools",
        "excludeTools",
        "Reseteo", # Capitalized
        "settings.json"
    ]
    for keyword in required_keywords:
        assert keyword in content, f"Error: Advanced keyword '{keyword}' not found in MCP section."

def test_hooks_subagents_deep_dive():
    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    required_keywords = [
        "Hooks",
        "Subagentes",
        "stdin/stdout",
        "exit 2",
        "determinista",
        "aislado",
        "Agent Teams",
        "headless"
    ]
    for keyword in required_keywords:
        assert keyword in content, f"Error: Deep-dive keyword '{keyword}' not found in Hooks/Subagents section."

def test_model_evaluation_content():
    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    required_keywords = [
        "Evaluación de Modelos",
        "Comparativa Técnica",
        "SWE-bench",
        "Terminal-Bench 2.0",
        "Gemini 3.1 Pro",
        "Claude 4.6 Sonnet",
        "GPT-5.3 Codex",
        "Casos de Uso Recomendados"
    ]
    for keyword in required_keywords:
        assert keyword in content, f"Error: Keyword '{keyword}' not found in Model Evaluation section."

if __name__ == "__main__":
    try:
        test_file_exists()
        test_spanish_headers()
        test_core_concepts_content()
        test_skills_content()
        test_mcp_advanced_content()
        test_hooks_subagents_deep_dive()
        test_model_evaluation_content()
        print("Success: All tests passed.")
    except AssertionError as e:
        print(e)
        exit(1)
