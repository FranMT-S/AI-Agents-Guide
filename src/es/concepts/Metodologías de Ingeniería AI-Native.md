# Metodologías de Ingeniería AI-Native

## Introducción

Cuando trabajas con agentes de IA, el código generado tiende a **alucinaciones, inconsistencias arquitectónicas y deuda técnica acumulada**. El problema fundamental no es la capacidad del modelo, sino la ausencia de un contrato claro sobre la intención, el comportamiento y los límites del sistema. El desarrollo asistido por IA, cuando carece de estructura, degenera en lo que se conoce como *vibe coding*: una programación puramente intuitiva donde el desarrollador no comprende ni audita la lógica, abrazando exponenciales de generación sin evaluar la calidad técnica subyacente.

Las metodologías AI-Native resuelven esto trasladando el esfuerzo desde el *prompting* conversacional efímero hacia la **ingeniería de sistemas deterministas**. En este paradigma, la IA actúa como un motor de generación eficiente, mientras que el desarrollador senior opera como un arquitecto que define las reglas, los contratos y los mecanismos de verificación.

**Regla de Oro:** Si no controlas la entrada (contexto estructurado) y la verificación (test runners, validadores de esquemas, críticos), tu agente generará deuda técnica a la velocidad de la luz.

---

## Capa Conceptual

Los siguientes conceptos son patrones de ingeniería de software validados a través del tiempo. Adaptarlos al desarrollo con IA es imperativo para garantizar la mantenibilidad y seguridad de sistemas complejos.

### Tabla Comparativa de Metodologías

| Metodología / Patrón | Propósito Principal | Mecanismo de Integración | Limitaciones Clave |
| :--- | :--- | :--- | :--- |
| **Spec-Driven (SDD)** | Define el *qué* y el *por qué* antes del *cómo*. | Flujo estructurado: *Constitution → Specify → Plan*. | *Overhead* alto para tareas menores. |
| **Test-Driven (TDD)** | Validación de caja negra (*fail-closed*). | Integración nativa con *test runners* (ej. Vitest, Pytest). | Requiere entornos de ejecución aislados. |
| **Contract-Driven (CDD)** | Garantiza interoperabilidad de APIs y esquemas. | Repositorio central de contratos OpenAPI/JSON Schema. | Exige diseño *schema-first*. |
| **Readme-Driven (RDD)** | Orientado al consumidor y experiencia de uso. | `README.md` como interfaz de usuario principal. | Riesgo de especulación excesiva (scope drift). |
| **Evaluator-Optimizer** | Auto-corrección iterativa sin intervención humana. | Agente Generador (Actor) + Agente Validador (Crítico). | Alta latencia y costo operativo (tokens). |

---

### Spec-Driven Development (SDD)

El **Spec-Driven Development (SDD)** no es una metodología ágil convencional ni un *framework* prescriptivo; es un cambio de paradigma arquitectónico que traslada la "fuente de verdad" del sistema desde la implementación (código fuente) hacia la especificación (artefactos de diseño). En el contexto de agentes de IA, SDD mitiga el comportamiento no determinista —el *vibe coding*— al obligar al agente a operar dentro de restricciones explícitas.

El paradigma subyacente es la **Descentralización de la Fuente de Verdad** (*Source of Truth Decentralization*). Al tratar la especificación como un artefacto ejecutable y versionable, el desarrollo pasa de ser una actividad de "generación impulsiva" a una de "construcción determinista".

#### Ventajas Analíticas
*   **Aislamiento de la Intención:** La especificación actúa como una capa de abstracción que protege el *intent* del desarrollador frente a las interpretaciones erróneas del agente de IA.
*   **Auditabilidad Arquitectónica:** Al separar la especificación de la implementación, el proceso de *Code Review* se simplifica: es posible auditar si el código resultante satisface el contrato de la especificación sin necesidad de analizar la lógica de bajo nivel del agente.
*   **Reducción de Deuda Técnica "Fantasma":** La IA tiende a introducir código excesivo o innecesario (*gold plating*). SDD establece un perímetro lógico que actúa como *fail-closed*, impidiendo que el agente implemente funcionalidades no solicitadas.

#### Desventajas y Desafíos Técnicos
*   **Fricción en la Velocidad Inicial:** La necesidad de documentar antes de generar incrementa el *time-to-first-code*. SDD es ineficiente en tareas de mantenimiento trivial o parches menores donde la sobrecarga documental supera el riesgo de alucinación.
*   **Riesgo de *Spec Drift*:** El código evoluciona más rápido que los documentos. Si la especificación no se mantiene como una "especificación viva", el sistema se vuelve inconsistente, y el agente comienza a ignorar documentos obsoletos, degradando la confianza en el sistema completo.
*   **Carga Cognitiva:** Requiere que el ingeniero sea capaz de proyectar la arquitectura completa antes de tocar el teclado. Si la especificación inicial es incompleta o errónea, la IA simplemente automatizará la construcción de una arquitectura defectuosa de manera más eficiente.

#### Paradigmas Arquitectónicos y *Gotchas*
*   **Convention over Configuration:** La estructura del repositorio (dónde vive la spec) debe seguir convenciones estrictas para que los agentes la descubran automáticamente sin configurar rutas manualmente.
*   **La trampa del "Super-Prompt":** Un error común es intentar que la especificación sea un documento de 50 páginas. Las ventanas de contexto tienen límites; la especificación debe ser **modular y atómica**. Si la especificación es masiva, el agente sufrirá de *atención difusa* y omitirá requisitos críticos.

#### Implementación Práctica (Agnóstica)

Esta implementación no depende de herramientas propietarias, sino de una estructura de directorios y artefactos que cualquier agente CLI puede procesar.

**Estructura de Directorio:**
```text
/docs/
├── specs/               # Especificaciones de alto nivel (qué y por qué)
│   └── feature-a.md
├── design/              # Planes técnicos (cómo)
│   └── feature-a.plan.md
└── tasks/               # Desglose de implementación (atómico)
    └── feature-a.tasks.md
```

**Esquema de la Especificación (`/docs/specs/feature-a.md`):**
```markdown
# [Nombre del Feature]
## Objetivos de Negocio
- Proporcionar [funcionalidad] para reducir [problema].

## Contrato de Comportamiento
- Entrada: [Estructura/Tipo]
- Salida: [Estructura/Tipo]
- Restricciones: [Tiempo, Memoria, Seguridad]
```

**Ejemplo de Plan de Tareas (`/docs/tasks/feature-a.tasks.md`):**
- [ ] Definir esquemas de datos base para la entidad X.
- [ ] Implementar middleware de validación para entradas.
- [ ] Configurar el gestor de estados para manejar el ciclo de vida.
- [ ] Validar flujos contra casos borde documentados.

**Ejemplo de Comando de Trabajo (Agnóstico):**
```bash
# Paso 1: Generar plan basado en el contrato de la especificación
agente-desarrollo -c "Analiza la especificación en /docs/specs/ y propone un diseño técnico en /docs/design/."

# Paso 2: Implementación atómica basada en el plan validado
agente-desarrollo -c "Ejecuta las tareas definidas en /docs/tasks/feature-a.tasks.md"
```

*Fuentes: [Spec Driven Development: qué es y qué propone](https://scrummanager.com/community/spec-driven-development-qu-es-de_dnde-viene-y-por-qu-importa) | [Using Spec-Driven Development with Claude Code](https://heeki.medium.com/using-spec-driven-development-with-claude-code-4a1ebe5d9f29) | [Conductor: Context-driven development](https://developers.googleblog.com/conductor-introducing-context-driven-development-for-gemini-cli/)*

---

### Test-Driven Development (TDD)

El **Test-Driven Development (TDD)** dicta que escribes el **test primero**, luego haces pasar el test (Ciclo Red-Green-Refactor: *Red*, escribes test que falla; *Green*, implementas código para pasarlo; *Refactor*, mejoras el código). En la era de la IA, TDD transforma una práctica que a menudo se percibía como una carga burocrática en un acelerador masivo de la productividad y la calidad. El test actúa como el *referee* absoluto para el agente de IA, proporcionando un objetivo binario e inequívoco.

**Paradigma Arquitectónico:** *Fail-closed Verification*. La IA genera iterativamente el código para satisfacer las pruebas. Si el *test runner* falla (estado *Red*), el sistema rechaza el intento y realimenta al agente con el registro de errores. Esto fuerza al agente a auto-corregirse sin intervención humana en el ciclo inmediato, asegurando que solo se integre código verificado.

#### Ventajas Analíticas
*   **Criterio de Éxito Inequívoco:** Los tests proporcionan al agente de IA un contrato ejecutable y un criterio de éxito binario (pasa/falla) que elimina la ambigüedad de los prompts.
*   **Auto-Corrección Dirigida:** El *feedback* estructurado del *test runner* (logs de errores) permite al agente depurar y refactorizar de manera autónoma, reduciendo la necesidad de intervención humana para corregir alucinaciones sutiles.
*   **Reducción de Regresiones:** El código generado está continuamente validado, lo que disminuye drásticamente la introducción de regresiones y errores inesperados.

#### Desventajas y Desafíos Técnicos
*   **Falsos Positivos o Negativos:** Un conjunto de tests mal diseñado (tests que pasan incorrectamente o fallan en código correcto) puede llevar al agente a soluciones subóptimas o a un ciclo de depuración ineficiente.
*   **Contexto de Test:** Para que el agente pueda ejecutar y pasar los tests, necesita un entorno de ejecución de pruebas configurado, lo que añade una capa de complejidad al contexto inicial.
*   **Acoplamiento de Tests:** Si los tests están demasiado acoplados a la implementación interna, el refactor se vuelve costoso, tanto para humanos como para agentes.

#### Paradigmas Arquitectónicos y *Gotchas*
*   **Mocking y Aislamiento:** Para tests unitarios, el agente necesita instrucciones claras sobre cómo aislar componentes usando *mocks* o *stubs* para evitar dependencias externas.
*   **Test como Especificación:** Un test bien escrito es una especificación ejecutable. El agente puede "aprender" el comportamiento deseado analizando el test antes de escribir una línea de código.

#### Implementación Práctica (Agnóstica)

Esta implementación utiliza estructuras de archivos comunes para tests y mecanismos genéricos de ejecución.

**Estructura de Directorio:**
```text
mi-proyecto/
├── src/
│   └── logic/
│       └── process-data.ts    # Lógica a implementar
└── __tests__/
    └── logic/
        └── process-data.test.ts # Tests para la lógica
```

**Esquema de Test (`__tests__/logic/process-data.test.ts`):**
```typescript
describe('processData', () => {
  it('should transform data correctly for valid input', async () => {
    const input = { id: '1', value: 10 };
    const expected = { processedId: 'ID-1', transformedValue: 100 };
    const result = await processData(input);
    expect(result).toEqual(expected);
  });

  it('should throw an error for invalid input', async () => {
    const input = { value: 'invalid' };
    await expect(processData(input)).rejects.toThrow('Invalid input');
  });
});
```

**Ejemplo de Comando de Trabajo (Agnóstico):**
```bash
# Paso 1: Iniciar agente en modo TDD, enlazado al sistema de tests
agente-desarrollo --modo tdd --comando-tests "npm test -- --filter processData" --comando-linter "npm run lint"

# Paso 2: Instrucción al agente para implementar la lógica
agente-desarrollo -c "Implementa la función processData en src/logic/process-data.ts para pasar todos los tests definidos."
```

*Fuentes: [Test-Driven Development with AI](https://www.builder.io/blog/test-driven-development-ai) | [Better AI-driven development with TDD](https://medium.com/effortless-programming/better-ai-driven-development-with-test-driven-development-d4849f67e339) | [Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes) | [TDD with AI](https://www.readysetcloud.io/blog/allen.helton/tdd-with-ai/)*

---

### Contract-Driven Development (CDD)

El **Contract-Driven Development (CDD)** prioriza la definición explícita de contratos (interfaces, esquemas, APIs) antes de la implementación. En un ecosistema de IA, la arquitectura debe ser inteligible para las máquinas, no solo para los desarrolladores humanos. Los LLMs, aunque potentes, luchan con la inferencia de la intención a través de jerarquías de clases complejas o polimorfismo, pero sobresalen cuando se les proporcionan entradas explícitas y declarativas como esquemas OpenAPI, GraphQL o JSON Schema. CDD establece una regla fundamental: **contratos sobre clases**.

**Paradigma Arquitectónico:** *Contracts as Code*. Los contratos son artefactos auto-descriptivos, parseables por máquinas y conscientes de las políticas de negocio (ej. autenticación, *rate-limiting*, autorización). Al centralizar estos contratos en un repositorio dedicado, se crea un punto de encuentro innegociable para consumidores y proveedores, lo que facilita la generación de *mocks*, la validación en CI/CD y el desarrollo paralelo sin bloqueos.

#### Ventajas Analíticas
*   **Claridad Unívoca para Agentes:** Los contratos proporcionan a los agentes una definición precisa e inambigua de los modelos de datos, las firmas de funciones y el comportamiento esperado de las APIs, eliminando alucinaciones sobre la estructura de la información.
*   **Integración y Consistencia:** Facilita la integración entre microservicios o componentes generados por diferentes agentes o equipos, ya que todos se adhieren al mismo contrato. Permite la validación temprana en el ciclo de desarrollo.
*   **Generación de Herramientas Auxiliares:** Los contratos pueden usarse para generar automáticamente clientes, *mocks*, stubs, validadores y documentación, aumentando la eficiencia y reduciendo errores manuales.

#### Desventajas y Desafíos Técnicos
*   **Sobrecarga Inicial:** Requiere una inversión significativa de tiempo en el diseño y la escritura de contratos antes de cualquier implementación, lo que puede ralentizar el inicio del proyecto.
*   **Mantenimiento de Contratos:** Los contratos deben mantenerse sincronizados con la evolución del sistema. Un *Contract Drift* (desfase entre el contrato y la implementación real) es una fuente de errores y de desconfianza.
*   **Rigidez Potencial:** Un diseño de contratos demasiado rígido puede dificultar la evolución y la flexibilidad del sistema si los requisitos cambian frecuentemente.

#### Paradigmas Arquitectónicos y *Gotchas*
*   **Schema-First Design:** Este es el principio fundamental de CDD. El diseño del esquema (la forma de los datos) se define antes que la lógica de negocio que lo consume o produce.
*   **Versionado de Contratos:** Es crucial versionar los contratos de API y datos para manejar la compatibilidad hacia atrás y hacia adelante (ej. `v1`, `v2`).
*   **Anotaciones Semánticas:** Incluir metadatos o anotaciones (`x-zone`, `x-rate-limit`) en los esquemas enriquece el contexto para los agentes, permitiéndoles tomar decisiones más informadas sin inferencia.

#### Implementación Práctica (Agnóstica)

Esta implementación se basa en el uso de archivos de esquema estandarizados y herramientas de validación.

**Estructura de Directorio:**
```text
mi-proyecto/
├── contracts/               # Repositorio central de contratos
│   ├── common/              # Definiciones de esquema reutilizables
│   │   └── base-types.yaml
│   └── api/                 # Contratos específicos de API
│       └── user-service.yaml
└── src/
    └── types/               # Tipos de datos generados o manuales
        └── api.ts
```

**Esquema de Contrato (Ej. OpenAPI `contracts/api/user-service.yaml`):**
```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Retrieves a list of users
      responses:
        '200':
          description: A list of user objects
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
components:
  schemas:
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
          format: email
```

**Ejemplos de Comandos de Trabajo (Agnóstico):**
```bash
# Paso 1: Validar la conformidad del contrato con la implementación existente
validador-contratos test --contrato contracts/api/user-service.yaml

# Paso 2: Generar un cliente SDK o un mock server a partir del contrato
generador-sdk --input contracts/api/user-service.yaml --output src/client/

# Paso 3: Instruir al agente para implementar una API basándose en un contrato
agente-desarrollo -c "Implementa el servicio /users GET API en src/services/user.ts siguiendo estrictamente el contrato en contracts/api/user-service.yaml"
```

*Fuentes: [Contract-Driven Development – a Real-World Adoption Journey](https://www.infoq.com/articles/contract-driven-adoption/) | [Contracts Over Classes: Architecting for AI Understanding](https://medium.com/software-architecture-in-the-age-of-ai/contracts-over-classes-architecting-for-ai-understanding-not-just-developer-comfort-646882ebb93c) | [The Power of Contract-Driven Development and AI-Powered Coding](https://medium.com/@ethaizone/the-power-of-contract-driven-development-and-ai-powered-coding-a-synergistic-approach-c09550a4d5fb)*

---

### Readme-Driven Development (RDD)

El **Readme-Driven Development (RDD)** es una metodología que exige documentar rigurosamente la interfaz pública y los escenarios de uso de una librería, componente o servicio en el archivo `README.md` *antes* de implementar la lógica subyacente. Se enfoca en la perspectiva del consumidor final del código.

**Paradigma Arquitectónico:** *Interface-First Design*. En lugar de construir una funcionalidad y luego documentarla, RDD invierte el proceso: se define cómo se usará y comportará el sistema desde fuera, y esa definición se convierte en el contrato principal para el desarrollo interno. Para un agente de IA, un `README.md` bien estructurado es una especificación de alto nivel que le permite comprender el comportamiento esperado de las APIs y generar implementaciones que satisfacen milimétricamente la experiencia de usuario documentada.

#### Ventajas Analíticas
*   **Claridad del Consumidor:** Fuerza a los desarrolladores y a los agentes de IA a pensar desde la perspectiva del usuario o del consumidor de la API, lo que resulta en interfaces más intuitivas y fáciles de usar.
*   **Reducción de Ambigüedad:** Un `README.md` detallado con ejemplos de uso y descripciones de API reduce significativamente la ambigüedad para los agentes de IA, que pueden generar código que se alinee directamente con la documentación.
*   **Comunicación Simplificada:** Sirve como un documento de comunicación conciso y centralizado para el equipo, explicando el *qué* y el *cómo usar* sin necesidad de sumergirse en la implementación.

#### Desventajas y Desafíos Técnicos
*   **Riesgo de *Scope Creep* Temprano:** Si la fase de diseño del `README.md` no está bien controlada, puede llevar a una especificación excesivamente ambiciosa o inestable antes de que la viabilidad técnica sea explorada.
*   **Mantenimiento Dual:** Requiere mantener el `README.md` y el código sincronizados. Un `README.md` obsoleto es peor que no tenerlo, ya que engaña tanto a humanos como a agentes.
*   **Limitado a Interfaces Públicas:** RDD es excelente para interfaces y comportamientos externos, pero es menos efectivo para guiar la implementación de lógicas de negocio internas o detalles arquitectónicos complejos que no se exponen directamente al consumidor.

#### Paradigmas Arquitectónicos y *Gotchas*
*   **Executable Documentation:** El `README.md` no es solo texto; debe contener ejemplos de código ejecutables y descripciones de API que sirvan como micro-especificaciones para los agentes.
*   **Reglas de Agente:** Para hacer RDD efectivo con IA, es crucial configurar reglas en el agente que le exijan leer el `README.md` como fuente primaria para comprender el *intent* antes de generar código.

#### Implementación Práctica (Agnóstica)

Esta implementación se centra en el `README.md` como un contrato ejecutable.

**Estructura de Directorio:**
```text
mi-proyecto/
├── README.md            # Especificación de uso público
└── .agent/              # Configuraciones específicas del agente
    └── rules/
        └── rdd-compliance.mdc # Regla para forzar el seguimiento del README
```

**Paso 1: El Contrato (Esquema de `README.md`)**
Al emplear cuádruple "backtick", el agente entiende que este es el documento primario. Todo el comportamiento público debe ser redactado aquí primero.

````markdown
# [Nombre de la Librería/Servicio]

## Instalación
```bash
npm install my-library
```

## Uso
```typescript
import { myFunction } from 'my-library';
myFunction('argumento');
```

## API
### `myFunction(param: string): void`
Descripción detallada de la función, sus parámetros y su comportamiento esperado.
````

**Paso 2: La Barrera (Regla de Agente)**
Se configura una regla automática (por ejemplo, en Cursor vía `.mdc` o genérica en `AGENTS.md`) para que el agente nunca ignore el contrato.

```yaml
---
name: RDD Compliance
description: Asegura que el código respeta el README.md como contrato de interfaz.
globs: ["src/**/*.ts"]
---

Before implementing any feature or API:
1. You MUST read `README.md` completely.
2. Ensure your implementation matches the documented public API in `README.md` exactly.
3. Forbidden: Inventing APIs, public methods, or behaviors not explicitly documented in the README.
```

**Paso 3: La Delegación (Comando de Trabajo Agnóstico)**
```bash
# Instruir al agente para generar el código interno que hace realidad el README
agente-desarrollo -c "Implementa la lógica interna de 'myFunction' en src/index.ts. Tu única métrica de éxito es que el código finalice compliendo lo que se publicita en el README.md."
```

*Fuente: [Readme-driven development](https://bensguide.substack.com/p/readme-driven-development)*

---

### Evaluator-Optimizer (Patrón Crítico-Actor)

El patrón **Evaluator-Optimizer** implementa un sistema robusto de auto-corrección sin incurrir en los costos y ataduras del *fine-tuning* de los modelos subyacentes. Se estructuran dos agentes especializados que operan en tándem: un **Generador** (*Optimizer* o Actor) que propone una solución, y un **Crítico** (*Evaluator*) que valida el resultado contra un marco de reglas estrictas. Si el Crítico encuentra fallos, el Generador se ve forzado a iterar hasta que la solución sea aceptable.

**Paradigma Arquitectónico:** *Iterative Self-Correction*. El núcleo del patrón radica en preservar inmutable el *intent* original del usuario, corrigiendo iterativamente únicamente la sintaxis o la lógica en base al *feedback* estructurado. Este bucle de retroalimentación cerrado es crucial para tareas de alta precisión donde la alucinación del modelo puede tener consecuencias graves.

#### Ventajas Analíticas
*   **Precisión Elevada:** Aumenta drásticamente la fiabilidad de las respuestas del modelo, especialmente en tareas críticas como la generación de código SQL, configuraciones de seguridad o análisis de vulnerabilidades.
*   **Auto-Depuración Autónoma:** El sistema puede identificar y corregir errores sin intervención humana, reduciendo la carga de trabajo de depuración para los desarrolladores.
*   **Mitigación de Alucinaciones:** Al tener un "segundo cerebro" (el Crítico) que valida las salidas del Generador, se reduce significativamente la probabilidad de alucinaciones.

#### Desventajas y Desafíos Técnicos
*   **Mayor Latencia y Costo:** La ejecución de dos modelos de lenguaje en tándem, con posibles múltiples iteraciones, incrementa significativamente la latencia y el consumo de *tokens*, elevando los costos de inferencia.
*   **Diseño del Crítico:** La efectividad del patrón depende directamente de la calidad del agente Crítico. Si el Crítico es débil o sus reglas son ambiguas, el bucle de auto-corrección será ineficiente.
*   **Bucle Infinito:** Existe el riesgo de que el Generador y el Crítico entren en un bucle infinito si el Generador no logra satisfacer las condiciones del Crítico o si el Crítico proporciona *feedback* contradictorio.

#### Paradigmas Arquitectónicos y *Gotchas*
*   **Feedback Estructurado:** El Crítico debe proporcionar *feedback* en un formato estructurado (ej. JSON con hallazgos específicos) para que el Generador pueda actuar sobre él de manera determinista.
*   **Reglas de Fallback:** Si el Generador falla sistemáticamente, es crucial tener *rule-based fallbacks* (reglas predefinidas no basadas en LLMs) que aseguren que la consulta final sea válida y segura.

#### Implementación Práctica (Agnóstica)

Esta implementación utiliza la orquestación de dos agentes con roles distintos.

**Estructura de Directorio:**
```text
mi-proyecto/
└── agents/                  # Definiciones de agentes especializados
    ├── code-generator.md    # Agente Generador (Actor)
    └── code-reviewer.md     # Agente Crítico (Evaluador)
```

**Ejemplo de Comando de Trabajo (Agnóstico):**
```bash
# Paso 1: El agente "actor" propone una implementación
agente-orquestador -c "Genera una implementación para el endpoint /auth/login en src/auth.ts." --use-agent code-generator

# Paso 2: El agente "crítico" audita la implementación
agente-orquestador -c "Audita el archivo src/auth.ts por seguridad y adherencia a las convenciones." --use-agent code-reviewer

# Paso 3: El agente "actor" corrige basándose en el feedback del crítico
agente-orquestador -c "Corrige los problemas encontrados por el code-reviewer en src/auth.ts." --use-agent code-generator
```

*Fuentes: [Building Self-Correcting LLM Systems: The Evaluator-Optimizer Pattern](https://dev.to/clayroach/building-self-correcting-llm-systems-the-evaluator-optimizer-pattern-169p) | [Evaluator-optimizer workflow with Pydantic AI](https://dylancastillo.co/til/evaluator-optimizer-pydantic-ai.html)*

---

## Ciclo de Trabajo Híbrido: Ejemplo Práctico

Para mostrar cómo funciona en la práctica un ciclo híbrido estructurado, consideremos el desarrollo de un módulo de carrito de compras que integra varias de estas metodologías.

### 1. Definición y Planificación (SDD)

Se inicia con una especificación detallada en `docs/spec.md`, que un agente de planificación transforma en un plan técnico (`docs/plan.md`) y un desglose de tareas (`docs/tasks.md`).

**Esquema de `docs/spec.md`:**
```markdown
# Spec: Carrito de Compras

## Requerimientos Funcionales
- [ ] Agregar productos (máx. 5 unidades por producto).
- [ ] Calcular subtotal, impuestos (15%) y total.
- [ ] Aplicar códigos de descuento (solo uno por pedido).

## Casos Borde Críticos
- Comportamiento si el stock disminuye durante el checkout.
- Prevenir la aplicación de múltiples descuentos simultáneamente.
```

**Esquema de `docs/plan.md`:**
```markdown
# Plan Técnico: Módulo de Carrito

## Componentes
- `src/cart/store.ts`: Gestor de estado del carrito.
- `src/cart/types.ts`: Definiciones de tipos para ítems y estado.
- `src/cart/api.ts`: Interfaz con servicios externos (stock, descuentos).

## Lógica Clave
- Función `addItem`: Valida cantidad máxima por producto (5).
- Función `applyDiscount`: Valida que solo un descuento esté activo.
```

### 2. Implementación y Validación Continua (TDD + Evaluator-Optimizer)

Cada tarea del plan se aborda con un enfoque TDD, donde los tests son escritos antes del código. Un agente generador implementa la lógica, y un agente crítico valida el resultado.

**Esquema de `__tests__/cart/store.test.ts` (TDD):**
```typescript
describe('CartStore', () => {
  it('should not exceed 5 units per product when adding multiple times', () => {
    const store = new CartStore(); // Instancia agnóstica del gestor de estado
    store.addItem({ productId: 'A', quantity: 3, price: 10 });
    store.addItem({ productId: 'A', quantity: 4, price: 10 }); // Añade 4 más, pero el límite es 5
    expect(store.getItemQuantity('A')).toBe(5);
  });

  it('should only apply one discount code', () => {
    const store = new CartStore();
    store.applyDiscount('CODE10', 10);
    store.applyDiscount('CODE20', 20); // Este no debería aplicarse
    expect(store.getCurrentDiscount()).toBe(10);
  });
});
```

**Ejemplo de Flujo de Agentes (TDD + Evaluator-Optimizer):**
```bash
# 1. Agente genera implementación basada en tests
agente-orquestador -c "Implementa el gestor de estado del carrito en src/cart/store.ts para que pase todos los tests en __tests__/cart/store.test.ts." --use-agent code-generator

# 2. Agente crítico valida el código generado
agente-orquestador -c "Revisa el código en src/cart/store.ts por adherencia a las specs, bugs y seguridad." --use-agent code-reviewer

# (Si el crítico encuentra problemas, el orquestador re-alimenta al generador)
```

---

## Matriz de Decisión: Cuál Metodología Usar

| Situación | Recomendación | Por Qué |
| :--- | :--- | :--- |
| **Inicio de un *feature* o épica de producto** | **SDD** | Restringe la autonomía del modelo, asegura que el agente opere sobre un documento versionable y auditable. |
| **Lógica de negocio altamente algorítmica y refactorización** | **TDD** | Establece una validación de caja negra (*fail-closed*) que fuerza la corrección sintáctica del agente en tiempo real. |
| **Diseño y orquestación de APIs o microservicios** | **CDD** | Mitiga alucinaciones en modelos de datos. Provee un punto de anclaje estático y verificable para el ecosistema. |
| **Desarrollo de librerías, SDKs o herramientas CLI** | **RDD** | Define el contrato de usuario y orienta la estructura arquitectónica puramente a la experiencia del consumidor externo. |
| **Generación dinámica de consultas complejas (ej. SQL) o validación E2E** | **Evaluator-Optimizer** | Garantiza precisión extrema a costa de latencia mediante un tándem de agentes en evaluación continua (*feedback loop* cerrado). |
| **Proyectos con complejidad media-alta y equipo distribuido** | **Combinación SDD + TDD + CDD** | Permite una especificación robusta, una implementación verificable y contratos claros entre servicios. |

---

> [!IMPORTANT]
> El éxito del desarrollo de software en la era de la IA reside en entender que **la IA no reemplaza la arquitectura de sistemas; la hace más estricta**. Si quieres escalabilidad, exige validaciones, contratos explícitos y revela el contexto de forma progresiva. Las metodologías AI-Native no son inventadas por proveedores específicos; son patrones de ingeniería adaptados al hecho de que ahora tienes un "compañero" que genera código.
