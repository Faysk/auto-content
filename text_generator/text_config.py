# text_generator/text_config.py

import os
import sys
import openai
from pathlib import Path
from dotenv import load_dotenv

# 🌱 Carrega variáveis do .env
load_dotenv()

# 📁 Diretório base deste arquivo
BASE_DIR = Path(__file__).resolve().parent
PROMPT_DIR = BASE_DIR / "data" / "inputs"
LOCAL_FRASES_PATH = PROMPT_DIR / "frases.json"

# 🔐 API Key obrigatória
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY não definida no .env")

# 🤖 Modelo (GPT-3.5, GPT-4o, etc.)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# 💰 Custo por 1k tokens
try:
    TOKEN_PRICE = float(os.getenv("TOKEN_PRICE", "0.0015"))
except ValueError:
    TOKEN_PRICE = 0.0015
    print("⚠️ Valor inválido em TOKEN_PRICE, usando 0.0015")

# 📜 Prompt padrão: tenta pegar do .env, senão de arquivos .txt
PROMPT_PADRAO = os.getenv("TEXT_PROMPT")

if not PROMPT_PADRAO:
    try:
        if not PROMPT_DIR.exists():
            raise FileNotFoundError(f"Pasta não encontrada: {PROMPT_DIR}")

        txt_files = list(PROMPT_DIR.glob("*.txt"))
        prompt_encontrado = False

        for file_path in txt_files:
            content = file_path.read_text(encoding="utf-8").strip()
            if content:
                PROMPT_PADRAO = content
                print(f"📄 Prompt carregado de: {file_path.name}")
                prompt_encontrado = True
                break

        if not prompt_encontrado:
            raise FileNotFoundError("Nenhum arquivo .txt com conteúdo válido encontrado.")

    except Exception as e:
        print("❌ Nenhum prompt encontrado em arquivos ou .env.")
        print("🔍 Crie um arquivo `.txt` com conteúdo dentro da pasta `/data/inputs/`")
        print(f"📦 Detalhe do erro: {e}")
        print("🛑 Encerrando execução.")
        sys.exit(1)

# 🎛️ Cliente OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)
