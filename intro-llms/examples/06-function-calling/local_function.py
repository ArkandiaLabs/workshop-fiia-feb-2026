import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from search_similar_issues import search_similar_issues

SYSTEM_PROMPT = """
Eres un experto en gestión de proyectos de software especializado en triaje de issues.

Tu trabajo es:
1. Analizar el issue recibido
2. Si crees que podría haber issues similares, USA la herramienta search_similar_issues
3. Basándote en tu análisis (y los issues similares si los buscaste), asigna una prioridad

## Criterios de prioridad
- **Urgent**: Seguridad comprometida, producción caída, datos en riesgo
- **High**: Funcionalidad crítica rota, muchos usuarios afectados
- **Medium**: Funcionalidad secundaria, workaround disponible
- **Low**: Mejoras, bugs cosméticos

## Cuándo buscar issues similares
- Cuando el problema suena común o frecuente
- Cuando mencionan componentes específicos (login, checkout, etc.)
- Cuando quieres verificar si es un duplicado o regresión

## Tu respuesta final debe incluir
- La prioridad asignada
- Tu razonamiento
- Si encontraste issues similares, menciona si es posible duplicado o regresión
"""

TOOLS = [
    {
        "type": "function",
        "name": "search_similar_issues",
        "description": """
            Busca issues similares en la base de datos del proyecto.
            
            Usa esta herramienta cuando:
            - El issue podría ser un duplicado de uno existente
            - Quieres verificar si hay issues relacionados
            - El problema descrito suena familiar o común
            
            NO uses esta herramienta cuando:
            - El issue es claramente único o nuevo
            - Ya tienes suficiente información para priorizar
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Palabras clave para buscar: componentes afectados, mensajes de error, síntomas"
                },
                "status_filter": {
                    "type": "string",
                    "enum": ["all", "open", "resolved"],
                    "default": "all",
                    "description": "Filtrar por estado: 'all' para todos, 'open' para abiertos, 'resolved' para resueltos"
                },
                "max_results": {
                    "type": "integer",
                    "default": 5,
                    "description": "Número máximo de resultados a retornar"
                }
            },
            "required": ["keywords"]
        }
    }
]

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "developer", "content": SYSTEM_PROMPT},
    {"role": "user", "content": """
Analiza este issue:

**ID**: BUG-626
**Título**: El proceso de pago no funciona con mi tarjeta Visa
**Descripción**: Estoy intentando comprar una suscripción, pero mi tarjeta Visa internacional sigue siendo rechazada.
"""}
]

response = client.responses.create(
    model="gpt-5",
    input=messages,
    tools=TOOLS,
    tool_choice="auto"
)

messages += response.output

for item in response.output:
    if item.type == "function_call":
        function_name = item.name
        print("El modelo quiere usar una función:", function_name)

        if function_name == "search_similar_issues":
            function_args = json.loads(item.arguments)
            print("Con argumentos:", function_args)
            function_response = search_similar_issues(**function_args)

            messages.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(function_response)
            })

print("Lista final de mensajes:")
print(json.dumps(messages, indent=2, ensure_ascii=False, default=str))

response = client.responses.create(
    model="gpt-5",
    input=messages,
    tools=TOOLS
)

print(f"Respuesta final del modelo: {response.output_text}")

