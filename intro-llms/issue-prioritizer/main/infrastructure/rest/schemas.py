"""
REST API schemas - Infrastructure models with technical metadata.
"""
from pydantic import BaseModel, Field

from main.domain.models.schemas import Priority


class PriorityResponse(BaseModel):
    """API response with technical metadata."""

    issue_id: str = Field(..., description="The issue identifier")
    priority: Priority = Field(..., description="Assigned priority level")
    reasoning: str = Field(..., description="Explanation for the priority")
    confidence: float = Field(..., description="Confidence score")
    impact_areas: list[str] = Field(..., description="Affected areas")

    # Technical metadata (belongs to infrastructure)
    model_used: str = Field(..., description="LLM model used")
    input_tokens: int = Field(..., description="Input tokens consumed")
    output_tokens: int = Field(..., description="Output tokens generated")
    total_cost: float = Field(..., description="Total cost in USD")
