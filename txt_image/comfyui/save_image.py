from pathlib import Path
from typing import Union

def salvar(vae_output_ref: list, path: Union[str, Path]):
    """
    Retorna o node 'SaveImage' com referência correta ao output do VAE.
    Espera-se que 'vae_output_ref' seja do tipo ["vae_decode", 0].
    """
    return {
        "class_type": "SaveImage",
        "inputs": {
            "images": vae_output_ref,
            "filename_prefix": str(Path(path).stem)
        }
    }

def node_save_image(nome_arquivo: str):
    """
    Versão manual estática, apontando para o output de vae_decode.
    """
    return "save_image", {
        "class_type": "SaveImage",
        "inputs": {
            "images": ["vae_decode", 0],
            "filename_prefix": str(nome_arquivo)
        }
    }
