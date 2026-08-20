import base64
import requests
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_USER = os.environ["GITHUB_USER"]

def github_create_repo(repo_name: str):
    url = "https://api.github.com/user/repos"
    payload = {"name": repo_name, "private": False}
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    return requests.post(url, json=payload, headers=headers)

def github_add_file(repo: str, path: str, content: str, message: str):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/{path}"
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode()
    }
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    return requests.put(url, json=payload, headers=headers)
