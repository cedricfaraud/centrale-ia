import os
import json

from groq import Groq
from openai import OpenAI

# --- Clients API gratuits ---

# Groq (Llama / Mixtral)
groq = Groq(api_key=os.environ["GROQ_API_KEY"])

# DeepSeek (via client OpenAI)
deepseek = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1",
)

# Gemini (via client OpenAI)
gemini = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# --- Agents IA gratuits ---

def orchestrateur(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def architecte(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def dev(prompt: str) -> str:
    r = deepseek.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def po(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def ivvq(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def devops(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def agent_github(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Tu es un agent GitHub.
Tu génères des actions concrètes pour :
- créer un dépôt GitHub via l'API REST
- ajouter des fichiers
- créer des commits
- créer des workflows GitHub Actions
- pousser du code automatiquement

Réponds uniquement en JSON structuré avec :
- repo_name
- files (nom + contenu)
- workflow (contenu YAML)
- commit_message
- api_calls (liste des appels API à effectuer)

Voici la demande :
{prompt}
"""
        }],
    )
    return r.choices[0].message.content

def agent_deploy(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Tu es un agent de déploiement.
Tu génères des actions concrètes pour déployer automatiquement un projet sur :
- Render
- Vercel
- HuggingFace Spaces

Réponds uniquement en JSON structuré avec :
- platform ("render" | "vercel" | "huggingface")
- deploy_config (dict)
- api_calls (liste des appels API à effectuer)

Voici la demande :
{prompt}
"""
        }],
    )
    return r.choices[0].message.content


# --- Orchestrateur multi-agents complet ---
from deploy_api import deploy_render, deploy_vercel, deploy_huggingface
from github_api import create_repo, add_files, add_workflow, commit_and_push

def run_orchestrateur_multi_agents(objectif: str) -> str:
    # 1. PO : cadrage du besoin
    po_prompt = f"""Objectif :
{objectif}

Donne une user story + critères d'acceptation."""
    po_result = po(po_prompt)

    # 2. Architecte : conception
    archi_prompt = f"""Cadrage :
{po_result}

Donne une architecture technique concise."""
    archi_result = architecte(archi_prompt)

    # 3. Dev : implémentation
    dev_prompt = f"""Architecture :
{archi_result}

Donne un plan d'implémentation concis."""
    dev_result = dev(dev_prompt)

    # 4. IVVQ : validation
    ivvq_prompt = f"""Plan :
{dev_result}

Donne une stratégie de tests concise."""
    ivvq_result = ivvq(ivvq_prompt)

    # 5. DevOps : pipeline CI/CD
    devops_prompt = f"""Plan :
{dev_result}

Donne un pipeline CI/CD concis."""
    devops_result = devops(devops_prompt)

    # 6. GitHub : génération du dépôt + fichiers
    github_prompt = f"""Projet :
Objectif :
{objectif}

Cadrage :
{po_result}

Architecture :
{archi_result}

Plan d'implémentation :
{dev_result}

Pipeline CI/CD :
{devops_result}

Génère un dépôt GitHub complet pour ce projet :
- repo_name
- files (nom + contenu)
- workflow (contenu YAML)
- commit_message
- api_calls (liste des appels API à effectuer)
Réponds uniquement en JSON."""
    github_plan_json = agent_github(github_prompt)

    try:
        github_plan = json.loads(github_plan_json)
        repo_name = github_plan.get("repo_name", "projet-discussion-famille")
        files = github_plan.get("files", [])
        workflow = github_plan.get("workflow", "")
        commit_message = github_plan.get("commit_message", "Initial commit")
    except Exception as e:
        repo_name = "projet-discussion-famille"
        files = []
        workflow = ""
        commit_message = f"Erreur parsing JSON GitHub : {e}"

    # Exécution réelle des actions GitHub
    try:
        repo_url = create_repo(repo_name)
        for f in files:
            add_files(repo_name, f["name"], f["content"])
        if workflow:
            add_workflow(repo_name, workflow)
        commit_and_push(repo_name, commit_message)
    except Exception as e:
        repo_url = f"Erreur lors de la création du dépôt GitHub : {e}"

    # 7. Déploiement automatique
    deploy_prompt = f"""Déploie automatiquement ce projet :
Repo GitHub : {repo_url}

Architecture :
{archi_result}

Plan d'implémentation :
{dev_result}

Pipeline DevOps :
{devops_result}
"""
    deploy_plan_json = agent_deploy(deploy_prompt)

    try:
        deploy_plan = json.loads(deploy_plan_json)
        platform = deploy_plan.get("platform")
        deploy_config = deploy_plan.get("deploy_config", {})
    except Exception as e:
        deploy_result = f"Erreur parsing JSON déploiement : {e}"
        platform = None

    if platform == "render":
        deploy_result = deploy_render(deploy_config)
    elif platform == "vercel":
        deploy_result = deploy_vercel(deploy_config)
    elif platform == "huggingface":
        deploy_result = deploy_huggingface(deploy_config)
    else:
        deploy_result = "Plateforme inconnue ou JSON invalide"

    synthese = f"""
# Synthèse orchestrateur multi-agents

## 1. Cadrage PO
{po_result}

## 2. Architecture
{archi_result}

## 3. Plan d'implémentation
{dev_result}

## 4. Stratégie IVVQ
{ivvq_result}

## 5. Pipeline DevOps
{devops_result}

## 6. Dépôt GitHub
{repo_url}

## 7. Déploiement automatique
{deploy_result}
"""

    return synthese
