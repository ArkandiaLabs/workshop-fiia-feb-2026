# Agentes de IA con Google ADK

Construcción de agentes inteligentes usando Google Agent Development Kit (ADK), desde ejemplos básicos hasta sistemas multi-agente complejos con workflows orquestados.

## Requisitos Previos

- Python 3.12+
- `uv` instalado (gestor de paquetes Python moderno)
- Google API Key (Gemini)

## Configuración

### 1. Navegar al directorio de agentes

```bash
cd agents
```

### 2. Sincronizar dependencias con uv

```bash
uv sync
```

Esto instalará automáticamente todas las dependencias definidas en `pyproject.toml`, incluyendo:
- `google-adk` - Framework para desarrollo de agentes
- `litellm` - Interfaz unificada para múltiples LLM providers

## 📚 Proyectos

### 1. [Intro - Ejemplos Introductorios](intro/README.md)

Ejemplos progresivos para aprender los conceptos fundamentales de Google ADK: agentes básicos, herramientas (tools), salidas estructuradas con Pydantic, y uso de múltiples modelos LLM.

### 2. [Workflows - Patrones de Orquestación](workflows/README.md)

Patrones avanzados de workflows para coordinar múltiples agentes: routing, ejecución secuencial, paralela, orquestación y evaluación/optimización.

### 3. [Incident Commander - Sistema Multi-Agente](incident-commander-system/README.md)

Sistema completo de gestión de incidentes usando múltiples agentes especializados que colaboran para diagnosticar, resolver y documentar incidentes de producción.

## 📋 Requisitos

- Python 3.12+
- `uv` (gestor de paquetes Python moderno)
- Google API Key (Gemini)
- Opcional: OpenAI API Key (para ejemplos multimodel)
