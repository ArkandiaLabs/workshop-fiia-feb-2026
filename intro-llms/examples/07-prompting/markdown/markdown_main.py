import os
from dotenv import load_dotenv
from openai import OpenAI

from prompt_loader import PromptLoader

load_dotenv()  # Cargar variables de entorno desde el archivo .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_loader = PromptLoader()

messages = prompt_loader.build_prompt(
    issue_id="124",
    title="Tiempo de espera de conexión a base de datos - servicio no disponible",
    description="Las conexiones a la base de datos se agotarán intermitentemente, causando que el servicio de API no esté disponible y afectando todas las solicitudes de los usuarios."
)

print("Mensajes construidos para el LLM:")
for msg in messages:
    print(f"{msg['role'].upper()}: {msg['content']}\n")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=messages,
    max_output_tokens=200
)

print(f"Respuesta: {response.output_text}")