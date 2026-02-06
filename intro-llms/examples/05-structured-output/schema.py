from pydantic import BaseModel, Field
from enum import Enum

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"
    

class PriorityAnalysis(BaseModel):
    """Output estructurado del LLM"""
    priority: Priority
    reasoning: str = Field(..., description="2-3 oraciones de explicación")
    confidence: float = Field(..., ge=0.0, le=1.0)
    impact_areas: list[str] = Field(default_factory=list)

