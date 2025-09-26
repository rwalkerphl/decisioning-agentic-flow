#!/bin/bash
# Automatic Git Push Script
# Use this after the one-time authentication setup

echo "🚀 Pushing changes to GitHub..."

# Add all changes
git add -A

# Commit with timestamp if there are changes
if git diff --staged --quiet; then
    echo "📝 No changes to commit"
else
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    git commit -m "📊 Update: $TIMESTAMP - Automated documentation and improvements"
    echo "✅ Changes committed"
fi

# Push to GitHub
if git push origin main; then
    echo "🎉 Successfully pushed to GitHub!"
    echo "🔗 View at: https://github.com/rwalkerphl/decisioning-agentic-flow"
else
    echo "❌ Push failed. Check your connection and authentication."
fi