# Python Tools Summary

Optimized for LLM consumption. Key concepts and architecture of Python development tools.

## UV: Package Manager & Environment Tool

**Purpose:** Single tool replacing pip, poetry, venv for package management.

**Key Concepts:**
- Virtual environments: Isolated Python projects with dependencies
- Lock files (uv.lock): Ensures reproducible builds across machines
- Python version management: Install and pin specific Python versions
- Dependency resolution: Smart algorithm for compatible versions
- Tool isolation: `uvx` runs tools in isolated environments

**Essential Commands:**
```bash
uv init my_project        # Create project
uv add requests           # Add dependency
uv add --dev pytest       # Dev-only dependency
uv lock --upgrade         # Update lock file
uv run script.py          # Run in project env
uvx ruff check .          # Run tool in isolation
```

**When to Use:**
- Creating new Python projects
- Managing dependencies
- Running tools without installing globally
- Publishing packages

**Architecture:** Uses Rust for speed. Concepts align with pip + poetry + venv combined.

---

## Ruff: Linter + Formatter

**Purpose:** Code quality - find bugs, fix style, organize imports.

**Key Concepts:**
- Rules: Hundreds of rules organized by category (E/F/W/I/etc.)
- Auto-fix: Many violations fixed automatically
- Import organization: Replaces isort
- No configuration required: Sensible defaults

**Essential Commands:**
```bash
ruff check .              # Find issues
ruff check --fix .        # Auto-fix issues
ruff format .             # Format code
```

**When to Use:**
- Before committing code
- In CI/CD pipelines
- Pre-commit hooks
- As IDE background tool

**Architecture:** Combines functionality of pylint, flake8, black, isort. 10-100x faster.

---

## Ty: Type Checker

**Purpose:** Static type analysis - catch errors before runtime.

**Key Concepts:**
- Type annotations: Function/variable type hints (Python 3.8+)
- Type narrowing: Refining types within conditional blocks
- Strict mode: Enforce annotations on all functions
- Zero runtime overhead: Analysis only, no runtime cost

**Essential Commands:**
```bash
ty check .                     # Check types
ty check --show-diagnostics .  # Detailed output
```

**When to Use:**
- After writing code (during development)
- Before type-critical operations
- In CI/CD pipelines
- Building APIs or libraries

**Architecture:** Works with PEP 484 type hints. Follows Python typing standards.

---

## Quality Gate Workflow

**Typical Development Flow:**
```
1. Write code
2. ruff check --fix (style/bugs)
3. ruff format (formatting)
4. ty check (type safety)
5. pytest (runtime tests)
6. Commit
```

**Pre-commit Hook:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  # ty check optional, slower
```

**Key Points:**
- UV manages dependencies for all three
- Ruff runs before ty (fixes style before type checking)
- Ty runs before tests (catches type errors early)
- All three are optional but recommended

---

## Configuration Example (pyproject.toml)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-app"
dependencies = ["requests>=2.31.0"]

[dependency-groups]
dev = ["pytest>=7.0", "ruff", "ty"]

[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
ignore = ["E501"]

[tool.ruff.format]
line-length = 100

[tool.ty]
python-version = "3.10"
strict = false
```

---

## Integration Points

**With IDE (VS Code):**
- Ruff: Real-time linting
- Ty: Real-time type checking
- Both: Show inline diagnostics

**With CI/CD:**
- Run quality checks on PRs
- Block merge if failures
- Report in PR comments

**With Development:**
- Git pre-commit hooks
- IDE on-save checks
- Manual: `uv run ruff check && ty check && uv run pytest`

---

## Common Patterns

**Pattern 1: New Python Project**
- `uv init` + add dependencies
- Configure ruff + ty in pyproject.toml
- Setup IDE linting/formatting

**Pattern 2: Legacy Code Migration**
- Run ruff fixes incrementally
- Add type annotations gradually
- Enable strict mode once clean

**Pattern 3: Team Consistency**
- Shared pyproject.toml config
- Pre-commit hooks enforce on local machine
- CI enforces on server

---

## Performance Notes

- **Ruff:** Processes 10K+ lines/sec. IDE integration is instant.
- **Ty:** Slower than ruff, 100s of lines/sec on large projects.
- **UV:** Lock resolution may take seconds for complex deps.

**Best Practice:** Run ruff locally, ty before pushing, full check in CI.

---

## Token Count: ~950 tokens

Used for: Context window optimization, agent prompts, decision trees.
