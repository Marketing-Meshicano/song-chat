# backend/services/manager.py

import json
from openai import OpenAI
from pydantic import ValidationError

from models import ManagerOutput
from prompts.manager_prompt import MANAGER_SYSTEM_PROMPT
from config import GROK_MODEL, XAI_API_KEY

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


class ManagerAgent:
    """Agente Manager: valida la solicitud y genera instrucciones técnicas."""

    def __init__(self):
        self.model = GROK_MODEL

    def process(self, cleaned_prompt: str) -> ManagerOutput:
        """
        Valida la solicitud y genera instrucciones técnicas para el Inge.
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": MANAGER_SYSTEM_PROMPT},
                    {"role": "user", "content": cleaned_prompt}
                ],
                temperature=0.2,
            )

            message_content = response.choices[0].message.content

            if message_content is None:
                return ManagerOutput(
                    is_valid=False,
                    technical_instructions=None,
                    validation_notes="La IA no devolvió contenido"
                )

            content = message_content.strip()
            data = json.loads(content)
            return ManagerOutput(**data)

        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON del Manager: {e}")
            return ManagerOutput(
                is_valid=False,
                technical_instructions=None,
                validation_notes="Error al procesar la respuesta de la IA"
            )

        except ValidationError as e:
            print(f"Error de validación del modelo Manager: {e}")
            return ManagerOutput(
                is_valid=False,
                technical_instructions=None,
                validation_notes="Respuesta de la IA no válida"
            )

        except Exception as e:
            print(f"Error inesperado en ManagerAgent: {e}")
            return ManagerOutput(
                is_valid=False,
                technical_instructions=None,
                validation_notes="Error inesperado al procesar la solicitud"
            )