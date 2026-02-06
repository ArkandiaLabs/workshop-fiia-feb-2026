# Ejemplos de Introducción a LLMs

Este directorio contiene ejemplos prácticos para aprender a trabajar con APIs de Large Language Models (LLMs).

## Requisitos Previos

- Python 3.12+
- API keys de los proveedores que desees usar (OpenAI, Anthropic, Google)

## Configuración

### 1. Crear entorno virtual

```bash
python -m venv venv
```

Activar el entorno virtual:

**macOS / Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

> Si tienes problemas de permisos en PowerShell, ejecuta primero:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo de ejemplo:

**macOS / Linux:**
```bash
cp .env.example .env
```

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Edita `.env` con tus claves:

```
OPENAI_API_KEY=tu_clave_de_openai
ANTHROPIC_API_KEY=tu_clave_de_anthropic
GEMINI_API_KEY=tu_clave_de_gemini
```

## Ejemplos

### 01 - Primera Llamada a un LLM

Ejemplos básicos de cómo hacer tu primera llamada a diferentes proveedores de LLMs.

```bash
# Usando OpenAI SDK
python 01-first-call/openai_first_call.py

# Usando OpenAI REST API directamente
python 01-first-call/openai_first_call_rest_api.py

# Usando Anthropic (Claude)
python 01-first-call/anthropic_first_call.py

# Usando Google Gemini
python 01-first-call/gemini_first_call.py
```

### 02 - Tokens y Costos

Aprende cómo funcionan los tokens y cómo calcular el costo de las llamadas.

```bash
python 02-tokens.py
```

Este script muestra:
- Conteo de tokens de entrada y salida
- Cálculo de costos basado en precios por millón de tokens

### 03 - Temperatura

Explora cómo el parámetro de temperatura afecta las respuestas del modelo.

```bash
# Comparar diferentes valores de temperatura (0.0, 0.5, 1.0, 1.5)
python 03-temperature/temperature.py

# Ejemplo con modelos de razonamiento
python 03-temperature/reasoning.py
```

- **Temperatura baja (0.0-0.5)**: Respuestas más deterministas y consistentes
- **Temperatura alta (1.0-1.5)**: Respuestas más creativas y variadas

### 04 - Streaming

Compara el comportamiento con y sin streaming de respuestas.

```bash
# Sin streaming - espera la respuesta completa
python 04-streaming/without_streaming.py

# Con streaming - recibe tokens en tiempo real
python 04-streaming/with_streaming.py
```

El streaming permite mostrar respuestas progresivamente al usuario, mejorando la experiencia en aplicaciones interactivas.

### 05 - Salida Estructurada

Aprende a obtener respuestas en formatos estructurados usando Pydantic.

```bash
# Sin structured output (solo prompting)
python 05-structured-output/without_structured_output.py

# Con structured output (usando Pydantic)
python 05-structured-output/with_structured_output.py
```

El archivo `schema.py` define el esquema de datos esperado usando Pydantic, garantizando que la respuesta del modelo siempre tenga el formato correcto.

### 06 - Function Calling

Aprende cómo los LLMs pueden invocar funciones externas para extender sus capacidades.

```bash
# Web search - el modelo usa herramientas built-in de OpenAI
python 06-function-calling/web_search_function.py

# Función local - el modelo decide cuándo llamar a una función personalizada
python 06-function-calling/local_function.py
```

- **`web_search_function.py`**: Usa la herramienta `web_search` integrada de OpenAI para buscar información en tiempo real
- **`local_function.py`**: Define una herramienta personalizada (`search_similar_issues`) que el modelo invoca para buscar issues similares en una base de datos local. Demuestra el ciclo completo: definición de tool → llamada del modelo → ejecución local → respuesta final
- **`search_similar_issues.py`**: Función auxiliar que simula una base de datos de issues (en producción conectaría a Jira, GitHub Issues, etc.)

### 07 - Prompting

Estrategias para organizar y externalizar prompts fuera del código principal.

```bash
# Enfoque con módulos Python
python 07-prompting/modules/module_main.py

# Enfoque con archivos Markdown
python 07-prompting/markdown/markdown_main.py
```

**Enfoque Módulos** (`modules/`):
- Los prompts se definen como constantes en `prioritizer_prompt.py` (system prompt, few-shot examples, user template)
- Versionados con `PROMPT_VERSION`, testeables y reutilizables
- La función `build_messages()` construye la lista de mensajes lista para el LLM

**Enfoque Markdown** (`markdown/`):
- Los prompts se almacenan en archivos `.md` separados en `prompts/` (system, examples, user)
- `prompt_loader.py` se encarga de cargar y ensamblar los archivos
- Ideal para prompts largos o cuando participan personas no-técnicas en su edición

Ambos enfoques usan el mismo caso de uso: un priorizador de issues que analiza bugs y asigna prioridad (Urgent/High/Medium/Low).

## Estructura del Proyecto

```
examples/
├── .env.example            # Plantilla de variables de entorno
├── requirements.txt        # Dependencias de Python
├── 01-first-call/          # Primeras llamadas a APIs
├── 02-tokens.py            # Tokens y costos
├── 03-temperature/         # Efectos de temperatura
├── 04-streaming/           # Streaming de respuestas
├── 05-structured-output/   # Salidas estructuradas con Pydantic
├── 06-function-calling/    # Invocación de funciones externas
│   ├── web_search_function.py
│   ├── local_function.py
│   └── search_similar_issues.py
└── 07-prompting/           # Organización de prompts
    ├── modules/            # Prompts como módulos Python
    └── markdown/           # Prompts como archivos Markdown
```

## Notas

- Asegúrate de tener saldo suficiente en tu cuenta del proveedor antes de ejecutar los ejemplos
- Los costos mostrados son aproximados y pueden variar según los precios actuales