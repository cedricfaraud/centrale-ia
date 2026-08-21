import os
import json
from openai import OpenAI

# --- Clients API gratuits ---
groq = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

deepseek = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1",
)

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
        model="mixtral-8x7b-instruct",
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

def run_orchestrateur_multi_agents(objectif: str) -> str:
    # 1. PO : cadrage du besoin
    po_prompt = f"""Tu es Product Owner.
Objectif utilisateur :
{objectif}

Clarifie le besoin, identifie les contraintes, et propose une user story + critères d'acceptation."""
    po_result = po(po_prompt)

    # 2. Architecte : conception
    archi_prompt = f"""Tu es Architecte logiciel.
Voici le cadrage du PO :
{po_result}

Propose une architecture technique (modules, flux, données, choix technos) adaptée."""
    archi_result = architecte(archi_prompt)

    # 3. Dev : implémentation
    dev_prompt = f"""Tu es Développeur senior.
Voici l'architecture proposée :
{archi_result}

Propose un plan d'implémentation détaillé (étapes, pseudo-code, fichiers, fonctions)."""
    dev_result = dev(dev_prompt)

    # 4. IVVQ : validation
    ivvq_prompt = f"""Tu es Ingénieur IVVQ.
Voici le plan d'implémentation :
{dev_result}

Propose une stratégie de tests (unitaires, intégration, validation), avec cas de test concrets."""
    ivvq_result = ivvq(ivvq_prompt)

    # 5. DevOps : pipeline CI/CD
    devops_prompt = f"""Tu es ingénieur DevOps senior.
Voici le plan d'implémentation :
{dev_result}

Génère un pipeline CI/CD complet, incluant :
- un workflow GitHub Actions
- un Dockerfile si nécessaire
- un script de déploiement
- un plan de monitoring
- un plan de rollback
"""
    devops_result = devops(devops_prompt)

    # 6. Déploiement automatique
    deploy_prompt = f"""Déploie automatiquement ce projet :
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

    # Synthèse finale
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

## 6. Déploiement automatique
{deploy_result}
"""

    return synthese
