"""Tests for lint_file functionality."""

import os
import tempfile

import pytest

from markdownlint import MarkdownlintError, lint_file


class TestLintFile:
    """File linting tests."""

    def test_lint_file_not_found(self) -> None:
        """Non-existent file should raise error."""
        with pytest.raises(MarkdownlintError):
            lint_file("/nonexistent/file.md")

    def test_lint_file_valid(self) -> None:
        """Valid markdown file should have no violations."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as f:
            f.write("# Heading\n\nContent\n")
            f.flush()
            path = f.name

        try:
            result = lint_file(path)
            assert result == []
        finally:
            os.unlink(path)

    def test_lint_file_with_violations(self) -> None:
        """File with violations should return violations."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as f:
            f.write("#Heading\n")
            f.flush()
            path = f.name

        try:
            result = lint_file(path)
            assert len(result) > 0
        finally:
            os.unlink(path)

    def test_lint_file_with_rules(self) -> None:
        """Rules parameter should be respected."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as f:
            f.write("#Heading\n")
            f.flush()
            path = f.name

        try:
            result = lint_file(path, rules=["MD018"])
            assert all(v.rule_id == "MD018" for v in result)
        finally:
            os.unlink(path)

    def test_lint_file_with_config(self) -> None:
        """Config parameter should be respected."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as f:
            f.write("x" * 51 + "\n")
            f.flush()
            path = f.name

        try:
            result = lint_file(path, config={"line_length": 50})
            assert any(v.rule_id == "MD013" for v in result)
        finally:
            os.unlink(path)

    def test_lint_file_relative_path(self) -> None:
        """Relative paths should work."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.md")
            with open(filepath, "w") as f:
                f.write("# Heading\n")

            cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = lint_file("test.md")
                assert result == []
            finally:
                os.chdir(cwd)

    def test_lint_file_utf8(self) -> None:
        """UTF-8 files should be handled correctly."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Heading\n\nContent with Ã©mojis: ð\n")
            f.flush()
            path = f.name

        try:
            result = lint_file(path)
            assert isinstance(result, list)
        finally:
            os.unlink(path)
