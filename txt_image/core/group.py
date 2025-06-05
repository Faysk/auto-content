import os
import json
import hashlib
from datetime import datetime

BASE_OUTPUT_DIR = "outputs"

def sanitize_path(text):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in text)

def get_checkpoint_name(payload):
    for node in payload["prompt"].values():
        if node["class_type"] == "CheckpointLoaderSimple":
            path = node["inputs"]["ckpt_name"]
            return os.path.basename(path).replace(".safetensors", "")
    return "unknown"

def extract_core_fingerprint(payload):
    filtered = {}

    for node_id, node in payload["prompt"].items():
        class_type = node.get("class_type", "")
        inputs = node.get("inputs", {})

        # Ignorar seed e variáveis variáveis
        if class_type == "KSampler":
            filtered[class_type] = {k: v for k, v in inputs.items() if k != "seed"}
        elif class_type == "SaveImage":
            continue
        else:
            filtered[class_type] = inputs

    # Ordena e serializa
    raw = json.dumps(filtered, sort_keys=True)
    hash_str = hashlib.md5(raw.encode("utf-8")).hexdigest()
    return hash_str, filtered

def ensure_unique_folder(base_name, fingerprint_id):
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

    for i in range(1, 9999):
        folder_name = f"{base_name}-{i:03d}"
        folder_path = os.path.join(BASE_OUTPUT_DIR, folder_name)

        fingerprint_file = os.path.join(folder_path, "fingerprint.json")
        if os.path.exists(folder_path):
            if os.path.exists(fingerprint_file):
                with open(fingerprint_file, "r") as f:
                    data = json.load(f)
                    if data.get("fingerprint_id") == fingerprint_id:
                        return folder_path  # já existe com mesma config
        else:
            os.makedirs(folder_path)
            return folder_path

    raise Exception("🔥 Limite de pastas atingido para esse modelo/config")

def save_metadata(folder_path, payload, nome_arquivo, fingerprint_id):
    metadata = {
        "nome_arquivo": nome_arquivo,
        "data_hora": datetime.now().isoformat(),
        "fingerprint_id": fingerprint_id,
        "variaveis_geracao": payload["prompt"]
    }
    with open(os.path.join(folder_path, "metadata.json"), "a", encoding="utf-8") as f:
        f.write(json.dumps(metadata, indent=2) + ",\n")

    # fingerprint salvo uma única vez
    fp_path = os.path.join(folder_path, "fingerprint.json")
    if not os.path.exists(fp_path):
        with open(fp_path, "w", encoding="utf-8") as f:
            json.dump({"fingerprint_id": fingerprint_id}, f, indent=2)

def get_output_folder(payload, nome_arquivo):
    fingerprint_id, _ = extract_core_fingerprint(payload)
    ckpt = get_checkpoint_name(payload)
    folder_path = ensure_unique_folder(ckpt, fingerprint_id)
    save_metadata(folder_path, payload, nome_arquivo, fingerprint_id)
    return folder_path
