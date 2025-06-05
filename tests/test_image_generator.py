from pathlib import Path
import importlib

import pytest


# ensure modules are imported fresh for each test

def reload_image_module():
    import txt_image.core.image_generator as img_mod
    importlib.reload(img_mod)
    return img_mod


def test_gerar_imagem_com_prompt(monkeypatch):
    img_mod = reload_image_module()

    # fake nodes
    monkeypatch.setattr(img_mod.ckpt_mod, "carregar_checkpoint", lambda: "ckpt")
    monkeypatch.setattr(img_mod.latent_mod, "criar_latente", lambda: "latent")
    monkeypatch.setattr(img_mod.prompt_pos_mod, "aplicar_prompt", lambda text: {"pos": text})
    monkeypatch.setattr(img_mod.prompt_neg_mod, "aplicar_prompt", lambda text: {"neg": text})
    monkeypatch.setattr(img_mod.ksampler_mod, "gerar", lambda **kwargs: "ksampler")
    monkeypatch.setattr(img_mod.vae_mod, "decode", lambda ref: "vae")
    monkeypatch.setattr(img_mod.save_mod, "salvar", lambda ref, name: "save")
    monkeypatch.setattr(img_mod, "client_id", lambda: "cid123")

    captured = {}
    def fake_send(payload):
        captured["payload"] = payload
    monkeypatch.setattr(img_mod, "enviar_para_comfyui", fake_send)

    cid = img_mod.gerar_imagem_com_prompt(
        "positivo", "negativo", Path("/tmp"), "nome")

    assert cid == "cid123"
    assert captured["payload"] == {
        "client_id": "cid123",
        "prompt": {
            "checkpoint": "ckpt",
            "latent": "latent",
            "prompt_pos": {"pos": "positivo"},
            "prompt_neg": {"neg": "negativo"},
            "ksampler": "ksampler",
            "vae_decode": "vae",
            "save_image": "save",
        },
    }
