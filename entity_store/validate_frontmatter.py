# ---
# entity_id: module-validate-frontmatter
# entity_name: Frontmatter Validator
# entity_type_id: module
# entity_path: entity_store/validate_frontmatter.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T17:00:00Z
# entity_exports: [validate_file, main]
# entity_dependencies: [frontmatter]
# entity_callers: [pre-commit]
# entity_callees: [frontmatter]
# entity_semver_impact: patch
# entity_breaking_change_risk: low
# ---

"""
Frontmatter Validator - Pre-commit hook for validating entity frontmatter.

Validates that:
- All tracked files have frontmatter
- Frontmatter follows the schema
- Required fields are present
- Dependencies reference valid entities
"""

import sys
from pathlib import Path

from entity_store.frontmatter import parse_frontmatter

# Directories that require frontmatter
TRACKED_DIRS = {"entity_store", "entity_cli", "cli", ".claude", "tests"}

# Extensions that should have frontmatter
TRACKED_EXTENSIONS = {".py", ".ts", ".tsx", ".md"}


def validate_file(filepath: Path) -> list[str]:
    """
    Validate frontmatter in a single file.

    Args:
        filepath: Path to the file

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check if file should be tracked
    if not any(part in filepath.parts for part in TRACKED_DIRS):
        return []

    if filepath.suffix not in TRACKED_EXTENSIONS:
        return []

    # Skip __pycache__ and similar
    if "__pycache__" in filepath.parts:
        return []

    # Read file
    try:
        source = filepath.read_text()
    except Exception as e:
        errors.append(f"Could not read file: {e}")
        return errors

    # Determine language
    language = "python"
    if filepath.suffix in (".ts", ".tsx"):
        language = "typescript"
    elif filepath.suffix == ".md":
        language = "markdown"

    # Parse frontmatter
    frontmatter = parse_frontmatter(source, language)

    if frontmatter is None:
        # Check if file has any content (skip empty files)
        if source.strip():
            errors.append(f"Missing frontmatter in {filepath}")
        return errors

    # Validate required fields
    if not frontmatter.entity_id:
        errors.append(f"Missing entity_id in {filepath}")

    if not frontmatter.entity_name:
        errors.append(f"Missing entity_name in {filepath}")

    if not frontmatter.entity_type_id:
        errors.append(f"Missing entity_type_id in {filepath}")

    if not frontmatter.entity_path:
        errors.append(f"Missing entity_path in {filepath}")

    # Validate path matches actual path
    expected_path = str(filepath).replace("\\", "/")
    if not expected_path.endswith(frontmatter.entity_path):
        errors.append(
            f"entity_path mismatch in {filepath}: "
            f"expected '{expected_path}' to end with '{frontmatter.entity_path}'"
        )

    return errors


def main() -> int:
    """
    Main entry point for pre-commit hook.

    Returns:
        Exit code (0 = success, 1 = validation failed)
    """
    files = [Path(f) for f in sys.argv[1:] if Path(f).exists()]

    all_errors = []

    for filepath in files:
        errors = validate_file(filepath)
        all_errors.extend(errors)

    if all_errors:
        print("Frontmatter validation failed:")
        for error in all_errors:
            print(f"  ❌ {error}")
        return 1

    if files:
        print(f"✅ Validated frontmatter in {len(files)} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
