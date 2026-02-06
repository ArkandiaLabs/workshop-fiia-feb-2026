"""
Ejemplo SIN structured output - usando solo prompting para obtener JSON.

Comparar con with_structured_output.py para ver las diferencias:
- Sin garantía de formato válido
- Requiere parseo manual
- El modelo puede desviarse del esquema
"""
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# El mismo issue que en el ejemplo con schema
issue = "Asunto: Botón de inicio de sesión roto\nLos usuarios no pueden iniciar sesión"

# Intentamos obtener JSON estructurado solo con instrucciones en el prompt
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "developer",
            "content": """Analiza issues y asigna prioridades.

Responde con las siguientes propiedades:
- La prioridad del issue (puede ser Low, Medium, High o Urgent)
- Un razonamiento de 2-3 oraciones explicando tu decisión
- Tu nivel de confianza en la decisión, entre 0 y 1
- Las áreas de impacto afectadas por el issue

Devuelve únicamente la información solicitada, sin texto adicional. y sin envoltorios."""
        },
        {"role": "user", "content": issue}
    ]
)

raw_output = response.output_text
print("=== Respuesta raw del modelo ===")
print(raw_output)
print()
