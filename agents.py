import os
import json

from openai import OpenAI

# --- Clients API gratuits ---

# DeepSeek (via OpenAI API format)
deepseek = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1",
)

# Gemini (via OpenAI API format)
gemini = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# --- Agents IA gratuits ---

def po(prompt: str) -> str:
    r = deepseek.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def dev(prompt: str) -> str:
    r = deepseek.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def devops(prompt: str) -> str:
    r = gemini.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def agent_github(prompt: str) -> str:
    r = deepseek.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{
            "role": "user",
            "content": f"""
Tu es un agent GitHub.
Génère un JSON structuré contenant :
- repo_name
- files : liste de fichiers {{"name": "...", "content": "..."}}
- commit_message

Réponds uniquement en JSON valide.
{prompt}
"""
        }],
    )
    return r.choices[0].message.content


def agent_deploy(prompt: str) -> str:
    r = gemini.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{
            "role": "user",
            "content": f"""
Tu es un agent de déploiement.
Génère un JSON structuré contenant :
- platform ("render" | "vercel" | "huggingface")
- deploy_config (dict)

Réponds uniquement en JSON valide.
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

# --- Orchestrateur multi-agents ---
def run_orchestrateur_multi_agents(objectif: str) -> str:

    # 1. PO
    po_prompt = f"""Objectif :
{objectif}

Donne :
- une user story
- 3 critères d'acceptation
Réponds en 10 lignes maximum."""
    po_result = po(po_prompt)

    # 2. Dev
    dev_prompt = f"""User story :
{po_result}

Donne un plan d'implémentation concis."""
    dev_result = dev(dev_prompt)

    # 3. DevOps
    devops_prompt = f"""Plan :
{dev_result}

Donne un pipeline CI/CD concis."""
    devops_result = devops(devops_prompt)

    # 4. GitHub
    github_prompt = f"""Projet :
Objectif : {objectif}
User story : {po_result}
Plan : {dev_result}
Pipeline : {devops_result}

Génère le dépôt complet."""
    github_plan_json = agent_github(github_prompt)

    try:
        github_plan = json.loads(github_plan_json)
        repo_name = github_plan.get("repo_name", "projet-auto")
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

    # 5. Déploiement
    deploy_prompt = f"""Déploie automatiquement ce projet :
Repo GitHub : {repo_url}
Plan : {dev_result}
Pipeline : {devops_result}
"""
    deploy_plan_json = agent_deploy(deploy_prompt)

    try:
        deploy_plan = json.loads(deploy_plan_json)
        platform = deploy_plan.get("platform")
        deploy_config = deploy_plan.get("deploy_config", {})
    except Exception as e:
        deploy_result = f"Erreur JSON déploiement : {e}"
        platform = None

    if platform == "render":
        deploy_result = deploy_render(deploy_config)
    elif platform == "vercel":
        deploy_result = deploy_vercel(deploy_config)
    elif platform == "huggingface":
        deploy_result = deploy_huggingface(deploy_config)
    else:
        deploy_result = "Plateforme inconnue ou JSON invalide"

    return f"""
# Synthèse orchestrateur multi-agents

## 1. Cadrage PO
{po_result}

## 2. Plan Dev
{dev_result}

## 3. Pipeline DevOps
{devops_result}

## 4. Dépôt GitHub
{repo_url}

## 5. Déploiement automatique
{deploy_result}
"""
