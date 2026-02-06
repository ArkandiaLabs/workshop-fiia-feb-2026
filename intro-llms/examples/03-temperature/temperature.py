import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Cargar variables de entorno desde el archivo .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = "Inventa un título de cargo creativo para una persona enfocada en Ingeniería de IA en una startup en LATAM. Dame solo el título."

for temp in [0.0, 0.5, 1.0, 1.5]:
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        temperature=temp
    )

    print(f"\n{'='*50}")
    print(f"Temperatura: {temp}")
    print(f"{'='*50}")
    print(f"Respuesta: {response.output_text}")
    print(f"Output tokens: {response.usage.output_tokens}")
