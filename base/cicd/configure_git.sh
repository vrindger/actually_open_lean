# configure_git.sh
#!/bin/bash

# Set GitHub username and PAT
GITHUB_USERNAME=$1
GITHUB_PAT=$2

# Configure Git to use the credentials
git config --global credential.helper store
echo "https://${GITHUB_USERNAME}:${GITHUB_PAT}@github.com" > ~/.git-credentials