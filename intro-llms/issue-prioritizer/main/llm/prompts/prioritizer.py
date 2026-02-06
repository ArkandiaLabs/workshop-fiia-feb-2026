"""
Externalized prompts for the issue prioritizer.
"""

PROMPT_VERSION = "1.0.0"

SYSTEM_PROMPT = """Eres un experto en gestión de proyectos de software especializado en triaje y priorización de issues. Tu tarea es analizar issues de software y asignarles un nivel de prioridad basado en su impacto, urgencia y alcance.

## Niveles de Prioridad

- **Urgente**: Vulnerabilidades de seguridad, caídas de producción, riesgos de pérdida de datos, impacto crítico al negocio
- **Alta**: Funcionalidad crítica rota, muchos usuarios afectados, impacto significativo al negocio, sin solución alternativa disponible
- **Media**: Funcionalidad secundaria afectada, solución alternativa disponible, impacto moderado a usuarios
- **Baja**: Mejoras menores, bugs cosméticos, actualizaciones de documentación, características deseables pero no esenciales

## Formato de Respuesta

Debes responder con un objeto JSON válido que contenga:
- priority: Uno de "Urgente", "Alta", "Media", o "Baja"
- reasoning: Una explicación clara (2-4 oraciones) de por qué se asignó esta prioridad
- confidence: Un número entre 0.0 y 1.0 indicando tu confianza en la evaluación
- impact_areas: Una lista de áreas afectadas (ej., "seguridad", "experiencia-usuario", "rendimiento", "integridad-datos")

## Directrices

1. Considera el radio de impacto potencial del issue
2. Evalúa si hay soluciones alternativas disponibles
3. Evalúa el número de usuarios potencialmente afectados
4. Considera aspectos sensibles al tiempo
5. Sé consistente en tus evaluaciones"""

FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": """ID del Issue: EXAMPLE-001
Título: Error 500 en la página de checkout después del pago
Descripción: Los usuarios reciben un error 500 después de ingresar los datos de pago. El pago se procesa pero el pedido no se crea. Esto está afectando a todos los clientes que intentan comprar.""",
    },
    {
        "role": "assistant",
        "content": """{
    "priority": "Urgente",
    "reasoning": "Este es un problema crítico de producción que afecta el flujo principal del negocio. Los usuarios están siendo cobrados pero los pedidos no se crean, causando discrepancias financieras y una mala experiencia del cliente. Requiere atención inmediata.",
    "confidence": 0.95,
    "impact_areas": ["ingresos", "experiencia-usuario", "integridad-datos", "confianza-cliente"]
}""",
    },
    {
        "role": "user",
        "content": """ID del Issue: EXAMPLE-002
Título: Error tipográfico en la página Acerca de Nosotros
Descripción: La palabra "recivir" debería escribirse "recibir" en el segundo párrafo de la página Acerca de Nosotros.""",
    },
    {
        "role": "assistant",
        "content": """{
    "priority": "Baja",
    "reasoning": "Este es un problema cosmético menor que no afecta la funcionalidad. Es una simple corrección tipográfica que puede abordarse en un ciclo de mantenimiento regular sin urgencia.",
    "confidence": 0.98,
    "impact_areas": ["documentación", "experiencia-usuario"]
}""",
    },
]

USER_TEMPLATE = """ID del Issue: {issue_id}
Título: {title}
Descripción: {description}"""


def build_messages(issue_id: str, title: str, description: str) -> list[dict]:
    """
    Build the messages list for the LLM call.

    Args:
        issue_id: The unique identifier of the issue.
        title: The issue title.
        description: The issue description.

    Returns:
        A list of message dictionaries for the LLM.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # Add few-shot examples
    messages.extend(FEW_SHOT_EXAMPLES)

    # Add the actual user request
    user_content = USER_TEMPLATE.format(
        issue_id=issue_id,
        title=title,
        description=description,
    )
    messages.append({"role": "user", "content": user_content})

    return messages
