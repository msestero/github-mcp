# GitHub MCP Server

A comprehensive Model Context Protocol (MCP) server for GitHub integration with Amazon Q CLI. This server provides powerful GitHub functionality directly in your Q CLI chat interface.

## 🚀 Features

- **Repository Management**
  - Create new repositories
  - Clone existing repositories
  - Get repository information
  - List your repositories

- **Code Operations**
  - Commit and push changes
  - Handle multiple files
  - Branch management

- **Issue Tracking**
  - Create new issues
  - Add labels and descriptions

## 🛠️ Available Tools

Once installed, you'll have access to these tools in Q CLI:

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `create_repo` | Create a new GitHub repository | "Create a new repository called my-awesome-project" |
| `commit_and_push` | Commit changes and push to GitHub | "Commit all changes with message 'Add new feature'" |
| `clone_repo` | Clone a GitHub repository | "Clone the repository user/repo-name" |
| `create_issue` | Create a new issue | "Create an issue titled 'Bug in login system'" |
| `list_repos` | List your repositories | "Show me my repositories" |
| `get_repo_info` | Get repository details | "Get info about user/repo-name" |

## 📋 Prerequisites

- Python 3.7+
- Amazon Q CLI installed and configured
- GitHub CLI (`gh`) installed and authenticated, OR
- GitHub Personal Access Token set as `GITHUB_TOKEN` environment variable

## 🔧 Installation

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/msestero/github-mcp.git
cd github-mcp

# Run the setup script
./setup.sh
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/msestero/github-mcp.git
cd github-mcp

# Install dependencies
pip install -r requirements.txt

# Add to Q CLI (replace with your actual path)
q mcp add --name github-server --command python3 --args "/path/to/github_mcp_server.py" --scope global
```

## 🔐 Authentication

The server supports two authentication methods:

### Option 1: GitHub CLI (Recommended)
```bash
gh auth login
```

### Option 2: Environment Variable
```bash
export GITHUB_TOKEN="your_github_token_here"
```

## 💡 Usage Examples

Start a new Q CLI chat session and try these commands:

### Creating Repositories
```
"Create a new public repository called my-web-app with description 'My awesome web application'"
```

### Committing Code
```
"Commit all changes in /path/to/my/repo with message 'Add authentication feature'"
```

### Cloning Repositories
```
"Clone the repository microsoft/vscode to my Projects folder"
```

### Managing Issues
```
"Create an issue in my-user/my-repo titled 'Add dark mode' with labels bug and enhancement"
```

### Repository Information
```
"Show me information about facebook/react"
"List my private repositories"
```

## 🔧 Configuration

The MCP server is added to your global Q CLI configuration at:
- `~/.aws/amazonq/mcp.json`

You can check the status with:
```bash
q mcp status --name github-server
q mcp list
```

## 🛡️ Security

- The server uses your existing GitHub authentication (gh CLI or token)
- No credentials are stored in the MCP server
- All operations respect your GitHub permissions
- Private repositories require appropriate access tokens

## 🐛 Troubleshooting

### Authentication Issues
```bash
# Check GitHub CLI status
gh auth status

# Re-authenticate if needed
gh auth login
```

### MCP Server Issues
```bash
# Check server status
q mcp status --name github-server

# View MCP configuration
q mcp list

# Remove and re-add server
q mcp remove --name github-server
./setup.sh
```

### Python Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- [Amazon Q CLI Documentation](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [GitHub API Documentation](https://docs.github.com/en/rest)

---

Made with ❤️ for the Amazon Q CLI community
