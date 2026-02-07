# ---
# entity_id: module-agents-dotfiles
# entity_name: Dotfile Management
# entity_type_id: module
# entity_path: agents/dotfiles.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [DotfileManager, DotfileLayer, apply_dotfiles, diff_dotfiles]
# entity_dependencies: [pydantic, pathlib, yaml]
# entity_callers: [cli, makefile]
# entity_callees: []
# entity_semver_impact: minor
# entity_breaking_change_risk: low
# ---

"""
Chezmoi-style Dotfile Management for Multi-Agent Environments.

This module provides a layered dotfile management system:

Layers (in order of precedence, lowest to highest):
1. org/       - Organization-wide settings (shared across all projects)
2. project/   - Project-specific settings (checked into repo)
3. local/     - Machine-specific settings (gitignored)

Each layer can contain:
- .claude/    - Claude Code settings
- .config/    - Application configs
- .env.*      - Environment files

Files are merged with later layers overriding earlier ones.
Templates use Jinja2-style syntax for variable substitution.

Directory Structure:
    dotfiles/
    ├── org/                    # Organization defaults
    │   ├── .claude/
    │   │   └── settings.json
    │   └── .config/
    │       └── git/
    ├── project/                # Project-specific
    │   ├── .claude/
    │   │   └── settings.json
    │   └── .config/
    └── local/                  # Machine-specific (gitignored)
        ├── .claude/
        │   └── settings.local.json
        └── .env.local
"""

import json
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class DotfileLayer(str, Enum):
    """Dotfile layer hierarchy."""

    ORG = "org"
    PROJECT = "project"
    LOCAL = "local"


class MergeStrategy(str, Enum):
    """How to merge files across layers."""

    REPLACE = "replace"    # Later layer completely replaces
    DEEP_MERGE = "deep_merge"  # Deep merge dicts/objects
    APPEND = "append"      # Append to lists
    SKIP = "skip"          # Don't overwrite if exists


@dataclass
class DotfileSpec:
    """Specification for a managed dotfile."""

    source: Path           # Source path in dotfiles/
    target: Path           # Target path (relative to home or project)
    layer: DotfileLayer
    merge_strategy: MergeStrategy = MergeStrategy.REPLACE
    template: bool = False  # Whether to process as template
    executable: bool = False  # Whether to make executable


@dataclass
class DotfileDiff:
    """Difference between source and target dotfile."""

    spec: DotfileSpec
    source_content: Optional[str]
    target_content: Optional[str]
    status: str  # "added", "modified", "unchanged", "missing"

    @property
    def has_changes(self) -> bool:
        return self.status in ("added", "modified")


class DotfileConfig(BaseModel):
    """Configuration for dotfile management."""

    dotfiles_root: Path = Field(default=Path("dotfiles"))
    target_root: Path = Field(default=Path.home())
    project_root: Path = Field(default=Path.cwd())

    # Layer-specific targets
    org_target: Path = Field(default=Path.home())
    project_target: Path = Field(default=Path.cwd())
    local_target: Path = Field(default=Path.home())

    # Variables for template substitution
    variables: dict[str, str] = Field(default_factory=dict)

    # Files to skip
    ignore_patterns: list[str] = Field(
        default_factory=lambda: [".git", "__pycache__", "*.pyc", ".DS_Store"]
    )


class DotfileManager:
    """
    Manages dotfile configuration across layers.

    Provides:
    - Layer-based file organization
    - Template processing
    - Diff and apply operations
    - Merge strategies for config files
    """

    def __init__(self, config: Optional[DotfileConfig] = None):
        """Initialize dotfile manager."""
        self.config = config or DotfileConfig()
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure dotfile directories exist."""
        for layer in DotfileLayer:
            layer_path = self.config.dotfiles_root / layer.value
            layer_path.mkdir(parents=True, exist_ok=True)
            (layer_path / ".claude").mkdir(exist_ok=True)
            (layer_path / ".config").mkdir(exist_ok=True)

    def discover_files(self, layer: Optional[DotfileLayer] = None) -> list[DotfileSpec]:
        """
        Discover all dotfiles in specified layer(s).

        Args:
            layer: Specific layer or None for all layers

        Returns:
            List of DotfileSpec objects
        """
        layers = [layer] if layer else list(DotfileLayer)
        specs = []

        for l in layers:
            layer_path = self.config.dotfiles_root / l.value
            if not layer_path.exists():
                continue

            for path in layer_path.rglob("*"):
                if path.is_file() and not self._should_ignore(path):
                    relative = path.relative_to(layer_path)
                    target = self._get_target_path(l, relative)

                    specs.append(DotfileSpec(
                        source=path,
                        target=target,
                        layer=l,
                        merge_strategy=self._infer_merge_strategy(path),
                        template=path.suffix == ".tmpl",
                    ))

        return specs

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        name = path.name
        for pattern in self.config.ignore_patterns:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        return False

    def _get_target_path(self, layer: DotfileLayer, relative: Path) -> Path:
        """Get target path for a dotfile."""
        if layer == DotfileLayer.ORG:
            return self.config.org_target / relative
        elif layer == DotfileLayer.PROJECT:
            return self.config.project_target / relative
        else:  # LOCAL
            return self.config.local_target / relative

    def _infer_merge_strategy(self, path: Path) -> MergeStrategy:
        """Infer merge strategy from file type."""
        suffix = path.suffix.lower()
        if suffix in (".json", ".yaml", ".yml", ".toml"):
            return MergeStrategy.DEEP_MERGE
        elif suffix in (".env", ".sh", ".bash"):
            return MergeStrategy.APPEND
        return MergeStrategy.REPLACE

    def diff(self, layer: Optional[DotfileLayer] = None) -> list[DotfileDiff]:
        """
        Show differences between source and target dotfiles.

        Args:
            layer: Specific layer or None for all

        Returns:
            List of DotfileDiff objects
        """
        specs = self.discover_files(layer)
        diffs = []

        for spec in specs:
            source_content = self._read_file(spec.source)
            target_content = self._read_file(spec.target) if spec.target.exists() else None

            if spec.template:
                source_content = self._process_template(source_content)

            if target_content is None:
                status = "added"
            elif source_content == target_content:
                status = "unchanged"
            else:
                status = "modified"

            diffs.append(DotfileDiff(
                spec=spec,
                source_content=source_content,
                target_content=target_content,
                status=status,
            ))

        return diffs

    def apply(
        self,
        layer: Optional[DotfileLayer] = None,
        dry_run: bool = False,
    ) -> list[DotfileSpec]:
        """
        Apply dotfiles to their target locations.

        Args:
            layer: Specific layer or None for all
            dry_run: If True, don't actually write files

        Returns:
            List of applied DotfileSpec objects
        """
        diffs = self.diff(layer)
        applied = []

        for d in diffs:
            if not d.has_changes:
                continue

            if not dry_run:
                self._apply_file(d)
            applied.append(d.spec)

        return applied

    def _apply_file(self, diff: DotfileDiff) -> None:
        """Apply a single dotfile."""
        spec = diff.spec
        content = diff.source_content

        # Ensure target directory exists
        spec.target.parent.mkdir(parents=True, exist_ok=True)

        if spec.merge_strategy == MergeStrategy.DEEP_MERGE and diff.target_content:
            content = self._deep_merge_content(
                diff.target_content,
                content,
                spec.source.suffix,
            )
        elif spec.merge_strategy == MergeStrategy.APPEND and diff.target_content:
            content = diff.target_content + "\n" + content

        # Write file
        spec.target.write_text(content)

        # Set permissions
        if spec.executable:
            spec.target.chmod(spec.target.stat().st_mode | 0o111)

    def _read_file(self, path: Path) -> Optional[str]:
        """Read file content."""
        try:
            return path.read_text()
        except Exception:
            return None

    def _process_template(self, content: Optional[str]) -> Optional[str]:
        """Process template variables."""
        if content is None:
            return None

        # Simple variable substitution {{ var }}
        result = content
        for key, value in self.config.variables.items():
            result = result.replace(f"{{{{ {key} }}}}", value)
            result = result.replace(f"{{{{{key}}}}}", value)

        return result

    def _deep_merge_content(
        self,
        base: str,
        override: str,
        suffix: str,
    ) -> str:
        """Deep merge two config files."""
        try:
            if suffix == ".json":
                base_data = json.loads(base)
                override_data = json.loads(override)
                merged = self._deep_merge_dict(base_data, override_data)
                return json.dumps(merged, indent=2)
            elif suffix in (".yaml", ".yml"):
                base_data = yaml.safe_load(base)
                override_data = yaml.safe_load(override)
                merged = self._deep_merge_dict(base_data, override_data)
                return yaml.dump(merged, default_flow_style=False)
        except Exception:
            pass

        # Fallback to replace
        return override

    def _deep_merge_dict(self, base: dict, override: dict) -> dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge_dict(result[key], value)
            else:
                result[key] = value
        return result

    def status(self) -> dict[str, Any]:
        """Get status of all dotfiles."""
        diffs = self.diff()
        return {
            "total": len(diffs),
            "added": len([d for d in diffs if d.status == "added"]),
            "modified": len([d for d in diffs if d.status == "modified"]),
            "unchanged": len([d for d in diffs if d.status == "unchanged"]),
            "by_layer": {
                layer.value: len([d for d in diffs if d.spec.layer == layer])
                for layer in DotfileLayer
            },
        }


# CLI functions
def apply_dotfiles(layer: Optional[str] = None, dry_run: bool = False) -> None:
    """Apply dotfiles from CLI."""
    manager = DotfileManager()
    layer_enum = DotfileLayer(layer) if layer else None

    applied = manager.apply(layer_enum, dry_run=dry_run)

    if dry_run:
        print(f"Would apply {len(applied)} files")
    else:
        print(f"Applied {len(applied)} files")

    for spec in applied:
        print(f"  {spec.layer.value}: {spec.target}")


def diff_dotfiles(layer: Optional[str] = None) -> None:
    """Show dotfile diff from CLI."""
    manager = DotfileManager()
    layer_enum = DotfileLayer(layer) if layer else None

    diffs = manager.diff(layer_enum)

    for d in diffs:
        if d.has_changes:
            symbol = "+" if d.status == "added" else "~"
            print(f"[{symbol}] {d.spec.layer.value}: {d.spec.target}")


def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Dotfile management")
    parser.add_argument("command", choices=["apply", "diff", "status"])
    parser.add_argument("--layer", choices=["org", "project", "local"])
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.command == "apply":
        apply_dotfiles(args.layer, args.dry_run)
    elif args.command == "diff":
        diff_dotfiles(args.layer)
    elif args.command == "status":
        manager = DotfileManager()
        status = manager.status()
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
