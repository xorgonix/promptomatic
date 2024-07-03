#!/bin/bash

# Set your repository directory
REPO_DIR="/path/to/your/repository"

# Navigate to the repository directory
cd "$REPO_DIR"

# Pull the latest changes from GitHub
git pull origin main

# Notify user of completion
echo "Repository sync complete!"
