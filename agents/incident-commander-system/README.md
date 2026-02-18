# Incident Commander — Sistema Multi-Agente para Investigación de Incidentes

Sistema multi-agente que simula la respuesta a incidentes de producción. Recibe alertas, investiga problemas usando herramientas especializadas, y genera diagnósticos con reportes escritos a disco.

**Demo principal del workshop "Fundamentos de Ingeniería de IA" - Sesión de Agentes IA.**

## ¿Qué Enseña Este Demo?

| Concepto | Cómo se ve en el demo |
|----------|----------------------|
| **Qué es un agente** | El Commander recibe un objetivo ("investigar el incidente") y decide autónomamente cómo resolverlo |
| **Function calling / Tools** | Cada investigación usa funciones concretas: `check_service_status()`, `search_logs()`, etc. |
| **MCP Tools** | El postmortem_agent escribe reportes a disco usando un servidor MCP de filesystem — la tool no vive en el código del agente |
| **ReAct loop** | En los traces de `adk web`: Thought → Action → Observation → Thought → ... |
| **Multi-agent** | El Commander delega a 3 sub-agentes especializados |
| **Orchestrator-Workers** | El Commander decide dinámicamente qué agente necesita y en qué orden |
| **Multi-modelo** | Configuración centralizada permite cambiar entre diferentes modelos (OpenAI, Gemini) desde una variable de entorno |
| **Configuración centralizada** | Un solo archivo `models.py` gestiona la configuración del modelo para todos los agentes |

**Framework:** Google ADK (Agent Development Kit)  
**Patrón de arquitectura:** Orchestrator-Workers con LLM-based orchestration  
**Modelos:** Configurable via `.env` (por defecto: gpt-5-nano para todos los agentes)

---

## Arquitectura

### Patrón: Orchestrator-Workers

El Incident Commander implementa el patrón **Orchestrator-Workers** de Anthropic. El orquestador (commander) usa su LLM para decidir dinámicamente a qué worker (sub-agent) delegar y en qué orden.

**Diferencia con Prompt Chaining:** El flujo natural del incidente tiende a ser secuencial (diagnosticar → logs → postmortem), pero la secuencia **no está hardcodeada** — el LLM decide. Con prompts vagos, puede cambiar el orden o volver a llamar a un agente.

### Diagramas de Arquitectura - Modelo C4

#### Nivel 1: Diagrama de Contexto

```mermaid
flowchart TD
    engineer["👤 <b>Ingeniero de Soporte</b><br/><i>Envía alertas de incidentes<br/>y recibe diagnósticos</i>"]

    incident_system["🤖 <b>Incident Commander System</b><br/><i>Sistema multi-agente que investiga<br/>incidentes de producción<br/>usando Google ADK</i>"]

    llm_provider["☁️ <b>Proveedor LLM</b><br/><i>OpenAI / Gemini</i>"]
    mcp_server["📁 <b>MCP Filesystem Server</b><br/><i>Node.js / npx</i>"]
    prod_platform["🖥️ <b>Plataforma de Producción</b><br/><i>auth-service, api-gateway,<br/>payments-api</i>"]

    engineer -- "Envía alertas y recibe diagnósticos<br/>(Chat / CLI / API REST)" --> incident_system
    incident_system -- "Envía prompts y recibe respuestas<br/>(API HTTP)" --> llm_provider
    incident_system -- "Escribe reportes postmortem<br/>(MCP Protocol)" --> mcp_server
    incident_system -- "Consulta estado, métricas y logs<br/>(Function Calling)" --> prod_platform

    style engineer fill:#08427b,color:#fff,stroke:#073b6f
    style incident_system fill:#1168bd,color:#fff,stroke:#0b4884
    style llm_provider fill:#999,color:#fff,stroke:#6b6b6b
    style mcp_server fill:#999,color:#fff,stroke:#6b6b6b
    style prod_platform fill:#999,color:#fff,stroke:#6b6b6b
```

#### Nivel 2: Diagrama de Contenedores

```mermaid
flowchart TD
    engineer["👤 <b>Ingeniero de Soporte</b><br/><i>Envía alertas de incidentes<br/>y recibe diagnósticos</i>"]

    subgraph incident_system ["🔲 Incident Commander System"]
        adk_agent["🤖 <b>Incident Commander Agent</b><br/><i>Python / Google ADK</i><br/><i>1 orquestador + 3 workers</i>"]
        adk_ui["🖥️ <b>ADK Web UI / CLI</b><br/><i>Google ADK</i><br/><i>adk web / adk run</i>"]
        fastapi["🌐 <b>FastAPI Custom Server</b><br/><i>Python / Uvicorn</i><br/><i>/health, /dev-ui, /docs</i>"]
    end

    llm_provider["☁️ <b>Proveedor LLM</b><br/><i>OpenAI / Gemini</i>"]
    mcp_server["📁 <b>MCP Filesystem Server</b><br/><i>Node.js / npx</i>"]
    prod_platform["🖥️ <b>Plataforma de Producción</b><br/><i>auth-service, api-gateway,<br/>payments-api</i>"]

    engineer -- "Chat / Terminal" --> adk_ui
    engineer -- "HTTP / REST" --> fastapi
    adk_ui -- "Usa" --> adk_agent
    fastapi -- "Usa" --> adk_agent
    adk_agent -- "Prompts y respuestas<br/>(API HTTP)" --> llm_provider
    adk_agent -- "Escribe reportes<br/>(MCP Protocol)" --> mcp_server
    adk_agent -- "Estado, métricas y logs<br/>(Function Calling)" --> prod_platform

    style engineer fill:#08427b,color:#fff,stroke:#073b6f
    style adk_agent fill:#1168bd,color:#fff,stroke:#0b4884
    style adk_ui fill:#1168bd,color:#fff,stroke:#0b4884
    style fastapi fill:#1168bd,color:#fff,stroke:#0b4884
    style llm_provider fill:#999,color:#fff,stroke:#6b6b6b
    style mcp_server fill:#999,color:#fff,stroke:#6b6b6b
    style prod_platform fill:#999,color:#fff,stroke:#6b6b6b
    style incident_system fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:5 5
```

#### Nivel 3: Diagrama de Componentes — Incident Commander Agent

```mermaid
flowchart TD
    subgraph adk_agent ["🔲 Incident Commander Agent"]
        commander["🎖️ <b>Incident Commander</b><br/><i>Python / Google ADK</i><br/><i>Orquestador</i>"]

        subgraph diagnostic_group [" "]
            diagnostic["🔍 <b>Diagnostic Agent</b><br/><i>Python / Google ADK</i><br/><i>LlmAgent - Worker</i>"]
            check_status["🔧 <b>check_service_status</b><br/><i>Componente: Python</i><br/><i>Verifica estado de un servicio<br/>(UP / DOWN / DEGRADED)</i>"]
            check_metrics["🔧 <b>check_metrics</b><br/><i>Componente: Python</i><br/><i>Consulta métricas de CPU,<br/>memoria, conexiones DB y latencia</i>"]
        end

        subgraph logs_group [" "]
            logs["📋 <b>Logs Agent</b><br/><i>Python / Google ADK</i><br/><i>LlmAgent - Worker</i>"]
            search_logs["🔧 <b>search_logs</b><br/><i>Componente: Python</i><br/><i>Busca logs filtrados por<br/>severidad y ventana de tiempo</i>"]
        end

        subgraph postmortem_group [" "]
            postmortem["📝 <b>Postmortem Agent</b><br/><i>Python / Google ADK</i><br/><i>LlmAgent - Worker</i>"]
            get_runbook["🔧 <b>get_runbook</b><br/><i>Componente: Python</i><br/><i>Obtiene procedimientos estándar<br/>de remediación</i>"]
            write_file["🔧 <b>write_file</b><br/><i>Componente: MCP Tool</i><br/><i>Escribe reportes postmortem<br/>a disco</i>"]
        end
    end

    llm_provider["☁️ <b>Proveedor LLM</b><br/><i>OpenAI / Gemini</i>"]
    mcp_server["📁 <b>MCP Filesystem Server</b><br/><i>Node.js / npx</i>"]
    prod_platform["🖥️ <b>Plataforma de Producción</b><br/><i>auth-service, api-gateway,<br/>payments-api</i>"]

    commander -- "Delega diagnóstico a subagente" --> diagnostic
    commander -- "Delega análisis de logs a subagente" --> logs
    commander -- "Delega reporte a subagente" --> postmortem
    commander -- "Usa para razonamiento" --> llm_provider

    diagnostic --> check_status
    diagnostic --> check_metrics
    check_status -- "Consulta estado" --> prod_platform
    check_metrics -- "Consulta métricas" --> prod_platform

    logs --> search_logs
    search_logs -- "Consulta logs" --> prod_platform

    postmortem --> get_runbook
    postmortem --> write_file
    get_runbook -- "Consulta runbooks" --> prod_platform
    write_file -- "Escribe reportes" --> mcp_server

    style commander fill:#08427b,color:#fff,stroke:#073b6f
    style diagnostic fill:#1168bd,color:#fff,stroke:#0b4884
    style logs fill:#1168bd,color:#fff,stroke:#0b4884
    style postmortem fill:#1168bd,color:#fff,stroke:#0b4884
    style check_status fill:#85bbf0,color:#000,stroke:#5a9bd5
    style check_metrics fill:#85bbf0,color:#000,stroke:#5a9bd5
    style search_logs fill:#85bbf0,color:#000,stroke:#5a9bd5
    style get_runbook fill:#85bbf0,color:#000,stroke:#5a9bd5
    style write_file fill:#85bbf0,color:#000,stroke:#5a9bd5
    style llm_provider fill:#999,color:#fff,stroke:#6b6b6b
    style mcp_server fill:#999,color:#fff,stroke:#6b6b6b
    style prod_platform fill:#999,color:#fff,stroke:#6b6b6b
    style adk_agent fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:5 5
    style diagnostic_group fill:none,stroke:#1168bd,stroke-width:1px,stroke-dasharray:3 3
    style logs_group fill:none,stroke:#1168bd,stroke-width:1px,stroke-dasharray:3 3
    style postmortem_group fill:none,stroke:#1168bd,stroke-width:1px,stroke-dasharray:3 3
```

### Agentes

#### 1. **incident_commander** (Orquestador)
- **Modelo:** Configurable via `MODEL_NAME` (default: gpt-5-nano)
- **Rol:** Coordina la investigación del incidente
- **Sub-agentes:** diagnostic_agent, logs_agent, postmortem_agent
- **Protocolo:** TRIAGE → CAUSA RAÍZ → REPORTE → RESUMEN

#### 2. **diagnostic_agent** (Worker)
- **Modelo:** Compartido desde `models.py`
- **Rol:** Especialista en verificar estado de servicios y métricas
- **Tools:**
  - `check_service_status(service_name)` — Verifica estado (UP/DOWN/DEGRADED)
  - `check_metrics(service_name)` — Revisa CPU, memoria, conexiones DB, latencia

#### 3. **logs_agent** (Worker)
- **Modelo:** Compartido desde `models.py`
- **Rol:** Especialista en análisis de logs y patrones de error
- **Tools:**
  - `search_logs(service_name, severity, minutes)` — Busca logs filtrados por severidad y ventana de tiempo

#### 4. **postmortem_agent** (Worker)
- **Modelo:** Compartido desde `models.py`
- **Rol:** Especialista en generar reportes de postmortem estructurados
- **Tools:**
  - `get_runbook(issue_type)` — Obtiene procedimientos estándar (runbooks)
  - `write_file(path, content)` — Escribe reportes a disco (via MCP filesystem server)

---

## Requisitos Previos

- **Python 3.12+**
- **uv** instalado (gestor de paquetes Python moderno)
- **Node.js y npx** (para el MCP filesystem server)
- **API Keys:**
  - Google API Key (para Gemini)
  - OpenAI API Key (para GPT-5-nano)

---

## Configuración

### 1. Navegar al directorio raíz de agentes

```bash
cd agents
```

### 2. Sincronizar dependencias con uv

```bash
uv sync
```

Esto instalará automáticamente:
- `google-adk` - Framework para desarrollo de agentes
- `litellm` - Interfaz unificada para múltiples LLM providers
- Dependencias del MCP server

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus API keys y configuración del modelo:

```env
# Model Configuration
MODEL_NAME=gpt-5-nano  # Opciones: gpt-5-nano, gpt-4o-mini, gpt-4o, gemini-2.0-flash, gemini-1.5-flash

# Google AI API Configuration
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=tu-google-api-key-aqui

# OpenAI API Configuration (requerido si usas modelos GPT)
OPENAI_API_KEY=tu-openai-api-key-aqui
```

**Nota sobre modelos:**
- Modelos **OpenAI** (`gpt-*`): Requieren `OPENAI_API_KEY`, se configuran automáticamente con LiteLLM
- Modelos **Gemini**: Requieren `GOOGLE_API_KEY`, se usan directamente
- Todos los agentes usan el mismo modelo configurado en `MODEL_NAME`

---

## Modos de Ejecución

### Opción 1: `adk web` (Recomendado para demos)

Interfaz web interactiva con visualización de traces y eventos:

```bash
cd agents/incident_commander/
adk web
```

Abre el navegador en `http://localhost:8000` (o el puerto indicado). Desde allí:
- Envía mensajes al agente en el chat
- Ve los traces de cada delegación y tool call
- Observa el flujo ReAct en tiempo real

### Opción 2: `adk run` (CLI interactivo)

```bash
cd agents/incident_commander/
adk run incident_commander
```

Conversación interactiva en la terminal.

### Opción 3: `adk api_server` (API REST automática)

```bash
cd agents/incident_commander/
adk api_server
```

Levanta un servidor FastAPI con endpoints REST y WebSocket. API docs en `/docs`.

### Opción 4: `uvicorn main:app` (FastAPI custom)

Servidor FastAPI personalizado con endpoints adicionales:

```bash
cd agents/incident-commander-system/incident_commander/
uvicorn main:app --reload --port 8000
```

Incluye:
- `/health` — Health check endpoint
- `/` — Información del servicio
- `/dev-ui/` — Dev UI de ADK
- `/docs` — API documentation

---

## Ejemplos de Entrada para Demos

### 1. Alerta completa (Demo principal — muestra los 3 sub-agentes)

```
ALERTA CRÍTICA — P1

Servicio afectado: auth-service
Estado: DOWN
Síntoma: Usuarios no pueden hacer login desde las 3:00 PM
Error reportado: HTTP 503 en todos los endpoints de autenticación
Servicios posiblemente afectados: api-gateway

Por favor investiga el incidente, identifica la causa raíz y genera un reporte de postmortem.
```

**Qué demuestra:** Flujo completo del Orchestrator-Workers. El commander delega secuencialmente a los 3 agentes. Se ven todas las tools en acción incluyendo el write_file del MCP.

### 2. Alerta vaga (Muestra razonamiento autónomo)

```
Alerta: Los usuarios están reportando que no pueden hacer login. Parece que algo se cayó.
Investiga qué está pasando.
```

**Qué demuestra:** Autonomía del agente. No le dicen qué servicio revisar ni en qué orden — el commander debe decidir por su cuenta. En los traces se ve el razonamiento del LLM.

### 3. Health check rápido (Demo parcial — solo diagnostic_agent)

```
Necesito un health check rápido de los 3 servicios: auth-service, api-gateway y payments-api.
Dame el estado y las métricas de cada uno.
```

**Qué demuestra:** El commander delega solo al diagnostic_agent. Se ven 6 tool calls. Útil para demos cortos.

### 4. Solo análisis de logs (Muestra delegación específica)

```
Revisa los logs de auth-service de los últimos 30 minutos. Necesito entender
qué pasó y cuándo empezó el problema.
```

**Qué demuestra:** El commander delega solo al logs_agent. Muestra delegación selectiva basada en la tarea.

### 5. Pregunta de seguimiento (Después de entrada 1 o 2)

```
¿Cuál es el impacto actual en los usuarios finales? ¿payments-api está en riesgo?
```

**Qué demuestra:** El agente mantiene contexto de la conversación. Muestra memory/session en ADK.

---

## Estructura del Proyecto

```
incident_commander/
├── __init__.py                  # Convención ADK: from . import agent
├── agent.py                     # Entry point: root_agent = incident_commander
├── models.py                    # Configuración centralizada del modelo
├── prompts.py                   # Prompts del orquestador
├── main.py                      # FastAPI custom (opcional)
├── .env.example                 # Plantilla de configuración
├── .gitignore                   # reports/, .env, __pycache__/, .adk/
├── reports/                     # Reportes generados por MCP
│   └── .gitkeep                 # Mantiene el directorio en git
└── sub_agents/                  # Workers especializados
    ├── diagnostic_agent/
    │   ├── __init__.py          # from . import agent
    │   ├── agent.py             # Define diagnostic_agent
    │   ├── prompts.py           # Prompts del agente
    │   └── tools.py             # Tools: check_service_status, check_metrics
    ├── logs_agent/
    │   ├── __init__.py
    │   ├── agent.py             # Define logs_agent
    │   ├── prompts.py           # Prompts del agente
    │   └── tools.py             # Tools: search_logs
    └── postmortem_agent/
        ├── __init__.py
        ├── agent.py             # Define postmortem_agent (con MCP)
        ├── prompts.py           # Prompts del agente
        └── tools.py             # Tools: get_runbook
```

**Notas de arquitectura:**
- **`models.py`**: Un solo archivo gestiona la configuración del modelo para todos los agentes
- **Imports absolutos**: Los sub-agentes importan con `from incident_commander.models import MODEL`
- **Estructura plana**: Archivos `prompts.py` y `tools.py` en lugar de subdirectorios
- **`sub_agents/`**: Directorio siguiendo la convención de Google ADK (evita conflictos con auto-discovery)

---

## Mock Data

El sistema usa **datos simulados inline** en las tools (no archivos externos):

- **Servicios:** auth-service (DOWN), api-gateway (DEGRADED), payments-api (HEALTHY)
- **Incidente simulado:** Agotamiento del pool de conexiones de BD tras deploy v2.4.1
- **Timeline:** Deploy a las 14:25 → Falla a las 14:58 → "Tiempo actual" simulado: 15:05 (2025-06-15)
- **Causa raíz:** Query `SELECT * FROM sessions WHERE expired=false` no cierra conexiones

---

## Recursos Adicionales

- **Google ADK Docs:** [https://google.github.io/adk-docs/](https://google.github.io/adk-docs/)
- **Anthropic Agent Patterns:** [https://www.anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)
- **MCP Documentation:** [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- **Design Document:** `.specs/features/agents/incident-commander/design.md` (en la raíz del repo)

---

## Licencia

Proyecto educativo para el workshop "Fundamentos de Ingeniería de IA".
