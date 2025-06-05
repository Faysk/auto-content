import os
import subprocess
from core.checkpoint_cycle import advance_checkpoint, get_current_checkpoint
from core.runner import log
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def fila_esta_vazia(endpoint):
    try:
        fila = requests.get(endpoint).json()
        return fila.get("exec_info", {}).get("queue_remaining", 1) == 0
    except:
        return False

def gerar_imagens_por_checkpoint(quantidade=6):
    for i in range(quantidade):
        log(f"🚀 Enviando imagem {i+1}/{quantidade} com checkpoint: {get_current_checkpoint()}")
        subprocess.run(["python", "main.py"])
        time.sleep(1)

def loop_checkpoints():
    while True:
        gerar_imagens_por_checkpoint(6)

        log("⏳ Aguardando fila zerar antes de trocar o checkpoint...")
        while not fila_esta_vazia(os.getenv("COMFY_ENDPOINT", "http://192.168.15.12:8188/prompt")):
            time.sleep(5)

        novo = advance_checkpoint()
        log(f"🔁 Checkpoint trocado para: {novo}")

if __name__ == "__main__":
    loop_checkpoints()
