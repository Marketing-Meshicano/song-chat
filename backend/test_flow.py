# backend/test_flow.py

import sys
import os

# Añadir la carpeta actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_orchestrator import AgentOrchestrator

def main():
    orchestrator = AgentOrchestrator()

    # Prompt de prueba
    user_prompt = "Dame 10 canciones de rock de los 2010s que sean buenas para hacer ejercicio y que no sean explícitas"

    print("=" * 60)
    print(f"PROMPT DEL USUARIO: {user_prompt}")
    print("=" * 60)

    # Ejecutar el flujo completo
    result = orchestrator.run(user_prompt)

    print("\n--- RESULTADO FINAL ---")
    if result.analyst:
        print(result.analyst.final_response)
    else:
        print("No se generó respuesta final.")

    print("\n" + "=" * 60)
    print("LOGS DE EJECUCIÓN (Vista intermedia)")
    print("=" * 60)

    for log in result.execution_logs:
        print(f"\n[{log.agent_name.upper()}]")
        print(f"  Success: {log.success}")
        print(f"  Timestamp: {log.timestamp}")
        if log.error_message:
            print(f"  Error: {log.error_message}")
        if log.output:
            print(f"  Output: {log.output}")

    print("\n" + "=" * 60)
    print("FLUJO COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    main()