import os
import requests
from datetime import datetime
from core.runner import log
from dotenv import load_dotenv
from txt_image.core.runner import log

load_dotenv()

COMFY_ENDPOINT = os.getenv("COMFY_ENDPOINT", "http://192.168.15.12:8188")

def show_status():
    try:
        response = requests.get(f"{COMFY_ENDPOINT}/prompt")
        data = response.json()

        queue = data.get("exec_info", {}).get("queue_remaining", "?")

        log("📊 STATUS DO COMFYUI:")
        log(f"→ Prompts na fila: {queue}")

        # Se houver mais dados, exiba também
        if "exec_info" in data:
            for key, value in data["exec_info"].items():
                if key != "queue_remaining":
                    log(f"→ {key}: {value}")

        print()
    except Exception as e:
        log(f"Erro ao consultar status do ComfyUI: {e}", ok=False)
