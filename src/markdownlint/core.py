"""Core linting functionality."""

import os
from typing import Any

from .models import MarkdownlintError, RuleInfo, Violation
from .rules import RuleEngine


class Markdownlint:
    """Main linting interface."""

    def __init__(self) -> None:
        self.engine = RuleEngine()

    def lint(
        self,
        text: str,
        rules: list[str] | None = None,
        config: dict[str, Any] | None = None,
    ) -> list[Violation]:
        """Lint a Markdown string.

        Args:
            text: Markdown content to lint
            rules: List of rule IDs to check, or None for all
            config: Configuration dict (e.g., {"line_length": 100})

        Returns:
            List of violations found

        Raises:
            MarkdownlintError: If input is not a string
        """
        if not isinstance(text, str):
            raise MarkdownlintError(
                f"Expected string input, got {type(text).__name__}"
            )

        if config is None:
            config = {}

        lines = text.split("\n")
        # Add newlines back to all lines except potentially the last
        if text.endswith("\n"):
            # If text ends with newline, all split lines should have newline restored
            lines = [line + "\n" for line in lines[:-1]] + [lines[-1]]
        else:
            # If text doesn't end with newline, all but last get newline, last doesn't
            if len(lines) > 1:
                lines = [line + "\n" for line in lines[:-1]] + [lines[-1]]
            # else single line with no trailing newline stays as is

        return self.engine.check(lines, rules, config)

    def lint_file(
        self,
        path: str,
        rules: list[str] | None = None,
        config: dict[str, Any] | None = None,
    ) -> list[Violation]:
        """Lint a file.

        Args:
            path: Path to Markdown file
            rules: List of rule IDs to check, or None for all
            config: Configuration dict

        Returns:
            List of violations found

        Raises:
            MarkdownlintError: If file not found or not readable
        """
        if not os.path.exists(path):
            raise MarkdownlintError(f"File not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except (IOError, OSError) as e:
            raise MarkdownlintError(f"Cannot read file {path}: {e}") from e

        return self.lint(text, rules, config)

    def list_rules(self) -> list[RuleInfo]:
        """Get list of all available rules."""
        return self.engine.get_rules()


# Create a singleton instance
_linter = Markdownlint()


def lint(
    text: str,
    rules: list[str] | None = None,
    config: dict[str, Any] | None = None,
) -> list[Violation]:
    """Lint a Markdown string.

    Args:
        text: Markdown content to lint
        rules: List of rule IDs to check, or None for all
        config: Configuration dict

    Returns:
        List of violations found
    """
    return _linter.lint(text, rules, config)


def lint_file(
    path: str,
    rules: list[str] | None = None,
    config: dict[str, Any] | None = None,
) -> list[Violation]:
    """Lint a file.

    Args:
        path: Path to Markdown file
        rules: List of rule IDs to check, or None for all
        config: Configuration dict

    Returns:
        List of violations found
    """
    return _linter.lint_file(path, rules, config)


def list_rules() -> list[RuleInfo]:
    """Get list of all available rules."""
    return _linter.list_rules()
