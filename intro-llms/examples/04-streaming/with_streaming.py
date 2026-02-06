import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Eres un agente de soporte senior. Analiza este caso escalado y determina:
1. La causa raíz más probable
2. Prioridad (P1-P4) con justificación
3. Acciones inmediatas recomendadas
4. Si requiere escalación a ingeniería

CASO #4521 - Cliente Enterprise (ARR: $120,000)

Timeline de tickets relacionados:
- Hace 3 días: "Reportes tardan más de lo normal" (cerrado como "resuelto")
- Hace 2 días: "Algunos usuarios no pueden hacer login por la mañana"
- Hace 1 día: "Exportación de datos falla intermitentemente"
- Hoy: "URGENTE: Dashboard no carga para todo el equipo de finanzas (30 usuarios)"

Contexto técnico del cliente:
- Plan Enterprise, región: São Paulo
- 450 usuarios activos, pico de uso: 9-11am BRT
- Integración activa con Salesforce y SAP
- Último deploy en su cuenta: hace 5 días (migración de base de datos)

Métricas actuales del sistema:
- Latencia API São Paulo: 340ms (normal: 120ms)
- Tasa de errores 5xx últimas 24h: 2.3% (normal: <0.1%)
- CPU cluster São Paulo: 78% (normal: 45%)
- Conexiones DB pool: 95/100 (casi agotado)

Historial del cliente:
- Cliente desde 2021, nunca tuvo issues mayores
- Contacto técnico muy competente
- Renovación de contrato en 45 días
"""

print("Analizando caso de soporte (con streaming)...\n")

start_time = time.time()
first_token_time = None

# Streaming: la respuesta llega token por token
stream = client.responses.create(
    model="gpt-5-mini",
    input=prompt,
    reasoning={
        "effort": "medium"
    },
    stream=True
)

# Procesar eventos del stream
for event in stream:
    match event.type:
        # Inicio de la respuesta
        case "response.created":
            print(f"[Respuesta iniciada - ID: {event.response.id}]\n")

        # El modelo empieza a razonar
        case "response.output_item.added":
            if event.item.type == "reasoning":
                print("[Razonando...]", end="", flush=True)

        # El modelo terminó de razonar, empieza a escribir
        case "response.output_item.done":
            if event.item.type == "reasoning":
                print(" ✓\n")

        # Contenido de la respuesta (token por token)
        case "response.output_text.delta":
            if first_token_time is None:
                first_token_time = time.time()
                ttft = first_token_time - start_time
                print(f"[Primer token en {ttft:.2f}s]\n")
            print(event.delta, end="", flush=True)

        # Respuesta completada - mostrar uso de tokens
        case "response.completed":
            total_time = time.time() - start_time
            usage = event.response.usage
            print(f"\n\n[Completado en {total_time:.2f}s]")
            print(f"  Tiempo al primer token: {first_token_time - start_time:.2f}s")
            print(f"  Input tokens:           {usage.input_tokens}")
            print(f"  Output tokens:          {usage.output_tokens}")
            print(f"  Reasoning tokens:       {usage.output_tokens_details.reasoning_tokens}")
