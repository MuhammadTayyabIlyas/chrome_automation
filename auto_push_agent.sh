#!/bin/bash

###############################################################################
# Auto-Push Agent for Git Repository
# This script automatically commits and pushes changes to the remote repository
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_PATH="/home/tayyabcheema777/ali"
LOG_FILE="$REPO_PATH/auto_push_agent.log"
MAX_LOG_SIZE=10485760  # 10MB

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ${message}" >> "$LOG_FILE"
}

# Function to rotate log if too large
rotate_log() {
    if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE") -gt $MAX_LOG_SIZE ]; then
        mv "$LOG_FILE" "${LOG_FILE}.old"
        print_message "$BLUE" "Log rotated due to size"
    fi
}

# Function to check if we're in a git repository
check_git_repo() {
    if ! git -C "$REPO_PATH" rev-parse --git-dir > /dev/null 2>&1; then
        print_message "$RED" "ERROR: Not a git repository: $REPO_PATH"
        exit 1
    fi
}

# Function to check internet connectivity
check_internet() {
    if ! ping -c 1 github.com > /dev/null 2>&1; then
        print_message "$YELLOW" "WARNING: No internet connection. Will retry later."
        return 1
    fi
    return 0
}

# Function to generate commit message
generate_commit_message() {
    local deleted_files=$(git -C "$REPO_PATH" diff --name-only --diff-filter=D | wc -l)
    local modified_files=$(git -C "$REPO_PATH" diff --name-only --diff-filter=M | wc -l)
    local new_files=$(git -C "$REPO_PATH" ls-files --others --exclude-standard | wc -l)

    local message="Auto-update: "
    local parts=()

    [ $new_files -gt 0 ] && parts+=("$new_files new")
    [ $modified_files -gt 0 ] && parts+=("$modified_files modified")
    [ $deleted_files -gt 0 ] && parts+=("$deleted_files deleted")

    if [ ${#parts[@]} -eq 0 ]; then
        message="Auto-update: minor changes"
    else
        message="${message}$(IFS=', '; echo "${parts[*]}") file(s)"
    fi

    echo "$message"
}

# Function to perform git operations
perform_git_operations() {
    cd "$REPO_PATH"

    # Check for changes
    if git diff-index --quiet HEAD -- && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        print_message "$BLUE" "No changes to commit"
        return 0
    fi

    print_message "$BLUE" "Changes detected, starting git operations..."

    # Add all changes (respecting .gitignore)
    print_message "$BLUE" "Staging changes..."
    git add -A

    # Generate commit message
    local commit_msg=$(generate_commit_message)
    print_message "$BLUE" "Commit message: $commit_msg"

    # Commit changes
    print_message "$BLUE" "Creating commit..."
    git commit -m "$commit_msg" || {
        print_message "$YELLOW" "Nothing to commit or commit failed"
        return 0
    }

    # Check internet before pushing
    if ! check_internet; then
        print_message "$YELLOW" "Cannot push: no internet connection"
        return 1
    fi

    # Pull with rebase to avoid merge conflicts
    print_message "$BLUE" "Pulling latest changes with rebase..."
    if ! git pull --rebase origin master; then
        print_message "$RED" "ERROR: Pull with rebase failed. Manual intervention required."
        git rebase --abort 2>/dev/null || true
        return 1
    fi

    # Push changes
    print_message "$BLUE" "Pushing to remote repository..."
    if git push origin master; then
        print_message "$GREEN" "✓ Successfully pushed to remote repository"
        return 0
    else
        print_message "$RED" "ERROR: Push failed"
        return 1
    fi
}

# Main execution
main() {
    rotate_log
    print_message "$GREEN" "=== Auto-Push Agent Started ==="

    check_git_repo

    if perform_git_operations; then
        print_message "$GREEN" "=== Auto-Push Agent Completed Successfully ==="
        exit 0
    else
        print_message "$YELLOW" "=== Auto-Push Agent Completed with Warnings ==="
        exit 1
    fi
}

# Run main function
main "$@"
