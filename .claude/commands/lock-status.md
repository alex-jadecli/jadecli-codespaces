# /lock-status

Show the lock status of all context files.

## Usage

```
/lock-status
```

## Behavior

1. Scan all files in `context/` directory recursively
2. Parse frontmatter from each `.md` file
3. Display table of lock statuses
4. Highlight any stale locks (> 1 hour)

## Output

```
File Lock Status
================

| File | Status | Locked By | Since | Duration |
|------|--------|-----------|-------|----------|
| context/sessions/2026-01-22.md | editing | wsl-a1b2c3 | 15:30 | 12m |
| context/sessions/2026-01-21.md | available | - | - | - |
| context/decisions/001-wsl-setup.md | available | - | - | - |
| context/knowledge/patterns.md | editing | codespace-x4y5z6 | 14:00 | 1h 42m |

Stale Locks (> 1 hour):
- context/knowledge/patterns.md locked by codespace-x4y5z6 for 1h 42m
  Consider: /force-unlock context/knowledge/patterns.md

Summary: 2 locked, 2 available, 1 stale
```

## Implementation

```python
import datetime
import os
import yaml
from pathlib import Path

def lock_status() -> dict:
    """Get lock status of all context files."""
    context_dir = Path('context')
    files = list(context_dir.rglob('*.md'))

    results = []
    stale = []
    now = datetime.datetime.now(datetime.timezone.utc)

    for filepath in files:
        with open(filepath, 'r') as f:
            content = f.read()

        if not content.startswith('---'):
            continue

        _, fm, _ = content.split('---', 2)
        frontmatter = yaml.safe_load(fm)

        status = frontmatter.get('status', 'unknown')
        locked_by = frontmatter.get('locked_by')
        locked_at = frontmatter.get('locked_at')

        duration = None
        is_stale = False

        if locked_at:
            start = datetime.datetime.fromisoformat(locked_at.replace('Z', '+00:00'))
            duration = now - start
            is_stale = duration > datetime.timedelta(hours=1)

        results.append({
            'file': str(filepath),
            'status': status,
            'locked_by': locked_by,
            'locked_at': locked_at,
            'duration': str(duration).split('.')[0] if duration else None,
            'is_stale': is_stale
        })

        if is_stale:
            stale.append({
                'file': str(filepath),
                'locked_by': locked_by,
                'duration': str(duration).split('.')[0]
            })

    return {
        'files': results,
        'stale': stale,
        'summary': {
            'locked': sum(1 for r in results if r['status'] == 'editing'),
            'available': sum(1 for r in results if r['status'] == 'available'),
            'stale': len(stale)
        }
    }
```
