#!/bin/bash
# GitHub MCP Server Setup Script

echo "🚀 Setting up GitHub MCP Server..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies in virtual environment..."
source venv/bin/activate
pip install -r requirements.txt

# Get the absolute paths
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/github_mcp_server.py"
PYTHON_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/venv/bin/python"

echo "📁 Server script location: $SCRIPT_PATH"
echo "🐍 Python interpreter: $PYTHON_PATH"

# Add MCP server to Q CLI
echo "🔧 Adding MCP server to Q CLI..."
q mcp add --name github-server --command "$PYTHON_PATH" --args "$SCRIPT_PATH" --scope global --force

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
