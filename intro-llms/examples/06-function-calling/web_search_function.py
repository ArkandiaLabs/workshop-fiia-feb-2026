import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Cargar variables de entorno desde el archivo .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1",
    input="¿Quién ganó la Copa América 2024 y en qué fecha?",
    tools=[{"type": "web_search"}]
)

print(response.output_text)