import os
import json

from groq import Groq
from openai import OpenAI

groq = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- Agents IA ---

def po(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="groq/compound",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def agent_github(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="groq/compound",
        messages=[{
            "role": "user",
            "content": f"""
Tu es un agent GitHub.
Génère un dépôt minimal contenant :
- index.html avec "Hello World"
- un commit_message

Réponds uniquement en JSON :
{prompt}
"""
        }],
    )
    return r.choices[0].message.content

# --- API GitHub ---
from github_api import (
    github_create_repo,
    github_add_file,
    github_commit_and_push
)

# --- Orchestrateur ultra-léger ---
def run_orchestrateur_multi_agents(objectif: str) -> str:

    # 1. PO
    po_prompt = f"Objectif : {objectif}. Donne un plan simple en 5 lignes."
    po_result = po(po_prompt)

    # 2. GitHub
    github_prompt = f"Plan : {po_result}. Génère le dépôt."
    github_plan_json = agent_github(github_prompt)

    try:
        github_plan = json.loads(github_plan_json)
        repo_name = github_plan.get("repo_name", "hello-world-web")
        files = github_plan.get("files", [])
        commit_message = github_plan.get("commit_message", "Initial commit")
    except Exception as e:
        return f"Erreur JSON GitHub : {e}"

    # Exécution GitHub
    try:
        repo_url = github_create_repo(repo_name)
        for f in files:
            github_add_file(repo_name, f["name"], f["content"])
        github_commit_and_push(repo_name, commit_message)
    except Exception as e:
        repo_url = f"Erreur GitHub : {e}"

    return f"""
# Projet généré

## Objectif
{objectif}

## Plan PO
{po_result}

## Dépôt GitHub
{repo_url}
"""
