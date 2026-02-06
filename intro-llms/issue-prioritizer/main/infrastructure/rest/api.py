"""
FastAPI REST API - Composition root for dependency injection.
"""
from fastapi import FastAPI, HTTPException

from main.domain.models.schemas import IssueRequest
from main.domain.services.prioritizer import PrioritizerService
from main.infrastructure.rest.schemas import PriorityResponse
from main.llm.adapters.litellm_issue_analyzer import LiteLLMIssueAnalyzer

app = FastAPI(
    title="API Priorizador de Issues",
    description="API para priorizar issues de software usando LLM",
    version="1.0.0",
)

# Composition: connect the pieces (dependency injection)
analyzer = LiteLLMIssueAnalyzer()
prioritizer = PrioritizerService(analyzer=analyzer)


@app.post("/prioritize", response_model=PriorityResponse)
async def prioritize_issue(issue: IssueRequest):
    """
    Prioritize a software issue.

    Args:
        issue: The issue request containing id, title, and description.

    Returns:
        Priority response with analysis and metadata.
    """
    try:
        # PrioritizationResult contains analysis + metadata
        result = prioritizer.prioritize(issue)

        # Map to PriorityResponse (infrastructure model)
        return PriorityResponse(
            issue_id=issue.issue_id,
            priority=result.analysis.priority,
            reasoning=result.analysis.reasoning,
            confidence=result.analysis.confidence,
            impact_areas=result.analysis.impact_areas,
            model_used=result.metadata.model_used,
            input_tokens=result.metadata.input_tokens,
            output_tokens=result.metadata.output_tokens,
            total_cost=result.metadata.total_cost,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
