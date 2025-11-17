# Auto-Push Agent Setup Guide

This guide will help you set up automatic Git pushing with secure credential storage.

## Quick Start

### Step 1: Set Up Credential Helper

Run the setup script to configure secure credential storage:

```bash
cd /home/tayyabcheema777/ali
./setup_git_credentials.sh
```

**Recommended options:**
- **WSL users**: Option 4 (Windows Credential Manager)
- **Linux users**: Option 3 (libsecret/GNOME Keyring) or Option 1 (cache)
- **Quick testing**: Option 1 (cache - stores for 1 hour)

### Step 2: Get GitHub Personal Access Token

Since you're using HTTPS or need credentials, you'll need a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a descriptive name (e.g., "Auto-Push Agent")
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

### Step 3: Run the Auto-Push Agent

```bash
cd /home/tayyabcheema777/ali
./auto_push_agent.py
```

**On first run**, you'll be prompted for:
- **Username**: Your GitHub username
- **Password**: Paste your Personal Access Token (not your GitHub password!)

The credentials will be securely stored and used automatically in future runs.

## Usage

### Manual Push
Run the agent anytime to commit and push all changes:
```bash
./auto_push_agent.py
```

### Automated Scheduled Pushes

#### Option A: Using Cron (Linux/WSL)
Set up automatic pushes every hour:
```bash
# Edit crontab
crontab -e

# Add this line to run every hour
0 * * * * cd /home/tayyabcheema777/ali && /usr/bin/python3 auto_push_agent.py >> /home/tayyabcheema777/ali/auto_push_cron.log 2>&1

# Or run every 30 minutes
*/30 * * * * cd /home/tayyabcheema777/ali && /usr/bin/python3 auto_push_agent.py >> /home/tayyabcheema777/ali/auto_push_cron.log 2>&1
```

#### Option B: Using systemd Timer (Linux)
For more reliable scheduling:
```bash
# Create service file
sudo nano /etc/systemd/system/auto-push.service

# Create timer file
sudo nano /etc/systemd/system/auto-push.timer

# Enable and start
sudo systemctl enable auto-push.timer
sudo systemctl start auto-push.timer
```

#### Option C: Manual Watch Script
Create a simple watch script:
```bash
#!/bin/bash
# watch_and_push.sh
while true; do
    cd /home/tayyabcheema777/ali
    ./auto_push_agent.py
    sleep 3600  # Sleep for 1 hour
done
```

## Viewing Logs

Check the agent's activity:
```bash
tail -f /home/tayyabcheema777/ali/auto_push_agent.log
```

## What Gets Pushed?

The agent respects `.gitignore` and will:
- ✅ Add all new files (not in .gitignore)
- ✅ Stage modified files
- ✅ Remove deleted files
- ❌ Skip virtual environments (`*_venv/`)
- ❌ Skip Python cache (`__pycache__/`)
- ❌ Skip log files (`*.log`)

## Troubleshooting

### Problem: Authentication Failed
**Solution**: Run git command manually once:
```bash
cd /home/tayyabcheema777/ali
git pull origin master
# Enter username and token when prompted
```

### Problem: Merge Conflicts
**Solution**: The agent will abort and notify you. Resolve manually:
```bash
git status
# Fix conflicts
git add .
git rebase --continue
./auto_push_agent.py
```

### Problem: No Internet Connection
**Solution**: The agent will commit locally and skip push. Run again when online.

### Problem: "Not a git repository"
**Solution**: Ensure you're in the correct directory:
```bash
cd /home/tayyabcheema777/ali
git status
```

## Security Notes

✅ **DO:**
- Use Personal Access Tokens (not passwords)
- Use credential helpers (cache, store, libsecret, wincred)
- Limit token scope to only what's needed
- Rotate tokens periodically

❌ **DON'T:**
- Share tokens in chat or code
- Use your GitHub password
- Commit credentials to the repository
- Use tokens with excessive permissions

## Files Created

- `setup_git_credentials.sh` - One-time credential setup
- `auto_push_agent.py` - Main auto-push script
- `auto_push_agent.log` - Activity log
- `.gitignore` - Files to ignore
- `AUTO_PUSH_SETUP.md` - This guide

## Advanced Configuration

### Change Commit Message Format
Edit `auto_push_agent.py`, find the `generate_commit_message()` function.

### Change Repository Path
Edit `REPO_PATH` in `auto_push_agent.py`.

### Adjust Log Retention
Edit `MAX_LOG_SIZE` in `auto_push_agent.py`.

## Need Help?

Check the logs:
```bash
tail -50 /home/tayyabcheema777/ali/auto_push_agent.log
```

Test git manually:
```bash
cd /home/tayyabcheema777/ali
git status
git pull origin master
git push origin master
```

## Next Steps

1. ✅ Run `./setup_git_credentials.sh`
2. ✅ Get GitHub Personal Access Token
3. ✅ Run `./auto_push_agent.py` and enter credentials
4. ✅ Set up automated scheduling (optional)
5. ✅ Monitor logs to ensure it works

---

**Repository**: https://github.com/MuhammadTayyabIlyas/chrome_automation
**Branch**: master
