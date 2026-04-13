"""Tests for core lint functionality."""

import pytest

from markdownlint import MarkdownlintError, Violation, lint


class TestLintBasic:
    """Basic lint function tests."""

    def test_lint_empty_string(self) -> None:
        """Empty string should have no violations."""
        result = lint("")
        assert result == []

    def test_lint_clean_markdown(self) -> None:
        """Clean markdown should have no violations."""
        text = "# Heading\n\nSome content here.\n"
        result = lint(text)
        assert result == []

    def test_lint_returns_list(self) -> None:
        """lint() should return a list."""
        result = lint("test")
        assert isinstance(result, list)

    def test_lint_returns_violations(self) -> None:
        """lint() should return Violation objects."""
        text = "#Heading\n"
        result = lint(text)
        assert all(isinstance(v, Violation) for v in result)

    def test_lint_non_string_input(self) -> None:
        """Non-string input should raise MarkdownlintError."""
        with pytest.raises(MarkdownlintError):
            lint(123)  # type: ignore

    def test_lint_non_string_input_list(self) -> None:
        """List input should raise MarkdownlintError."""
        with pytest.raises(MarkdownlintError):
            lint(["not", "a", "string"])  # type: ignore

    def test_lint_with_none_rules(self) -> None:
        """Passing None for rules should check all rules."""
        text = "#Heading\n"
        result = lint(text, rules=None)
        assert len(result) > 0

    def test_lint_with_specific_rules(self) -> None:
        """Passing specific rules should only check those."""
        text = "#Heading\n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id == "MD018" for v in result)

    def test_lint_with_empty_rules(self) -> None:
        """Passing empty rules list should return no violations."""
        text = "#Heading\n"
        result = lint(text, rules=[])
        assert result == []

    def test_lint_violations_sorted(self) -> None:
        """Violations should be sorted by line then column."""
        text = "#H1\n\n##H2\n"
        result = lint(text)
        for i in range(len(result) - 1):
            v1 = result[i]
            v2 = result[i + 1]
            assert (v1.line, v1.column) <= (v2.line, v2.column)

    def test_lint_with_config(self) -> None:
        """Config should be passed to rules."""
        text = "This is a very long line that exceeds the default limit of 120 characters and should trigger a violation if we use a shorter limit like 50.\n"
        result = lint(text, config={"line_length": 50})
        assert any(v.rule_id == "MD013" for v in result)

    def test_lint_preserves_line_numbers(self) -> None:
        """Line numbers in violations should be 1-indexed."""
        text = "# Heading\n#Heading\n"
        result = lint(text)
        assert any(v.line == 2 for v in result)
