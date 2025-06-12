import os
import re
import asyncio
import edge_tts
import unicodedata

# 🔧 Configurações
from .tts_config import VOICE, RATE, OUTPUT_DIR

# 🔁 Importa gerador de texto e utilitários
from text_generator.text_creator import gerar_texto, slugify

def limpar_texto_para_tts(texto: str) -> str:
    """
    Remove símbolos problemáticos, normaliza o texto e limpa marcas como 'Chapter 1'.
    """
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')  # remove acentos
    linhas = texto.strip().splitlines()
    linhas_limpas = []

    for linha in linhas:
        linha = re.sub(r"(?i)(chapter|cap[ií]tulo)\s*\d+\s*[-:]*\s*", "", linha)
        linha = re.sub(r"[*•#>]+", "", linha)
        linha = re.sub(r"\s{2,}", " ", linha)
        linhas_limpas.append(linha.strip())

    return "\n".join(linhas_limpas).strip()

def quebrar_em_linhas_simples(texto: str, max_palavras: int = 10) -> list[str]:
    """
    Quebra o texto em blocos de no máximo `max_palavras` palavras.
    """
    palavras = texto.split()
    linhas = []

    for i in range(0, len(palavras), max_palavras):
        linha = " ".join(palavras[i:i + max_palavras])
        linhas.append(linha)

    return linhas

def salvar_legenda_simples(linhas: list[str], caminho_srt: str):
    """
    Salva o conteúdo da legenda como texto simples, uma linha por vez.
    """
    with open(caminho_srt, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(f"{linha}\n")

async def gerar_audio_e_legenda(texto: str, nome_base: str = None):
    """
    Gera áudio narrado (.mp3) e legenda simples (.srt) em inglês.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    texto_limpo = limpar_texto_para_tts(texto)
    if not texto_limpo.strip():
        print("⚠️ Texto vazio após limpeza.")
        return

    if not nome_base:
        nome_base = slugify(texto_limpo.splitlines()[0])

    caminho_mp3 = os.path.join(OUTPUT_DIR, f"{nome_base}.mp3")
    caminho_srt = os.path.join(OUTPUT_DIR, f"{nome_base}.srt")

    linhas_legenda = quebrar_em_linhas_simples(texto_limpo, max_palavras=10)

    # Remove mp3 antigo, se existir
    if os.path.exists(caminho_mp3):
        os.remove(caminho_mp3)

    # Gera áudio com edge-tts
    communicate = edge_tts.Communicate(" ".join(linhas_legenda), voice=VOICE, rate=RATE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            with open(caminho_mp3, "ab") as f:
                f.write(chunk["data"])

    # Salva legenda simplificada
    salvar_legenda_simples(linhas_legenda, caminho_srt)

    print(f"🔊 Audio saved: {caminho_mp3}")
    print(f"📄 Simple text caption saved: {caminho_srt}")

# Execução direta
if __name__ == "__main__":
    texto = gerar_texto()
    asyncio.run(gerar_audio_e_legenda(texto))
    print("\n✅ English text, audio and .srt generated successfully.")
