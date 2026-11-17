# backend/services/receptionist.py

import json
from openai import OpenAI
from pydantic import ValidationError

from models import ReceptionistOutput
from prompts.receptionist_prompt import RECEPCIONISTA_SYSTEM_PROMPT
from config import GROK_MODEL, XAI_API_KEY

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


class ReceptionistAgent:
    """Agente Recepcionista: decide si se necesita consultar la base de datos."""

    def __init__(self):
        self.model = GROK_MODEL

    def process(self, user_prompt: str) -> ReceptionistOutput:
        """
        Procesa el prompt del usuario y decide si se necesita consultar la base de datos.
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": RECEPCIONISTA_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
            )

            message_content = response.choices[0].message.content

            if message_content is None:
                return ReceptionistOutput(
                    needs_database=False,
                    cleaned_prompt=user_prompt,
                    reason="La IA no devolvió contenido"
                )

            content = message_content.strip()
            data = json.loads(content)
            return ReceptionistOutput(**data)

        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON del Recepcionista: {e}")
            return ReceptionistOutput(
                needs_database=False,
                cleaned_prompt=user_prompt,
                reason="Error al procesar la respuesta de la IA"
            )

        except ValidationError as e:
            print(f"Error de validación del modelo: {e}")
            return ReceptionistOutput(
                needs_database=False,
                cleaned_prompt=user_prompt,
                reason="Respuesta de la IA no válida"
            )

        except Exception as e:
            print(f"Error inesperado en ReceptionistAgent: {e}")
            return ReceptionistOutput(
                needs_database=False,
                cleaned_prompt=user_prompt,
                reason="Error inesperado al procesar la solicitud"
            )