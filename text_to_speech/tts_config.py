# tts/tts_config.py

# 🇧🇷 Português - Brasil
# VOICE = "pt-BR-AntonioNeural"    # Masculina, realista
# VOICE = "pt-BR-FranciscaNeural" # Feminina, neutra, realista
# VOICE = "pt-BR-ThalitaNeural"     # Feminina, suave e clara
# VOICE = "pt-BR-DavisNeural"     # Masculino, jovem, suave
# VOICE = "pt-BR-GloriaNeural"    # Feminina, tom enérgico

# 🇺🇸 Inglês - Estados Unidos
# VOICE = "en-US-GuyNeural"       # Masculino, equilibrado
# VOICE = "en-US-DavisNeural"     # Masculino, jovem e suave
# VOICE = "en-US-ChristopherNeural" # Masculino, maduro e confiante
# VOICE = "en-US-RogerNeural"     # Masculino, formal
# VOICE = "en-US-TonyNeural"      # Masculino, descontraído
import os

VOICE = os.getenv("TTS_VOICE", "en-US-JennyNeural")  # Feminina, natural, ótima para narração
# VOICE = "en-US-AriaNeural"      # Feminina, expressiva e envolvente
# VOICE = "en-US-AnaNeural"       # Feminina, leve sotaque latino
# VOICE = "en-US-AmberNeural"     # Feminina, jovem e vibrante
# VOICE = "en-US-MichelleNeural"  # Feminina, clara e articulada

# 🇬🇧 Inglês - Reino Unido
# VOICE = "en-GB-RyanNeural"      # Masculino, jovem britânico
# VOICE = "en-GB-ThomasNeural"    # Masculino, formal
# VOICE = "en-GB-LibbyNeural"     # Feminina, adolescente, energética
# VOICE = "en-GB-SoniaNeural"     # Feminina, sotaque indiano britânico
# VOICE = "en-GB-MaisieNeural"    # Feminina, gentil e clara

# 🇦🇺 Inglês - Austrália
# VOICE = "en-AU-NatashaNeural"   # Feminina, calorosa e natural
# VOICE = "en-AU-WilliamNeural"   # Masculino, descontraído

# 🇨🇦 Inglês - Canadá
# VOICE = "en-CA-ClaraNeural"     # Feminina, neutra e clara
# VOICE = "en-CA-LiamNeural"      # Masculino, calmo e neutro

# 🇮🇳 Inglês - Índia
# VOICE = "en-IN-NeerjaNeural"    # Feminina, leve sotaque indiano
# VOICE = "en-IN-PrabhatNeural"   # Masculino, articulado

# 🌍 Outros sotaques
# VOICE = "en-NZ-MitchellNeural"  # Masculino, Nova Zelândia
# VOICE = "en-NZ-MollyNeural"     # Feminina, Nova Zelândia
# VOICE = "en-ZA-LeahNeural"      # Feminina, África do Sul
# VOICE = "en-ZA-LukeNeural"      # Masculino, África do Sul
# VOICE = "en-IE-ConnorNeural"    # Masculino, Irlanda
# VOICE = "en-IE-EmilyNeural"     # Feminina, Irlanda
# VOICE = "en-SG-WayneNeural"     # Masculino, Cingapura
# VOICE = "en-SG-LunaNeural"      # Feminina, Cingapura

# 🔧 Configurações adicionais
RATE = os.getenv("TTS_RATE", "+0%")          # Velocidade (ex: -10%, +20%)
OUTPUT_DIR = os.getenv("TTS_OUTPUT_DIR", "audios/")  # Pasta de saída dos áudios
# VOLUME = "+0%"                 # Volume (ex: -10%, +20%)
# SAMPLE_RATE = 24000           # Taxa de amostragem (ex: 16000, 24000, 48000)

