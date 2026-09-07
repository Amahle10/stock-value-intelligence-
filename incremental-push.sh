#!/usr/bin/env bash

set -euo pipefail

BATCH_SIZE=200
REMOTE="origin"
REMOTE_BRANCH="main"
TEMP_BRANCH="incremental-main"

echo "======================================"
echo " Incremental Git Push"
echo "======================================"

# Verify repository
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
    echo "ERROR: Not inside a Git repository."
    exit 1
}

# Verify remote
git remote get-url "$REMOTE" >/dev/null 2>&1 || {
    echo "ERROR: Remote '$REMOTE' does not exist."
    exit 1
}

echo
echo "Remote:"
git remote get-url "$REMOTE"

echo
echo "Current branch:"
CURRENT_BRANCH="$(git branch --show-current)"
echo "$CURRENT_BRANCH"

echo
echo "Checking ignored heavy directories..."

if git ls-files | grep -qE '(^|/)(node_modules|\.venv)/'; then
    echo "ERROR: node_modules or .venv are still tracked."
    echo "Fix .gitignore before continuing."
    exit 1
fi

echo
echo "Checking for files larger than 50 MB..."

find . \
    -type f \
    -not -path "./.git/*" \
    -not -path "./.venv/*" \
    -not -path "*/node_modules/*" \
    -size +50M \
    -print

# ------------------------------------------------
# Create orphan branch only if we haven't already
# ------------------------------------------------

if [ "$CURRENT_BRANCH" = "$TEMP_BRANCH" ]; then
    echo
    echo "Already on $TEMP_BRANCH."
    echo "Continuing existing incremental migration."
else
    echo
    echo "Creating clean incremental branch..."

    git checkout --orphan "$TEMP_BRANCH"

    # Remove old tracked index without deleting files
    git rm -rf --cached . >/dev/null 2>&1 || true
fi

echo
echo "Collecting non-ignored project files..."

mapfile -d '' FILES < <(
    git ls-files \
        --others \
        --exclude-standard \
        -z
)

TOTAL=${#FILES[@]}

if [ "$TOTAL" -eq 0 ]; then
    echo "No untracked files available to commit."
    exit 0
fi

echo
echo "Total files: $TOTAL"
echo "Batch size: $BATCH_SIZE"

START=0
BATCH=1

while [ "$START" -lt "$TOTAL" ]; do

    END=$((START + BATCH_SIZE))

    if [ "$END" -gt "$TOTAL" ]; then
        END=$TOTAL
    fi

    COUNT=$((END - START))

    echo
    echo "======================================"
    echo " Batch $BATCH"
    echo " Files $((START + 1)) - $END of $TOTAL"
    echo "======================================"

    CURRENT_FILES=(
        "${FILES[@]:START:COUNT}"
    )

    git add -- "${CURRENT_FILES[@]}"

    echo
    echo "Staged:"
    git diff --cached --stat

    git commit -m "chore: import project batch $BATCH"

    echo
    echo "Pushing batch $BATCH..."

    git push "$REMOTE" HEAD:"$REMOTE_BRANCH"

    echo
    echo "✓ Batch $BATCH pushed successfully."

    START=$END
    BATCH=$((BATCH + 1))
done

echo
echo "======================================"
echo " All project batches pushed"
echo "======================================"

git branch -M "$REMOTE_BRANCH"

echo
echo "Current branch:"
git branch --show-current

echo
echo "Repository status:"
git status

echo
echo "Recent commits:"
git log --oneline -10

echo
echo "Done."
