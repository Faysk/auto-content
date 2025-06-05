import os
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, nome_base="log", log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.nome_base = nome_base
        self.arquivo = self.log_dir / f"{self.nome_base}.log"
        self.linha("INÍCIO DO LOG")

    def log(self, mensagem: str):
        agora = datetime.now().strftime("%H:%M:%S")
        linha = f"[{agora}] {mensagem}"
        print(linha)
        with open(self.arquivo, "a", encoding="utf-8") as f:
            f.write(linha + "\n")

    def sucesso(self, mensagem: str):
        self.log(f"✅ {mensagem}")

    def erro(self, mensagem: str):
        self.log(f"❌ {mensagem}")

    def bloco(self, titulo: str):
        self.linha(titulo)

    def destaque(self, texto: str):
        self.log("=" * 60)
        self.log(texto)
        self.log("=" * 60)

    def linha(self, titulo=None):
        if titulo:
            self.log(f"\n=== {titulo} ===")
        else:
            self.log("-" * 40)

    def caminho(self):
        return str(self.arquivo.resolve())
