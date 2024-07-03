#!/bin/bash

# Set your repository directory
#REPO_DIR="/path/to/your/repository"

# Navigate to the repository directory
#cd "$REPO_DIR"

# Pull the latest changes from GitHub
git pull origin main

# Add all changes to staging
git add .

# Commit the changes with a message
git commit -m "Auto-commit from shell script"

# Push the changes to GitHub
git push origin main

# Notify user of completion
echo "Repository sync complete!"
