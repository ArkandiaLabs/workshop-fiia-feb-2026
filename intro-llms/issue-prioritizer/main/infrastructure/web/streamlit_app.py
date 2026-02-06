"""
Streamlit UI for the Issue Prioritizer.
"""
import requests
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Priorizador de Issues",
    page_icon="🎯",
    layout="wide",
)

# Priority emoji mapping
PRIORITY_EMOJIS = {
    "Urgente": "🔴",
    "Alta": "🟠",
    "Media": "🟡",
    "Baja": "🟢",
}


def main():
    """Main Streamlit application."""
    st.title("🎯 Priorizador de Issues")
    st.markdown("Analiza y prioriza issues de software usando IA")

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuración")
        api_url = st.text_input(
            "URL de la API",
            value="http://localhost:8000",
            help="La URL base de la API del Priorizador de Issues",
        )

        st.markdown("---")
        st.markdown("### Acerca de")
        st.markdown(
            """
            Esta herramienta usa LLM para analizar issues de software
            y asignar niveles de prioridad basados en:
            - Severidad del impacto
            - Número de usuarios afectados
            - Criticidad para el negocio
            - Soluciones alternativas disponibles
            """
        )

    # Main form
    st.header("Enviar Issue para Análisis")

    with st.form("issue_form"):
        issue_id = st.text_input(
            "ID del Issue",
            placeholder="PROJ-123",
            help="Identificador único del issue",
        )

        title = st.text_input(
            "Título",
            placeholder="Breve descripción del issue",
            help="Un título corto y descriptivo (5-200 caracteres)",
        )

        description = st.text_area(
            "Descripción",
            placeholder="Descripción detallada del issue, incluyendo pasos para reproducir, comportamiento esperado y comportamiento actual...",
            height=200,
            help="Descripción detallada del issue (10-5000 caracteres)",
        )

        submitted = st.form_submit_button("🔍 Analizar Issue", use_container_width=True)

    # Handle form submission
    if submitted:
        if not issue_id or not title or not description:
            st.error("Por favor complete todos los campos")
            return

        if len(title) < 5:
            st.error("El título debe tener al menos 5 caracteres")
            return

        if len(description) < 10:
            st.error("La descripción debe tener al menos 10 caracteres")
            return

        with st.spinner("Analizando issue..."):
            try:
                response = requests.post(
                    f"{api_url}/prioritize",
                    json={
                        "issue_id": issue_id,
                        "title": title,
                        "description": description,
                    },
                    timeout=60,
                )

                if response.status_code == 200:
                    result = response.json()
                    display_result(result)
                else:
                    st.error(f"Error de API: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    f"No se pudo conectar a la API en {api_url}. "
                    "Asegúrese de que la API esté ejecutándose."
                )
            except requests.exceptions.Timeout:
                st.error("La solicitud expiró. Por favor intente de nuevo.")
            except Exception as e:
                st.error(f"Ocurrió un error: {str(e)}")


def display_result(result: dict):
    """Display the prioritization result."""
    st.header("Resultado del Análisis")

    priority = result["priority"]
    emoji = PRIORITY_EMOJIS.get(priority, "⚪")

    # Priority display
    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            label="Prioridad",
            value=f"{emoji} {priority}",
        )

        confidence_pct = result["confidence"] * 100
        st.metric(
            label="Confianza",
            value=f"{confidence_pct:.1f}%",
        )

    with col2:
        st.subheader("Razonamiento")
        st.info(result["reasoning"])

    # Impact areas
    if result["impact_areas"]:
        st.subheader("Áreas de Impacto")
        cols = st.columns(len(result["impact_areas"]))
        for idx, area in enumerate(result["impact_areas"]):
            with cols[idx]:
                st.markdown(f"**{area}**")

    # Technical metadata expander
    with st.expander("📊 Detalles Técnicos"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Modelo", result["model_used"])

        with col2:
            total_tokens = result["input_tokens"] + result["output_tokens"]
            st.metric("Tokens Usados", f"{total_tokens:,}")

        with col3:
            cost_display = f"${result['total_cost']:.6f}"
            st.metric("Costo", cost_display)

        st.markdown("---")
        st.markdown("**Desglose de Tokens:**")
        st.markdown(f"- Tokens de entrada: {result['input_tokens']:,}")
        st.markdown(f"- Tokens de salida: {result['output_tokens']:,}")


if __name__ == "__main__":
    main()
