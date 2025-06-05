from txt_image.core.checkpoint_cycle import get_current_checkpoint

def carregar_checkpoint():
    return {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": f"{get_current_checkpoint()}"
        }
    }

# Opcional para compatibilidade
def node_checkpoint():
    return "checkpoint", carregar_checkpoint()
