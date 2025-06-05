from pathlib import Path
from txt_image.comfyui import (
    checkpoint as ckpt_mod,
    latent_image as latent_mod,
    prompt_positivo as prompt_pos_mod,
    prompt_negativo as prompt_neg_mod,
    ksampler as ksampler_mod,
    vae_decode as vae_mod,
    save_image as save_mod
)
from txt_image.core.api import enviar_para_comfyui
from txt_image.comfyui.utils import client_id

def gerar_imagem_com_prompt(prompt_positivo: str, prompt_negativo: str, output_path: Path, nome_base: str) -> str:
    print(f"🖼️ Montando payload para: {nome_base}")

    # 1. Criar os nodes do pipeline ComfyUI
    nodes = {
        "checkpoint": ckpt_mod.carregar_checkpoint(),
        "latent": latent_mod.criar_latente(),
        "prompt_pos": prompt_pos_mod.aplicar_prompt(prompt_positivo),
        "prompt_neg": prompt_neg_mod.aplicar_prompt(prompt_negativo),
    }

    # 2. KSampler com todas as referências corretas
    nodes["ksampler"] = ksampler_mod.gerar(
        latent=["latent", 0],
        checkpoint=["checkpoint", 0],
        prompt_pos=["prompt_pos", 0],
        prompt_neg=["prompt_neg", 0]
    )

    # 3. VAEDecode (referência ao output do KSampler)
    nodes["vae_decode"] = vae_mod.decode(["ksampler", 0])

    # 4. SaveImage (referência ao output do VAE)
    nodes["save_image"] = save_mod.salvar(["vae_decode", 0], nome_base)

    # 5. Payload final com client_id
    cid = client_id()
    payload = {
        "client_id": cid,
        "prompt": nodes
    }

    # 6. Enviar para ComfyUI
    enviar_para_comfyui(payload)

    print(f"✅ Payload enviado para ComfyUI com prefixo '{nome_base}'")
    return cid
