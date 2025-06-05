# text_gerador_api.py

from text_generator.text_config import client, OPENAI_MODEL, TOKEN_PRICE

def gerar_texto_ia(prompt: str) -> str:
    """
    Gera texto usando a API da OpenAI.
    
    Parâmetros:
        prompt (str): Texto base enviado para o modelo gerar a resposta.

    Retorno:
        str: Texto gerado pela IA.
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4096
        )

        texto = response.choices[0].message.content.strip()

        # Informações sobre o uso da API
        if hasattr(response, "usage"):
            tokens = response.usage.total_tokens
            custo = (tokens / 1000) * TOKEN_PRICE
            print(f"🧾 Tokens usados: {tokens} | Custo estimado: U${custo:.5f}")

        return texto

    except Exception as e:
        raise RuntimeError(f"Erro ao gerar texto com OpenAI: {e}")
