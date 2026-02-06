"""
Input guardrails for validating and sanitizing input before LLM processing.
"""
import html
import re

from main.domain.models.schemas import IssueRequest


class InputRails:
    """Input validation and sanitization for issue requests."""

    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 5000

    def validate(self, issue: IssueRequest) -> IssueRequest:
        """
        Validate and sanitize an issue request.

        Args:
            issue: The issue request to validate.

        Returns:
            A sanitized issue request.

        Raises:
            ValueError: If the issue is invalid after sanitization.
        """
        # Sanitize HTML/scripts from title and description
        sanitized_title = self._sanitize_text(issue.title)
        sanitized_description = self._sanitize_text(issue.description)

        # Truncate if exceeds limits
        sanitized_title = sanitized_title[: self.MAX_TITLE_LENGTH]
        sanitized_description = sanitized_description[: self.MAX_DESCRIPTION_LENGTH]

        # Validate not empty after sanitization
        if not sanitized_title.strip():
            raise ValueError("El título no puede estar vacío después de la sanitización")
        if not sanitized_description.strip():
            raise ValueError("La descripción no puede estar vacía después de la sanitización")

        return IssueRequest(
            issue_id=issue.issue_id,
            title=sanitized_title,
            description=sanitized_description,
        )

    def _sanitize_text(self, text: str) -> str:
        """
        Remove potentially dangerous content from text.

        Args:
            text: The text to sanitize.

        Returns:
            Sanitized text.
        """
        # Remove script tags and their content
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)

        # Remove other HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        # Escape HTML entities
        text = html.unescape(text)

        # Remove null bytes
        text = text.replace("\x00", "")

        # Normalize whitespace
        text = " ".join(text.split())

        return text.strip()
