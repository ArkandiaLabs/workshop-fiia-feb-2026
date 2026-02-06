"""
Interface for issue analysis.
"""
from typing import Protocol

from main.domain.models.schemas import IssueRequest, PrioritizationResult


class IssueAnalyzer(Protocol):
    """Interface that defines the contract for obtaining priority analysis."""

    def analyze_priority(self, issue: IssueRequest) -> PrioritizationResult:
        """
        Analyze an issue and return the prioritization result with analysis and metadata.

        Args:
            issue: The issue request to analyze.

        Returns:
            Complete prioritization result including analysis and LLM metadata.
        """
        ...
