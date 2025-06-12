# text_gerador_local.py

import json
import random
from text_config import LOCAL_FRASES_PATH

def gerar_texto_local() -> str:
    """
    Retorna uma frase aleatória do arquivo local `frases.json`.

    Retorno:
        str: Frase aleatória ou mensagem de erro amigável.
    """
    try:
        with open(LOCAL_FRASES_PATH, "r", encoding="utf-8") as f:
            frases = json.load(f)

        if not isinstance(frases, list) or not frases:
            raise ValueError("Arquivo de frases está vazio ou mal formatado.")

        return random.choice(frases)

    except FileNotFoundError:
        return f"⚠️ Arquivo não encontrado: {LOCAL_FRASES_PATH}"
    except json.JSONDecodeError:
        return "⚠️ Erro ao ler o arquivo: JSON mal formatado."
    except Exception as e:
        return f"⚠️ Erro inesperado ao acessar frases locais: {e}"
