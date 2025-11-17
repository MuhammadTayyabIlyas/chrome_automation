#!/usr/bin/env python3
"""
Push All Repositories - Batch Git Push
Reads repos_config.json and pushes all enabled repositories
"""

import sys
import json
import subprocess
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "repos_config.json"
PUSH_SCRIPT = Path(__file__).parent / "universal_git_push.py"


def load_config():
    """Load repository configuration"""
    if not CONFIG_FILE.exists():
        print(f"Error: Config file not found: {CONFIG_FILE}")
        return None

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        return None


def push_repository(repo):
    """Push a single repository"""
    print("\n" + "=" * 70)
    print(f"📦 Processing: {repo['name']}")
    print("=" * 70)

    folder = Path(repo['folder'])
    remote = repo['remote']

    if not folder.exists():
        print(f"❌ Folder does not exist: {folder}")
        return False

    # Run universal push script
    cmd = [sys.executable, str(PUSH_SCRIPT), str(folder), remote]
    result = subprocess.run(cmd)

    return result.returncode == 0


def main():
    """Main entry point"""
    print("🚀 Push All Repositories - Batch Git Push")
    print("=" * 70)

    config = load_config()
    if not config:
        return 1

    repos = [r for r in config.get('repositories', []) if r.get('enabled', True)]

    if not repos:
        print("No enabled repositories found in config")
        return 1

    print(f"Found {len(repos)} enabled repository(ies)\n")

    results = {}
    for repo in repos:
        success = push_repository(repo)
        results[repo['name']] = success

    # Summary
    print("\n" + "=" * 70)
    print("📊 Summary")
    print("=" * 70)

    for name, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {name}")

    successful = sum(1 for s in results.values() if s)
    total = len(results)

    print(f"\nCompleted: {successful}/{total} repositories")

    return 0 if successful == total else 1


if __name__ == "__main__":
    sys.exit(main())
