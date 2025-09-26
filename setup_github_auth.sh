#!/bin/bash
# GitHub Authentication Setup Script
# Run this once with your Personal Access Token

echo "🔐 Setting up GitHub authentication for Decisioning Agentic Flow"
echo "=================================================="

echo "Enter your GitHub Personal Access Token:"
read -s TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ No token provided. Exiting."
    exit 1
fi

echo "🔧 Configuring Git credentials..."

# Set up credential storage
git config --global credential.helper store

# Update remote URL with token
git remote set-url origin https://$TOKEN@github.com/rwalkerphl/decisioning-agentic-flow.git

echo "✅ Authentication configured!"
echo "🚀 Testing push to GitHub..."

# Test push
if git push origin main; then
    echo "✅ SUCCESS! GitHub authentication is working!"
    echo "🎯 Future pushes will work automatically"
else
    echo "❌ Push failed. Please check your token and try again."
    exit 1
fi

echo "🎉 Setup complete! Your repository is ready for automatic pushes."