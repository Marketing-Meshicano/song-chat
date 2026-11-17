song-chat/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── agent_orchestrator.py
│   ├── models.py
│   ├── database.py
│   ├── prompts/
│   │   ├── receptionist_prompt.py
│   │   ├── manager_prompt.py
│   │   ├── inge_prompt.py
│   │   └── analyst_prompt.py
│   ├── services/
│   │   ├── receptionist.py
│   │   ├── manager.py
│   │   ├── inge.py
│   │   └── analyst.py
│   └── test_flow.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── data/
│   └── songs.db
├── requirements.txt
└── .env

## HOW TO RUN ##

1. Instala las dependencias:
   pip install -r requirements.txt

2. Crea un archivo .env en la raíz del proyecto con tu API key:
   XAI_API_KEY=tu_api_key_aqui
   GROK_MODEL=grok-3

3. Para probar el flujo de agentes:
   python -m backend.test_flow

4. Para correr la API con FastAPI:
   uvicorn backend.main:app --reload