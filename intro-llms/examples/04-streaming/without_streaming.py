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

print("Analizando caso de soporte (sin streaming)...\n")

start_time = time.time()

# Sin streaming: la respuesta llega completa al final
response = client.responses.create(
    model="gpt-5-mini",
    input=prompt,
    reasoning={
        "effort": "medium"
    }
)

end_time = time.time()
elapsed_time = end_time - start_time

# La respuesta llega completa
print(response.output_text)

# Mostrar métricas
usage = response.usage
print(f"\n[Completado en {elapsed_time:.2f} segundos]")
print(f"  Input tokens:     {usage.input_tokens}")
print(f"  Output tokens:    {usage.output_tokens}")
print(f"  Reasoning tokens: {usage.output_tokens_details.reasoning_tokens}")
