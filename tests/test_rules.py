"""Tests for individual markdown linting rules."""

import pytest

from markdownlint import lint


class TestMD001HeadingIncrement:
    """MD001: Heading increment tests."""

    def test_md001_valid_increment(self) -> None:
        """Valid heading increments should have no violations."""
        text = "# H1\n\n## H2\n\n### H3\n"
        result = lint(text, rules=["MD001"])
        assert all(v.rule_id != "MD001" for v in result)

    def test_md001_skip_level(self) -> None:
        """Skipping heading levels should trigger violation."""
        text = "# H1\n\n### H3\n"
        result = lint(text, rules=["MD001"])
        assert any(v.rule_id == "MD001" for v in result)

    def test_md001_skip_multiple_levels(self) -> None:
        """Skipping multiple levels should trigger violation."""
        text = "# H1\n\n#### H4\n"
        result = lint(text, rules=["MD001"])
        assert any(v.rule_id == "MD001" for v in result)

    def test_md001_first_heading_any_level(self) -> None:
        """First heading can be any level."""
        text = "### H3\n"
        result = lint(text, rules=["MD001"])
        assert all(v.rule_id != "MD001" for v in result)

    def test_md001_allows_return_to_lower(self) -> None:
        """Can return to lower heading levels."""
        text = "# H1\n\n## H2\n\n# H1\n"
        result = lint(text, rules=["MD001"])
        assert all(v.rule_id != "MD001" for v in result)


class TestMD003HeadingStyle:
    """MD003: Heading style consistency tests."""

    def test_md003_all_atx(self) -> None:
        """All ATX headings should be valid."""
        text = "# H1\n\n## H2\n\n### H3\n"
        result = lint(text, rules=["MD003"])
        assert all(v.rule_id != "MD003" for v in result)

    def test_md003_mixed_styles(self) -> None:
        """Mixing ATX and setext should trigger violation."""
        text = "H1\n==\n\n## H2\n"
        result = lint(text, rules=["MD003"])
        assert any(v.rule_id == "MD003" for v in result)

    def test_md003_all_setext(self) -> None:
        """All setext headings should be valid."""
        text = "H1\n==\n\nH2\n--\n"
        result = lint(text, rules=["MD003"])
        assert all(v.rule_id != "MD003" for v in result)


class TestMD009TrailingWhitespace:
    """MD009: Trailing whitespace tests."""

    def test_md009_no_trailing(self) -> None:
        """Lines without trailing whitespace should be valid."""
        text = "# Heading\nContent\n"
        result = lint(text, rules=["MD009"])
        assert all(v.rule_id != "MD009" for v in result)

    def test_md009_trailing_space(self) -> None:
        """Trailing space should trigger violation."""
        text = "# Heading  \nContent\n"
        result = lint(text, rules=["MD009"])
        assert any(v.rule_id == "MD009" for v in result)

    def test_md009_trailing_tab(self) -> None:
        """Trailing tab should trigger violation."""
        text = "# Heading\t\nContent\n"
        result = lint(text, rules=["MD009"])
        assert any(v.rule_id == "MD009" for v in result)

    def test_md009_multiple_trailing(self) -> None:
        """Multiple trailing spaces should trigger violation."""
        text = "Content      \n"
        result = lint(text, rules=["MD009"])
        assert any(v.rule_id == "MD009" for v in result)


class TestMD010HardTabs:
    """MD010: Hard tabs tests."""

    def test_md010_no_tabs(self) -> None:
        """No tabs should be valid."""
        text = "# Heading\nContent with spaces\n"
        result = lint(text, rules=["MD010"])
        assert all(v.rule_id != "MD010" for v in result)

    def test_md010_hard_tab(self) -> None:
        """Hard tab should trigger violation."""
        text = "Content\twith\ttab\n"
        result = lint(text, rules=["MD010"])
        assert any(v.rule_id == "MD010" for v in result)

    def test_md010_tab_in_indentation(self) -> None:
        """Tab in indentation should trigger violation."""
        text = "\tIndented\n"
        result = lint(text, rules=["MD010"])
        assert any(v.rule_id == "MD010" for v in result)


class TestMD012MultipleBlankLines:
    """MD012: Multiple consecutive blank lines tests."""

    def test_md012_single_blank_lines(self) -> None:
        """Single blank lines should be valid."""
        text = "# Heading\n\nContent\n\nMore\n"
        result = lint(text, rules=["MD012"])
        assert all(v.rule_id != "MD012" for v in result)

    def test_md012_double_blank_lines(self) -> None:
        """Double blank lines should trigger violation."""
        text = "# Heading\n\n\nContent\n"
        result = lint(text, rules=["MD012"])
        assert any(v.rule_id == "MD012" for v in result)

    def test_md012_triple_blank_lines(self) -> None:
        """Triple blank lines should trigger violations."""
        text = "# Heading\n\n\n\nContent\n"
        result = lint(text, rules=["MD012"])
        assert len([v for v in result if v.rule_id == "MD012"]) >= 2


class TestMD013LineLength:
    """MD013: Line length tests."""

    def test_md013_short_line(self) -> None:
        """Short lines should be valid."""
        text = "# Heading\n"
        result = lint(text, rules=["MD013"])
        assert all(v.rule_id != "MD013" for v in result)

    def test_md013_long_line_default(self) -> None:
        """Line exceeding default limit should trigger violation."""
        text = "x" * 121 + "\n"
        result = lint(text, rules=["MD013"])
        assert any(v.rule_id == "MD013" for v in result)

    def test_md013_custom_limit(self) -> None:
        """Custom limit should be respected."""
        text = "x" * 51 + "\n"
        result = lint(text, rules=["MD013"], config={"line_length": 50})
        assert any(v.rule_id == "MD013" for v in result)

    def test_md013_at_limit(self) -> None:
        """Line at limit should be valid."""
        text = "x" * 120 + "\n"
        result = lint(text, rules=["MD013"])
        assert all(v.rule_id != "MD013" for v in result)


class TestMD018HeadingSpace:
    """MD018: Missing space after heading hash tests."""

    def test_md018_proper_space(self) -> None:
        """Proper spacing should be valid."""
        text = "# Heading\n## Heading\n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id != "MD018" for v in result)

    def test_md018_missing_space(self) -> None:
        """Missing space should trigger violation."""
        text = "#Heading\n"
        result = lint(text, rules=["MD018"])
        assert any(v.rule_id == "MD018" for v in result)

    def test_md018_multiple_hashes(self) -> None:
        """Missing space with multiple hashes should trigger violation."""
        text = "##Heading\n"
        result = lint(text, rules=["MD018"])
        assert any(v.rule_id == "MD018" for v in result)

    def test_md018_empty_heading(self) -> None:
        """Empty heading should be valid."""
        text = "# \n"
        result = lint(text, rules=["MD018"])
        assert all(v.rule_id != "MD018" for v in result)


class TestMD022HeadingSpacing:
    """MD022: Headings surrounded by blank lines tests."""

    def test_md022_proper_spacing(self) -> None:
        """Proper spacing should be valid."""
        text = "\n# Heading\n\nContent\n"
        result = lint(text, rules=["MD022"])
        assert all(v.rule_id != "MD022" for v in result)

    def test_md022_no_space_before(self) -> None:
        """Missing blank line before heading should trigger violation."""
        text = "Content\n# Heading\n"
        result = lint(text, rules=["MD022"])
        assert any(v.rule_id == "MD022" for v in result)

    def test_md022_no_space_after(self) -> None:
        """Missing blank line after heading should trigger violation."""
        text = "# Heading\nContent\n"
        result = lint(text, rules=["MD022"])
        assert any(v.rule_id == "MD022" for v in result)


class TestMD023HeadingStart:
    """MD023: Headings start at beginning of line tests."""

    def test_md023_at_beginning(self) -> None:
        """Heading at start should be valid."""
        text = "# Heading\n"
        result = lint(text, rules=["MD023"])
        assert all(v.rule_id != "MD023" for v in result)

    def test_md023_indented_heading(self) -> None:
        """Indented heading should trigger violation."""
        text = "  # Heading\n"
        result = lint(text, rules=["MD023"])
        assert any(v.rule_id == "MD023" for v in result)

    def test_md023_space_indented(self) -> None:
        """Space-indented heading should trigger violation."""
        text = " # Heading\n"
        result = lint(text, rules=["MD023"])
        assert any(v.rule_id == "MD023" for v in result)


class TestMD047FileEndNewline:
    """MD047: File end with newline tests."""

    def test_md047_ends_with_newline(self) -> None:
        """File ending with newline should be valid."""
        text = "# Heading\n"
        result = lint(text, rules=["MD047"])
        assert all(v.rule_id != "MD047" for v in result)

    def test_md047_no_newline(self) -> None:
        """File not ending with newline should trigger violation."""
        text = "# Heading"
        result = lint(text, rules=["MD047"])
        assert any(v.rule_id == "MD047" for v in result)

    def test_md047_content_no_newline(self) -> None:
        """Content without final newline should trigger violation."""
        text = "Content"
        result = lint(text, rules=["MD047"])
        assert any(v.rule_id == "MD047" for v in result)
