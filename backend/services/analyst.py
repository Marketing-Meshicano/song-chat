# backend/services/analyst.py

import json
from openai import OpenAI
from pydantic import ValidationError

from models import AnalystOutput
from prompts.analyst_prompt import ANALYST_SYSTEM_PROMPT
from config import GROK_MODEL, XAI_API_KEY

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


class AnalystAgent:
    """Agente Analista: genera la respuesta final para el usuario."""

    def __init__(self):
        self.model = GROK_MODEL

    def process(self, original_prompt: str, db_results: list[dict] | None) -> AnalystOutput:
        """
        Genera una respuesta final natural combinando el prompt original
        y los resultados de la base de datos.
        """
        try:
            context = f"""Prompt original del usuario: {original_prompt}

Resultados de la base de datos: {db_results if db_results else 'No se encontraron resultados'}"""

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ANALYST_SYSTEM_PROMPT},
                    {"role": "user", "content": context}
                ],
                temperature=0.4,
            )

            message_content = response.choices[0].message.content

            if message_content is None:
                return AnalystOutput(
                    final_response="Lo siento, no pude generar una respuesta en este momento.",
                    used_data=bool(db_results)
                )

            content = message_content.strip()
            data = json.loads(content)
            return AnalystOutput(**data)

        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON del Analista: {e}")
            return AnalystOutput(
                final_response="Ocurrió un error al procesar la respuesta.",
                used_data=bool(db_results)
            )

        except ValidationError as e:
            print(f"Error de validación del modelo Analyst: {e}")
            return AnalystOutput(
                final_response="La respuesta generada no tiene el formato esperado.",
                used_data=bool(db_results)
            )

        except Exception as e:
            print(f"Error inesperado en AnalystAgent: {e}")
            return AnalystOutput(
                final_response="Ocurrió un error inesperado al generar la respuesta final.",
                used_data=bool(db_results)
            )