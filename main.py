from fastapi import FastAPI
from agents import orchestrateur, architecte, dev, po, ivvq

app = FastAPI()

@app.post("/projet")
def lancer_projet(description: str):
    backlog = po(f"Crée le backlog complet pour : {description}")
    archi = architecte(f"Propose l'architecture complète pour : {description}")
    code = dev(f"Commence à coder le cœur du projet : {description}")
    tests = ivvq(f"Propose les tests IVVQ pour : {description}")

    return {
        "backlog": backlog,
        "architecture": archi,
        "code": code,
        "tests": tests,
    }

@app.post("/chef-de-projet")
def chef_de_projet(description: str):
    """
    Route chef de projet : un seul prompt, toute l'équipe travaille.
    """
    # Le chef de projet (orchestrateur) reformule le besoin
    synthese = orchestrateur(
        f"Tu es chef de projet. Reformule clairement le besoin suivant : {description}"
    )

    backlog = po(
        f"À partir de ce besoin reformulé, crée un backlog complet, structuré en user stories : {synthese}"
    )

    archi = architecte(
        f"À partir de ce besoin reformulé, propose une architecture technique complète, modulaire : {synthese}"
    )

    code = dev(
        f"Commence à implémenter le cœur du système en respectant l'architecture suivante : {archi}"
    )

    tests = ivvq(
        f"Propose un plan de tests IVVQ détaillé pour valider ce système : {synthese}"
    )

    return {
        "synthese": synthese,
        "backlog": backlog,
        "architecture": archi,
        "code": code,
        "tests": tests,
    }
