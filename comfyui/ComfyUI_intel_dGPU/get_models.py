"""_summary_ some starting models for ComfyUI - set docker-compose env var COMFYUI_MODELS_DOWNLOAD to 1 to download models."""

import logging
import logging.config
import os
from datetime import UTC, datetime
from typing import Final

COMFYUI_BASEDIR: Final[str] = f"{os.environ.get('PATH_COMFY_BASE')}"
COMFYUI_VENV: Final[str] = f"{os.environ.get('PATH_COMFY_PY_DEPENDS')}/venv"
MODELS_BASEDIR: Final[str] = f"{os.environ.get('PATH_COMFY_MODELS')}"

WGET_ARGS: Final[str] = "-c --no-verbose --show-progress --progress=bar:force:noscroll"


class ISO8601Formatter(logging.Formatter):
    """ISO8601Formatter puts ISO8601 UTC time in logged messages."""

    def formatTime(self: "ISO8601Formatter", record: logging.LogRecord, datefmt: str | None = None) -> str:  # noqa: N802, ARG002
        """Format the time of the log record - ISO8601 UTC."""
        return f"{datetime.fromtimestamp(record.created).astimezone(UTC).isoformat(timespec='milliseconds')}Z"


logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "ISO8601Formatter": {
                "()": ISO8601Formatter,
                "format": "%(asctime)s - %(levelname)s --] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "ISO8601Formatter",
            },
        },
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": ["console"],
            },
        },
    },
)

logger = logging.getLogger()

# SDXL
logger.info("__> Downloading models...")
logger.info("___> COMFYUI_BASEDIR = %s/", MODELS_BASEDIR)
logger.info("___> COMFYUI_VENV = %s/", COMFYUI_VENV)
logger.info("___> MODELS_BASEDIR = %s/", MODELS_BASEDIR)

# (custom nodes) ControlNet Preprocessor nodes by Fannovel16
logger.info("____> (%s/custom_nodes/) ==>   ControlNet Preprocessor nodes custom_nodes...", COMFYUI_BASEDIR)
os.system(f". {COMFYUI_VENV}/bin/activate && cd {COMFYUI_BASEDIR}/custom_nodes \
          && git clone https://github.com/Fannovel16/comfy_controlnet_preprocessors; \
          cd comfy_controlnet_preprocessors && python3 install.py")

logger.info("____> (%s/checkpoints/) ==>   SD1.5...", MODELS_BASEDIR)
logger.info("____> (%s/checkpoints/) ==>  SD1.5 anime style...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_hard.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3A1_orangemixs.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3A3_orangemixs.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/anything-v3-fp16-pruned.safetensors -P {MODELS_BASEDIR}/checkpoints/")

# Waifu Diffusion 1.5 (anime style SD2.x 768-v)
logger.info("____> (%s/checkpoints/) ==>  Waifu Diffusion 1.5...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/waifu-diffusion/wd-1-5-beta2/resolve/main/checkpoints/wd-1-5-beta2-fp16.safetensors -P {MODELS_BASEDIR}/checkpoints/")

# VAE
logger.info("____> (%s/vae/) ==> VAE...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors -P {MODELS_BASEDIR}/vae/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/VAEs/orangemix.vae.pt -P {MODELS_BASEDIR}/vae/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt -P {MODELS_BASEDIR}/vae/")


# Loras
logger.info("____> (%s/loras/) ==>  Loras...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://civitai.com/api/download/models/10350 -O {MODELS_BASEDIR}/loras/theovercomer8sContrastFix_sd21768.safetensors")
os.system(f"wget {WGET_ARGS} https://civitai.com/api/download/models/10638 -O {MODELS_BASEDIR}/loras/theovercomer8sContrastFix_sd15.safetensors")


# T2I-Adapter
logger.info("____> ({%s/controlnet/) ==>  T2I-Adapter...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_depth_sd14v1.pth -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_seg_sd14v1.pth -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_sketch_sd14v1.pth -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_keypose_sd14v1.pth -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_openpose_sd14v1.pth -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_color_sd14v1.pth -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_canny_sd14v1.pth -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_style_sd14v1.pth -P {MODELS_BASEDIR}/style_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_depth-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_scribble-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_openpose-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")

# ESRGAN upscale models
logger.info("____> (%s/upscale_models/) ==>  ESRGAN upscale models...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/sberbank-ai/Real-ESRGAN/resolve/main/RealESRGAN_x2.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/sberbank-ai/Real-ESRGAN/resolve/main/RealESRGAN_x4.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x-UltraSharp.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_RealisticRescaler_100000_G.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/BSRGAN.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/BSRGANx2.pth -P {MODELS_BASEDIR}/upscale_models/")


# T2I Styles Model
logger.info("____> (%s/style_models/) ==> T2I Styles Model...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_style_sd14v1.pth -P {MODELS_BASEDIR}/style_models/")

# CLIPVision model (needed for styles model)
logger.info("____> (%s/clip_vision/) ==> CLIPVision model...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/openai/clip-vit-large-patch14/resolve/main/pytorch_model.bin -O {MODELS_BASEDIR}/clip_vision/clip_vit14.bin")

# ControlNet
logger.info("____> (%s/controlnet/) ==> ControlNet...", MODELS_BASEDIR)
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_depth-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_scribble-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_openpose-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")

logger.info("__> Done!")
