"""
    _summary_ some starting models for ComfyUI - set docker-compose env var COMFYUI_MODELS_DOWNLOAD to 1 to download models
"""

import os
from typing import Final

BASEDIR: Final[str] = "/ComfyUI"
MODELS_BASEDIR: Final[str] = "/models"

# SDXL
print("__> Downloading models...")
print("____> SDXL...")
os.system(f"wget -c https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")
os.system(f"wget -c https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0_0.9vae.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")
os.system(f"wget -c https://huggingface.co/stabilityai/stable-diffusion-xl-base-0.9/resolve/main/sd_xl_base_0.9.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")

# SD1.5
print("____> SD1.5...")
os.system(f"wget -c https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt -P ${MODELS_BASEDIR}/models/checkpoints/")

# SD2
print("____> SD2...")
os.system(f"wget -c https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-ema-pruned.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")
os.system(f"wget -c https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")

# Some SD1.5 anime style
print("____> SD1.5 anime style...")
os.system(f"wget -c https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_hard.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")
os.system(f"wget -c https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3A1_orangemixs.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")
os.system(f"wget -c https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3A3_orangemixs.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")
os.system(f"wget -c https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/anything-v3-fp16-pruned.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")

# Waifu Diffusion 1.5 (anime style SD2.x 768-v)
print("____> Waifu Diffusion 1.5...")
os.system(f"wget -c https://huggingface.co/waifu-diffusion/wd-1-5-beta2/resolve/main/checkpoints/wd-1-5-beta2-fp16.safetensors -P ${MODELS_BASEDIR}/models/checkpoints/")

# VAE
print("____> VAE...")
os.system(f"wget -c https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors -P ${MODELS_BASEDIR}/models/vae/")
os.system(f"wget -c https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/VAEs/orangemix.vae.pt -P ${MODELS_BASEDIR}/models/vae/")
os.system(f"wget -c https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt -P ${MODELS_BASEDIR}/models/vae/")


# Loras
print("____> Loras...")
os.system(f"wget -c https://civitai.com/api/download/models/10350 -O ${MODELS_BASEDIR}/models/loras/theovercomer8sContrastFix_sd21768.safetensors")
os.system(f"wget -c https://civitai.com/api/download/models/10638 -O ${MODELS_BASEDIR}/models/loras/theovercomer8sContrastFix_sd15.safetensors")


# T2I-Adapter
print("____> T2I-Adapter...")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_depth_sd14v1.pth -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_seg_sd14v1.pth -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_sketch_sd14v1.pth -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_keypose_sd14v1.pth -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_openpose_sd14v1.pth -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_color_sd14v1.pth -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_canny_sd14v1.pth -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_style_sd14v1.pth -P ${MODELS_BASEDIR}/models/style_models/")
os.system(f"wget -c https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_depth-fp16.safetensors -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_scribble-fp16.safetensors -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_openpose-fp16.safetensors -P ${MODELS_BASEDIR}/models/controlnet/")

# ESRGAN upscale models
print("____> ESRGAN upscale models...")
os.system(f"wget -c https://huggingface.co/sberbank-ai/Real-ESRGAN/resolve/main/RealESRGAN_x2.pth -P ${MODELS_BASEDIR}/models/upscale_models/")
os.system(f"wget -c https://huggingface.co/sberbank-ai/Real-ESRGAN/resolve/main/RealESRGAN_x4.pth -P ${MODELS_BASEDIR}/models/upscale_models/")
os.system(f"wget -c https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x-UltraSharp.pth -P ${MODELS_BASEDIR}/models/upscale_models/")
os.system(f"wget -c https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_RealisticRescaler_100000_G.pth -P ${MODELS_BASEDIR}/models/upscale_models/")
os.system(f"wget -c https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/BSRGAN.pth -P ${MODELS_BASEDIR}/models/upscale_models/")
os.system(f"wget -c https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/BSRGANx2.pth -P ${MODELS_BASEDIR}/models/upscale_models/")


# T2I Styles Model
print("____> T2I Styles Model...")
os.system(f"wget -c https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_style_sd14v1.pth -P ${MODELS_BASEDIR}/models/style_models/")

# CLIPVision model (needed for styles model)
print("____> CLIPVision model...")
os.system(f"wget -c https://huggingface.co/openai/clip-vit-large-patch14/resolve/main/pytorch_model.bin -O ${MODELS_BASEDIR}/models/clip_vision/clip_vit14.bin")

# ControlNet Preprocessor nodes by Fannovel16
print("____> ControlNet Preprocessor nodes...")
os.system(f"cd ${BASEDIR}/custom_nodes && git clone https://github.com/Fannovel16/comfy_controlnet_preprocessors; cd comfy_controlnet_preprocessors && python3 install.py")

# ControlNet
print("____> ControlNet...")
os.system(f"wget -c https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_depth-fp16.safetensors -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_scribble-fp16.safetensors -P ${MODELS_BASEDIR}/models/controlnet/")
os.system(f"wget -c https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_openpose-fp16.safetensors -P ${MODELS_BASEDIR}/models/controlnet/")

print("__> Done!")
