import os
from dotenv import load_dotenv
from openai import OpenAI

from schema import PriorityAnalysis

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.parse(
    model="gpt-4.1-mini",
    input=[
        {"role": "developer", "content": "Analiza issues y asigna prioridades."},
        {"role": "user", "content": "Asunto: Botón de inicio de sesión roto\nLos usuarios no pueden iniciar sesión"}
    ],
    text_format=PriorityAnalysis,
)

result = response.output_parsed
print(result.model_dump_json(indent=2))