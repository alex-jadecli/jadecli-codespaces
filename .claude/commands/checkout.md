# /checkout

Lock a file for editing in the multi-agent environment.

## Usage

```
/checkout <filepath>
```

## Example

```
/checkout context/sessions/2026-01-22.md
```

## Behavior

1. Read the target file
2. Check frontmatter `status` field
3. If `status: editing`:
   - Report who has the lock (`locked_by`)
   - Report when locked (`locked_at`)
   - FAIL - do not proceed
4. If `status: available`:
   - Generate agent ID: `$(hostname)-$(head -c 3 /dev/urandom | xxd -p)`
   - Update frontmatter:
     - `locked_by: <agent-id>`
     - `locked_at: <current ISO-8601>`
     - `status: editing`
   - Prepend to `edit_history`:
     - `agent: <agent-id>`
     - `action: checkout`
     - `at: <current ISO-8601>`
   - Write the file
   - Report success

## Output

**Success:**
```
Checked out: context/sessions/2026-01-22.md
Locked by: wsl-a1b2c3
Locked at: 2026-01-22T15:30:00Z
```

**Failure:**
```
Cannot checkout: context/sessions/2026-01-22.md
Already locked by: codespace-x4y5z6
Locked at: 2026-01-22T14:00:00Z (1h 30m ago)
```

## Implementation

```python
import datetime
import hashlib
import socket
import yaml

def checkout(filepath: str) -> dict:
    """Lock a file for editing."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse frontmatter
    if content.startswith('---'):
        _, fm, body = content.split('---', 2)
        frontmatter = yaml.safe_load(fm)
    else:
        raise ValueError("File missing frontmatter")

    # Check lock status
    if frontmatter.get('status') == 'editing':
        return {
            'success': False,
            'locked_by': frontmatter['locked_by'],
            'locked_at': frontmatter['locked_at']
        }

    # Generate agent ID
    agent_id = f"{socket.gethostname()}-{hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:6]}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Update frontmatter
    frontmatter['locked_by'] = agent_id
    frontmatter['locked_at'] = now
    frontmatter['status'] = 'editing'

    history = frontmatter.get('edit_history', [])
    history.insert(0, {'agent': agent_id, 'action': 'checkout', 'at': now})
    frontmatter['edit_history'] = history[:20]  # Keep last 20

    # Write back
    new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---{body}"
    with open(filepath, 'w') as f:
        f.write(new_content)

    return {'success': True, 'agent_id': agent_id, 'locked_at': now}
```
