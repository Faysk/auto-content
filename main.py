import asyncio
from pathlib import Path
from datetime import datetime

# 🧠 Texto & utilidades
from text_generator.text_creator import gerar_texto, slugify
from text_to_speech.tts_generator import gerar_audio_e_legenda, quebrar_em_linhas_simples

# 🎯 Prompts e vídeo
try:
    from video_generator.prompt_generator import gerar_prompts_para_trecho
    from video_generator.comfy_generator import gerar_video_para_trecho
    from video_generator.logger import iniciar_logger
    VIDEO_ENABLED = True
except ModuleNotFoundError:
    VIDEO_ENABLED = False

    def gerar_prompts_para_trecho(trecho: str) -> dict:
        return {"prompt": trecho}

    def gerar_video_para_trecho(**kwargs) -> None:
        print("📽️ Módulo de vídeo ausente. Pulando geração de vídeo.")

    def iniciar_logger(nome: str):
        def log(msg: str) -> None:
            print(msg)

        return log

# 📁 Diretórios principais
base_dir = Path(__file__).resolve().parent
outputs_dir = base_dir / "video_generator" / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)

# 🗂️ Nome base da sessão
data_str = datetime.now().strftime("%Y%m%d_%H%M%S")
log = iniciar_logger(f"sessao_{data_str}")

async def executar_fluxo():
    log("🚀 Iniciando sessão de geração de microconteúdo...")

    # 1. Texto principal (ex: resumo de livro)
    texto = gerar_texto()
    nome_base = slugify(texto.split("\n")[0]) + f"_{data_str}"
    linhas = quebrar_em_linhas_simples(texto, max_palavras=10)

    # 2. Gera áudio e legenda com base no texto inteiro
    await gerar_audio_e_legenda(texto, nome_base)

    # 3. Para cada trecho textual → gerar vídeo correspondente
    for i, trecho in enumerate(linhas):
        try:
            log(f"\n🎬 Trecho {i:02} → '{trecho}'")

            # Gera prompts positivos e negativos via GPT-4o
            prompts = gerar_prompts_para_trecho(trecho)

            # Chama geração do vídeo
            gerar_video_para_trecho(
                prompt_texto=prompts["prompt"],
                nome_base=nome_base,
                id_trecho=i
            )

        except Exception as e:
            log(f"❌ Falha no trecho {i:02}: {e}")

    log("\n✅ Sessão concluída com sucesso.")

# 🎯 Execução principal
if __name__ == "__main__":
    asyncio.run(executar_fluxo())
