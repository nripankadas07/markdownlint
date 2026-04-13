"""Markdownlint: Validate Markdown files against configurable style rules."""

from .core import lint, lint_file, list_rules
from .models import MarkdownlintError, RuleInfo, Violation

__version__ = "1.0.0"
__all__ = [
    "lint",
    "lint_file",
    "list_rules",
    "Violation",
    "RuleInfo",
    "MarkdownlintError",
]
