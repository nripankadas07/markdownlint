"""Markdown linting rules implementation."""

import re
from typing import Any, Callable

from .models import RuleInfo, Violation


class RuleEngine:
    """Engine for running linting rules."""

    def __init__(self) -> None:
        self.rules: dict[str, Callable[..., list[Violation]]] = {
            "MD001": self._check_heading_increment,
            "MD003": self._check_heading_style,
            "MD009": self._check_trailing_whitespace,
            "MD010": self._check_hard_tabs,
            "MD012": self._check_blank_lines,
            "MD013": self._check_line_length,
            "MD018": self._check_heading_space,
            "MD022": self._check_heading_spacing,
            "MD023": self._check_heading_start,
            "MD047": self._check_final_newline,
        }

    def get_rules(self) -> list[RuleInfo]:
        """Get all available rules."""
        return [
            RuleInfo(
                "MD001",
                "Heading increment",
                "Heading levels should increment by one at a time",
            ),
            RuleInfo(
                "MD003",
                "Heading style",
                "Heading style should be consistent (ATX vs setext)",
            ),
            RuleInfo(
                "MD009", "Trailing whitespace", "Lines should not have trailing whitespace"
            ),
            RuleInfo(
                "MD010", "Hard tabs", "Code blocks should use spaces, not hard tabs"
            ),
            RuleInfo(
                "MD012",
                "Multiple blank lines",
                "Multiple consecutive blank lines should be reduced to one",
            ),
            RuleInfo(
                "MD013",
                "Line length",
                "Line length should not exceed the configured limit",
            ),
            RuleInfo(
                "MD018",
                "No missing space after hash",
                "ATX headings should have a space after the opening hash",
            ),
            RuleInfo(
                "MD022",
                "Headings should be surrounded by blank lines",
                "Headings should be surrounded by blank lines",
            ),
            RuleInfo(
                "MD023",
                "Heading start of line",
                "Headings must start at the beginning of the line",
            ),
            RuleInfo(
                "MD047",
                "File end newline",
                "Files should end with a single newline character",
            ),
        ]

    def _is_code_fence_line(self, line: str) -> bool:
        """Check if line starts a code fence."""
        stripped = line.lstrip()
        return stripped.startswith("```") or stripped.startswith("~~~")

    def _is_indented_code_block(self, line: str) -> bool:
        """Check if line is part of an indented code block (4 spaces or ctab)."""
        return line.startswith("    ") or line.startswith("\t")

    def _get_in_code_block_lines(self, lines: list[str]) -> set[int]:
        """Get set of line numbers (0-indexed) that are inside code blocks."""
        in_code: set[int] = set()
        in_fence = False
        fence_char = ""

        for idx, line in enumerate(lines):
            stripped = line.lstrip()

            if in_fence:
                if stripped.startswith(fence_char):
                    in_fence = False
                else:
                    in_code.add(idx)
            elif self._is_code_fence_line(line):
                fence_char = stripped[0]
                in_fence = True
            elif self._is_indented_code_block(line):
                in_code.add(idx)

        return in_code

    def _get_in_html_comment(self, lines: list[str]) -> set[int]:
        """Get set of line numbers (0-indexed) inside HTML comments."""
        in_comment: set[int] = set()
        in_html_comment = False

        for idx, line in enumerate(lines):
            if "!--" in line:
                in_html_comment = True
            if in_html_comment:
                in_comment.add(idx)
            if "-->" in line:
                in_html_comment = False

        return in_comment

    def _check_heading_increment(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD001: Check heading level increment."""
        violations = []
        prev_level = 0
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in code_lines or idx in comment_lines:
                continue

            stripped = line.lstrip()
            if stripped.startswith("#"):
                level = len(stripped) - len(stripped.lstrip("#"))
                if level > 6 or not stripped[level:].startswith(" "):
                    continue

                if prev_level > 0 and level > prev_level + 1:
                    violations.append(
                        Violation(
                            "MD001",
                            idx + 1,
                            1,
                            f"Heading level {level} skips level(s) from {prev_level}",
                        )
                    )
                prev_level = level

        return violations

    def _check_heading_style(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD003: Check heading style consistency."""
        violations = []
        atx_count = 0
        setext_count = 0
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in code_lines or idx in comment_lines:
                continue

            if idx + 1 < len(lines):
                next_line = lines[idx + 1]
                if re.match(r"^=+\s*$", next_line) or re.match(r"^-+\s*$", next_line):
                    setext_count += 1
                    continue

            stripped = line.lstrip()
            if stripped.startswith("#") and len(stripped) > 0:
                hashes = 0
                for char in stripped:
                    if char == "#":
                        hashes += 1
                    else:
                        break
                if hashes <= 6:
                    atx_count += 1

        if atx_count > 0 and setext_count > 0:
            for idx, line in enumerate(lines):
                if idx in code_lines or idx in comment_lines:
                    continue
                if idx + 1 < len(lines):
                    next_line = lines[idx + 1]
                    if re.match(r"^=+\s*$", next_line) or re.match(
                        r"^-+\s*$", next_line
                    ):
                        violations.append(
                            Violation(
                                "MD003",
                                idx + 1,
                                1,
                                "Heading style is inconsistent (mixing ATX and setext)",
                            )
                        )

        return violations

    def _check_trailing_whitespace(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD009: Check for trailing whitespace."""
        violations = []
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in code_lines or idx in comment_lines:
                continue

            if line.rstrip("\n") != line.rstrip():
                violations.append(
                    Violation(
                        "MD009",
                        idx + 1,
                        len(line.rstrip("\n")) + 1,
                        "Trailing whitespace",
                    )
                )

        return violations

    def _check_hard_tabs(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD010: Check for hard tabs outside code blocks."""
        violations = []
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in comment_lines:
                continue

            if "\t" in line:
                col = line.index("\t") + 1
                violations.append(
                    Violation(
                        "MD010", idx + 1, col, "Hard tabs should not be used"
                    )
                )

        return violations

    def _check_blank_lines(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD012: Check for multiple consecutive blank lines."""
        violations = []
        blank_count = 0
        blank_start = 0

        for idx, line in enumerate(lines):
            if line.strip() == "":
                if blank_count == 0:
                    blank_start = idx
                blank_count += 1
            else:
                if blank_count > 1:
                    for blank_idx in range(blank_start + 1, blank_start + blank_count):
                        violations.append(
                            Violation(
                                "MD012",
                                blank_idx + 1,
                                1,
                                "Multiple consecutive blank lines",
                            )
                        )
                blank_count = 0

        return violations

    def _check_line_length(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD013: Check line length."""
        violations = []
        max_length = config.get("line_length", 120)
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in code_lines or idx in comment_lines:
                continue

            line_len = len(line.rstrip("\n"))
            if line_len > max_length:
                violations.append(
                    Violation(
                        "MD013",
                        idx + 1,
                        max_length + 1,
                        f"Line length {line_len} exceeds limit {max_length}",
                    )
                )

        return violations

    def _check_heading_space(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD018: Check for missing space after # in ATX headings."""
        violations = []
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in code_lines or idx in comment_lines:
                continue

            stripped = line.lstrip()
            if stripped.startswith("#"):
                hashes = 0
                for char in stripped:
                    if char == "#":
                        hashes += 1
                    else:
                        break

                if hashes <= 6:
                    if len(stripped) > hashes:
                        next_char = stripped[hashes]
                        if next_char != " " and next_char != "\n":
                            violations.append(
                                Violation(
                                    "MD018",
                                    idx + 1,
                                    hashes + 1,
                                    "Missing space after # in ATX heading",
                                )
                            )

        return violations

    def _check_heading_spacing(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD022: Check heading blank line spacing."""
        violations = []
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in code_lines or idx in comment_lines:
                continue

            stripped = line.lstrip()
            if stripped.startswith("#"):
                is_atx = stripped.startswith("#") and len(stripped) > 0

                if is_atx:
                    if idx > 0:
                        prev_line = lines[idx - 1]
                        if prev_line.strip() != "":
                            violations.append(
                                Violation(
                                    "MD022",
                                    idx + 1,
                                    1,
                                    "Headings should be surrounded by blank lines",
                                )
                            )

                    if idx < len(lines) - 1:
                        next_line = lines[idx + 1]
                        if next_line.strip() != "":
                            violations.append(
                                Violation(
                                    "MD022",
                                    idx + 1,
                                    1,
                                    "Headings should be surrounded by blank lines",
                                )
                            )

        return violations

    def _check_heading_start(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD023: Check that headings start at beginning of line."""
        violations = []
        code_lines = self._get_in_code_block_lines(lines)
        comment_lines = self._get_in_html_comment(lines)

        for idx, line in enumerate(lines):
            if idx in code_lines or idx in comment_lines:
                continue

            stripped = line.lstrip()
            if stripped.startswith("#"):
                if line != stripped:
                    violations.append(
                        Violation(
                            "MD023",
                            idx + 1,
                            1,
                            "Headings must start at the beginning of the line",
                        )
                    )

        return violations

    def _check_final_newline(
        self, lines: list[str], config: dict[str, Any]
    ) -> list[Violation]:
        """MD047: Check that file ends with single newline."""
        violations = []

        if len(lines) == 0:
            return violations

        last_line = lines[-1]
        if last_line and not last_line.endswith("\n"):
            violations.append(
                Violation(
                    "MD047", len(lines), len(last_line) + 1, "File should end with newline"
                )
            )

        return violations

    def check(
        self,
        lines: list[str],
        rules: list[str] | None = None,
        config: dict[str, Any] | None = None,
    ) -> list[Violation]:
        """Run all specified rules."""
        if config is None:
            config = {}

        if rules is None:
            rules = list(self.rules.keys())

        violations: list[Violation] = []

        for rule_id in rules:
            if rule_id in self.rules:
                rule_func = self.rules[rule_id]
                violations.extend(rule_func(lines, config))

        return sorted(violations, key=lambda v: (v.line, v.column))
