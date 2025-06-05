import random

def gerar(latent, checkpoint, prompt_pos, prompt_neg):
    return {
        "class_type": "KSampler",
        "inputs": {
            "seed": random.randint(0, 2**31 - 1),  # Seed aleatória de 32 bits
            "steps": 60,
            "cfg": 6,
            "sampler_name": "dpmpp_3m_sde_gpu",
            "scheduler": "karras",
            "denoise": 0.9,
            "model": checkpoint,
            "positive": prompt_pos,
            "negative": prompt_neg,
            "latent_image": latent
        }
    }
