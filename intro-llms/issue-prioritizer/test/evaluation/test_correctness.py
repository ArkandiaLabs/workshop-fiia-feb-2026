"""
Evaluations using OpenEvals.
"""
import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from openevals.llm import create_llm_as_judge

from main.domain.models.schemas import IssueRequest, Priority

# Load environment variables and set OPENAI_API_KEY for the evaluator
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("LLM_API_KEY", "")
from main.domain.services.prioritizer import PrioritizerService
from main.llm.adapters.litellm_issue_analyzer import LiteLLMIssueAnalyzer

# Load dataset from JSON file
GOLDEN_SET_PATH = Path(__file__).parent / "golden_set.json"
with open(GOLDEN_SET_PATH, encoding="utf-8") as f:
    GOLDEN_SET = json.load(f)


@pytest.fixture
def prioritizer_service() -> PrioritizerService:
    """Create a PrioritizerService instance for testing."""
    analyzer = LiteLLMIssueAnalyzer()
    return PrioritizerService(analyzer=analyzer)


@pytest.fixture
def evaluator():
    """Create an LLM-as-judge evaluator."""
    return create_llm_as_judge(
        prompt="""Estás evaluando un sistema de priorización de issues.

Dado:
- Issue: {input}
- Prioridad Esperada: {expected}
- Prioridad Actual: {actual}
- Razonamiento: {reasoning}

Evalúa si la prioridad actual es aceptable. Considera:
1. Coincidencia exacta es lo mejor
2. Diferencia de un nivel (ej., Alta vs Urgente) puede ser aceptable si el razonamiento es sólido
3. Diferencia de dos o más niveles no es aceptable

Responde con un objeto JSON:
{{"score": <0.0 a 1.0>, "explanation": "<explicación breve>"}}
""",
        model="gpt-4.1",
    )


@pytest.mark.parametrize(
    "test_case",
    GOLDEN_SET,
    ids=[case["input"]["issue_id"] for case in GOLDEN_SET],
)
def test_priority_correctness(test_case, prioritizer_service, evaluator):
    """Test that priorities are assigned correctly using LLM-as-judge."""
    # Arrange
    issue = IssueRequest(**test_case["input"])
    expected_priority = test_case["expected_priority"]

    # Act
    result = prioritizer_service.prioritize(issue)
    actual_priority = result.analysis.priority.value

    # Evaluate with LLM
    evaluation = evaluator(
        input=f"{test_case['input']['title']}: {test_case['input']['description']}",
        expected=expected_priority,
        actual=actual_priority,
        reasoning=result.analysis.reasoning,
    )

    # Assert
    score = evaluation["score"] if isinstance(evaluation, dict) else evaluation.score
    explanation = evaluation.get("explanation", "") if isinstance(evaluation, dict) else evaluation.explanation
    assert score >= 0.7, (
        f"Discrepancia de prioridad para {test_case['input']['issue_id']}: "
        f"se esperaba {expected_priority}, se obtuvo {actual_priority}. "
        f"Evaluación: {explanation}"
    )


def test_output_structure(prioritizer_service):
    """Test that the output has the correct structure (deterministic test)."""
    # Arrange
    issue = IssueRequest(
        issue_id="STRUCT-001",
        title="Test issue for structure validation",
        description="This is a test description to validate the output structure "
        "of the prioritization service.",
    )

    # Act
    result = prioritizer_service.prioritize(issue)

    # Assert structure
    assert result.analysis is not None
    assert result.metadata is not None

    # Assert analysis fields
    assert isinstance(result.analysis.priority, Priority)
    assert isinstance(result.analysis.reasoning, str)
    assert len(result.analysis.reasoning) > 0
    assert 0.0 <= result.analysis.confidence <= 1.0
    assert isinstance(result.analysis.impact_areas, list)

    # Assert metadata fields
    assert isinstance(result.metadata.model_used, str)
    assert result.metadata.input_tokens >= 0
    assert result.metadata.output_tokens >= 0
    assert result.metadata.total_cost >= 0.0


def test_input_validation(prioritizer_service):
    """Test that input validation works correctly."""
    # Test with HTML in input - should be sanitized
    issue = IssueRequest(
        issue_id="VAL-001",
        title="Test with <script>alert('xss')</script> content",
        description="Description with <b>HTML tags</b> and "
        "<script>malicious code</script> that should be sanitized.",
    )

    result = prioritizer_service.prioritize(issue)

    # Should succeed without error
    assert result.analysis is not None
    assert result.analysis.priority is not None
