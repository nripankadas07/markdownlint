# markdownlint

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Validate Markdown files against configurable common style rules for developers.

## Features

- **Zero dependencies** — pure Python, no external libraries required
- **10 built-in rules** — covers common Markdown style issues
- **Configurable** — enable/disable rules, customize thresholds
- **Simple API** — lint strings or files with a single function call
- **Type hints** — full type annotation support
- **Comprehensive** — 30+ test cases, >80% code coverage

## Installation

### From source

Clone and install:

```bash
git clone https://github.com/nripankadas07/markdownlint.git
cd markdownlint
pip install -e .
```

### Quick install from GitHub

```bash
pip install git+https://github.com/nripankadas07/markdownlint.git
```

## Quick Start

### Lint a string

```python
from markdownlint import lint

text = """# My Document

This is content.
"""

violations = lint(text)
for v in violations:
    print(f"{v.rule_id}: Line {v.line}, Col {v.column}: {v.message}")
```

### Lint a file

```python
from markdownlint import lint_file

violations = lint_file("README.md")
for v in violations:
    print(f"{v.rule_id}: {v.message}")
```

### Check specific rules

```python
# Only check MD018 (missing space after #) and MD009 (trailing whitespace)
violations = lint(text, rules=["MD018", "MD009"])
```

### Configure rules

```python
# Custom line length limit
violations = lint(text, config={"line_length": 80})
```

### List all available rules

```python
from markdownlint import list_rules

rules = list_rules()
for rule in rules:
    print(f"{rule.rule_id}: {rule.name}")
    print(f"  {rule.description}")
```

## API Reference

### `lint(text: str, rules: list[str] | None = None, config: dict | None = None) -> list[Violation]`

Lint a Markdown string.

**Parameters:**
- `text` (str): Markdown content to validate
- `rules` (list[str], optional): Specific rule IDs to check. If None, all rules are checked.
- `config` (dict, optional): Configuration options (e.g., `{"line_length": 100}`)

**Returns:**
- List of `Violation` objects, sorted by line and column

**Raises:**
- `MarkdownlintError`: If input is not a string

### `lint_file(path: str, rules: list[str] | None = None, config: dict | None = None) -> list[Violation]`

Lint a Markdown file.

**Parameters:**
- `path` (str): Path to Markdown file
- `rules` (list[str], optional): Specific rule IDs to check
- `config` (dict, optional): Configuration options

**Returns:**
- List of `Violation` objects

**Raises:**
- `MarkdownlintError`: If file not found or not readable

### `list_rules() -> list[RuleInfo]`

Get all available rules.

**Returns:**
- List of `RuleInfo` objects with metadata about each rule

### `Violation` (dataclass)

Represents a single style violation.

**Attributes:**
- `rule_id` (str): Rule identifier (e.g., "MD001")
- `line` (int): Line number (1-indexed)
- `column` (int): Column number (1-indexed)
- `message` (str): Human-readable description
- `severity` (str): "error" or "warning"

### `RuleInfo` (dataclass)

Information about a linting rule.

**Attributes:**
- `rule_id` (str): Rule identifier
- `name` (str): Short name
- `description` (str): Detailed description
- `default_enabled` (bool): Whether enabled by default

### `MarkdownlintError` (exception)

Raised for user errors (bad input, missing files, etc.).

## Rules

| ID | Name | Description |
|---|---|---|
| **MD001** | Heading increment | Heading levels should increment by one at a time |
| **MD003** | Heading style | Heading style should be consistent (ATX vs setext) |
| **MD009** | Trailing whitespace | Lines should not have trailing whitespace |
| **MD010** | Hard tabs | Code blocks should use spaces, not hard tabs |
| **MD012** | Multiple blank lines | Multiple consecutive blank lines should be reduced to one |
| **MD013** | Line length | Line length should not exceed the configured limit (default: 120) |
| **MD018** | No missing space after hash | ATX headings should have a space after the opening hash |
| **MD022** | Heading blank lines | Headings should be surrounded by blank lines |
| **MD023** | Heading start of line | Headings must start at the beginning of the line |
| **MD047** | File end newline | Files should end with a single newline character |

## Configuration

Pass a `config` dict to customize rule behavior:

```python
config = {
    "line_length": 100,  # Change MD013 limit (default: 120)
}

violations = lint(text, config=config)
```

## Edge Cases Handled

- **Code fences** — violations inside ` ``` ` or ` ~~~` blocks are excluded
- **Indented code blocks** — 4-space indented code is excluded
- **HTML comments** — violations inside `<!-- -->` are excluded
- **Empty files** — handled gracefully
- **UTF-8 content** — full Unicode support

## Running Tests

Install test dependencies:

```bash
pip install pytest pytest-cov
```

Run tests:

```bash
pytest tests/ -v
```

With coverage report:

```bash
pytest tests/ --cov=src/markdownlint --cov-report=term-missing
```

## Development

The project follows TDD principles with comprehensive test coverage:

- **30+ tests** covering all rules and edge cases
- **Type hints** on all functions
- **Clean code** with functions ≤30 lines, nesting ≤3 levels
- **No dead code** — every function is tested

## License

MIT License — see LICENSE file for details.

Copyright (c) 2026 Nripanka Das# markdownlint
Validate Markdown files against configurable common style rules. Zero dependencies.
