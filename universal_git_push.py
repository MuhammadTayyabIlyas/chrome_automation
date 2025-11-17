#!/usr/bin/env python3
"""
Universal Git Push Workflow
Automatically push any folder to any GitHub SSH repository
Usage: ./universal_git_push.py <folder_path> <git_ssh_url>
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path
import socket
import json

# Configuration
SSH_KEY_PATH = Path.home() / ".ssh" / "id_ed25519"
LOG_DIR = Path.home() / "ali" / "git_push_logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logging(repo_name):
    """Setup logging for specific repository"""
    log_file = LOG_DIR / f"{repo_name}_push.log"

    # Rotate log if too large
    if log_file.exists() and log_file.stat().st_size > 10 * 1024 * 1024:
        log_file.rename(LOG_DIR / f"{repo_name}_push.log.old")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def run_command(cmd, cwd=None, check=True, timeout=300):
    """Run a shell command and return output"""
    try:
        cmd_env = os.environ.copy()
        cmd_env['GIT_SSH_COMMAND'] = f'ssh -i {SSH_KEY_PATH} -o StrictHostKeyChecking=no'

        result = subprocess.run(
            cmd,
            cwd=cwd,
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
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_ssh_key(logger):
    """Check if SSH key exists and has correct permissions"""
    if not SSH_KEY_PATH.exists():
        logger.error(f"SSH key not found: {SSH_KEY_PATH}")
        return False

    stat = SSH_KEY_PATH.stat()
    if stat.st_mode & 0o077:
        logger.info("Fixing SSH key permissions...")
        SSH_KEY_PATH.chmod(0o600)

    return True


def test_github_connection(logger):
    """Test SSH connection to GitHub"""
    logger.info("Testing SSH connection to GitHub...")
    success, stdout, stderr = run_command(['ssh', '-T', 'git@github.com'], check=False, timeout=10)

    if 'successfully authenticated' in stderr.lower():
        logger.info("✓ SSH connection to GitHub verified")
        return True
    elif 'permission denied' in stderr.lower():
        logger.error("✗ SSH authentication failed")
        return False
    return False


def check_internet(logger):
    """Check if there's internet connectivity"""
    try:
        socket.create_connection(("github.com", 22), timeout=5)
        return True
    except OSError:
        logger.warning("No internet connection detected")
        return False


def init_git_repo(folder_path, git_ssh_url, logger):
    """Initialize git repository if not exists"""
    git_dir = folder_path / ".git"

    if not git_dir.exists():
        logger.info("Initializing new git repository...")
        success, _, stderr = run_command(['git', 'init'], cwd=folder_path)
        if not success:
            logger.error(f"Failed to initialize git: {stderr}")
            return False

        # Set default branch to main
        run_command(['git', 'branch', '-M', 'main'], cwd=folder_path, check=False)

    # Check if remote exists
    success, output, _ = run_command(['git', 'remote', 'get-url', 'origin'], cwd=folder_path, check=False)

    if success and output:
        # Remote exists, check if it matches
        if output != git_ssh_url:
            logger.info(f"Updating remote URL from {output} to {git_ssh_url}")
            run_command(['git', 'remote', 'set-url', 'origin', git_ssh_url], cwd=folder_path)
    else:
        # Add remote
        logger.info(f"Adding remote: {git_ssh_url}")
        success, _, stderr = run_command(['git', 'remote', 'add', 'origin', git_ssh_url], cwd=folder_path)
        if not success:
            logger.error(f"Failed to add remote: {stderr}")
            return False

    return True


def create_gitignore_if_needed(folder_path, logger):
    """Create .gitignore if it doesn't exist"""
    gitignore_path = folder_path / ".gitignore"

    if not gitignore_path.exists():
        logger.info("Creating .gitignore file...")
        default_gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environments
*_venv/
venv/
ENV/
env/

# Logs
*.log

# OS Files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Temporary files
*.tmp
*.temp
*.swp
*.swo
"""
        gitignore_path.write_text(default_gitignore)


def count_changes(folder_path):
    """Count different types of changes"""
    success, output, _ = run_command(['git', 'status', '--porcelain'], cwd=folder_path)
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


def generate_commit_message(folder_path):
    """Generate an informative commit message"""
    new, modified, deleted, total = count_changes(folder_path)

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

    return f"{message}\n\nTimestamp: {timestamp}\n🤖 Universal Git Push Workflow"


def get_default_branch(folder_path, logger):
    """Get the default branch name"""
    # Try to get current branch
    success, branch, _ = run_command(['git', 'branch', '--show-current'], cwd=folder_path, check=False)
    if success and branch:
        return branch

    # Try main
    success, _, _ = run_command(['git', 'show-ref', '--verify', 'refs/heads/main'], cwd=folder_path, check=False)
    if success:
        return 'main'

    # Try master
    success, _, _ = run_command(['git', 'show-ref', '--verify', 'refs/heads/master'], cwd=folder_path, check=False)
    if success:
        return 'master'

    # Default to main
    return 'main'


def push_to_github(folder_path, git_ssh_url, logger):
    """Main function to push folder to GitHub"""

    # Initialize or verify git repository
    if not init_git_repo(folder_path, git_ssh_url, logger):
        return False

    # Create .gitignore if needed
    create_gitignore_if_needed(folder_path, logger)

    # Check for changes
    success, status, _ = run_command(['git', 'status', '--porcelain'], cwd=folder_path)

    if not status:
        logger.info("No changes to commit")
        # Still try to push in case there are unpushed commits
    else:
        logger.info("Changes detected, staging files...")

        # Stage all changes
        success, _, stderr = run_command(['git', 'add', '-A'], cwd=folder_path)
        if not success:
            logger.error(f"Failed to stage changes: {stderr}")
            return False

        # Generate commit message
        commit_msg = generate_commit_message(folder_path)
        logger.info(f"Commit message: {commit_msg.split(chr(10))[0]}")

        # Commit changes
        success, stdout, stderr = run_command(['git', 'commit', '-m', commit_msg], cwd=folder_path, check=False)
        if not success:
            if 'nothing to commit' in stderr.lower():
                logger.info("Nothing to commit (working tree clean)")
            else:
                logger.error(f"Commit failed: {stderr}")
                return False
        else:
            logger.info("✓ Commit created successfully")

    # Check internet
    if not check_internet(logger):
        logger.warning("Cannot push: no internet connection")
        logger.info("Changes are committed locally")
        return False

    # Get default branch
    branch = get_default_branch(folder_path, logger)
    logger.info(f"Using branch: {branch}")

    # Try to pull first (if remote exists)
    logger.info("Pulling latest changes...")
    success, stdout, stderr = run_command(
        ['git', 'pull', '--rebase', 'origin', branch],
        cwd=folder_path,
        check=False,
        timeout=60
    )

    if not success:
        if 'no tracking information' in stderr or 'does not exist' in stderr:
            logger.info("First push to remote")
        else:
            logger.warning(f"Pull failed: {stderr}")

    # Push to GitHub
    logger.info(f"Pushing to {git_ssh_url}...")
    success, stdout, stderr = run_command(
        ['git', 'push', '-u', 'origin', branch],
        cwd=folder_path,
        timeout=60
    )

    if not success:
        logger.error(f"Push failed: {stderr}")
        return False

    logger.info("✓ Successfully pushed to GitHub")
    if stdout:
        logger.info(f"Push result: {stdout}")

    return True


def main():
    """Main entry point"""
    if len(sys.argv) != 3:
        print("Usage: ./universal_git_push.py <folder_path> <git_ssh_url>")
        print("\nExample:")
        print("  ./universal_git_push.py /home/user/myproject git@github.com:username/repo.git")
        return 1

    folder_path = Path(sys.argv[1]).resolve()
    git_ssh_url = sys.argv[2]

    # Validate inputs
    if not folder_path.exists():
        print(f"Error: Folder does not exist: {folder_path}")
        return 1

    if not folder_path.is_dir():
        print(f"Error: Not a directory: {folder_path}")
        return 1

    if not git_ssh_url.startswith('git@github.com:'):
        print(f"Error: Invalid SSH URL format. Must start with 'git@github.com:'")
        return 1

    # Extract repo name for logging
    repo_name = git_ssh_url.split(':')[-1].replace('.git', '').replace('/', '_')
    logger = setup_logging(repo_name)

    logger.info("=" * 70)
    logger.info("🚀 Universal Git Push Workflow Started")
    logger.info(f"Folder: {folder_path}")
    logger.info(f"Remote: {git_ssh_url}")
    logger.info("=" * 70)

    # Check SSH key
    if not check_ssh_key(logger):
        return 1

    # Test GitHub connection
    if not test_github_connection(logger):
        return 1

    # Push to GitHub
    success = push_to_github(folder_path, git_ssh_url, logger)

    logger.info("=" * 70)
    if success:
        logger.info("✓ Workflow Completed Successfully")
    else:
        logger.warning("⚠ Workflow Completed with Warnings/Errors")
    logger.info("=" * 70)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
