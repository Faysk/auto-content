def decode(samples_ref: list):
    """
    Retorna o node 'VAEDecode' com a entrada 'samples' como referência ao output do KSampler.
    Exemplo: decode(["ksampler", 0])
    """
    return {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": samples_ref,
            "vae": ["checkpoint", 2]
        }
    }

def node_vae_decode():
    """
    Retorno manual fixo para testes.
    """
    return "vae_decode", decode(["ksampler", 0])
