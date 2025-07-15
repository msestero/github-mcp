# GitHub MCP Server

A Model Context Protocol (MCP) server for GitHub integration with Amazon Q CLI.

## Overview

This MCP server provides GitHub functionality to Amazon Q CLI, allowing you to interact with GitHub repositories, issues, pull requests, and more directly from your chat interface.

## Features

- Repository management
- Issue tracking
- Pull request operations
- GitHub API integration

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd github-mcp

# Install dependencies
pip install -r requirements.txt
```

## Usage

Add this MCP server to your Q CLI configuration:

```bash
q mcp add --name github-server --command python3 --args "/path/to/github_mcp_server.py"
```

## Development

This project is built using Python and follows the MCP protocol specification.

## License

MIT License
