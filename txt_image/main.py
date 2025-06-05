import os
import requests
from datetime import datetime
from comfyui.utils import slugify, client_id
from core.runner import load_nodes, log
from core.monitor import show_status
from dotenv import load_dotenv

load_dotenv()

from txt_image.comfyui.utils import slugify, client_id
from txt_image.core.runner import load_nodes, log
from txt_image.core.monitor import show_status

# === Configurações ===
COMFY_ENDPOINT = os.getenv(
    "COMFY_ENDPOINT", "http://192.168.15.12:8188/prompt"
)
COMFY_OUTPUT_DIR = "ComfyUI/output"  # ajuste se for diferente no seu setup
DRY_RUN = False

# === Nome de saída com timestamp ===
NOME_ARQUIVO = f"Comfy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
nome_arquivo = slugify(NOME_ARQUIVO)

# === Monta o payload completo ===
payload = {
    "prompt": load_nodes(trecho=None, nome_arquivo=nome_arquivo),
    "client_id": client_id()
}

# === Execução ===
if DRY_RUN:
    log(f"[DRY RUN] Payload para '{nome_arquivo}':", ok=True)
    print(payload)
else:
    try:
        # Envia para a API do ComfyUI
        response = requests.post(COMFY_ENDPOINT, json=payload)
        success = response.status_code == 200
        log(f"Imagem gerada: '{nome_arquivo}.png' | Status: {response.status_code}", success)

        show_status()  # Mostra status da fila no momento

        if success:
            # Aguarda, detecta e move a(s) imagem(ns)
            log("✅ Payload enviado com sucesso. Use watcher.py para monitorar a fila.")

        else:
            print(response.text)

    except Exception as e:
        log(f"Erro ao enviar payload: {e}", ok=False)
