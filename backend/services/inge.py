import json
import sqlite3
from openai import OpenAI
from pydantic import ValidationError

from models import IngeOutput
from prompts.inge_prompt import INGE_SYSTEM_PROMPT
from config import GROK_MODEL, XAI_API_KEY

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


class IngeAgent:
    """Agente Inge: genera y ejecuta consultas SQL."""

    def __init__(self, db_path: str = "data/songs.db"):
        self.model = GROK_MODEL
        self.db_path = db_path

    def _execute_query(self, sql_query: str) -> tuple[bool, list | str]:
        """Ejecuta una consulta SQL y retorna los resultados o un error."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
            conn.close()
            return True, results
        except Exception as e:
            return False, str(e)

    def process(self, technical_instructions: str) -> IngeOutput:
        """
        Recibe instrucciones técnicas del Manager, genera una consulta SQL
        y la ejecuta contra la base de datos.
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": INGE_SYSTEM_PROMPT},
                    {"role": "user", "content": technical_instructions}
                ],
                temperature=0.1,
            )

            message_content = response.choices[0].message.content

            if message_content is None:
                return IngeOutput(
                    sql_query=None,
                    execution_success=False,
                    results=None,
                    error_message="La IA no devolvió contenido"
                )

            content = message_content.strip()
            data = json.loads(content)
            sql_query = data.get("sql_query")

            # Ejecutar la consulta
            success, execution_result = self._execute_query(sql_query)

            if success:
                return IngeOutput(
                    sql_query=sql_query,
                    execution_success=True,
                    results=execution_result,           # Aquí execution_result es una lista
                    error_message=None
                )
            else:
                return IngeOutput(
                    sql_query=sql_query,
                    execution_success=False,
                    results=None,
                    error_message=execution_result      # Aquí execution_result es un string
                )

        except json.JSONDecodeError as e:
            return IngeOutput(
                sql_query=None,
                execution_success=False,
                results=None,
                error_message=f"Error al parsear JSON del Inge: {e}"
            )

        except Exception as e:
            return IngeOutput(
                sql_query=None,
                execution_success=False,
                results=None,
                error_message=f"Error inesperado en IngeAgent: {e}"
            )