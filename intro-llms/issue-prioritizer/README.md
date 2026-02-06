# Issue Prioritizer - Priorizador Inteligente de Issues

Sistema de priorización automática de issues de software usando Large Language Models (LLMs).

## 🎯 Características

- Priorización inteligente de issues (Urgente, Alta, Media, Baja)
- API REST con FastAPI
- Interfaz web con Streamlit
- Testing con golden set
- Tracking de tokens y costos

## 📋 Requisitos Previos

- Python 3.12+
- API key de OpenAI (u otro proveedor compatible con LiteLLM)

## 🚀 Configuración

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu LLM_API_KEY
```

## 💻 Uso

### API REST

```bash
uvicorn main.infrastructure.rest.api:app --reload
```

Documentación: `http://localhost:8000/docs`

### Interfaz Web

```bash
# En una terminal separada (con la API corriendo)
streamlit run main/infrastructure/web/streamlit_app.py
```

Aplicación: `http://localhost:8501`

## 🧪 Testing

```bash
pytest test/evaluation/test_correctness.py -v
```

## 🏗️ Arquitectura

```
issue-prioritizer/
├── main/
│   ├── domain/              # Lógica de negocio pura
│   │   ├── interfaces/      # Contratos/abstracciones
│   │   ├── models/          # Entidades y esquemas Pydantic
│   │   └── services/        # Servicios de dominio
│   ├── llm/                 # Capa de integración LLM
│   │   ├── adapters/        # Implementaciones concretas
│   │   ├── guardrails/      # Validaciones entrada/salida
│   │   └── prompts/         # Prompts externalizados
│   └── infrastructure/      # Detalles de implementación
│       ├── rest/            # API FastAPI
│       └── web/             # Interfaz Streamlit
└── test/
    └── evaluation/          # Tests y golden set
```
