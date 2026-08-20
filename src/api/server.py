from fastapi import FastAPI
from src.orchestrateur.graph import app as orchestrateur_app


api = FastAPI()

@api.post("/run")
async def run_task(payload: dict):
    task = payload.get("task", "")
    result = orchestrateur_app.invoke({"input": task})
    return {"result": result}
