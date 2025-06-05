# watcher.py
import requests
import time
from datetime import datetime

COMFY_ENDPOINT = "http://192.168.15.12:8188/prompt"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def monitorar_fila(intervalo=2):
    log("📡 Iniciando monitoramento da fila do ComfyUI...")
    anterior = None
    while True:
        try:
            res = requests.get(COMFY_ENDPOINT)
            fila = res.json().get("exec_info", {}).get("queue_remaining", "?")
            if fila != anterior:
                log(f"🕒 Fila restante: {fila}")
                anterior = fila
            if fila == 0:
                log("✅ Fila finalizada.")
                break
        except Exception as e:
            log(f"❌ Erro ao consultar fila: {e}")
        time.sleep(intervalo)

if __name__ == "__main__":
    monitorar_fila()
