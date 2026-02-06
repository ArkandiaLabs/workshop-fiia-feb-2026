import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Cargar variables de entorno desde el archivo .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {"role": "developer", "content": "Eres un asistente útil."},
        {"role": "user", "content": "¿Qué es un bug de software?"}
    ]
)

# Explorar la respuesta
print(f"Modelo: {response.model}")
print(f"Contenido: {response.output_text}")