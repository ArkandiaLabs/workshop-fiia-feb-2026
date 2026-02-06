"""
Domain models - Pure business entities without infrastructure concerns.
"""
from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Issue priority levels."""

    LOW = "Baja"
    MEDIUM = "Media"
    HIGH = "Alta"
    URGENT = "Urgente"


class IssueRequest(BaseModel):
    """Request to prioritize an issue."""

    issue_id: str = Field(..., description="Unique identifier for the issue")
    title: str = Field(..., min_length=5, max_length=200, description="Issue title")
    description: str = Field(
        ..., min_length=10, max_length=5000, description="Issue description"
    )


class PriorityAnalysis(BaseModel):
    """Analysis result from the prioritization process."""

    priority: Priority = Field(..., description="Assigned priority level")
    reasoning: str = Field(..., description="Explanation for the priority assignment")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score between 0 and 1"
    )
    impact_areas: list[str] = Field(
        default_factory=list, description="Areas affected by this issue"
    )


class LLMMetadata(BaseModel):
    """Technical metadata from the LLM execution."""

    model_used: str = Field(..., description="Model identifier used for the request")
    input_tokens: int = Field(..., ge=0, description="Number of input tokens")
    output_tokens: int = Field(..., ge=0, description="Number of output tokens")
    total_cost: float = Field(..., ge=0.0, description="Total cost in USD")


class PrioritizationResult(BaseModel):
    """Complete prioritization result - domain wrapper."""

    analysis: PriorityAnalysis = Field(..., description="The priority analysis")
    metadata: LLMMetadata = Field(..., description="LLM execution metadata")
