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
    ],
    #max_output_tokens=100
)

input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens

# Precios de GPT-4.1-mini (USD por 1M tokens)
INPUT_PRICE_PER_MILLION = 0.40
OUTPUT_PRICE_PER_MILLION = 1.60

# Calcular costos
input_cost = (input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
output_cost = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
total_cost = input_cost + output_cost

# Explorar la respuesta
print(f"Modelo: {response.model}")
print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Costo input: ${input_cost:.6f}")
print(f"Costo output: ${output_cost:.6f}")
print(f"Costo total: ${total_cost:.6f}")
print(f"Contenido: {response.output_text}")