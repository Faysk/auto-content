def criar_latente():
    """
    Retorna o node 'EmptyLatentImage' configurado com resolução vertical (720x1280)
    e batch_size = 1, ideal para geração de imagens estilo retrato.
    """
    return {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "width": 720,
            "height": 1280,
            "batch_size": 1
        }
    }
