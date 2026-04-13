"""Tests for edge cases and complex scenarios."""

import pytest

from markdownlint import lint, list_rules


class TestCodeBlockHandling:
    """Code block exclusion tests."""

    def test_code_fence_excludes_violations(self) -> None:
        """Violations inside code fences should be excluded."""
        text = "```\n#No space heading\n```\n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id != "MD018" for v in result)

    def test_indented_code_block(self) -> None:
        """Indented code blocks should be excluded."""
        text = "    #No space heading\n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id != "MD018" for v in result)

    def test_code_fence_triple_tilde(self) -> None:
        """Triple tilde code fences should be recognized."""
        text = "~~~\n#No space\n~~~\n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id != "MD018" for v in result)

    def test_code_block_with_violations_outside(self) -> None:
        """Outside code block violations should be detected."""
        text = "#No space\n\n```\n#Also no space\n```\n"
        result = lint(text, rules=["MD018"])
        assert len([v for v in result if v.line == 1]) > 0


class TestHtmlCommentHandling:
    """HTML comment exclusion tests."""

    def test_html_comment_excludes_violations(self) -> None:
        """Violations inside HTML comments should be excluded."""
        text = "<!-- #No space heading -->\n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id != "MD018" for v in result)

    def test_multiline_html_comment(self) -> None:
        """Multiline HTML comments should be excluded."""
        text = "<!--\n#No space\n-->\n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id != "MD018" for v in result)


class TestViolationProperties:
    """Tests for violation object properties."""

    def test_violation_has_rule_id(self) -> None:
        """Violations should have rule_id."""
        text = "#Heading\n"
        result = lint(text)
        assert all(hasattr(v, "rule_id") for v in result)

    def test_violation_has_line(self) -> None:
        """Violations should have line number."""
        text = "#Heading\n"
        result = lint(text)
        assert all(hasattr(v, "line") and v.line > 0 for v in result)

    def test_violation_has_column(self) -> None:
        """Violations should have column number."""
        text = "#Heading\n"
        result = lint(text)
        assert all(hasattr(v, "column") and v.column > 0 for v in result)

    def test_violation_has_message(self) -> None:
        """Violations should have message."""
        text = "#Heading\n"
        result = lint(text)
        assert all(hasattr(v, "message") and v.message for v in result)

    def test_violation_has_severity(self) -> None:
        """Violations should have severity."""
        text = "#Heading\n"
        result = lint(text)
        assert all(
            hasattr(v, "severity") and v.severity in ("error", "warning")
            for v in result
        )


class TestListRules:
    """Tests for list_rules functionality."""

    def test_list_rules_returns_list(self) -> None:
        """list_rules should return a list."""
        rules = list_rules()
        assert isinstance(rules, list)

    def test_list_rules_not_empty(self) -> None:
        """list_rules should return at least one rule."""
        rules = list_rules()
        assert len(rules) > 0

    def test_list_rules_has_expected_count(self) -> None:
        """list_rules should return all 10 expected rules."""
        rules = list_rules()
        assert len(rules) == 10

    def test_list_rules_all_enabled_by_default(self) -> None:
        """All rules should be enabled by default."""
        rules = list_rules()
        assert all(r.default_enabled for r in rules)

    def test_list_rules_has_descriptions(self) -> None:
        """All rules should have descriptions."""
        rules = list_rules()
        assert all(r.description for r in rules)

    def test_list_rules_contains_md001(self) -> None:
        """MD001 should be in rules."""
        rules = list_rules()
        assert any(r.rule_id == "MD001" for r in rules)

    def test_list_rules_contains_md047(self) -> None:
        """MD047 should be in rules."""
        rules = list_rules()
        assert any(r.rule_id == "MD047" for r in rules)


class TestComplexScenarios:
    """Tests for complex markdown scenarios."""

    def test_multiple_violations_per_line(self) -> None:
        """Multiple violations can occur on same line."""
        text = "#Heading   \n"
        result = lint(text, rules=["MD018", "MD009"])
        # Could have both missing space and trailing whitespace
        assert len(result) > 0

    def test_nested_heading_levels(self) -> None:
        """Should handle nested heading levels correctly."""
        text = "# H1\n\n## H2\n\n### H3\n\n## H2\n"
        result = lint(text, rules=["MD001"])
        assert all(v.rule_id != "MD001" for v in result)

    def test_empty_lines_between_content(self) -> None:
        """Multiple blank lines between content should be detected."""
        text = "# Heading\n\n\n\nContent\n"
        result = lint(text, rules=["MD012"])
        violations = [v for v in result if v.rule_id == "MD012"]
        assert len(violations) >= 2

    def test_long_file_with_many_violations(self) -> None:
        """Should handle large files."""
        lines = ["# Heading\n"]
        for i in range(100):
            lines.append(f"x" * 121 + "\n")
        text = "".join(lines)
        result = lint(text, rules=["MD013"])
        assert len([v for v in result if v.rule_id == "MD013"]) >= 50

    def test_mixed_rule_violations(self) -> None:
        """Should detect violations from multiple rules."""
        text = "#H1\n\n\n\nContent  \n"
        result = lint(text)
        rule_ids = {v.rule_id for v in result}
        assert "MD018" in rule_ids or "MD009" in rule_ids or "MD012" in rule_ids

    def test_whitespace_only_lines(self) -> None:
        """Lines with only whitespace should be handled."""
        text = "# Heading\n   \nContent\n"
        result = lint(text)
        assert isinstance(result, list)

    def test_line_with_only_newline(self) -> None:
        """Blank lines should be handled."""
        text = "# Heading\n\nContent\n"
        result = lint(text)
        assert isinstance(result, list)
