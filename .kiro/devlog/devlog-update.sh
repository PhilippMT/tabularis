#!/bin/bash
# Development Log Auto-Update Script
# Automatically captures and summarizes daily development progress
# Usage: ./devlog-update.sh [optional-hours]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVLOG_FILE="$SCRIPT_DIR/DEVLOG.md"
GIT_DIR="$(git rev-parse --git-dir 2>/dev/null || echo '.git')"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Development Log Update System${NC}"
echo -e "${BLUE}========================================${NC}"

# Function to get current date formatted
get_date() {
    date +"%B %d, %Y (%A)"
}

# Function to get hackathon day number
get_hackathon_day() {
    # Hackathon started January 5, 2026
    HACKATHON_START="2026-01-05"
    CURRENT_DATE=$(date +"%Y-%m-%d")
    
    # Calculate days difference
    START_EPOCH=$(date -d "$HACKATHON_START" +%s 2>/dev/null || date -jf "%Y-%m-%d" "$HACKATHON_START" +%s 2>/dev/null)
    CURRENT_EPOCH=$(date -d "$CURRENT_DATE" +%s 2>/dev/null || date -jf "%Y-%m-%d" "$CURRENT_DATE" +%s 2>/dev/null)
    
    if [ ! -z "$START_EPOCH" ] && [ ! -z "$CURRENT_EPOCH" ]; then
        DAYS_DIFF=$(( ($CURRENT_EPOCH - $START_EPOCH) / 86400 ))
        echo $((DAYS_DIFF + 1))
    else
        echo "1"
    fi
}

# Function to gather user information
gather_user_info() {
    echo -e "\n${YELLOW}Please provide information about today's work:${NC}\n"
    
    # Question 1: What did you work on?
    echo -e "${BLUE}1. What did you work on today?${NC} (Features, bugs, refactoring, etc.)"
    read -p "   Answer: " WORK_FOCUS
    
    # Question 2: Time spent
    echo -e "\n${BLUE}2. How much time did you spend?${NC} (Total hours)"
    read -p "   Hours: " HOURS_SPENT
    HOURS_SPENT=${HOURS_SPENT:-0}
    
    # Question 3: Main accomplishments
    echo -e "\n${BLUE}3. What were your main accomplishments?${NC} (Brief summary)"
    read -p "   Answer: " ACCOMPLISHMENTS
    
    # Question 4: Challenges
    echo -e "\n${BLUE}4. Any challenges or blockers?${NC} (Optional - press Enter to skip)"
    read -p "   Answer: " CHALLENGES
    
    # Question 5: Key decisions
    echo -e "\n${BLUE}5. Key technical decisions made?${NC} (Optional - press Enter to skip)"
    read -p "   Answer: " DECISIONS
    
    # Question 6: Next steps
    echo -e "\n${BLUE}6. What's planned for the next session?${NC}"
    read -p "   Answer: " NEXT_STEPS
    
    # Question 7: Learnings
    echo -e "\n${BLUE}7. Any new learnings or insights?${NC} (Optional - press Enter to skip)"
    read -p "   Answer: " LEARNINGS
    
    # Question 8: Kiro usage
    echo -e "\n${BLUE}8. Which Kiro prompts were most helpful?${NC} (Optional - press Enter to skip)"
    read -p "   Answer: " KIRO_USAGE
}

# Function to analyze git activity
analyze_git_activity() {
    echo -e "\n${YELLOW}Analyzing git activity...${NC}"
    
    # Check if git repo exists
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${YELLOW}  Note: Not in a git repository - skipping git analysis${NC}"
        return
    fi
    
    # Get today's date range
    TODAY_START=$(date +"%Y-%m-%d")
    TODAY_END=$(date +"%Y-%m-%d" -d "tomorrow" 2>/dev/null || date -v+1d +"%Y-%m-%d")
    
    # Get commits for today
    echo -e "\n${BLUE}Today's Commits:${NC}"
    COMMITS=$(git log --since="$TODAY_START" --until="$TODAY_END" --oneline 2>/dev/null | wc -l)
    echo "  Total commits: $COMMITS"
    
    if [ $COMMITS -gt 0 ]; then
        echo "  Commit messages:"
        git log --since="$TODAY_START" --until="$TODAY_END" --pretty=format:"    - %h: %s" 2>/dev/null || true
    fi
    
    # Get line changes
    echo -e "\n${BLUE}Code Changes:${NC}"
    STATS=$(git log --since="$TODAY_START" --until="$TODAY_END" --pretty=tformat: --numstat 2>/dev/null | \
        awk '{add+=$1; del+=$2} END {print add "," del}')
    
    LINES_ADDED=$(echo $STATS | cut -d',' -f1)
    LINES_REMOVED=$(echo $STATS | cut -d',' -f2)
    LINES_ADDED=${LINES_ADDED:-0}
    LINES_REMOVED=${LINES_REMOVED:-0}
    
    echo "  Lines added: $LINES_ADDED"
    echo "  Lines removed: $LINES_REMOVED"
    echo "  Net change: $((LINES_ADDED - LINES_REMOVED))"
    
    # Files modified
    echo -e "\n${BLUE}Files Modified:${NC}"
    FILES=$(git diff --name-only HEAD~1 HEAD 2>/dev/null | wc -l || echo "N/A")
    echo "  Total files: $FILES"
}

# Function to generate devlog entry
generate_entry() {
    local DAY=$(get_hackathon_day)
    local DATE=$(get_date)
    
    echo -e "\n${YELLOW}Generating devlog entry...${NC}"
    
    cat > /tmp/devlog_entry.txt << EOF
## Day $DAY ($DATE) - $WORK_FOCUS [$HOURS_SPENT h]

### 📊 **Daily Metrics**
- **Time Spent**: ${HOURS_SPENT} hours
- **Commits Made**: $COMMITS
- **Lines Added**: $LINES_ADDED
- **Lines Removed**: $LINES_REMOVED
- **Net Lines**: $((LINES_ADDED - LINES_REMOVED))

### 🎯 **Accomplishments**
- $ACCOMPLISHMENTS

### 💻 **Technical Progress**
**Commits Made Today:**
\`\`\`
$(git log --since="$TODAY_START" --until="$TODAY_END" --oneline 2>/dev/null || echo "No commits today")
\`\`\`

**Code Changes:**
- Files modified: $FILES
- Lines added: $LINES_ADDED
- Lines removed: $LINES_REMOVED
- Net change: $((LINES_ADDED - LINES_REMOVED))

### 🚧 **Challenges & Solutions**
${CHALLENGES:-"No significant challenges today."}

### 🧠 **Key Decisions**
${DECISIONS:-"No major architectural decisions made today."}

### 📚 **Learnings & Insights**
${LEARNINGS:-"Continued building on existing knowledge."}

### ⚡ **Kiro CLI Usage**
${KIRO_USAGE:-"Standard prompt usage during development."}

### 📋 **Next Session Plan**
- $NEXT_STEPS

---

EOF
    
    echo -e "${GREEN}Entry generated successfully${NC}"
}

# Function to append entry to devlog
append_entry() {
    echo -e "\n${YELLOW}Appending entry to devlog...${NC}"
    
    # Read the current devlog
    local TEMP_FILE="/tmp/devlog_temp.md"
    
    # Create new devlog with entry inserted after the "Daily Development Entries" line
    awk '
        /^## Daily Development Entries/ {
            print $0
            print ""
            while ((getline line < "/tmp/devlog_entry.txt") > 0) {
                print line
            }
            close("/tmp/devlog_entry.txt")
            next
        }
        { print }
    ' "$DEVLOG_FILE" > "$TEMP_FILE"
    
    mv "$TEMP_FILE" "$DEVLOG_FILE"
    echo -e "${GREEN}Entry appended to $DEVLOG_FILE${NC}"
}

# Function to update statistics
update_statistics() {
    echo -e "\n${YELLOW}Updating development statistics...${NC}"
    
    # Count day entries (## Day X entries)
    TOTAL_DAYS=$(grep -c "^## Day [0-9]" "$DEVLOG_FILE" || echo "1")
    
    # Parse total hours from all entries
    TOTAL_HOURS=$(grep "Time Spent" "$DEVLOG_FILE" | grep -oE "[0-9]+(\.[0-9]+)?" | \
        awk '{sum+=$1} END {print sum}' || echo "0")
    
    # Get total commits from git
    TOTAL_COMMITS=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    
    # Get cumulative line changes
    CUMULATIVE_STATS=$(git log --pretty=tformat: --numstat 2>/dev/null | \
        awk '{add+=$1; del+=$2} END {print add "," del}' || echo "0,0")
    
    TOTAL_ADDED=$(echo $CUMULATIVE_STATS | cut -d',' -f1)
    TOTAL_REMOVED=$(echo $CUMULATIVE_STATS | cut -d',' -f2)
    
    # Update statistics in devlog
    sed -i.bak "
        s/\*\*Total Development Days\*\*: [0-9]*/\*\*Total Development Days\*\*: $TOTAL_DAYS/
        s/\*\*Total Hours Logged\*\*: [0-9.]*h/\*\*Total Hours Logged\*\*: ${TOTAL_HOURS}h/
        s/\*\*Total Commits\*\*: [0-9]*/\*\*Total Commits\*\*: $TOTAL_COMMITS/
        s/\*\*Lines of Code Added\*\*: [0-9]*/\*\*Lines of Code Added\*\*: $TOTAL_ADDED/
        s/\*\*Lines of Code Removed\*\*: [0-9]*/\*\*Lines of Code Removed\*\*: $TOTAL_REMOVED/
    " "$DEVLOG_FILE"
    
    rm -f "$DEVLOG_FILE.bak"
    
    echo -e "${GREEN}Statistics updated:${NC}"
    echo "  Total days: $TOTAL_DAYS"
    echo "  Total hours: ${TOTAL_HOURS}h"
    echo "  Total commits: $TOTAL_COMMITS"
    echo "  Lines added: $TOTAL_ADDED"
    echo "  Lines removed: $TOTAL_REMOVED"
}

# Main execution
main() {
    # Gather user information
    gather_user_info
    
    # Analyze git activity
    analyze_git_activity
    
    # Generate and append entry
    generate_entry
    append_entry
    
    # Update statistics
    update_statistics
    
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}Development log updated successfully!${NC}"
    echo -e "${GREEN}========================================${NC}\n"
    
    # Show summary
    echo -e "${BLUE}📊 Today's Summary:${NC}"
    echo "  Focus: $WORK_FOCUS"
    echo "  Time: ${HOURS_SPENT}h"
    echo "  Commits: $COMMITS"
    echo "  Code changes: +$LINES_ADDED, -$LINES_REMOVED"
}

# Run main function
main
