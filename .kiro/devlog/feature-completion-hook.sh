#!/bin/bash
# Feature Completion Hook
# Automatically captures feature milestones when code is committed
# Should be integrated with your git workflow or CI/CD system
# Usage: ./feature-completion-hook.sh "Feature Name" "feature-branch-name"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVLOG_FILE="$SCRIPT_DIR/DEVLOG.md"

# Color codes
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

FEATURE_NAME="${1:-Feature}"
FEATURE_BRANCH="${2:-$(git branch --show-current 2>/dev/null)}"
CURRENT_DATE=$(date +"%B %d, %Y")

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Feature Completion Milestone${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Get feature branch stats
echo -e "${YELLOW}Analyzing feature completion...${NC}\n"

# Get commits in this feature
MAIN_BRANCH="${MAIN_BRANCH:-main}"
if git rev-parse --verify "$MAIN_BRANCH" >/dev/null 2>&1; then
    COMMITS=$(git log "$MAIN_BRANCH..$FEATURE_BRANCH" --oneline 2>/dev/null | wc -l)
    FILES=$(git diff "$MAIN_BRANCH..$FEATURE_BRANCH" --name-only 2>/dev/null | wc -l)
    STATS=$(git diff "$MAIN_BRANCH..$FEATURE_BRANCH" --numstat 2>/dev/null | \
        awk '{add+=$1; del+=$2} END {print add "," del}' || echo "0,0")
else
    COMMITS=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    FILES="N/A"
    STATS="0,0"
fi

LINES_ADDED=$(echo $STATS | cut -d',' -f1)
LINES_REMOVED=$(echo $STATS | cut -d',' -f2)
LINES_ADDED=${LINES_ADDED:-0}
LINES_REMOVED=${LINES_REMOVED:-0}

# Create milestone entry
cat > /tmp/feature_milestone.txt << EOF

---

### ✨ **Feature Milestone**: $FEATURE_NAME
**Date**: $CURRENT_DATE  
**Branch**: $FEATURE_BRANCH

**Feature Statistics:**
- **Commits**: $COMMITS
- **Files Modified**: $FILES
- **Lines Added**: $LINES_ADDED
- **Lines Removed**: $LINES_REMOVED
- **Net Change**: $((LINES_ADDED - LINES_REMOVED))

**Status**: Feature implementation complete, ready for code review and testing.

*Automatically captured on feature completion*

EOF

echo -e "${GREEN}Feature milestone:${NC}"
echo "  Feature: $FEATURE_NAME"
echo "  Branch: $FEATURE_BRANCH"
echo "  Commits: $COMMITS"
echo "  Files: $FILES"
echo "  Changes: +$LINES_ADDED, -$LINES_REMOVED"

echo -e "\n${YELLOW}Note: This milestone will be included in the end-of-day devlog update.${NC}"
echo -e "${YELLOW}Run './devlog-update.sh' at the end of your work session to consolidate.${NC}\n"

# Store feature info for devlog update to pick up
mkdir -p "$SCRIPT_DIR/.feature-milestones"
echo "$FEATURE_NAME|$FEATURE_BRANCH|$COMMITS|$FILES|$LINES_ADDED|$LINES_REMOVED" >> \
    "$SCRIPT_DIR/.feature-milestones/$(date +%Y-%m-%d).txt"

echo -e "${GREEN}✓ Feature milestone recorded${NC}\n"
