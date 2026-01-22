#!/usr/bin/env bash
# Post-edit hook: Log edits to context files
# This hook runs after Edit tool completes

set -euo pipefail

# Get the file that was edited from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.input.file_path // empty')

# Only log context file edits
if [[ ! "$FILE_PATH" =~ ^context/ ]]; then
    exit 0
fi

# Log to a file for debugging/auditing
LOG_FILE=".claude/edit-log.txt"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
AGENT_ID="${HOSTNAME:-unknown}-$$"

echo "$TIMESTAMP | $AGENT_ID | edited | $FILE_PATH" >> "$LOG_FILE"

exit 0
