#!/bin/bash

# 🚀 GitHub Deployment Script for Map Route Extractor
# This script helps you deploy your project to GitHub

echo "🧭 Map Route Extractor - GitHub Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

print_status "Git is installed"

# Check if we're in the right directory
if [ ! -f "launch_app.py" ]; then
    print_error "This script must be run from the MapRouteExtractor directory"
    exit 1
fi

print_status "In correct directory"

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
else
    print_info "Git repository already exists"
fi

# Add all files to git
print_info "Adding files to Git..."
git add .

# Check if there are any changes to commit
if git diff --cached --quiet; then
    print_warning "No changes to commit"
else
    print_info "Committing changes..."
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

    print_status "Changes committed"
fi

# Get GitHub username
echo ""
print_info "Please enter your GitHub username:"
read -r GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    print_error "GitHub username cannot be empty"
    exit 1
fi

# Repository name
REPO_NAME="map-route-extractor"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

print_info "Repository URL: $REPO_URL"

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    print_warning "Remote 'origin' already exists. Updating..."
    git remote set-url origin "$REPO_URL"
else
    print_info "Adding remote origin..."
    git remote add origin "$REPO_URL"
fi

print_status "Remote origin configured"

# Set main branch
print_info "Setting up main branch..."
git branch -M main

# Push to GitHub
print_info "Pushing to GitHub..."
echo ""
print_warning "Make sure you've created the repository on GitHub first!"
print_info "Repository should be: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

read -p "Have you created the repository on GitHub? (y/n): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if git push -u origin main; then
        print_status "Successfully pushed to GitHub!"
    else
        print_error "Failed to push to GitHub. Please check your credentials and repository."
        exit 1
    fi
else
    print_warning "Please create the repository on GitHub first, then run this script again."
    print_info "Repository settings:"
    print_info "- Name: $REPO_NAME"
    print_info "- Description: AI-powered map route extraction and documentation system"
    print_info "- Public/Private: Your choice"
    print_info "- Don't initialize with README (we have our own)"
    exit 0
fi

# Success message
echo ""
print_status "🎉 Deployment Complete!"
echo ""
print_info "Your repository is now available at:"
echo "🔗 https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
print_info "Next steps:"
echo "1. 🌟 Add repository description and topics"
echo "2. 📝 Enable Issues, Wiki, and Discussions"
echo "3. 🏷️  Create a release (v2.0.0)"
echo "4. 📢 Share your project with the community"
echo ""
print_info "For detailed instructions, see GITHUB_SETUP.md"
echo ""
print_status "Happy coding! 🚀"
