"""Data models for markdownlint."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Violation:
    """Represents a single style violation in a Markdown file."""

    rule_id: str
    line: int
    column: int
    message: str
    severity: Literal["error", "warning"] = "error"

    def __eq__(self, other: object) -> bool:
        """Check equality for testing."""
        if not isinstance(other, Violation):
            return NotImplemented
        return (
            self.rule_id == other.rule_id
            and self.line == other.line
            and self.column == other.column
            and self.message == other.message
            and self.severity == other.severity
        )

    def __repr__(self) -> str:
        return (
            f"Violation(rule_id='{self.rule_id}', line={self.line}, "
            f"column={self.column}, message='{self.message}')"
        )


@dataclass
class RuleInfo:
    """Information about a linting rule."""

    rule_id: str
    name: str
    description: str
    default_enabled: bool = True

    def __eq__(self, other: object) -> bool:
        """Check equality for testing."""
        if not isinstance(other, RuleInfo):
            return NotImplemented
        return (
            self.rule_id == other.rule_id
            and self.name == other.name
            and self.description == other.description
            and self.default_enabled == other.default_enabled
        )


class MarkdownlintError(Exception):
    """Base exception for markdownlint errors."""

    pass
