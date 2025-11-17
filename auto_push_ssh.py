#!/usr/bin/env python3
"""
Auto-Push Agent for Git Repository (SSH-based)
Automatically commits and pushes changes using SSH authentication
No credentials needed - uses your existing SSH keys
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path
import socket

# Configuration
REPO_PATH = Path("/home/tayyabcheema777/ali")
LOG_FILE = REPO_PATH / "auto_push_ssh.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
SSH_KEY_PATH = Path.home() / ".ssh" / "id_ed25519"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def rotate_log():
    """Rotate log file if it exceeds max size"""
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > MAX_LOG_SIZE:
        old_log = LOG_FILE.with_suffix('.log.old')
        LOG_FILE.rename(old_log)
        logger.info("Log rotated due to size")


def run_command(cmd, cwd=None, check=True, timeout=300, env=None):
    """Run a shell command and return output"""
    try:
        # Use existing environment and add SSH agent socket if available
        cmd_env = os.environ.copy()
        if env:
            cmd_env.update(env)

        # Ensure SSH key is used
        cmd_env['GIT_SSH_COMMAND'] = f'ssh -i {SSH_KEY_PATH} -o StrictHostKeyChecking=no'

        result = subprocess.run(
            cmd,
            cwd=cwd or REPO_PATH,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout,
            env=cmd_env
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip(), e.stderr.strip()
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {' '.join(cmd)}")
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_ssh_key():
    """Check if SSH key exists"""
    if not SSH_KEY_PATH.exists():
        logger.error(f"SSH key not found: {SSH_KEY_PATH}")
        logger.error("Please set up SSH keys first")
        return False

    # Check key permissions
    stat = SSH_KEY_PATH.stat()
    if stat.st_mode & 0o077:
        logger.warning(f"SSH key has insecure permissions: {oct(stat.st_mode)}")
        logger.info("Fixing SSH key permissions...")
        SSH_KEY_PATH.chmod(0o600)

    return True


def test_github_connection():
    """Test SSH connection to GitHub"""
    logger.info("Testing SSH connection to GitHub...")
    success, stdout, stderr = run_command(['ssh', '-T', 'git@github.com'], check=False, timeout=10)

    # GitHub returns exit code 1 but with success message
    if 'successfully authenticated' in stderr.lower():
        logger.info("✓ SSH connection to GitHub verified")
        return True
    elif 'permission denied' in stderr.lower():
        logger.error("✗ SSH authentication failed - check your SSH keys")
        logger.error("Your SSH key may not be added to GitHub")
        logger.error("Go to: https://github.com/settings/keys")
        return False
    else:
        logger.warning(f"Unexpected response: {stderr}")
        return False


def check_git_repo():
    """Check if the directory is a git repository"""
    success, _, _ = run_command(['git', 'rev-parse', '--git-dir'], check=False)
    if not success:
        logger.error(f"Not a git repository: {REPO_PATH}")
        return False
    return True


def check_internet():
    """Check if there's internet connectivity"""
    try:
        socket.create_connection(("github.com", 22), timeout=5)
        return True
    except OSError:
        logger.warning("No internet connection detected")
        return False


def get_git_status():
    """Get git status information"""
    success, output, _ = run_command(['git', 'status', '--porcelain'])
    if not success:
        return None
    return output


def count_changes():
    """Count different types of changes"""
    success, output, _ = run_command(['git', 'status', '--porcelain'])
    if not success:
        return 0, 0, 0, 0

    new_files = 0
    modified_files = 0
    deleted_files = 0

    for line in output.split('\n'):
        if not line:
            continue
        status = line[:2]
        if '?' in status:
            new_files += 1
        elif 'M' in status:
            modified_files += 1
        elif 'D' in status:
            deleted_files += 1

    total = new_files + modified_files + deleted_files
    return new_files, modified_files, deleted_files, total


def generate_commit_message():
    """Generate an informative commit message based on changes"""
    new, modified, deleted, total = count_changes()

    if total == 0:
        return "Auto-update: minor changes"

    parts = []
    if new > 0:
        parts.append(f"{new} new")
    if modified > 0:
        parts.append(f"{modified} modified")
    if deleted > 0:
        parts.append(f"{deleted} deleted")

    message = f"Auto-update: {', '.join(parts)} file(s)"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"{message}\n\nTimestamp: {timestamp}\n🤖 Generated with Auto-Push Agent"


def get_changed_files_summary():
    """Get a summary of changed files for logging"""
    success, output, _ = run_command(['git', 'status', '--short'])
    if success and output:
        lines = output.split('\n')[:10]  # Show first 10 files
        summary = '\n'.join(lines)
        if len(output.split('\n')) > 10:
            summary += f"\n... and {len(output.split('\n')) - 10} more files"
        return summary
    return "No changes"


def perform_git_operations():
    """Perform git add, commit, pull, and push operations"""
    try:
        # Check for changes
        status = get_git_status()
        if not status:
            logger.info("No changes to commit")
            return True

        logger.info("Changes detected:")
        logger.info(f"\n{get_changed_files_summary()}")

        # Add all changes (respecting .gitignore)
        logger.info("Staging changes...")
        success, _, stderr = run_command(['git', 'add', '-A'])
        if not success:
            logger.error(f"Failed to stage changes: {stderr}")
            return False

        # Generate commit message
        commit_msg = generate_commit_message()
        logger.info(f"Commit message: {commit_msg.split(chr(10))[0]}")

        # Commit changes
        logger.info("Creating commit...")
        success, stdout, stderr = run_command(['git', 'commit', '-m', commit_msg], check=False)
        if not success:
            if 'nothing to commit' in stderr.lower():
                logger.info("Nothing to commit (working tree clean)")
                return True
            logger.error(f"Commit failed: {stderr}")
            return False

        logger.info(f"✓ Commit created successfully")

        # Check internet before pushing
        if not check_internet():
            logger.warning("Cannot push: no internet connection")
            logger.info("Changes are committed locally and will be pushed when internet is available")
            return False

        # Check if we have unpushed commits
        success, output, _ = run_command(['git', 'rev-list', '@{u}..HEAD', '--count'], check=False)
        if success and output.isdigit():
            unpushed = int(output)
            if unpushed > 0:
                logger.info(f"Found {unpushed} unpushed commit(s)")

        # Pull with rebase to avoid merge conflicts
        logger.info("Pulling latest changes with rebase...")
        success, stdout, stderr = run_command(
            ['git', 'pull', '--rebase', 'origin', 'master'],
            check=False,
            timeout=60
        )

        if not success:
            logger.error(f"Pull with rebase failed: {stderr}")
            # Abort rebase
            run_command(['git', 'rebase', '--abort'], check=False)
            return False

        if 'up to date' not in stdout.lower() and stdout:
            logger.info(f"Pull result: {stdout}")

        # Push changes
        logger.info("Pushing to remote repository via SSH...")
        success, stdout, stderr = run_command(['git', 'push', 'origin', 'master'], timeout=60)

        if not success:
            logger.error(f"Push failed: {stderr}")
            return False

        logger.info("✓ Successfully pushed to remote repository")
        if stdout:
            logger.info(f"Push result: {stdout}")

        return True

    except Exception as e:
        logger.error(f"Unexpected error during git operations: {e}", exc_info=True)
        return False


def main():
    """Main execution function"""
    rotate_log()
    logger.info("=" * 70)
    logger.info("🚀 Auto-Push Agent Started (SSH Mode)")
    logger.info("=" * 70)

    # Change to repository directory
    os.chdir(REPO_PATH)

    # Check SSH key
    if not check_ssh_key():
        logger.error("SSH key check failed")
        return 1

    # Check if it's a git repository
    if not check_git_repo():
        logger.error("Not a valid git repository")
        return 1

    # Test GitHub connection
    if not test_github_connection():
        logger.error("GitHub SSH connection failed")
        return 1

    # Perform git operations
    success = perform_git_operations()

    logger.info("=" * 70)
    if success:
        logger.info("✓ Auto-Push Agent Completed Successfully")
    else:
        logger.warning("⚠ Auto-Push Agent Completed with Warnings/Errors")
    logger.info("=" * 70)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
