# /checkin

Unlock a file after editing in the multi-agent environment.

## Usage

```
/checkin <filepath>
```

## Example

```
/checkin context/sessions/2026-01-22.md
```

## Behavior

1. Read the target file
2. Check frontmatter `status` field
3. If `status: available`:
   - Warn that file wasn't checked out
   - Proceed anyway (idempotent)
4. If `status: editing`:
   - Update frontmatter:
     - `locked_by: null`
     - `locked_at: null`
     - `status: available`
     - `last_edited_by: <current agent-id>`
     - `last_edited_at: <current ISO-8601>`
   - Prepend to `edit_history`:
     - `agent: <agent-id>`
     - `action: checkin`
     - `at: <current ISO-8601>`
   - Write the file
   - Report success

## Output

**Success:**
```
Checked in: context/sessions/2026-01-22.md
Released by: wsl-a1b2c3
Edit duration: 12m 34s
```

**Warning:**
```
Warning: context/sessions/2026-01-22.md was not checked out
Marking as available anyway.
```

## Implementation

```python
import datetime
import yaml

def checkin(filepath: str, agent_id: str) -> dict:
    """Unlock a file after editing."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse frontmatter
    if content.startswith('---'):
        _, fm, body = content.split('---', 2)
        frontmatter = yaml.safe_load(fm)
    else:
        raise ValueError("File missing frontmatter")

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    was_locked = frontmatter.get('status') == 'editing'
    locked_at = frontmatter.get('locked_at')

    # Calculate duration if was locked
    duration = None
    if was_locked and locked_at:
        start = datetime.datetime.fromisoformat(locked_at.replace('Z', '+00:00'))
        end = datetime.datetime.now(datetime.timezone.utc)
        duration = end - start

    # Update frontmatter
    frontmatter['locked_by'] = None
    frontmatter['locked_at'] = None
    frontmatter['status'] = 'available'
    frontmatter['last_edited_by'] = agent_id
    frontmatter['last_edited_at'] = now

    history = frontmatter.get('edit_history', [])
    history.insert(0, {'agent': agent_id, 'action': 'checkin', 'at': now})
    frontmatter['edit_history'] = history[:20]

    # Write back
    new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---{body}"
    with open(filepath, 'w') as f:
        f.write(new_content)

    return {
        'success': True,
        'was_locked': was_locked,
        'duration': str(duration) if duration else None
    }
```

## Commit Message

After checkin, commit with:
```
context: update <filename> - <brief summary>
```
