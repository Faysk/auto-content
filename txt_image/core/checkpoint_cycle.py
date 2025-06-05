import json
import os

CKPT_FILE = "ckpt_config.json"
CKPT_LIST = [
    # "cuterealism_v10.safetensors",
    # "cyberrealistic_v80.safetensors",
    # "cyberrealisticXL_v56.safetensors",
    # "cyberrealisticXL_v57.safetensors",
    # "damnPonyxlRealistic_v30.safetensors",
    # "epicrealismXL_vxviLastfameRealism.safetensors",
    # "imperfectXLTrueNSFWToe_v100.safetensors",
    # "inpaintSDXLPony_inpaintPony.safetensors",
    # "japaneseStyleRealistic_v20.safetensors",
    # "juggernautXL_ragnarokBy.safetensors",
    # "juggernautXL_versionXInpaint.safetensors",
    # "lazymixRealAmateur_v40Inpainting.safetensors",
    # "lustifySDXLNSFW_oltFIXEDTEXTURES.safetensors",
    # "majicmixHorror_v1.safetensors",
    # "majicmixRealistic_v7.safetensors",
    # "onlyPorn_realPorn.safetensors",
    # "ponylutionxl_Illust01.safetensors",
    # "preciseFluxDevNF4FP8FP16_v10Fp16.safetensors",
    # "preciseFluxDevNF4FP8FP16_v10Fp8.safetensors",
      "realDream_sdxl6.safetensors"
    # "unstableIllusion_nf46GB.safetensors",
    # "unstableIllusion_sdxxxl.safetensors",
    # "unstableIllusionSDXL_SDXL.safetensors",
    # "virtualphotorealisti_v10.safetensors"
]

def get_current_checkpoint():
    if os.path.exists(CKPT_FILE):
        with open(CKPT_FILE, "r") as f:
            return json.load(f).get("current")
    return CKPT_LIST[0]

def advance_checkpoint():
    current = get_current_checkpoint()
    try:
        index = CKPT_LIST.index(current)
        next_index = (index + 1) % len(CKPT_LIST)
        next_ckpt = CKPT_LIST[next_index]
    except ValueError:
        next_ckpt = CKPT_LIST[0]

    with open(CKPT_FILE, "w") as f:
        json.dump({"current": next_ckpt}, f)
    return next_ckpt

def reset_checkpoint():
    with open(CKPT_FILE, "w") as f:
        json.dump({"current": CKPT_LIST[0]}, f)
