#!/usr/bin/env python3
"""
GitHub MCP Server
A Model Context Protocol server for GitHub operations including creating repos and committing code.
"""

import asyncio
import json
import sys
import os
import subprocess
from typing import Any, Dict, List, Optional
from github import Github
import requests


class GitHubMCPServer:
    def __init__(self):
        # Initialize GitHub client - will use token from environment or gh CLI
        self.github_token = self._get_github_token()
        self.github_client = Github(self.github_token) if self.github_token else None
        
        self.tools = {
            "create_repo": {
                "name": "create_repo",
                "description": "Create a new GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Repository name"
                        },
                        "description": {
                            "type": "string",
                            "description": "Repository description (optional)"
                        },
                        "private": {
                            "type": "boolean",
                            "description": "Whether the repository should be private (default: false)"
                        },
                        "initialize": {
                            "type": "boolean",
                            "description": "Initialize with README (default: true)"
                        }
                    },
                    "required": ["name"]
                }
            },
            "commit_and_push": {
                "name": "commit_and_push",
                "description": "Commit changes and push to GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_path": {
                            "type": "string",
                            "description": "Local repository path"
                        },
                        "commit_message": {
                            "type": "string",
                            "description": "Commit message"
                        },
                        "files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific files to commit (optional, commits all changes if not specified)"
                        },
                        "branch": {
                            "type": "string",
                            "description": "Branch to push to (default: current branch)"
                        }
                    },
                    "required": ["repo_path", "commit_message"]
                }
            },
            "clone_repo": {
                "name": "clone_repo",
                "description": "Clone a GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_url": {
                            "type": "string",
                            "description": "GitHub repository URL or owner/repo format"
                        },
                        "destination": {
                            "type": "string",
                            "description": "Local destination path (optional)"
                        },
                        "branch": {
                            "type": "string",
                            "description": "Specific branch to clone (optional)"
                        }
                    },
                    "required": ["repo_url"]
                }
            },
            "create_issue": {
                "name": "create_issue",
                "description": "Create a new issue in a GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {
                            "type": "string",
                            "description": "Repository in owner/repo format"
                        },
                        "title": {
                            "type": "string",
                            "description": "Issue title"
                        },
                        "body": {
                            "type": "string",
                            "description": "Issue description (optional)"
                        },
                        "labels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Issue labels (optional)"
                        }
                    },
                    "required": ["repo", "title"]
                }
            },
            "list_repos": {
                "name": "list_repos",
                "description": "List GitHub repositories for the authenticated user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["all", "owner", "public", "private"],
                            "description": "Type of repositories to list (default: all)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of repositories to return (default: 10)"
                        }
                    }
                }
            },
            "get_repo_info": {
                "name": "get_repo_info",
                "description": "Get information about a specific GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {
                            "type": "string",
                            "description": "Repository in owner/repo format"
                        }
                    },
                    "required": ["repo"]
                }
            }
        }

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from environment or gh CLI"""
        # Try environment variable first
        token = os.getenv('GITHUB_TOKEN')
        if token:
            return token
        
        # Try to get token from gh CLI
        try:
            result = subprocess.run(['gh', 'auth', 'token'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def _run_git_command(self, command: List[str], cwd: str = None) -> Dict[str, Any]:
        """Run a git command and return the result"""
        try:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True)
            return {
                "success": True,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Command failed: {' '.join(command)}",
                "stdout": e.stdout,
                "stderr": e.stderr,
                "return_code": e.returncode
            }

    async def create_repo(self, name: str, description: str = "", private: bool = False, initialize: bool = True) -> str:
        """Create a new GitHub repository"""
        if not self.github_client:
            return "❌ GitHub authentication required. Set GITHUB_TOKEN environment variable or use 'gh auth login'"
        
        try:
            user = self.github_client.get_user()
            repo = user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=initialize
            )
            
            return f"✅ Repository created successfully!\n🔗 URL: {repo.html_url}\n📝 Clone: git clone {repo.clone_url}"
        
        except Exception as e:
            return f"❌ Failed to create repository: {str(e)}"

    async def commit_and_push(self, repo_path: str, commit_message: str, files: List[str] = None, branch: str = None) -> str:
        """Commit changes and push to GitHub"""
        if not os.path.exists(repo_path):
            return f"❌ Repository path does not exist: {repo_path}"
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return f"❌ Not a git repository: {repo_path}"
        
        results = []
        
        # Add files
        if files:
            for file in files:
                result = self._run_git_command(['git', 'add', file], cwd=repo_path)
                if not result['success']:
                    return f"❌ Failed to add file {file}: {result['stderr']}"
        else:
            result = self._run_git_command(['git', 'add', '.'], cwd=repo_path)
            if not result['success']:
                return f"❌ Failed to add files: {result['stderr']}"
        
        # Commit
        result = self._run_git_command(['git', 'commit', '-m', commit_message], cwd=repo_path)
        if not result['success']:
            if "nothing to commit" in result['stdout']:
                return "ℹ️ No changes to commit"
            return f"❌ Failed to commit: {result['stderr']}"
        
        results.append(f"✅ Committed: {commit_message}")
        
        # Push
        push_cmd = ['git', 'push']
        if branch:
            push_cmd.extend(['origin', branch])
        
        result = self._run_git_command(push_cmd, cwd=repo_path)
        if not result['success']:
            return f"❌ Failed to push: {result['stderr']}"
        
        results.append("✅ Pushed to GitHub successfully")
        
        return "\n".join(results)

    async def clone_repo(self, repo_url: str, destination: str = None, branch: str = None) -> str:
        """Clone a GitHub repository"""
        clone_cmd = ['git', 'clone']
        
        if branch:
            clone_cmd.extend(['-b', branch])
        
        clone_cmd.append(repo_url)
        
        if destination:
            clone_cmd.append(destination)
        
        result = self._run_git_command(clone_cmd)
        
        if result['success']:
            return f"✅ Repository cloned successfully\n📁 Location: {destination or repo_url.split('/')[-1].replace('.git', '')}"
        else:
            return f"❌ Failed to clone repository: {result['stderr']}"

    async def create_issue(self, repo: str, title: str, body: str = "", labels: List[str] = None) -> str:
        """Create a new issue in a GitHub repository"""
        if not self.github_client:
            return "❌ GitHub authentication required"
        
        try:
            repository = self.github_client.get_repo(repo)
            issue = repository.create_issue(
                title=title,
                body=body,
                labels=labels or []
            )
            
            return f"✅ Issue created successfully!\n🔗 URL: {issue.html_url}\n#️⃣ Number: #{issue.number}"
        
        except Exception as e:
            return f"❌ Failed to create issue: {str(e)}"

    async def list_repos(self, repo_type: str = "all", limit: int = 10) -> str:
        """List GitHub repositories"""
        if not self.github_client:
            return "❌ GitHub authentication required"
        
        try:
            user = self.github_client.get_user()
            repos = user.get_repos(type=repo_type)
            
            repo_list = []
            for i, repo in enumerate(repos):
                if i >= limit:
                    break
                
                visibility = "🔒 Private" if repo.private else "🌍 Public"
                repo_list.append(f"📁 {repo.name} - {visibility}\n   🔗 {repo.html_url}\n   📝 {repo.description or 'No description'}")
            
            if not repo_list:
                return "No repositories found"
            
            return f"📚 Your repositories ({len(repo_list)} of {repos.totalCount}):\n\n" + "\n\n".join(repo_list)
        
        except Exception as e:
            return f"❌ Failed to list repositories: {str(e)}"

    async def get_repo_info(self, repo: str) -> str:
        """Get information about a specific repository"""
        if not self.github_client:
            return "❌ GitHub authentication required"
        
        try:
            repository = self.github_client.get_repo(repo)
            
            info = f"""📁 Repository: {repository.full_name}
📝 Description: {repository.description or 'No description'}
🌍 Visibility: {'Private' if repository.private else 'Public'}
⭐ Stars: {repository.stargazers_count}
🍴 Forks: {repository.forks_count}
📊 Language: {repository.language or 'Not specified'}
🔗 URL: {repository.html_url}
📅 Created: {repository.created_at.strftime('%Y-%m-%d')}
📅 Updated: {repository.updated_at.strftime('%Y-%m-%d')}
📏 Size: {repository.size} KB"""
            
            return info
        
        except Exception as e:
            return f"❌ Failed to get repository info: {str(e)}"

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "github-mcp-server",
                            "version": "1.0.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": list(self.tools.values())
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                result_text = ""
                
                if tool_name == "create_repo":
                    result_text = await self.create_repo(**arguments)
                elif tool_name == "commit_and_push":
                    result_text = await self.commit_and_push(**arguments)
                elif tool_name == "clone_repo":
                    result_text = await self.clone_repo(**arguments)
                elif tool_name == "create_issue":
                    result_text = await self.create_issue(**arguments)
                elif tool_name == "list_repos":
                    result_text = await self.list_repos(**arguments)
                elif tool_name == "get_repo_info":
                    result_text = await self.get_repo_info(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result_text
                            }
                        ]
                    }
                }
            
            else:
                raise ValueError(f"Unknown method: {method}")
                
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }

    async def run(self):
        """Main server loop"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                response = await self.handle_request(request)
                print(json.dumps(response), flush=True)
                
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)


async def main():
    server = GitHubMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
