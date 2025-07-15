#!/bin/bash
# GitHub MCP Server Setup Script

echo "🚀 Setting up GitHub MCP Server..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Get the absolute path to the server script
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/github_mcp_server.py"

echo "📁 Server script location: $SCRIPT_PATH"

# Add MCP server to Q CLI
echo "🔧 Adding MCP server to Q CLI..."
q mcp add --name github-server --command python3 --args "$SCRIPT_PATH" --scope global --force

echo "✅ Setup complete!"
echo ""
echo "🎉 Your GitHub MCP server is now available in Q CLI with these tools:"
echo "   • github-server___create_repo - Create new GitHub repositories"
echo "   • github-server___commit_and_push - Commit and push code changes"
echo "   • github-server___clone_repo - Clone GitHub repositories"
echo "   • github-server___create_issue - Create GitHub issues"
echo "   • github-server___list_repos - List your repositories"
echo "   • github-server___get_repo_info - Get repository information"
echo ""
echo "💡 Start a new Q CLI chat session to use these tools!"
echo "   Example: 'Create a new repository called my-project'"
