# backend/main.py

import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_orchestrator import AgentOrchestrator

app = FastAPI(title="Song Chat API", version="1.0")

# Permitir CORS (necesario para el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción deberías restringirlo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = AgentOrchestrator()


class UserPrompt(BaseModel):
    prompt: str


@app.post("/query")
def process_query(user_input: UserPrompt):
    """
    Recibe un prompt del usuario y ejecuta todo el flujo de agentes.
    Devuelve la respuesta final y los logs intermedios.
    """
    result = orchestrator.run(user_input.prompt)
    return result


@app.get("/")
def root():
    return {"message": "Song Chat API activa"}


@app.get("/health")
def health_check():
    return {"status": "ok"}