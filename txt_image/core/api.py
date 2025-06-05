import os
import requests
from dotenv import load_dotenv

load_dotenv()

COMFY_ENDPOINT = os.getenv("COMFY_ENDPOINT", "http://192.168.15.12:8188/prompt")

def enviar_para_comfyui(payload: dict):
    response = requests.post(COMFY_ENDPOINT, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Erro ComfyUI: {response.status_code} - {response.text}")
    return response.json()
