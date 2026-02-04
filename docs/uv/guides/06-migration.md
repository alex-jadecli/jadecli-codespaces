# Migration

Guide for migrating to uv from other Python package managers.

## Migrating from pip

Convert a `requirements.txt` file:

```bash
uv pip compile requirements.txt
```

Or migrate to a modern `pyproject.toml`:

```bash
uv init --python 3.12
```

Then add your dependencies:

```bash
uv add package1 package2 package3
```

## Migrating from Poetry

If you're coming from Poetry:

1. Export your dependencies from `pyproject.toml`
2. Create a new uv project:

```bash
uv init
```

3. Add your dependencies:

```bash
uv add $(grep "^[a-z]" pyproject.toml | cut -d' ' -f1)
```

## Migrating from Pipenv

Convert your `Pipfile` to `pyproject.toml`:

```bash
uv init
```

Then add your dependencies from the original Pipfile.

## Compatibility

uv is designed to be compatible with existing Python packaging standards, so most projects can be migrated with minimal changes.

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/migration/
