#!/bin/sh
# Setup Python virtual environment if we don't see anything there as in a first launch run or if the repository does not exist.

# debug below
# sleep 600
echo "---] Starting ComfyUI container."

jq -n 'env'

if [ -e $$PATH_INIT_TOUCH_FILE ]; then
    echo "----] CONTAINER HAS BEEN PREVIOUSLY STARTED - TOUCH FILE ${PATH_INIT_TOUCH_FILE} EXISTS"
else
    echo "----] CONTAINER HAS NOT BEEN PREVIOUSLY STARTED - TOUCH FILE ${PATH_INIT_TOUCH_FILE} DOES NOT EXIST"
fi
echo "----] clinfo output:"

clinfo | head -6

if [ ! -e $$PATH_INIT_TOUCH_FILE ]; then
    echo "--] First time launching container, setting things up."
    echo "----] creating directories for models dir at ${PATH_COMFY_MODELS}"
    mkdir -p "${PATH_COMFY_MODELS}"/checkpoints
    mkdir -p "${PATH_COMFY_MODELS}"/clip_vision
    mkdir -p "${PATH_COMFY_MODELS}"/configs
    mkdir -p "${PATH_COMFY_MODELS}"/controlnet
    mkdir -p "${PATH_COMFY_MODELS}"/diffusers
    mkdir -p "${PATH_COMFY_MODELS}"/embeddings
    mkdir -p "${PATH_COMFY_MODELS}"/gligen
    mkdir -p "${PATH_COMFY_MODELS}"/hypernetworks
    mkdir -p "${PATH_COMFY_MODELS}"/loras
    mkdir -p "${PATH_COMFY_MODELS}"/photomaker
    mkdir -p "${PATH_COMFY_MODELS}"/style_models
    mkdir -p "${PATH_COMFY_MODELS}"/unet
    mkdir -p "${PATH_COMFY_MODELS}"/upscale_models
    mkdir -p "${PATH_COMFY_MODELS}"/vae
    mkdir -p "${PATH_COMFY_MODELS}"/vae_approx
    echo "----] creating virtual environment in: ${PATH_COMFY_PY_DEPENDS}/venv"
    python3 -m venv "$PATH_COMFY_PY_DEPENDS/venv"
    # Clone repository if we have an empty space available.
    echo "----] purging out comfyui and comfyui-manager repositories. will put again - this goes to whatever is mounted to ${PATH_COMFY_BASE}"
    rm -rf "${PATH_COMFY_BASE:?}/"*
    rm -rf "${PATH_COMFY_BASE:?}"/.*
    rm -rf /tmp/ComfyUI-Manager
    echo "----] cloning comfyui and comfyui-manager repositories."
    git rev-parse --git-dir >/dev/null 2>&1 || git clone https://github.com/comfyanonymous/ComfyUI.git "${PATH_COMFY_BASE}"
    mkdir /tmp/ComfyUI-Manager -p
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git /tmp/ComfyUI-Manager
    echo "----] copying comfyui-manager to ${PATH_COMFY_BASE}/custom_nodes."
    cp -r /tmp/ComfyUI-Manager "${PATH_COMFY_BASE}"/custom_nodes
    git config --global core.filemode false

    # place extra_model_paths.yaml
    echo "----] placing extra_model_paths.yaml in ${PATH_COMFY_BASE}"
    cp /extra_model_paths.yaml "${PATH_COMFY_BASE}"/extra_model_paths.yaml

    # Set the first launch variable to true.
    FirstLaunch=true
    # touch our initialization file for comfy setup (lives in ).
    echo "----] First launch var set to true, touching ${PATH_INIT_TOUCH_FILE}"
    echo "----] should now proceed to deal with dependencies for python - will enter py venv in ${PATH_COMFY_PY_DEPENDS}/venv"
    touch "${PATH_INIT_TOUCH_FILE}"
fi

# Activate the virtual environment to use for ComfyUI
if [ -f "${PATH_COMFY_PY_DEPENDS}"/venv/bin/activate ]; then
    echo "---] Activating python venv in ${PATH_COMFY_PY_DEPENDS}/venv"
    # shellcheck disable=SC1091
    . "${PATH_COMFY_PY_DEPENDS}"/venv/bin/activate
else
    echo "ERROR] Cannot activate python venv."
    echo "--------] check value of env var 'PATH_COMFY_PY_DEPENDS', note script appends '/venv' to this py dependency path"
    echo "--------] value should be base py depends dir - set to: ${PATH_COMFY_PY_DEPENDS}"
    echo "ERROR] Will not recreate venv here: remove touch file at ${PATH_INIT_TOUCH_FILE} and restart the container, it should repopulate the venv"
    echo "- FATAL -"
    exit 1
fi

# Install pip requirements if launching for the first time.
if [ "$FirstLaunch" = "true" ]; then
    echo "---] Installing ComfyUI Python dependencies - note this is for xpu, as opposed to internal on-CPU-GPU."
    pip install -r "${PATH_COMFY_PY_DEPENDS}"/requirements-ipex.txt
    pip install -r "${PATH_COMFY_PY_DEPENDS}"/requirements-comfy.txt

    # install extra models if docker-compose COMFYUI_MODELS_DOWNLOAD=1
    if [ "$COMFYUI_MODELS_DOWNLOAD" = "1" ]; then
        echo "---] Downloading extra models for ComfyUI. this may take some time..."
        python3 "${PATH_COMFY_PY_DEPENDS}"/scripts/get_models.py
    fi
fi

# Launch ComfyUI based on whether ipexrun is set to be used or not. Explicit string splitting is done by the shell here so shellcheck warning is ignored.
# shellcheck disable=SC2154
if [ "$UseIPEXRUN" = "true" ] && [ "$UseXPU" = "true" ]; then
    echo "---] Using ipexrun xpu to launch ComfyUI."
    # shellcheck disable=SC2086,SC2154
    exec ipexrun xpu $IPEXRUNArgs main.py $ComfyArgs
elif [ "$UseIPEXRUN" = "true" ] && [ "$UseXPU" = "false" ]; then
    echo "Using ipexrun cpu to launch ComfyUI."
    # shellcheck disable=SC2086
    exec ipexrun $IPEXRUNArgs main.py $ComfyArgs
else
    echo "---] No command to use ipexrun to launch ComfyUI. Launching normally."
    # shellcheck disable=SC2086
    python3 main.py $ComfyArgs
fi
