import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
message = client.messages.create(
    messages=[
        {"role": "assistant", "content": "Eres un asistente útil."},
        {"role": "user", "content": "¿Qué es un bug de software?"}
    ],
    model="claude-haiku-4-5-20251001",
    max_tokens=500
)
print(message.content[0].text)