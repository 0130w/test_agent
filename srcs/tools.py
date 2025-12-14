from github import Github
from langchain_core.tools import tool

import os
import subprocess

@tool
def list_files(dir: str = '.') -> str:
    """
    list files in dir
    """
    try:
        return str(os.listdir(dir))
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def read_file(file_path: str) -> str:
    """
    read file content
    """
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"
    
@tool
def write_file(file_path: str, content: str) -> str:
    """
    write content into file
    """
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool
def run_shell_command(command: str) -> str:
    """
    run shell command
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return f"Command Success:\n{result.stdout}"
        else:
            return f"Command Failed:\n{result.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"
    
@tool
def create_pull_request(title: str, body: str, head_branch: str, base_branch: str = "main") -> str:
    """
    create pull request
    """
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    if not token or not repo_name:
        return f"Error: GITHUB_TOKEN or GITHUB_REPO env variables are missing"

    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head_branch,
            base=base_branch
        )
        return f"PR Created Successfully! URL: {pr.html_url}"
    except Exception as e:
        return f"Error creating PR: {e}"