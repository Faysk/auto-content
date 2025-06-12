import asyncio

# 🧠 Texto & utilidades
from text_generator.text_creator import gerar_texto, slugify
from text_to_speech.tts_generator import gerar_audio_e_legenda


async def executar_fluxo() -> None:
    """Gera texto e converte o resultado em áudio."""
    print("🚀 Iniciando sessão de geração de microconteúdo...")

    texto = gerar_texto()
    nome_base = slugify(texto.split("\n")[0])

    await gerar_audio_e_legenda(texto, nome_base)

    print("✅ Texto e áudio gerados com sucesso.")


if __name__ == "__main__":
    asyncio.run(executar_fluxo())
