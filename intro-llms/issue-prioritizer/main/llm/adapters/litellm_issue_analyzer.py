"""
LiteLLM adapter that implements the IssueAnalyzer interface.
"""
import warnings
from typing import Optional

# Suppress Pydantic serialization warning from LiteLLM's Responses API
# This is a known issue: https://github.com/BerriAI/litellm/issues/11759
warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
)

import litellm

from main.config import settings
from main.domain.models.schemas import (
    IssueRequest,
    LLMMetadata,
    PriorityAnalysis,
    PrioritizationResult,
)
from main.llm.guardrails.input_rails import InputRails
from main.llm.guardrails.output_rails import OutputRails
from main.llm.prompts.prioritizer import build_messages


class LiteLLMIssueAnalyzer:
    """Adapter that implements IssueAnalyzer using LiteLLM."""

    def __init__(
        self, model: Optional[str] = None, temperature: float = 0.0, api_key: Optional[str] = None
    ):
        """
        Initialize the LiteLLM issue analyzer.

        Args:
            model: The model to use. Defaults to settings.llm_model.
            temperature: Temperature for generation. Defaults to 0.0.
        """
        self.model = model or settings.llm_model
        self.api_key = api_key or settings.llm_api_key
        self.temperature = temperature
        self.input_rails = InputRails()
        self.output_rails = OutputRails()

    def analyze_priority(self, issue: IssueRequest) -> PrioritizationResult:
        """
        Analyze an issue and return the prioritization result.

        Args:
            issue: The issue request to analyze.

        Returns:
            Complete prioritization result with analysis and metadata.
        """
        # 1. Validate input
        validated = self.input_rails.validate(issue)

        # 2. Build messages
        messages = build_messages(
            validated.issue_id, validated.title, validated.description
        )

        # 3. Call LiteLLM Responses API
        response = litellm.responses(
            model=self.model,
            api_key=self.api_key,
            input=messages,
            temperature=self.temperature,
            text={"format": {"type": "json_object"}},
        )

        # 4. Parse and validate output
        content = response.output[0].content[0].text
        analysis = PriorityAnalysis.model_validate_json(content)
        analysis = self.output_rails.validate(analysis)

        # 5. Build result with metadata
        metadata = LLMMetadata(
            model_used=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_cost=litellm.completion_cost(completion_response=response),
        )

        return PrioritizationResult(analysis=analysis, metadata=metadata)
