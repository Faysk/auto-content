import json
from pathlib import Path
import importlib

import pytest


def setup_module(module):
    # ensure OPENAI_API_KEY exists before importing modules that require it
    import os
    os.environ.setdefault("OPENAI_API_KEY", "test-key")


def reload_text_modules():
    """Reload modules to apply patches cleanly."""
    import text_generator.text_gerador_local as local_mod
    import text_generator.text_creator as creator_mod
    importlib.reload(local_mod)
    importlib.reload(creator_mod)
    return local_mod, creator_mod


def test_gerar_texto_local_returns_phrase(tmp_path, monkeypatch):
    frases_file = tmp_path / "frases.json"
    frases_file.write_text(json.dumps(["frase1", "frase2"]), encoding="utf-8")

    local_mod, creator_mod = reload_text_modules()

    monkeypatch.setattr(local_mod, "LOCAL_FRASES_PATH", Path(frases_file))
    monkeypatch.setattr(local_mod.random, "choice", lambda seq: seq[0])

    texto = creator_mod.gerar_texto_local()
    assert texto == "frase1"


def test_gerar_texto_local_missing_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "nao_existe.json"

    local_mod, creator_mod = reload_text_modules()

    monkeypatch.setattr(local_mod, "LOCAL_FRASES_PATH", Path(missing_file))

    texto = creator_mod.gerar_texto_local()
    assert "Arquivo não encontrado" in texto
