# ---
# entity_id: module-check-breaking-changes
# entity_name: Breaking Change Checker
# entity_type_id: module
# entity_path: entity_store/check_breaking_changes.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T17:00:00Z
# entity_exports: [check_breaking_changes, main]
# entity_dependencies: [frontmatter, visualize]
# entity_callers: [pre-commit, ci]
# entity_callees: [frontmatter, visualize]
# entity_semver_impact: patch
# entity_breaking_change_risk: low
# ---

"""
Breaking Change Checker - Pre-push hook for detecting breaking changes.

Analyzes staged changes and detects:
- Modifications to high-risk entities
- Changes to public API
- Removed or renamed exports
- Modified function signatures

Follows https://semver.org/ guidelines:
- MAJOR: Breaking API changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes (backwards compatible)
"""

import subprocess
import sys
from pathlib import Path

from entity_store.frontmatter import BreakingChangeRisk, parse_frontmatter


def get_changed_files() -> list[Path]:
    """Get list of files changed in staged commits."""
    try:
        # Get files changed between HEAD and origin/main
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [Path(f) for f in result.stdout.strip().split("\n") if f]
    except subprocess.CalledProcessError:
        # Fallback to staged files
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            return [Path(f) for f in result.stdout.strip().split("\n") if f]
        except subprocess.CalledProcessError:
            return []


def check_breaking_changes() -> tuple[bool, list[str]]:
    """
    Check for breaking changes in staged files.

    Returns:
        Tuple of (has_breaking_changes, messages)
    """
    changed_files = get_changed_files()
    if not changed_files:
        return False, ["No changed files to analyze"]

    messages = []
    breaking_changes = []

    for filepath in changed_files:
        if not filepath.exists():
            continue

        if filepath.suffix not in (".py", ".ts", ".tsx"):
            continue

        try:
            source = filepath.read_text()
        except Exception:
            continue

        # Determine language
        language = "python" if filepath.suffix == ".py" else "typescript"

        # Parse frontmatter
        frontmatter = parse_frontmatter(source, language)
        if frontmatter is None:
            continue

        # Check for breaking change risk
        if frontmatter.entity_breaking_change_risk == BreakingChangeRisk.HIGH:
            breaking_changes.append(
                {
                    "file": str(filepath),
                    "entity": frontmatter.entity_name,
                    "risk": "HIGH",
                    "callers": frontmatter.entity_callers,
                    "semver": frontmatter.entity_semver_impact.value,
                }
            )

        if frontmatter.entity_public_api and frontmatter.would_break_dependents():
            breaking_changes.append(
                {
                    "file": str(filepath),
                    "entity": frontmatter.entity_name,
                    "risk": "PUBLIC API",
                    "callers": frontmatter.entity_callers,
                    "semver": "major",
                }
            )

    if breaking_changes:
        messages.append("⚠️  BREAKING CHANGES DETECTED")
        messages.append("")
        messages.append("The following changes may break downstream code:")
        messages.append("")

        for change in breaking_changes:
            messages.append(f"  📁 {change['file']}")
            messages.append(f"     Entity: {change['entity']}")
            messages.append(f"     Risk: {change['risk']}")
            messages.append(f"     Semver Impact: {change['semver'].upper()}")
            if change["callers"]:
                messages.append(f"     Dependents: {', '.join(change['callers'][:5])}")
            messages.append("")

        messages.append("Required actions:")
        messages.append("  1. Ensure this is intentional")
        messages.append("  2. Update CHANGELOG.md")
        messages.append("  3. Use 'feat!:' or 'BREAKING CHANGE:' in commit message")
        messages.append("  4. Bump to next MAJOR version")

        return True, messages

    return False, ["✅ No breaking changes detected"]


def main() -> int:
    """
    Main entry point for pre-push hook.

    Returns:
        Exit code (0 = success, 1 = breaking changes found)
    """
    has_breaking, messages = check_breaking_changes()

    for msg in messages:
        print(msg)

    # Return 0 to allow push (warning only)
    # Change to `return 1 if has_breaking else 0` to block pushes
    return 0


if __name__ == "__main__":
    sys.exit(main())
