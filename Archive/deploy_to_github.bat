@echo off
REM 🚀 GitHub Deployment Script for Map Route Extractor (Windows)
REM This script helps you deploy your project to GitHub

echo 🧭 Map Route Extractor - GitHub Deployment Script
echo ==================================================

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

echo ✅ Git is installed

REM Check if we're in the right directory
if not exist "launch_app.py" (
    echo ❌ This script must be run from the MapRouteExtractor directory
    pause
    exit /b 1
)

echo ✅ In correct directory

REM Initialize git repository if not already initialized
if not exist ".git" (
    echo ℹ️  Initializing Git repository...
    git init
    echo ✅ Git repository initialized
) else (
    echo ℹ️  Git repository already exists
)

REM Add all files to git
echo ℹ️  Adding files to Git...
git add .

REM Commit changes
echo ℹ️  Committing changes...
git commit -m "Initial commit: Map Route Extractor v2.0 - Enhanced Features

🎯 New Features:
- Smart source/destination labeling
- Compass integration  
- Landmark detection with emojis
- Professional Word document generation
- Modern responsive web interface
- HuggingFace AI integration

🔧 Technical Improvements:
- Enhanced OpenCV processing
- Improved algorithm accuracy
- Better error handling
- Performance optimizations"

echo ✅ Changes committed

REM Get GitHub username
echo.
set /p GITHUB_USERNAME=Please enter your GitHub username: 

if "%GITHUB_USERNAME%"=="" (
    echo ❌ GitHub username cannot be empty
    pause
    exit /b 1
)

REM Repository name
set REPO_NAME=map-route-extractor
set REPO_URL=https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo ℹ️  Repository URL: %REPO_URL%

REM Check if remote already exists and configure
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Remote 'origin' already exists. Updating...
    git remote set-url origin %REPO_URL%
) else (
    echo ℹ️  Adding remote origin...
    git remote add origin %REPO_URL%
)

echo ✅ Remote origin configured

REM Set main branch
echo ℹ️  Setting up main branch...
git branch -M main

REM Push to GitHub
echo ℹ️  Pushing to GitHub...
echo.
echo ⚠️  Make sure you've created the repository on GitHub first!
echo ℹ️  Repository should be: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.

set /p CONFIRM=Have you created the repository on GitHub? (y/n): 
if /i "%CONFIRM%"=="y" (
    git push -u origin main
    if %errorlevel% equ 0 (
        echo ✅ Successfully pushed to GitHub!
    ) else (
        echo ❌ Failed to push to GitHub. Please check your credentials and repository.
        pause
        exit /b 1
    )
) else (
    echo ⚠️  Please create the repository on GitHub first, then run this script again.
    echo ℹ️  Repository settings:
    echo - Name: %REPO_NAME%
    echo - Description: AI-powered map route extraction and documentation system
    echo - Public/Private: Your choice
    echo - Don't initialize with README (we have our own)
    pause
    exit /b 0
)

REM Success message
echo.
echo ✅ 🎉 Deployment Complete!
echo.
echo ℹ️  Your repository is now available at:
echo 🔗 https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.
echo ℹ️  Next steps:
echo 1. 🌟 Add repository description and topics
echo 2. 📝 Enable Issues, Wiki, and Discussions
echo 3. 🏷️  Create a release (v2.0.0)
echo 4. 📢 Share your project with the community
echo.
echo ℹ️  For detailed instructions, see GITHUB_SETUP.md
echo.
echo ✅ Happy coding! 🚀

pause
