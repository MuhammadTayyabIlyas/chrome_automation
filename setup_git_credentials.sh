#!/bin/bash

###############################################################################
# Git Credential Helper Setup Script
# This script helps you configure secure credential storage for Git
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}=== Git Credential Helper Setup ===${NC}\n"

# Check if running on WSL
if grep -qi microsoft /proc/version; then
    echo -e "${BLUE}Detected WSL environment${NC}"
    WSL=true
else
    WSL=false
fi

echo -e "${YELLOW}Available credential helper options:${NC}"
echo "1. cache - Store credentials in memory for 15 minutes (default: secure, temporary)"
echo "2. store - Store credentials in plain text file (less secure, permanent)"
echo "3. libsecret - Use GNOME Keyring (most secure for Linux, requires setup)"
if [ "$WSL" = true ]; then
    echo "4. wincred - Use Windows Credential Manager (recommended for WSL)"
fi
echo ""

read -p "Select option (1-4): " option

case $option in
    1)
        echo -e "\n${BLUE}Setting up cache credential helper...${NC}"
        git config --global credential.helper 'cache --timeout=3600'
        echo -e "${GREEN}✓ Credential helper set to cache (1 hour timeout)${NC}"
        echo -e "${YELLOW}Note: You'll need to enter credentials once, then they'll be cached for 1 hour${NC}"
        ;;
    2)
        echo -e "\n${YELLOW}WARNING: This stores credentials in plain text!${NC}"
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            git config --global credential.helper store
            echo -e "${GREEN}✓ Credential helper set to store${NC}"
            echo -e "${YELLOW}Credentials will be stored in ~/.git-credentials${NC}"
        else
            echo -e "${RED}Cancelled${NC}"
            exit 1
        fi
        ;;
    3)
        echo -e "\n${BLUE}Setting up libsecret credential helper...${NC}"

        # Check if libsecret is available
        if ! dpkg -l | grep -q libsecret-1-dev; then
            echo -e "${YELLOW}Installing required packages...${NC}"
            sudo apt-get update
            sudo apt-get install -y libsecret-1-0 libsecret-1-dev
        fi

        # Build the credential helper
        if [ ! -f "/usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret" ]; then
            echo -e "${YELLOW}Building libsecret credential helper...${NC}"
            cd /usr/share/doc/git/contrib/credential/libsecret
            sudo make
        fi

        git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
        echo -e "${GREEN}✓ Credential helper set to libsecret${NC}"
        ;;
    4)
        if [ "$WSL" = true ]; then
            echo -e "\n${BLUE}Setting up Windows Credential Manager...${NC}"
            git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager-core.exe"
            echo -e "${GREEN}✓ Credential helper set to Windows Credential Manager${NC}"
        else
            echo -e "${RED}This option is only available on WSL${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}=== Configuration Summary ===${NC}"
git config --global --list | grep credential

echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Run the auto-push agent: ./auto_push_agent.py"
echo "2. On first run, you'll be prompted for your GitHub credentials"
echo "3. Future runs will use the stored credentials automatically"

echo -e "\n${YELLOW}For GitHub, you'll need a Personal Access Token (not password):${NC}"
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Give it a name and select 'repo' scope"
echo "4. Copy the token and use it as your password when prompted"

echo -e "\n${GREEN}Setup complete!${NC}"
