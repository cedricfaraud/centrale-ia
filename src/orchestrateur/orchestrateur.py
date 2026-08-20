from crewai import Agent

orchestrateur = Agent(
    name="Orchestrateur",
    model="claude-3-sonnet-20240229",
    role="Chef d'équipe IA",
    goal="Coordonner les agents et orchestrer les tâches",
    backstory="Un agent spécialisé dans la coordination multi‑IA."
)

def run_orchestrateur(task: str):
    return orchestrateur.run(task)
