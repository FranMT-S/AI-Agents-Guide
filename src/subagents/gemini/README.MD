## Subagentes Gemini

Gemini no soporta subdirectorios para agents, por lo que los agentes en src/subagents/gemini/ se deben colocar en el directorio de subagentes de gemini `agents` directamente

Debido a que gemini-cli no soporta que un subagente llame a otro subagente, se usara una skill que sirva como orchestrator. esta skill le dira al agente main como llamar a los subagentes.