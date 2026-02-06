"""
Output guardrails for validating LLM responses.
"""
from main.domain.models.schemas import Priority, PriorityAnalysis


class OutputRails:
    """Output validation for priority analysis results."""

    MAX_REASONING_LENGTH = 1000

    def validate(self, analysis: PriorityAnalysis) -> PriorityAnalysis:
        """
        Validate and sanitize a priority analysis result.

        Args:
            analysis: The analysis result to validate.

        Returns:
            A validated and potentially corrected analysis.
        """
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, analysis.confidence))

        # Ensure priority is a valid enum value
        priority = self._validate_priority(analysis.priority)

        # Truncate reasoning if too long
        reasoning = analysis.reasoning[: self.MAX_REASONING_LENGTH]

        # Ensure impact_areas is a list
        impact_areas = list(analysis.impact_areas) if analysis.impact_areas else []

        return PriorityAnalysis(
            priority=priority,
            reasoning=reasoning,
            confidence=confidence,
            impact_areas=impact_areas,
        )

    def _validate_priority(self, priority: Priority) -> Priority:
        """
        Validate that priority is a valid enum value.

        Args:
            priority: The priority to validate.

        Returns:
            A valid Priority enum value.
        """
        if isinstance(priority, Priority):
            return priority

        # Try to convert string to Priority
        priority_str = str(priority).strip().title()
        try:
            return Priority(priority_str)
        except ValueError:
            # Default to Medium if invalid
            return Priority.MEDIUM
