@echo off
REM Set your repository directory
SET REPO_DIR=C:\path\to\your\repository

REM Navigate to the repository directory
cd /d %REPO_DIR%

REM Pull the latest changes from GitHub
git pull origin main

REM Notify user of completion
echo Repository sync complete!
pause
