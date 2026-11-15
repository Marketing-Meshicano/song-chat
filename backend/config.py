import os
from dotenv import load_dotenv

load_dotenv()

# Modelo de Grok que usarán todos los agentes
GROK_MODEL = os.getenv("GROK_MODEL", "grok-3")

# API Key
XAI_API_KEY = os.getenv("XAI_API_KEY")