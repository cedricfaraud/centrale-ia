import os
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
        model="mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def ivvq(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="phi-3-mini-4k-instruct",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content
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

    # 5. Synthèse finale
    synthese = f"""# Synthèse orchestrateur multi-agents

## 1. Cadrage PO
{po_result}

## 2. Architecture
{archi_result}

## 3. Plan d'implémentation
{dev_result}

## 4. Stratégie IVVQ
{ivvq_result}
"""
    return synthese
