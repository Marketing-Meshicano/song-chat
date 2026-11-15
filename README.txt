song-chat/
├── backend/
│   ├── main.py
│   ├── database.py
│   └── services/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── data/
│   └── songs.db          ← SQLite
└── requirements.txt

##HOW TO RUN##

First, execute: 
pip install -r requirements.txt

If you want to change model add this line to the env. file:
GROK_MODEL=grok-4.20-multi-agent-latest
