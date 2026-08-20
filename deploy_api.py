import os
import requests

RENDER_TOKEN = os.environ.get("RENDER_TOKEN")
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")


# --- Render ---

def deploy_render(config: dict):
    """
    config : dict avec la config Render, par ex :
    {
        "serviceType": "web_service",
        "name": "centrale-ia",
        "env": "python",
        "region": "frankfurt",
        "branch": "main",
        "repo": "https://github.com/cedricfaraud/centrale-ia"
    }
    """
    if not RENDER_TOKEN:
        raise RuntimeError("RENDER_TOKEN manquant dans les variables d'environnement")

    url = "https://api.render.com/v1/services"
    headers = {
        "Authorization": f"Bearer {RENDER_TOKEN}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=config, headers=headers)
    resp.raise_for_status()
    return resp.json()


# --- Vercel ---

def deploy_vercel(config: dict):
    """
    config : dict avec la config Vercel, par ex :
    {
        "name": "centrale-ia",
        "project": "centrale-ia",
        "gitRepository": {
            "type": "github",
            "repo": "cedricfaraud/centrale-ia"
        }
    }
    """
    if not VERCEL_TOKEN:
        raise RuntimeError("VERCEL_TOKEN manquant dans les variables d'environnement")

    url = "https://api.vercel.com/v13/deployments"
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=config, headers=headers)
    resp.raise_for_status()
    return resp.json()


# --- HuggingFace Spaces ---

def deploy_huggingface(config: dict):
    """
    config : dict avec la config HF Space, par ex :
    {
        "name": "centrale-ia",
        "type": "streamlit",
        "sdk": "streamlit",
        "repo_url": "https://github.com/cedricfaraud/centrale-ia"
    }
    """
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN manquant dans les variables d'environnement")

    url = "https://huggingface.co/api/spaces"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=config, headers=headers)
    resp.raise_for_status()
    return resp.json()
