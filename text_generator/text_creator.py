# text_generator/text_creator.py

import re
from text_config import PROMPT_PADRAO
from text_gerador_api import gerar_texto_ia
from text_gerador_local import gerar_texto_local

def gerar_texto(prompt: str = PROMPT_PADRAO) -> str:
    """
    Gera texto usando a API da OpenAI.
    Se houver erro ou indisponibilidade, utiliza fallback local.
    """
    try:
        print("⚙️  Gerando texto via OpenAI...")
        return gerar_texto_ia(prompt)
    except Exception as e:
        print(f"⚠️ Erro ao usar API: {e}")
        print("🔄 Usando frase local como fallback...")
        return gerar_texto_local()

def slugify(text: str, max_length: int = 50) -> str:
    """
    Converte um texto em um nome de arquivo seguro (slug).
    Remove acentos, caracteres especiais e limita tamanho.
    """
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)        # Remove caracteres especiais
    text = re.sub(r"[\s_-]+", "_", text)        # Espaços e hífens → underscore
    return text[:max_length]

# Teste isolado
if __name__ == "__main__":
    texto = gerar_texto()
    print("\n📜 Texto gerado:\n")
    print(texto)
