import os
import requests
from dotenv import load_dotenv

load_dotenv()
response = requests.post(
    "https://api.openai.com/v1/responses",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    },
    json={
        "model": "gpt-4.1-mini",
        "input": [
            {"role": "developer", "content": "Eres un asistente útil."},
            {"role": "user", "content": "¿Qué es un bug de software?"}
        ]
    }
)

data = response.json()

# Extraer el texto de la respuesta
output_text = data['output'][0]['content'][0]['text']
print(f"Contenido: {output_text}")