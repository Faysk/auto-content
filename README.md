# 🤖 Projeto de Geração de Conteúdo Automatizado

Este projeto gera frases, curiosidades e roteiros curtos automaticamente, ideais para vídeos verticais (TikTok, Reels, Shorts, etc.).

💡 Utiliza a OpenAI (GPT) para geração de texto com fallback local, conversão em áudio com voz neural e estrutura modular preparada para renderização de vídeo e publicação automática.

---

## 🧠 Funcionalidades Atuais

- ✅ Geração de conteúdo via **OpenAI API** (`gpt-3.5-turbo`, `gpt-4o`, etc.)
- ✅ Fallback automático para frases locais (`frases.json`)
- ✅ Prompt dinâmico via `.env` ou arquivos `.txt`
- ✅ Conversão de texto em áudio com voz neural (`edge-tts`)
- ✅ Estrutura modular pronta para expansão (vídeo, agendamento, redes sociais)
- ✅ Cálculo de custo por geração com base em tokens

---

## 🧩 Estrutura de Pastas

```
auto-content/
├── text_generator/
│   ├── text_config.py         # Configurações gerais e carregamento do prompt
│   ├── text_creator.py        # Geração de texto via OpenAI ou fallback
│   ├── text_gerador_api.py    # Uso da OpenAI API
│   ├── text_gerador_local.py  # Leitura de frases locais
│   └── data/
│       └── inputs/
│           ├── prompt.txt     # Arquivo de prompt principal
│           └── frases.json    # Frases locais para fallback
├── text_to_speech/
│   ├── tts_generator.py       # Converte o texto gerado em áudio
│   ├── tts_config.py          # Configurações da voz
│   └── audios/                # Pasta de saída dos .mp3
└── .env                       # Chave da API e parâmetros
```

---

## 💰 Preços por Modelo OpenAI (maio/2025)

| Modelo          | Tipo            | Preço por 1.000 tokens |
|-----------------|------------------|------------------------|
| `gpt-3.5-turbo` | Entrada/Saída    | **US$ 0.0015**         |
| `gpt-4o`        | Entrada           | **US$ 0.0050**         |
|                 | Saída             | **US$ 0.0150**         |
| `gpt-4-turbo`   | Entrada           | **US$ 0.0100**         |
|                 | Saída             | **US$ 0.0300**         |

> 💡 Recomenda-se usar `gpt-3.5-turbo` para testes e execuções frequentes com custo baixo.

---

## ⚙️ Como Usar

### 1. Clone ou descompacte o projeto

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd auto-content
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou instale diretamente:

```bash
pip install openai python-dotenv edge-tts
```

### 3. Configure o `.env`

Copie o exemplo e edite com sua chave da OpenAI:

```bash
cp .env.example .env
```

Exemplo de conteúdo:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo
TOKEN_PRICE=0.0015
TEXT_PROMPT=
```

---

## 🧠 Etapa 1 – Geração de Texto

- Gera texto com base em um prompt fornecido via `.env` ou por arquivos `.txt` dentro de `data/inputs/`.
- Se a API falhar, utiliza uma frase aleatória do arquivo `frases.json`.

### Execução:

```bash
python text_generator/text_creator.py
```

---

## 🗣️ Etapa 2 – Conversão de Texto em Áudio (Text-to-Speech)

- Utiliza o pacote gratuito `edge-tts` da Microsoft.
- Gera `.mp3` com voz neural realista (pt-BR).
- Salva os arquivos automaticamente com nomes baseados no conteúdo.

### Configuração (`tts_config.py`):

```python
VOICE = "pt-BR-AntonioNeural"
RATE = "+0%"
OUTPUT_DIR = "audios/"
```

> Outras vozes disponíveis: `pt-BR-BrendaNeural`, `pt-BR-AntonioNeural`

### Execução completa (Texto + Áudio):

```bash
python text_to_speech/tts_generator.py
```

### Exemplo de saída:

```
📄 Prompt carregado de: prompt.txt
⚙️  Gerando texto via OpenAI...
🧾 Tokens usados: 62 | Custo estimado: U$0.00009
🔊 Áudio salvo em: audios/os-ursos-polares-são-canhotos.mp3
```

---

## 📦 requirements.txt

```txt
openai>=1.0.0
python-dotenv>=1.0.0
edge-tts>=6.1.10

# (Futuro)
# elevenlabs
# moviepy
# ffmpeg-python
```

---

## 🧱 Próximas Etapas (Planejadas)

- 🎬 Renderização automática de vídeo (`moviepy`)
- 🧠 Legenda embutida e efeitos sonoros
- 📲 Publicação automática em TikTok, YouTube Shorts e Instagram Reels
- 🗓️ Agendamento com n8n ou cron

---

## 📄 Licença

MIT © [Seu Nome ou Projeto]