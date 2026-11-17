# backend/agent_orchestrator.py

import sys
import os
from datetime import datetime

# Añadir la carpeta actual al path para que Python encuentre los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import (
    QueryFlowResult,
    AgentExecutionLog,
    ReceptionistOutput,
    ManagerOutput,
    IngeOutput,
    AnalystOutput
)
from services.receptionist import ReceptionistAgent
from services.manager import ManagerAgent
from services.inge import IngeAgent
from services.analyst import AnalystAgent

class AgentOrchestrator:
    """Coordina el flujo completo de los 4 agentes."""

    def __init__(self):
        self.receptionist = ReceptionistAgent()
        self.manager = ManagerAgent()
        self.inge = IngeAgent()
        self.analyst = AnalystAgent()
        self.logs: list[AgentExecutionLog] = []

    def _log(self, agent_name: str, success: bool, input_prompt: str, output: dict | None, error: str | None = None):
        """Registra la ejecución de un agente."""
        log = AgentExecutionLog(
            agent_name=agent_name,
            success=success,
            input_prompt=input_prompt,
            output=output,
            error_message=error,
            timestamp=datetime.now()
        )
        self.logs.append(log)

    def run(self, user_prompt: str) -> QueryFlowResult:
        """Ejecuta todo el flujo de agentes."""
        self.logs = []  # Reiniciamos los logs en cada ejecución

        # 1. Recepcionista
        receptionist_output: ReceptionistOutput = self.receptionist.process(user_prompt)
        self._log(
            agent_name="receptionist",
            success=True,
            input_prompt=user_prompt,
            output=receptionist_output.model_dump()
        )

        if not receptionist_output.needs_database:
            # Si no necesita base de datos, el analista responde directamente
            analyst_output = self.analyst.process(user_prompt, None)
            self._log(
                agent_name="analyst",
                success=True,
                input_prompt=user_prompt,
                output=analyst_output.model_dump()
            )
            return QueryFlowResult(
                original_prompt=user_prompt,
                receptionist=receptionist_output,
                analyst=analyst_output,
                execution_logs=self.logs
            )

        # 2. Manager
        manager_output: ManagerOutput = self.manager.process(receptionist_output.cleaned_prompt)
        self._log(
            agent_name="manager",
            success=manager_output.is_valid,
            input_prompt=receptionist_output.cleaned_prompt,
            output=manager_output.model_dump()
        )

        if not manager_output.is_valid:
            # Si no es válida, el analista responde explicando por qué
            analyst_output = self.analyst.process(user_prompt, None)
            self._log(
                agent_name="analyst",
                success=True,
                input_prompt=user_prompt,
                output=analyst_output.model_dump()
            )
            return QueryFlowResult(
                original_prompt=user_prompt,
                receptionist=receptionist_output,
                manager=manager_output,
                analyst=analyst_output,
                execution_logs=self.logs
            )

        # 3. Inge
        inge_output: IngeOutput = self.inge.process(manager_output.technical_instructions or "")
        self._log(
            agent_name="inge",
            success=inge_output.execution_success,
            input_prompt=manager_output.technical_instructions or "",
            output=inge_output.model_dump()
        )

        # 4. Analista
        analyst_output: AnalystOutput = self.analyst.process(
            original_prompt=user_prompt,
            db_results=inge_output.results
        )
        self._log(
            agent_name="analyst",
            success=True,
            input_prompt=user_prompt,
            output=analyst_output.model_dump()
        )

        return QueryFlowResult(
            original_prompt=user_prompt,
            receptionist=receptionist_output,
            manager=manager_output,
            inge=inge_output,
            analyst=analyst_output,
            execution_logs=self.logs
        )