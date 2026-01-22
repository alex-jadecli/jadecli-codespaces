#!/usr/bin/env bash
# Pre-edit hook: Warn if editing a context file without checkout
# This hook runs before Edit tool is used

set -euo pipefail

# Get the file being edited from stdin (JSON format from Claude Code hooks)
# Format: {"tool": "Edit", "input": {"file_path": "...", ...}}
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.input.file_path // empty')

# Only check context files
if [[ ! "$FILE_PATH" =~ ^context/ ]]; then
    exit 0
fi

# Check if file exists and has frontmatter
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Extract status from frontmatter
if head -1 "$FILE_PATH" | grep -q "^---$"; then
    STATUS=$(sed -n '/^---$/,/^---$/p' "$FILE_PATH" | grep "^status:" | cut -d: -f2 | tr -d ' ')
    LOCKED_BY=$(sed -n '/^---$/,/^---$/p' "$FILE_PATH" | grep "^locked_by:" | cut -d: -f2 | tr -d ' ')

    if [[ "$STATUS" == "editing" && "$LOCKED_BY" != "null" ]]; then
        echo "WARNING: File $FILE_PATH is locked by $LOCKED_BY"
        echo "Use /checkout first or verify you have the lock"
        # Don't block, just warn - the rule will enforce proper behavior
    fi
fi

exit 0
