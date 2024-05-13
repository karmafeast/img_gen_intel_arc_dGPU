#!/bin/sh
CONTAINER_ALREADY_STARTED=$INIT_TOUCH_FILE
# Setup Python virtual environment if we don't see anything there as in a first launch run or if the repository does not exist.

# debug below
# sleep 600

if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    echo "|__> First time launching container, setting things up."
    echo "|____> creating virtual environment in: ${VENVDir}."
    python3 -m venv "$VENVDir"
    # Clone repository if we have an empty space available.
    echo "|____> purging out comfyui and comfyui-manager repositories. will put again (this goes to whatever is mounted to /ComfyUI)."
    rm -rf /ComfyUI/*
    rm -rf /ComfyUI/.*
    rm -rf /tmp/ComfyUI-Manager
    echo "|____> cloning comfyui and comfyui-manager repositories."
    git rev-parse --git-dir >/dev/null 2>&1 || git clone https://github.com/comfyanonymous/ComfyUI.git /ComfyUI
    mkdir /tmp/ComfyUI-Manager -p
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git /tmp/ComfyUI-Manager
    echo "|____> copying comfyui-manager to /ComfyUI/custom_nodes."
    cp -r /tmp/ComfyUI-Manager /ComfyUI/custom_nodes
    git config core.filemode false

    # place extra_model_paths.yaml
    echo "|____> placing extra_model_paths.yaml in /ComfyUI."
    cp /extra_model_paths.yaml /ComfyUI/extra_model_paths.yaml

    # Set the first launch variable to true.
    FirstLaunch=true
    # Make a file in /tmp/ to indicate the first launch step has been executed.
    echo "|____> First launch var set to true, touching ${CONTAINER_ALREADY_STARTED}"
    echo "|____> should now proceed to deal with dependencies for python (will enter py venv in ${VENVDir})."
    touch "$CONTAINER_ALREADY_STARTED"
fi

# Activate the virtual environment to use for ComfyUI
if [ -f "$VENVDir"/bin/activate ]; then
    echo "|__> Activating python venv in ${VENVDir}."
    . "$VENVDir"/bin/activate
else
    echo "|ERROR> Cannot activate python venv. check value of env var 'VENVDir' (set to: ${VENVDir}). Exiting immediately."
    exit 1
fi

# Install pip requirements if launching for the first time.
if [ "$FirstLaunch" = "true" ]; then
    echo "|__> Installing ComfyUI Python dependencies - note this is for xpu, as opposed to internal on-CPU-GPU."
    pip install -r /requirements-ipex.txt --upgrade
    pip install -r /requirements-comfy.txt

    # install extra models if docker-compose COMFYUI_MODELS_DOWNLOAD=1
    if [ "$COMFYUI_MODELS_DOWNLOAD" = "1" ]; then
        echo "|__> Downloading extra models for ComfyUI. this may take some time..."
        python3 /ComfyUI/download_models.py
    fi
fi

# Launch ComfyUI based on whether ipexrun is set to be used or not. Explicit string splitting is done by the shell here so shellcheck warning is ignored.
if [ "$UseIPEXRUN" = "true" ] && [ "$UseXPU" = "true" ]; then
    echo "|__> Using ipexrun xpu to launch ComfyUI."
    # shellcheck disable=SC2086
    exec ipexrun xpu $IPEXRUNArgs main.py $ComfyArgs
elif [ "$UseIPEXRUN" = "true" ] && [ "$UseXPU" = "false" ]; then
    echo "Using ipexrun cpu to launch ComfyUI."
    # shellcheck disable=SC2086
    exec ipexrun $IPEXRUNArgs main.py $ComfyArgs
else
    echo "|__> No command to use ipexrun to launch ComfyUI. Launching normally."
    # shellcheck disable=SC2086
    python3 main.py $ComfyArgs
fi
