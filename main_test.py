import sys
import json
import importlib
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# 📁 Caminho para os nodes
subdir = Path(__file__).resolve().parent / "image_video" / "comfyui_txt_img_vid"
sys.path.append(str(subdir))

# 🔧 Funções utilitárias
from image_video.comfyui_txt_img_vid.utils import carregar_config

# Lista dos nodes na ordem correta
ORDEM_TESTE = [
    "01_checkpoint_img",
    "02_latent_image",
    "03_prompt_positivo",
    "04_prompt_negativo",
    "05_ksampler_img",
    "06_vae_decode_img",
    "08_checkpoint_svd",
    "14_prompt_positivo_video",  # agora node 08
    "15_prompt_negativo_video",  # agora node 09
    "07_svd_conditioning"
]

COMFY_URL = "http://127.0.0.1:8188"


def montar_payload_teste(config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    payload = {}
    print("⚙️ Montando payload mínimo de teste...\n")

    for idx, nome in enumerate(ORDEM_TESTE):
        try:
            mod = importlib.import_module(nome)
            func = getattr(mod, f"node_{nome}")
            node = func(config)
            payload[str(idx).zfill(2)] = node

            if nome == "07_svd_conditioning":
                print(f"\n🔎 Diagnóstico: prompts estão vindo de nodes 08 e 09 (CLIPTextEncode)")
                print(f"   ➕ Prompt Positivo: {config.get('prompt')}")
                print(f"   ➖ Prompt Negativo: {config.get('negative_prompt')}")

            print(f"  ✅ Node {idx:02} - {nome}")
        except Exception as e:
            print(f"  ❌ Erro no node {nome}: {e}")
            raise

    return payload


def aguardar_resposta(prompt_id: str, timeout=120):
    print(f"\n🕒 Aguardando resposta do ComfyUI para prompt_id: {prompt_id}")
    inicio = time.time()
    while time.time() - inicio < timeout:
        resp = requests.get(f"{COMFY_URL}/history")
        if resp.status_code == 200:
            historico = resp.json()
            if prompt_id in historico:
                resultado = historico[prompt_id]
                if "outputs" in resultado:
                    print(f"✅ Execução concluída em {int(time.time() - inicio)}s")
                    return resultado
                if "error" in resultado:
                    print("❌ Erro detectado:", resultado["error"])
                    return None
        time.sleep(2)
    print("⏱️ Tempo limite excedido sem resposta.")
    return None


if __name__ == "__main__":
    print("🔍 Diagnóstico de Prompt no SVD Conditioning + Execução\n")

    config_path = subdir / "config.json"
    if not config_path.exists():
        print(f"❌ Configuração não encontrada: {config_path}")
        sys.exit(1)

    config = carregar_config(str(config_path))
    config.update({
        "prompt": "Two dads with contrasting philosophies standing in dramatic lighting",
        "negative_prompt": "blurry, distorted, cartoonish, low quality",
        "filename_prefix": "prompt_test",
        "seed": 123456789
    })

    if not config["prompt"]:
        print("❌ Prompt vazio no config. Corrija isso.")
        sys.exit(1)

    payload = montar_payload_teste(config)

    try:
        print("\n📡 Enviando payload para ComfyUI...")
        response = requests.post(f"{COMFY_URL}/prompt", json=payload)
        if response.status_code != 200:
            print(f"❌ Erro ao enviar payload: {response.text}")
            sys.exit(1)

        resposta = response.json()
        prompt_id = resposta.get("prompt_id")
        if not prompt_id:
            print("❌ 'prompt_id' ausente na resposta.")
            sys.exit(1)

        aguardar_resposta(prompt_id)

    except Exception as e:
        print(f"❌ Erro inesperado ao enviar ou aguardar payload: {e}")
