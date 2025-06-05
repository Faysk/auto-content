def aplicar_prompt(texto: str):
    return {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["checkpoint", 1],
            "text": texto.strip()
        }
    }
