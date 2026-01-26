#!/bin/bash

# Deployment script for Hugging Face Spaces
# This script helps you deploy the Todo API backend to Hugging Face Spaces

echo "🚀 Todo API Backend - Hugging Face Spaces Deployment"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Check if Hugging Face remote exists
if git remote | grep -q "space"; then
    echo "✅ Hugging Face Space remote already configured"
else
    echo "🔗 Adding Hugging Face Space as remote..."
    read -p "Enter your Hugging Face Space URL (e.g., https://huggingface.co/spaces/username/space-name): " SPACE_URL
    git remote add space "$SPACE_URL"
    echo "✅ Remote added"
fi

# Copy Space README
echo "📝 Preparing README for Hugging Face Space..."
cp SPACE_README.md README.md
echo "✅ README prepared"

# Show current status
echo ""
echo "📊 Current Git Status:"
git status --short

# Ask for confirmation
echo ""
read -p "Do you want to commit and push to Hugging Face Spaces? (y/n): " CONFIRM

if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
    # Add all files
    echo "📦 Adding files..."
    git add .

    # Commit
    echo "💾 Committing changes..."
    read -p "Enter commit message (default: 'Deploy Todo API backend'): " COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"Deploy Todo API backend"}
    git commit -m "$COMMIT_MSG"

    # Push to Hugging Face Space
    echo "🚀 Pushing to Hugging Face Space..."
    git push space main

    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "🎉 Your backend should be building now."
    echo "📍 Check your Space at: https://huggingface.co/spaces/fouziabibi/todo"
    echo "📚 API Docs will be at: https://fouziabibi-todo.hf.space/docs"
    echo ""
    echo "⏳ Note: Initial build may take 5-10 minutes."
else
    echo "❌ Deployment cancelled"
fi
