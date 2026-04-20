# Metodologías AI-Native: Cómo Evitar Que Tu Agente Genere Deuda Técnica a la Velocidad de la Luz

Cuando trabajas con agentes de IA, el código generado tiende a **alucinaciones, inconsistencias arquitectónicas y deuda técnica acumulada**. El problema fundamental no es la capacidad del modelo, sino la ausencia de un contrato claro sobre la intención, el comportamiento y los límites del sistema. El desarrollo asistido por IA, cuando carece de estructura, degenera en lo que se conoce como *vibe coding*: una programación puramente intuitiva donde el desarrollador no comprende ni audita la lógica, abrazando exponenciales de generación sin evaluar la calidad técnica subyacente.

Las metodologías AI-Native resuelven esto trasladando el esfuerzo desde el *prompting* conversacional efímero hacia la **ingeniería de sistemas deterministas**. En este paradigma, la IA actúa como un motor de generación eficiente, mientras que el desarrollador senior opera como un arquitecto que define las reglas, los contratos y los mecanismos de verificación.

**Regla de Oro:** Si no controlas la entrada (contexto estructurado) y la verificación (test runners, validadores de esquemas, críticos), tu agente generará deuda técnica más rápido de lo que tú puedes leerla.

---

## La Capa Conceptual: Patrones Comprobados para Rescatar a tu Agente del Caos

Los siguientes conceptos son patrones de ingeniería de software validados a través del tiempo. Adaptarlos al desarrollo con IA es imperativo para garantizar la mantenibilidad y seguridad de sistemas complejos donde una máquina generará la mayor parte del texto ejecutable.

### Tabla Comparativa: Eligiendo la Restricción Correcta para tu Proyecto

| Metodología / Patrón | Propósito Principal | Mecanismo de Integración | Limitaciones Clave |
| :--- | :--- | :--- | :--- |
| **Spec-Driven (SDD)** | Define el *qué* y el *por qué* antes del *cómo*. | Flujo estructurado: *Specify → Plan → Implement → Verify*. | *Overhead* alto para tareas menores. |
| **Test-Driven (TDD)** | Validación de caja negra (*fail-closed*). | Ciclo Red-Green-Refactor con *test runners* (Vitest, Pytest). | Requiere entornos de ejecución aislados. |
| **Contract-Driven (CDD)** | Garantiza interoperabilidad de APIs y esquemas. | Repositorio central de contratos OpenAPI/JSON Schema. | Exige diseño *schema-first*. |
| **Readme-Driven (RDD)** | Orientado al consumidor y experiencia de uso. | `README.md` como interfaz de usuario principal. | Riesgo de especulación excesiva (scope drift). |
| **Evaluator-Optimizer** | Auto-corrección iterativa sin intervención humana. | Agente Generador (Actor) + Agente Validador (Crítico). | Alta latencia y costo operativo (tokens). |

---

### Spec-Driven Development: El Antídoto Contra el 'Vibe Coding' y la Generación Impulsiva

El **Spec-Driven Development (SDD)** no es una metodología ágil convencional ni un *framework* prescriptivo; es un cambio de paradigma arquitectónico que traslada la "fuente de verdad" del sistema desde la implementación (código fuente) hacia la especificación (artefactos de diseño). En el contexto de agentes de IA, SDD mitiga el comportamiento no determinista —el *vibe coding*— al obligar al agente a operar dentro de restricciones explícitas.

El paradigma subyacente es la **Descentralización de la Fuente de Verdad**. Al tratar la especificación como un artefacto ejecutable y versionable, el desarrollo pasa de ser una actividad de "generación impulsiva" a una de "construcción determinista".

#### El Valor Real
*   **Aislamiento de la Intención:** La especificación actúa como una capa de abstracción que protege la intención original del desarrollador frente a las interpretaciones erróneas del agente de IA.
*   **Auditabilidad Arquitectónica:** Al separar la especificación de la implementación, el proceso de *Code Review* se simplifica: auditas si el código satisface el documento sin perderte en el razonamiento del LLM.
*   **Reducción de Deuda Técnica "Fantasma":** La IA tiende a introducir código innecesario (*gold plating*). SDD establece un perímetro lógico *fail-closed*, impidiendo que el agente implemente funcionalidades no solicitadas.

#### Puntos Ciegos y Desafíos Técnicos
*   **Fricción en la Velocidad Inicial:** La necesidad de documentar antes de generar incrementa el *time-to-first-code*. SDD es ineficiente en tareas triviales.
*   **Riesgo de *Spec Drift*:** Si la especificación no se actualiza con el código, el agente comenzará a ignorar documentos obsoletos, degradando la confianza de todo el sistema.
*   **Carga Cognitiva:** Requiere que el ingeniero proyecte la arquitectura antes de tocar el teclado. Si la especificación inicial es errónea, la IA simplemente automatizará la construcción de una mala arquitectura a mayor velocidad.

#### Trampas Comunes (*Gotchas*)
*   **Convention over Configuration:** La estructura del repositorio debe seguir convenciones estrictas para que los agentes descubran los documentos automáticamente sin rutas configuradas manualmente.
*   **La trampa del "Super-Prompt":** Un error común es crear un documento de 50 páginas. La especificación debe ser **modular y atómica**, de lo contrario el agente sufrirá de atención difusa y olvidará partes críticas.

#### Implementación Práctica: Flujo Completo con Cuatro Fases

El flujo SDD moderno opera en cuatro fases, tratando los documentos como artefactos de primera clase versionados en Git al lado del código fuente.

**Estructura de Directorio:**
```text
mi-proyecto/
├── docs/
│   ├── specs/                  # Specifications (what and why)
│   │   └── auth-service.md
│   ├── design/                 # Technical plans (how)
│   │   └── auth-service.plan.md
│   └── tasks/                  # Atomic implementation breakdown
│       └── auth-service.tasks.md
└── AGENTS.md                   # Project constitution for the agent
```

**Fase 1 — Especificación (`docs/specs/auth-service.md`):**
```markdown
# Spec: Auth Service with OAuth 2.0

## Business Objectives
- Implement user authentication to reduce unauthorized access.

## Behavior Contract
- Input: Google OAuth callback with `code` param.
- Output: Signed JWT with 24h expiration in an HTTP-only cookie.
- Constraints:
  - JWT secret MUST be injected via env variable, never hardcoded.
  - Tokens MUST be invalidated on logout via a revocation list.

## Edge Cases
- Expired or replayed OAuth codes must return HTTP 401.
- Concurrent login from two devices is allowed, but each gets its own token.
```

**Fase 2 — Descomposición en Tareas (`docs/tasks/auth-service.tasks.md`):**
```markdown
- [ ] Implement JWT service with 24h expiration and env-based secret.
- [ ] Configure Google OAuth middleware with callback validation.
- [ ] Create HTTP-only cookie handler for token delivery.
- [ ] Implement token revocation list (in-memory for MVP, Redis for prod).
- [ ] Write unit tests for token expiration and replay attack rejection.
- [ ] Validate all flows against edge cases defined in the spec.
```

**Fase 3 — Implementación Atómica (Prompt al Agente):**
```bash
# Instruct the agent to work from the spec, one task at a time
claude -p "Read docs/specs/auth-service.md and docs/tasks/auth-service.tasks.md.
Execute only Task 1: Implement the JWT service. Do not implement other tasks.
The only criterion for success is that the spec's behavior contract is satisfied." \
  --allowedTools "Read,Write,Edit,Bash" \
  --max-turns 15
```

**Fase 4 — Auditoría Adversarial (Segundo Agente):**
```bash
# Use a secondary, read-only agent to audit implementation drift
gemini -p "You are an auditor. Compare the current implementation in src/auth/
against the contract defined in docs/specs/auth-service.md.
Identify any deviations, missing edge cases, or violations.
Output your findings as a structured JSON report." \
  --yolo
```

*Fuentes: [Using Spec-Driven Development with Claude Code](https://heeki.medium.com/using-spec-driven-development-with-claude-code-4a1ebe5d9f29) | [Conductor: Context-driven development](https://developers.googleblog.com/conductor-introducing-context-driven-development-for-gemini-cli/) | [Spec Driven Development](https://scrummanager.com/community/spec-driven-development-qu-es-de_dnde-viene-y-por-qu-importa)*

---

### Test-Driven Development: El Único Veredicto Binario que un Agente No Puede Ignorar

El **Test-Driven Development (TDD)** dicta que escribes el **test primero**, después haces pasar el test (ciclo Red-Green-Refactor). En la era de la IA, TDD transforma una práctica percibida como carga burocrática en un acelerador de productividad. El test actúa como el *referee* absoluto para el agente de IA, proporcionando un objetivo binario e inequívoco. Prompting an AI agent with "make a login button" is a gamble — prompting it with a test suite that defines exactly how that button must behave is a contract.

**Paradigma Arquitectónico:** *Fail-closed Verification*. La IA genera iterativamente el código para satisfacer las pruebas. Si el *test runner* falla (estado *Red*), el sistema rechaza el intento y retroalimenta al agente con el registro de errores, forzando la corrección sin intervención humana en el ciclo inmediato.

#### El Valor Real
*   **Criterio de Éxito Inequívoco:** Los tests proporcionan un contrato ejecutable (pasa/falla) que elimina la ambigüedad que sufren los prompts en lenguaje natural.
*   **Auto-Corrección Dirigida:** El *feedback* estructurado del *test runner* permite al agente depurar de manera autónoma, corrigiendo alucinaciones de forma invisible para el usuario.
*   **Reducción de Regresiones:** El código generado siempre se valida contra una suite paralela de pruebas estrictas.

#### Puntos Ciegos y Desafíos Técnicos
*   **Falsos Positivos o Negativos:** Un test mal diseñado puede atrapar al agente en un bucle infinito buscando una solución que el test hace imposible satisfacer.
*   **El Entorno Primero:** Para que el agente ejecute y pase tests, necesita un entorno de ejecución (Node.js, Pytest) configurado y funcional. Sin esto, el ciclo no puede arrancar.
*   **Acoplamiento de Tests:** Si los tests están fuertemente acoplados a detalles de implementación internos, cualquier refactorización del agente romperá la suite.

#### Trampas Comunes (*Gotchas*)
*   **Mocking y Aislamiento:** Define explícitamente cómo el agente debe usar *mocks* o *stubs*. Si intenta consultar una API real durante un test de unidad, el test fallará por razones externas al código.
*   **Test como Especificación:** Un test bien escrito es un contrato ejecutable. El modelo extraerá la intención del sistema *leyendo el test* antes de escribir una sola línea funcional — lo que lo convierte en el artefacto de diseño más poderoso que puedes darle.

#### Implementación Práctica: El Ciclo Red-Green-Refactor con un Agente Real

El siguiente ejemplo construye un carrito de compras paso a paso, mostrando el flujo completo que el agente ejecuta.

**Estructura de Directorio:**
```text
mi-proyecto/
├── src/
│   └── cart/
│       ├── store.ts          # Logic to implement (starts empty)
│       └── types.ts          # Type definitions
└── __tests__/
    └── cart/
        └── store.test.ts     # Tests written FIRST (before store.ts exists)
```

**Fase RED — Escribir los Tests Antes del Código (`__tests__/cart/store.test.ts`):**
```typescript
import { CartStore } from '../../src/cart/store';

describe('CartStore', () => {
  it('should calculate the correct total for multiple items', () => {
    const store = new CartStore();
    store.addItem({ productId: 'A', price: 10, quantity: 2 });
    store.addItem({ productId: 'B', price: 5, quantity: 3 });
    // Total: (10 * 2) + (5 * 3) = 35
    expect(store.getTotal()).toBe(35);
  });

  it('should not exceed 5 units per product', () => {
    const store = new CartStore();
    store.addItem({ productId: 'A', price: 10, quantity: 3 });
    store.addItem({ productId: 'A', price: 10, quantity: 4 }); // Should be capped
    expect(store.getItemQuantity('A')).toBe(5);
  });

  it('should only apply one discount code at a time', () => {
    const store = new CartStore();
    store.applyDiscount('CODE10', 10);
    store.applyDiscount('CODE20', 20); // Second discount should be rejected
    expect(store.getActiveDiscount()).toBe(10);
  });

  it('should throw an error when adding an item with negative price', () => {
    const store = new CartStore();
    expect(() => store.addItem({ productId: 'X', price: -5, quantity: 1 }))
      .toThrow('Price cannot be negative');
  });
});
```

**Fase GREEN — Prompt al Agente para Implementar:**
```bash
# The agent reads the failing tests and implements the minimum code to make them pass
claude -p "The test suite in __tests__/cart/store.test.ts defines the full behavior
for CartStore. Implement the CartStore class in src/cart/store.ts.
Write the minimum code required to pass all tests. Do not add features not covered by tests.
Run 'npm test' after each change to verify progress." \
  --allowedTools "Read,Write,Edit,Bash" \
  --max-turns 20
```

**Fase REFACTOR — Prompt para la Mejora:**
```bash
# After tests pass, ask the agent to clean the implementation
claude -p "All tests in __tests__/cart/store.test.ts pass. Now refactor src/cart/store.ts:
1. Improve variable naming for readability.
2. Extract repeated logic into private helper methods.
3. Ensure all edge cases have inline comments explaining the business rule.
Run 'npm test' after refactoring to confirm no regressions." \
  --allowedTools "Read,Write,Edit,Bash" \
  --max-turns 10
```

*Fuentes: [Test-Driven Development with AI](https://www.builder.io/blog/test-driven-development-ai) | [Better AI-driven development with TDD](https://medium.com/effortless-programming/better-ai-driven-development-with-test-driven-development-d4849f67e339) | [Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)*

---

### Contract-Driven Development: Contratos Estrictos para Máquinas Probabilísticas

El **Contract-Driven Development (CDD)** prioriza la definición explícita de contratos (interfaces, esquemas, APIs) antes de la implementación. Los LLMs luchan con la inferencia a través de jerarquías de clases complejas o polimorfismo profundo, pero sobresalen cuando se les proporcionan entradas declarativas como OpenAPI, GraphQL schema o JSON Schema. La regla es innegociable: **contratos sobre clases**.

**Paradigma Arquitectónico:** *Contracts as Code*. Los contratos son artefactos auto-descriptivos, parseables por máquinas y estandarizados. Al centralizarlos en un repositorio dedicado, crean el punto de encuentro innegociable entre consumidores y proveedores, facilitando la generación automática de mocks, la validación en CI/CD y el desarrollo paralelo de múltiples agentes sin bloqueos.

#### El Valor Real
*   **Claridad Unívoca para Agentes:** Despeja toda duda sobre la firma de métodos, tipos de retorno y estructuras de datos de respuesta.
*   **Integración Paralela:** Varios subagentes pueden trabajar en paralelo si todos respetan el mismo contrato YAML de antemano — sin coordinación conversacional.
*   **Generación de Herramientas Auxiliares:** Los esquemas sirven para generar automáticamente clientes SDK, *mocks* de servidor y documentación sin esfuerzo manual adicional.

#### Puntos Ciegos y Desafíos Técnicos
*   **Sobrecarga Inicial:** Requiere definir todo el esquema rigurosamente antes de empezar a implementar lógica de negocio.
*   **Contract Drift:** Un esquema desactualizado engaña mortalmente al agente: trabajará sobre una definición obsoleta mientras la API en producción es completamente diferente.

#### Trampas Comunes (*Gotchas*)
*   **Schema-First Design:** El diseño del esquema siempre precede a cualquier capa lógica. Nunca al revés.
*   **Anotaciones Semánticas:** Añadir extensiones como `x-rate-limit` o `x-auth-required` en el esquema instruye directamente al agente sin requerirle inferir contexto del nombre del endpoint.
*   **Contract-as-Test en CI/CD:** El pipeline de CI debe fallar automáticamente si la API devuelve un campo extra, un tipo cambiado o falta un código de error documentado en el contrato.

#### Implementación Práctica: Del Contrato YAML al Código Generado

**Estructura de Directorio:**
```text
mi-proyecto/
├── contracts/
│   ├── common/
│   │   └── base-types.yaml          # Reusable schema definitions ($ref targets)
│   └── api/
│       └── user-service.yaml        # OpenAPI 3.x contract for user management
└── src/
    ├── types/
    │   └── api.ts                   # Types generated from the contract
    └── services/
        └── user.service.ts          # Implementation driven by the contract
```

**Contrato OpenAPI (`contracts/api/user-service.yaml`):**
```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
paths:
  /users:
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Validation error (malformed email or missing required fields)
        '409':
          description: User with this email already exists
components:
  schemas:
    CreateUserRequest:
      type: object
      required: [name, email]
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 100
        email:
          type: string
          format: email
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
        createdAt:
          type: string
          format: date-time
```

**Flujo de Trabajo Completo:**
```bash
# Step 1: Generate TypeScript types from the contract automatically
npx openapi-typescript contracts/api/user-service.yaml -o src/types/api.ts

# Step 2: Generate a mock server to test against before implementing
npx @stoplight/prism-cli mock contracts/api/user-service.yaml &

# Step 3: Instruct the agent to implement the service using the contract as law
claude -p "Implement the POST /users endpoint in src/services/user.service.ts.
The OpenAPI contract is in contracts/api/user-service.yaml — it is the single source of truth.
Use the generated types from src/types/api.ts.
Return HTTP 409 if email already exists. Return HTTP 400 for any validation error.
Do not add any field or behavior not documented in the contract." \
  --allowedTools "Read,Write,Edit,Bash" \
  --max-turns 15

# Step 4: Validate the implementation against the contract in CI
npx @schemathesis/cli run contracts/api/user-service.yaml \
  --url http://localhost:3000 \
  --checks all
```

*Fuentes: [Contract-Driven Development – a Real-World Adoption Journey](https://www.infoq.com/articles/contract-driven-adoption/) | [Contracts Over Classes: Architecting for AI Understanding](https://medium.com/software-architecture-in-the-age-of-ai/contracts-over-classes-architecting-for-ai-understanding-not-just-developer-comfort-646882ebb93c) | [The Power of Contract-Driven Development and AI-Powered Coding](https://medium.com/@ethaizone/the-power-of-contract-driven-development-and-ai-powered-coding-a-synergistic-approach-c09550a4d5fb)*

---

### Readme-Driven Development: Forzando a la IA a Pensar en Quien Usará el Código

El **Readme-Driven Development (RDD)** exige escribir el `README.md` completo *antes* de la primera línea de implementación. En lugar de construir código y luego documentarlo, defines cómo se usará el sistema desde afuera (*interface-first*), y esa definición se convierte en el contrato principal de desarrollo. Para un agente de IA, un `README.md` bien estructurado con ejemplos ejecutables es una especificación de alto nivel que le permite comprender el comportamiento esperado sin ambigüedad.

**Paradigma Arquitectónico:** *Interface-First Design*. El `README.md` no es solo documentación — es la especificación del sistema vista desde los ojos del consumidor final. Esto fuerza al agente a pensar en la usabilidad antes que en la arquitectura interna.

#### El Valor Real
*   **Claridad del Consumidor:** Promueve interfaces más intuitivas al forzar al agente a diseñar empezando desde la experiencia de uso, no desde la conveniencia técnica de implementación.
*   **Early Consensus:** Al compartir el `README.md` primero, el equipo puede dar feedback sobre el diseño de la API antes de que se escriba una sola línea de código.
*   **Avoids Over-Engineering:** Mantiene la documentación liviana y centrada en lo que el usuario necesita saber para comenzar, frenando la tendencia del modelo de añadir capas de abstracción innecesarias.

#### Puntos Ciegos y Desafíos Técnicos
*   **Riesgo de *Scope Creep*:** Es fácil diseñar en markdown funciones ambiciosas que luego toman semanas en codificarse con calidad real.
*   **Mantenimiento Dual:** Un `README.md` obsoleto es peor que no tenerlo — engaña tanto a humanos como al agente. Debe actualizarse **antes** de que se cambie el código.
*   **Limitado a Interfaces Públicas:** RDD no puede guiar la arquitectura de controladores profundos o lógica de negocio interna. Solo describe lo que es visible para el consumidor externo.

#### Trampas Comunes (*Gotchas*)
*   **Executable Documentation:** Los bloques de código dentro del `README.md` deben ser completos y ejecutables, no pseudocódigo. El agente los leerá como contratos.
*   **Reglas de Agente Estrictas:** Sin anclajes rígidos en `AGENTS.md` o `.mdc`, el agente simplemente ignorará el `README.md` al momento de codificar.

#### Implementación Práctica: Construcción de una Librería Python Paso a Paso

El siguiente ejemplo muestra RDD aplicado a una librería de Python para obtener precios de criptomonedas.

**Estructura de Directorio:**
```text
mi-proyecto/
├── README.md                # Written FIRST — public interface and usage contract
├── tests/
│   └── test_usage.py        # Tests derived directly from README.md examples
├── src/
│   └── cryptopricefetcher/
│       └── client.py        # Implementation written LAST to satisfy README + tests
└── .agent/
    └── rules/
        └── rdd-compliance.mdc  # Rule that forces the agent to follow the README
```

**Paso 1 — La Especificación: Escribir el `README.md` Primero:**
````markdown
# CryptoPriceFetcher

A lightweight Python library to fetch real-time cryptocurrency prices.

## Installation
```bash
pip install cryptopricefetcher
```

## Usage

```python
from cryptopricefetcher import Client

client = Client(api_key="your_api_key")

# Get the current price of Bitcoin in USD
price = client.get_price("BTC")
print(f"Current BTC price: ${price:.2f}")

# Get prices for multiple assets in batch
prices = client.get_prices(["BTC", "ETH", "SOL"])
print(prices)  # {"BTC": 67400.0, "ETH": 3200.0, "SOL": 145.0}
```

## Error Handling
```python
from cryptopricefetcher import Client, AssetNotFoundError, AuthenticationError

try:
    price = client.get_price("UNKNOWN")
except AssetNotFoundError as e:
    print(f"Asset not found: {e}")
except AuthenticationError as e:
    print(f"Invalid API key: {e}")
```
````

**Paso 2 — La Prueba: Tests Derivados Directamente del README:**
```python
# tests/test_usage.py
# Every test here mirrors a usage example from README.md.
# If README.md changes, these tests must be updated first.
from cryptopricefetcher import Client, AssetNotFoundError, AuthenticationError

def test_get_single_price_returns_float():
    client = Client(api_key="test_key")
    price = client.get_price("BTC")
    assert isinstance(price, float)
    assert price > 0

def test_get_prices_batch_returns_dict():
    client = Client(api_key="test_key")
    prices = client.get_prices(["BTC", "ETH"])
    assert isinstance(prices, dict)
    assert "BTC" in prices and "ETH" in prices

def test_unknown_asset_raises_asset_not_found_error():
    client = Client(api_key="test_key")
    with pytest.raises(AssetNotFoundError):
        client.get_price("UNKNOWN_COIN_XYZ")
```

**Paso 3 — La Barrera: Regla para Forzar que el Agente Siga el README:**
```yaml
---
name: RDD Compliance
description: Forces the agent to follow README.md as the primary interface contract.
globs: ["src/**/*.py"]
---

Before implementing any feature, class, or function:
1. You MUST read README.md completely.
2. Your implementation must match every documented public interface exactly.
3. Forbidden: Any public method, class, or exception not explicitly documented in README.md.
4. If README.md and the tests conflict, report the conflict — do not resolve it unilaterally.
```

**Paso 4 — La Delegación: Prompt al Agente:**
```bash
claude -p "Read README.md and tests/test_usage.py completely.
Implement the CryptoPriceFetcher library in src/cryptopricefetcher/client.py.
Your only metric of success: the public API matches README.md exactly and all tests pass.
Run 'pytest tests/' after implementing to verify." \
  --allowedTools "Read,Write,Edit,Bash" \
  --max-turns 20
```

*Fuentes: [Readme-driven development](https://bensguide.substack.com/p/readme-driven-development) | [README-Driven Development (deterministic.space)](https://deterministic.space/readme-driven-development.html)*

---

### Evaluator-Optimizer (Crítico-Actor): Dos Modelos Discuten para Que Tú No Tengas Que Depurar

El patrón **Evaluator-Optimizer** implementa auto-corrección iterativa sin reentrenamiento ni fine-tuning de los modelos subyacentes. Un **Generador** (Actor) propone la solución, y un **Crítico** (Evaluador) la evalúa contra criterios de corrección estrictos. Si el Crítico encuentra fallos, el Generador recibe el feedback estructurado y reintenta. El bucle continúa hasta que la solución pase la validación o se alcance un límite de iteraciones.

La clave conceptual es que el Evaluador preserva el **intent** original del usuario durante todo el ciclo — solo se corrige la sintaxis o la lógica, nunca se redefine el objetivo.

**Paradigma Arquitectónico:** *Iterative Self-Correction*. Extraído de un caso de producción real: los LLMs generan SQL con la intención correcta pero con errores de sintaxis específicos del motor de base de datos (como usar `count() * duration` en lugar de `sum(duration)` en ClickHouse). En lugar de reentrenar el modelo para que aprenda ClickHouse, el sistema detecta el error, le explica *exactamente* qué está mal, y el modelo lo corrige en el siguiente turno.

#### El Valor Real
*   **Precisión sin Fine-Tuning:** Corrige errores sistemáticos del modelo en tiempo real sin tocar los pesos del modelo. Efectivo para SQL, regex, YAML de configuración y cualquier dominio con criterios de éxito binarios.
*   **Auto-Depuración Autónoma:** El sistema identifica y corrige errores sin intervención humana, reduciendo el tiempo de depuración de horas a segundos.
*   **Rule-Based Fallbacks:** Cuando el LLM falla repetidamente, reglas deterministas (no basadas en LLMs) pueden capturar patrones de error comunes y aplicar correcciones automáticas.

#### Puntos Ciegos y Desafíos Técnicos
*   **Coste por Iteración:** Cada iteración consume tokens de dos modelos. Sin un techo de iteraciones, el coste puede escalar exponencialmente en bucles largos.
*   **Bucle Infinito:** Si el Evaluador es demasiado estricto o proporciona feedback contradictorio, y el Generador no puede satisfacerlo, el sistema se queda en un bucle hasta agotar el límite.
*   **Calidad del Evaluador:** La efectividad del patrón depende completamente de la calidad del Evaluador. Un Crítico débil valida código incorrecto como correcto.

#### Trampas Comunes (*Gotchas*)
*   **Feedback Estructurado y Específico:** El Crítico debe decir *exactamente* qué está mal y por qué, no solo "error". En el ejemplo del SQL: "Fix: Replace `count() * duration_ns` with `sum(duration_ns)` — ClickHouse requires column references to be inside aggregate functions."
*   **Preservar el Intent:** El Generador en cada iteración recibe el objetivo original + el feedback de la última iteración. Nunca solo el feedback. Sin el goal original, el modelo pierde el contexto de qué está intentando hacer.
*   **Max Iterations:** Define siempre un máximo de 3-5 iteraciones. Si supera el límite, escala a revisión humana o aplica el rule-based fallback.

#### Implementación Práctica: Auto-Corrección de SQL para Generación Dinámica

**Estructura de Directorio:**
```text
mi-proyecto/
└── agents/
    ├── code-generator.md    # Generator agent system prompt (Actor)
    └── code-reviewer.md     # Evaluator agent system prompt (Critic)
```

**Definición del Sistema (Python — implementación del loop):**
```python
import json

def generate_sql(goal: str, feedback: str | None = None) -> str:
    """Calls the Generator LLM with the original goal and optional critique feedback."""
    prompt = f"Generate a ClickHouse SQL query to: {goal}"
    if feedback:
        # Preserve the original intent while providing specific correction
        prompt += f"\n\nPrevious attempt was incorrect. Specific issues to fix:\n{feedback}"
        prompt += "\nIMPORTANT: Keep the original analysis goal unchanged. Only fix the syntax issues listed above."
    # Call your LLM here (Claude, Gemini, GPT-4, etc.)
    return call_llm(prompt)

def evaluate_sql(sql: str, goal: str) -> dict:
    """Evaluates the generated SQL using EXPLAIN AST (fast, no data scan) then SELECT LIMIT 1."""
    # First pass: validate syntax cheaply with EXPLAIN AST
    explain_result = run_query(f"EXPLAIN AST {sql}")
    if explain_result.error:
        return {
            "is_approved": False,
            "feedback": f"Syntax error: {explain_result.error}. Fix the specific clause mentioned."
        }
    # Second pass: test execution with a minimal scan
    test_result = run_query(f"SELECT * FROM ({sql}) LIMIT 1")
    if test_result.error:
        return {
            "is_approved": False,
            "feedback": f"Execution error: {test_result.error}. Column references and table names must match the schema."
        }
    return {"is_approved": True, "feedback": ""}

def run_evaluator_optimizer(goal: str, max_iterations: int = 3) -> str:
    """Main loop: generate, evaluate, and iterate until success or max_iterations."""
    feedback = None

    for attempt in range(1, max_iterations + 1):
        print(f"--- Attempt {attempt}/{max_iterations} ---")
        sql = generate_sql(goal, feedback)
        result = evaluate_sql(sql, goal)

        if result["is_approved"]:
            print(f"Success on attempt {attempt}.")
            return sql

        print(f"Feedback for next attempt: {result['feedback']}")
        feedback = result["feedback"]

    # If all LLM attempts fail, apply deterministic rule-based fixes
    print("LLM failed to self-correct. Applying rule-based fallback.")
    return apply_rule_based_fallback(sql)

def apply_rule_based_fallback(sql: str) -> str:
    """Applies common ClickHouse syntax fixes as a deterministic safety net."""
    # Common pattern: count() * column -> sum(column)
    sql = re.sub(r'count\(\)\s*\*\s*(\w+)', r'sum(\1)', sql)
    # Common pattern: database.table -> table (when db is already selected)
    sql = re.sub(r'\botel\.(\w+)\b', r'\1', sql)
    return sql
```

**Ejemplo del Efecto Real (basado en producción):**
```sql
-- Attempt 1 (Generator): Common mistake across all models
SELECT service_name,
       count() * (duration_ns/1000000) as total_duration_ms,
       count() as request_count
FROM otel.traces
WHERE service_name IN ('frontend', 'backend')
GROUP BY service_name
ORDER BY total_duration_ms DESC

-- Evaluator finds 2 issues:
-- 1. Error 215: count() * duration_ns — duration_ns must be inside an aggregate function
-- 2. Error 60: otel.traces — connection already specifies database, use 'traces' only

-- Attempt 2 (Generator + Evaluator Feedback): Self-corrected
SELECT service_name,
       sum(duration_ns/1000000) as total_duration_ms,
       count() as request_count,
       avg(duration_ns/1000000) as avg_duration_ms  -- Model even added useful metric
FROM traces
WHERE service_name IN ('frontend', 'backend')
GROUP BY service_name
ORDER BY total_duration_ms DESC

-- Evaluator: APPROVED (validates in 96ms via SELECT LIMIT 1)
```

*Fuentes: [Building Self-Correcting LLM Systems: The Evaluator-Optimizer Pattern](https://dev.to/clayroach/building-self-correcting-llm-systems-the-evaluator-optimizer-pattern-169p) | [Evaluator-optimizer workflow with Pydantic AI](https://dylancastillo.co/til/evaluator-optimizer-pydantic-ai.html) | [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)*

---

## El Ciclo Híbrido en Acción: Orquestando Metodologías Sin Que el Proyecto Colapse

Para demostrar cómo funciona en la práctica, el siguiente ejemplo construye un módulo de carrito de compras completo combinando SDD + TDD + Evaluator-Optimizer, mostrando exactamente qué hace el agente en cada fase y por qué.

### Fase 1: Definición (SDD) — Antes de Generar una Sola Línea

Se parte de una especificación detallada y versionada. El agente no genera código hasta que la especificación esté aprobada y en Git.

**`docs/specs/cart.md` — El Contrato de Alto Nivel:**
```markdown
# Spec: Shopping Cart Module

## Functional Requirements
- [ ] Add products (max 5 units per product).
- [ ] Calculate subtotal, taxes (15%), and total.
- [ ] Apply discount codes (only one per order at a time).

## Critical Edge Cases
- If stock decreases during checkout, the cart must be re-validated.
- Multiple discounts simultaneously applied must be rejected with HTTP 409.
- Negative prices or quantities must throw a validation error.
```

**`docs/tasks/cart.tasks.md` — Desglose Atómico:**
```markdown
- [ ] Task 1: Implement CartStore with addItem() and 5-unit cap.
- [ ] Task 2: Implement getTotal() with tax calculation (15%).
- [ ] Task 3: Implement applyDiscount() rejecting multiple active codes.
- [ ] Task 4: Write unit tests for all edge cases defined in the spec.
- [ ] Task 5: Run audit agent against spec to verify no behavioral drift.
```

### Fase 2: Implementación y Validación Continua (TDD + Evaluator-Optimizer)

Los tests se escriben primero; el Agente Generador implementa; el Agente Crítico audita.

**`__tests__/cart/store.test.ts` — Escrito ANTES de la implementación:**
```typescript
describe('CartStore', () => {
  it('should cap quantity at 5 units per product', () => {
    const store = new CartStore();
    store.addItem({ productId: 'A', quantity: 3, price: 10 });
    store.addItem({ productId: 'A', quantity: 4, price: 10 }); // Over the limit
    expect(store.getItemQuantity('A')).toBe(5);
  });

  it('should calculate total with 15% tax correctly', () => {
    const store = new CartStore();
    store.addItem({ productId: 'A', quantity: 2, price: 100 });
    // Subtotal: 200 | Tax: 30 | Total: 230
    expect(store.getTotal()).toBe(230);
  });

  it('should reject a second discount code when one is already active', () => {
    const store = new CartStore();
    store.applyDiscount('CODE10', 10);
    expect(() => store.applyDiscount('CODE20', 20))
      .toThrow('A discount is already active. Remove it before applying a new one.');
  });
});
```

**Flujo Agente Generador → Agente Crítico:**
```bash
# Generator: implement from the failing tests
claude -p "Implement CartStore in src/cart/store.ts to pass all tests in __tests__/cart/.
Run 'npm test' after each change. Do not implement any feature not covered by the tests." \
  --allowedTools "Read,Write,Edit,Bash" \
  --max-turns 20

# Critic (Evaluator): audit implementation drift from the spec
gemini -p "Compare src/cart/store.ts against docs/specs/cart.md.
Identify any spec violations, missing edge cases, or behaviors added beyond what was specified.
Report findings as a JSON array with keys: issue, location, severity (low/medium/critical)." \
  --yolo
```

---

## Matriz de Decisión: Qué Metodología Usar Antes de Que el Proyecto Colapse Solo

| Situación | Recomendación | Mayor Beneficio |
| :--- | :--- | :--- |
| **Inicio de un feature masivo / épica de negocio** | **SDD** | Restringe la imaginación incontrolada del modelo a un plano versionable y estricto con criterios de auditoría claros. |
| **Lógica algorítmica compleja que no admite fallas** | **TDD** | El LLM se centra en pasar validaciones binarias y no divaga en refactorizaciones no solicitadas. |
| **Diseño y orquestación de APIs o microservicios** | **CDD** | Salva al agente de alucinar modelos de datos. El contrato OpenAPI es la única fuente de verdad. |
| **Desarrollo de librerías, SDKs o herramientas CLI** | **RDD** | Optimiza al agente para la usabilidad de terceros. Todo se diseña desde afuera hacia adentro. |
| **Generación dinámica de SQL, regex, configs complejas** | **Evaluator-Optimizer** | Corrige errores sistemáticos en tiempo real sin fine-tuning, con un rule-based fallback como red de seguridad. |
| **Proyectos maduros con múltiples capas de negocio** | **Mix (SDD + TDD)** | Intenciones macro claras con validación binaria estricta para aislar regresiones en cada capa. |

---

> [!IMPORTANT]
> El éxito del desarrollo de software en la era de la IA reside en entender que **la IA no reemplaza la arquitectura de sistemas; la hace inmensamente más estricta**. Si buscas escalabilidad a largo plazo, no entregues código crudo al modelo: exígele que procese validaciones blindadas, pague peaje mediante TDD u opere atado a un contrato explícito preexistente.
