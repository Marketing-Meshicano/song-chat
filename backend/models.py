from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# ============================================
# Modelos de salida de cada agente
# ============================================

class ReceptionistOutput(BaseModel):
    needs_database: bool
    cleaned_prompt: str
    reason: Optional[str] = None


class ManagerOutput(BaseModel):
    is_valid: bool
    technical_instructions: Optional[str] = None
    validation_notes: Optional[str] = None


class IngeOutput(BaseModel):
    sql_query: Optional[str] = None
    execution_success: bool
    results: Optional[list[dict]] = None
    error_message: Optional[str] = None


class AnalystOutput(BaseModel):
    final_response: str
    used_data: bool


# ============================================
# Log mejorado para identificar errores
# ============================================

class AgentExecutionLog(BaseModel):
    """Registro detallado de cada agente (optimizado para debugging y errores)"""
    agent_name: Literal["receptionist", "manager", "inge", "analyst"]
    success: bool
    input_prompt: str
    output: Optional[dict] = None
    error_message: Optional[str] = None
    raw_response: Optional[str] = None
    model_used: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    execution_time_ms: Optional[float] = None


# ============================================
# Resultado completo del flujo
# ============================================

class QueryFlowResult(BaseModel):
    """Resultado final del flujo completo de los 4 agentes"""
    original_prompt: str
    receptionist: ReceptionistOutput
    manager: Optional[ManagerOutput] = None
    inge: Optional[IngeOutput] = None
    analyst: Optional[AnalystOutput] = None
    execution_logs: list[AgentExecutionLog] = Field(default_factory=list)
    total_execution_time_ms: Optional[float] = None