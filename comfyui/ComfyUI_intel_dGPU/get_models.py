"""
    _summary_ some starting models for ComfyUI - set docker-compose env var COMFYUI_MODELS_DOWNLOAD to 1 to download models
"""

import os
from typing import Final

COMFYUI_BASEDIR: Final[str] = "/ComfyUI"
COMFYUI_VENV: Final[str] = "/deps/venv"
MODELS_BASEDIR: Final[str] = "/models"

WGET_ARGS: Final[str] = "-c --no-verbose --show-progress"

# SDXL
print("__> Downloading models...")
print(f"___> COMFYUI_BASEDIR = {MODELS_BASEDIR}/")
print(f"___> COMFYUI_VENV = {COMFYUI_VENV}/")
print(f"___> MODELS_BASEDIR = {MODELS_BASEDIR}/")

# (custom nodes) ControlNet Preprocessor nodes by Fannovel16
print(f"____> ({COMFYUI_BASEDIR}/custom_nodes/) ==>   ControlNet Preprocessor nodes custom_nodes...")
os.system(f"source {COMFYUI_VENV}/bin/activate && cd {COMFYUI_BASEDIR}/custom_nodes && git clone https://github.com/Fannovel16/comfy_controlnet_preprocessors; cd comfy_controlnet_preprocessors && python3 install.py")

print(f"____> ({MODELS_BASEDIR}/checkpoints/) ==>   SDXL...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0_0.9vae.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/stabilityai/stable-diffusion-xl-base-0.9/resolve/main/sd_xl_base_0.9.safetensors -P {MODELS_BASEDIR}/checkpoints/")

# SD1.5
print(f"____> ({MODELS_BASEDIR}/checkpoints/) ==>   SD1.5...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt -P {MODELS_BASEDIR}/checkpoints/")

# SD2
print(f"____> ({MODELS_BASEDIR}/checkpoints/) ==>   SD2...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-ema-pruned.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.safetensors -P {MODELS_BASEDIR}/checkpoints/")

# Some SD1.5 anime style
print(f"____> ({MODELS_BASEDIR}/checkpoints/) ==>  SD1.5 anime style...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_hard.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3A1_orangemixs.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3A3_orangemixs.safetensors -P {MODELS_BASEDIR}/checkpoints/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/anything-v3-fp16-pruned.safetensors -P {MODELS_BASEDIR}/checkpoints/")

# Waifu Diffusion 1.5 (anime style SD2.x 768-v)
print(f"____> ({MODELS_BASEDIR}/checkpoints/) ==>  Waifu Diffusion 1.5...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/waifu-diffusion/wd-1-5-beta2/resolve/main/checkpoints/wd-1-5-beta2-fp16.safetensors -P {MODELS_BASEDIR}/checkpoints/")

# VAE
print(f"____> ({MODELS_BASEDIR}/vae/) ==> VAE...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors -P {MODELS_BASEDIR}/vae/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/VAEs/orangemix.vae.pt -P {MODELS_BASEDIR}/vae/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt -P {MODELS_BASEDIR}/vae/")


# Loras
print(f"____> ({MODELS_BASEDIR}/loras/) ==>  Loras...")
os.system(f"wget {WGET_ARGS} https://civitai.com/api/download/models/10350 -O {MODELS_BASEDIR}/loras/theovercomer8sContrastFix_sd21768.safetensors")
os.system(f"wget {WGET_ARGS} https://civitai.com/api/download/models/10638 -O {MODELS_BASEDIR}/loras/theovercomer8sContrastFix_sd15.safetensors")


# T2I-Adapter
print(f"____> ({MODELS_BASEDIR}/controlnet/) ==>  T2I-Adapter...")
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
print(f"____> ({MODELS_BASEDIR}/upscale_models/) ==>  ESRGAN upscale models...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/sberbank-ai/Real-ESRGAN/resolve/main/RealESRGAN_x2.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/sberbank-ai/Real-ESRGAN/resolve/main/RealESRGAN_x4.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x-UltraSharp.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_RealisticRescaler_100000_G.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/BSRGAN.pth -P {MODELS_BASEDIR}/upscale_models/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/BSRGANx2.pth -P {MODELS_BASEDIR}/upscale_models/")


# T2I Styles Model
print(f"____> ({MODELS_BASEDIR}/style_models/) ==> T2I Styles Model...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models/t2iadapter_style_sd14v1.pth -P {MODELS_BASEDIR}/style_models/")

# CLIPVision model (needed for styles model)
print(f"____> ({MODELS_BASEDIR}/clip_vision/) ==> CLIPVision model...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/openai/clip-vit-large-patch14/resolve/main/pytorch_model.bin -O {MODELS_BASEDIR}/clip_vision/clip_vit14.bin")

# ControlNet
print(f"____> ({MODELS_BASEDIR}/controlnet/) ==> ControlNet...")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_depth-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_scribble-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")
os.system(f"wget {WGET_ARGS} https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_openpose-fp16.safetensors -P {MODELS_BASEDIR}/controlnet/")

print("__> Done!")
