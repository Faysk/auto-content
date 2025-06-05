import importlib
from inspect import signature
from datetime import datetime
from pathlib import Path

# Caminho absoluto para a pasta comfyui (relativo ao runner.py)
COMFY_PATH = Path(__file__).resolve().parents[1] / "comfyui"
_module_cache = {}

def log(msg, ok=True):
    prefix = "[✅]" if ok else "[❌]"
    cor = "\033[92m" if ok else "\033[91m"
    reset = "\033[0m"
    print(f"{cor}{prefix} {datetime.now().strftime('%H:%M:%S')} - {msg}{reset}")

def import_node_module(module_name):
    if module_name in _module_cache:
        return _module_cache[module_name]
    mod = importlib.import_module(f"txt_image.comfyui.{module_name}")  # usa caminho absoluto
    _module_cache[module_name] = mod
    return mod

def call_with_optional_args(func, **kwargs):
    sig = signature(func)
    args = {}
    for param in sig.parameters:
        if param in kwargs:
            args[param] = kwargs[param]
    return func(**args)

def file_sort_key(name):
    try:
        return int(name.split("_")[0])
    except:
        return 9999

def load_nodes(trecho=None, nome_arquivo=None):
    node_outputs = {}
    name_to_index = {}
    index = 1

    files = sorted(
        [f for f in COMFY_PATH.iterdir() if f.suffix == ".py" and f.name != "utils.py"],
        key=lambda f: file_sort_key(f.name)
    )

    for file in files:
        module_name = file.stem
        module = import_node_module(module_name)

        for attr in dir(module):
            if attr.startswith("node_"):
                func = getattr(module, attr)
                result = call_with_optional_args(func, trecho=trecho, nome_arquivo=nome_arquivo)

                if isinstance(result, tuple):
                    node_name, content = result
                else:
                    node_name = attr.replace("node_", "")
                    content = result

                node_outputs[str(index)] = content
                name_to_index[node_name] = index
                index += 1

    # Ajusta conexões entre os nós
    for node in node_outputs.values():
        if "inputs" in node:
            for k, v in node["inputs"].items():
                if isinstance(v, list) and isinstance(v[0], str) and v[0] in name_to_index:
                    v[0] = str(name_to_index[v[0]])

    return node_outputs
