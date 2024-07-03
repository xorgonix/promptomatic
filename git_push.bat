@echo off
REM Set your repository directory
SET REPO_DIR=C:\path\to\your\repository

REM Navigate to the repository directory
cd /d %REPO_DIR%

REM Pull the latest changes from GitHub
git pull origin main

REM Add all changes to staging
git add .

REM Commit the changes with a message
git commit -m "Auto-commit from batch script"

REM Push the changes to GitHub
git push origin main

REM Notify user of completion
echo Repository sync complete!
pause
