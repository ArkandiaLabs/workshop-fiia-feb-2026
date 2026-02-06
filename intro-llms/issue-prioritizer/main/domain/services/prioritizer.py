"""
Prioritizer Service - Domain service that orchestrates the prioritization.
Depends only on abstractions (IssueAnalyzer), not on concrete implementations.
"""
from main.domain.interfaces.issue_analyzer import IssueAnalyzer
from main.domain.models.schemas import IssueRequest, PrioritizationResult


class PrioritizerService:
    """Domain service - depends only on abstractions."""

    def __init__(self, analyzer: IssueAnalyzer):
        """
        Initialize the prioritizer service.

        Args:
            analyzer: An implementation of the IssueAnalyzer interface.
        """
        self.analyzer = analyzer

    def prioritize(self, issue: IssueRequest) -> PrioritizationResult:
        """
        Prioritize an issue using the injected analyzer.

        Args:
            issue: The issue request to prioritize.

        Returns:
            Complete prioritization result with analysis and metadata.
        """
        return self.analyzer.analyze_priority(issue)
