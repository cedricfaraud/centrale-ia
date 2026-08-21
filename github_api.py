import base64
import requests
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_USER = os.environ["GITHUB_USER"]

BASE_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# 1️⃣ Créer un dépôt
def github_create_repo(repo_name: str):
    url = "https://api.github.com/user/repos"
    payload = {"name": repo_name, "private": False}
    r = requests.post(url, json=payload, headers=BASE_HEADERS)
    r.raise_for_status()
    return r.json()["html_url"]


# 2️⃣ Ajouter un fichier
def github_add_file(repo: str, path: str, content: str, message: str):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/{path}"
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode()
    }
    r = requests.put(url, json=payload, headers=BASE_HEADERS)
    r.raise_for_status()
    return r.json()


# 3️⃣ Ajouter un workflow GitHub Actions
def github_add_workflow(repo: str, workflow_yaml: str):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/.github/workflows/ci.yml"
    payload = {
        "message": "Add CI workflow",
        "content": base64.b64encode(workflow_yaml.encode()).decode()
    }
    r = requests.put(url, json=payload, headers=BASE_HEADERS)
    r.raise_for_status()
    return r.json()


# 4️⃣ Commit final (techniquement inutile, GitHub API commit déjà)
def github_commit_and_push(repo: str, message: str):
    # On ne fait rien : GitHub API commit déjà dans add_file()
    return {"status": "ok", "message": message}
