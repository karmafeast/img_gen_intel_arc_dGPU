# # SPDX-License-Identifier: Apache-2.0
FROM intel/intel-extension-for-pytorch:2.1.30-xpu as comfyui_base
SHELL ["/bin/bash", "-l", "-c"]
ARG PATH_COMFY_BASE=/ComfyUI
ARG PATH_COMFY_INPUT=/ComfyUI_input
ARG PATH_COMFY_MODELS=/ComfyUI_models
ARG PATH_COMFY_OUTPUT=/ComfyUI_ouput
ARG PATH_COMFY_PY_DEPENDS=/ComfyUI_deps
ARG PATH_INIT_TOUCH_FILE=/ComfyUI_deps/touchme.comfyinit
ARG PYTHON_VERSION=3.11.9

ARG UseXPU=true
ARG NEOReadDebugKeys=1
ARG ClDeviceGlobalMemSizeAvailablePercent=100
ARG SYCL_PI_LEVEL_ZERO_SINGLE_THREAD_MODE=0
ARG SYCL_CACHE_PERSISTENT=1
ARG OverrideDefaultFP64Settings=1
ARG IGC_EnableDPEmulation=1
ARG IPEX_XPU_ONEDNN_LAYOUT=1
# set COMFYUI_MODELS_DOWNLOAD to 1 if want to run get_models.py if container 1st start,
#  --> you can override this in ../docker-compose.yaml and ignore this value
ARG COMFYUI_MODELS_DOWNLOAD=0
ARG UseXPU=true
# Set to the arguments you want to pass to ipexrun.
# Example for CPU: --multi-task-manager 'taskset' --memory-allocator ${ALLOCATOR}
# Example for XPU: --convert-fp64-to-fp32
ARG IPEXRUNArgs="--convert-fp64-to-fp32"
ARG UseIPEXRUN=true
#ARG ALLOCATOR_LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc.so
ARG DPCPP_VER=2024.1.0-963
ARG MKL_VER=2024.1.0-691
ARG CMPLR_COMMON_VER=2024.1
ARG ComfyArgs=--normalvram --preview-method auto --listen --use-pytorch-cross-attention

# Set apt install to not be interactive
ENV DEBIAN_FRONTEND=noninteractive

ENV PATH_COMFY_BASE=$PATH_COMFY_BASE
ENV PATH_COMFY_INPUT=$PATH_COMFY_INPUT
ENV PATH_COMFY_MODELS=$PATH_COMFY_MODELS
ENV PATH_COMFY_OUTPUT=$PATH_COMFY_OUTPUT
ENV PATH_COMFY_PY_DEPENDS=$PATH_COMFY_PY_DEPENDS
ENV PATH_INIT_TOUCH_FILE=$PATH_INIT_TOUCH_FILE
ENV PYTHON_VERSION=$PYTHON_VERSION
ENV UseXPU=$UseXPU
ENV NEOReadDebugKeys=$NEOReadDebugKeys
ENV ClDeviceGlobalMemSizeAvailablePercent=$ClDeviceGlobalMemSizeAvailablePercent
# set COMFYUI_MODELS_DOWNLOAD to 1 if want to run get_models.py if container 1st start,
#  --> you can override this in ../docker-compose.yaml and ignore this value
ENV COMFYUI_MODELS_DOWNLOAD=$COMFYUI_MODELS_DOWNLOAD
# Set to the arguments you want to pass to ipexrun.
# Example for CPU: --multi-task-manager 'taskset' --memory-allocator ${ALLOCATOR}
# Example for XPU: --convert-fp64-to-fp32
ENV IPEXRUNArgs=$IPEXRUNArgs
ENV UseIPEXRUN=$UseIPEXRUN
# Force 100% available VRAM size for compute-runtime.
# See https://github.com/intel/compute-runtime/issues/586
ENV ClDeviceGlobalMemSizeAvailablePercent=$ClDeviceGlobalMemSizeAvailablePercent
#ENV LD_PRELOAD=$ALLOCATOR_LD_PRELOAD
ENV ComfyArgs="$ComfyArgs --output-directory $PATH_COMFY_OUTPUT --input-directory $PATH_COMFY_INPUT"

RUN printenv

# Install Python and other associated packages from PPA since default is 3.10
ARG PYTHON=python3.11
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    ${PYTHON} \
    lib${PYTHON} \
    python3-pip \
    ${PYTHON}-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update pip
RUN pip --no-cache-dir install --upgrade \
    pip \
    setuptools

# Softlink Python to make it default.
RUN ln -sf "$(which ${PYTHON})" /usr/local/bin/python && \
    ln -sf "$(which ${PYTHON})" /usr/local/bin/python3 && \
    ln -sf "$(which ${PYTHON})" /usr/bin/python && \
    ln -sf "$(which ${PYTHON})" /usr/bin/python3

# Sets versions of Level-Zero, OpenCL and memory allocator chosen.
ARG ALLOCATOR_LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc.so

# Install Comfy UI/Pytorch dependencies.
RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    ${ALLOCATOR_PACKAGE} \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    git \
    numactl && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

# Install prerequisites to install oneAPI runtime libraries.
RUN echo "|__> GETTING PACKAGES..." && \
    apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    bat \
    build-essential \
    ca-certificates \
    curl \
    fonts-noto \
    fonts-powerline \
    git \
    gnupg2 \
    google-perftools \
    gpg-agent \
    htop \
    iproute2 \
    iputils-ping \
    jq \
    libbz2-dev \
    libc6-dev \
    libffi-dev \
    libgdbm-dev \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libjpeg-turbo-progs \
    libjpeg-turbo8 \
    libncursesw5-dev \
    libpng16-16 \
    libreadline-dev \
    libsqlite3-dev \
    libsqlite3-dev \
    libssl-dev \
    libssl-dev \
    libtk tk-dev \
    libxcb-render-util0-dev \
    libxcb-shape0-dev \
    libxcb-xfixes0-dev \
    lzma liblzma-dev \
    net-tools \
    numactl \
    openssl \
    software-properties-common \
    tk \
    tk-dev \
    ubuntu-image \
    unzip \
    zlib1g-dev \
    wget && \
    ldconfig && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "|__> build/installing jless (json viewer)..." && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y
RUN cargo install jless


RUN echo "|__> linking batcat to replace cat, setting no paging..." && \
    ln -s /usr/bin/batcat /usr/local/bin/cat && \
    ln -s /usr/bin/batcat /usr/local/bin/bat && \
    echo 'export BAT_PAGER=""' >> ~/.bashrc

# # install pyenv, and put PYTHON_VERSION as global python version
# RUN echo "|__> PYTHON - INSTALLING PYENV..." && \
#     curl https://pyenv.run | bash

# RUN . ~/.bashrc && \
#     echo "|__> PYTHON BEFORE PYENV..." && \
#     echo "|____> which python: $(which python)" && \
#     echo "|____> which python3: $(which python3)" && \
#     echo "|____> which pip: $(which pip)" && \
#     echo "|____> which pip3: $(which pip3)" && \
#     echo "|____> env vars:" && \
#     jq -n 'env' && \
#     printenv

# RUN echo "|__> YOU MAY SEE ERRORS HERE ABOUT LOADING ENVVARS FOR PYENV, YOU CAN IGNORE..." && \
#     echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
#     echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
#     echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
#     echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile && \
#     echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile && \
#     echo 'eval "$(pyenv init -)"' >> ~/.profile

# RUN . ~/.bashrc && \
#     pyenv update && \
#     pyenv doctor && \
#     pyenv install ${PYTHON_VERSION} && \
#     pyenv global ${PYTHON_VERSION}

# RUN . ~/.bashrc && \
#     echo "|__> PYTHON AFTER PYENV..." && \
#     echo "|____> which python: $(which python)" && \
#     echo "|____> which python3: $(which python3)" && \
#     echo "|____> which pip: $(which pip)" && \
#     echo "|____> which pip3: $(which pip3)" && \
#     echo "|____> env vars:" && \
#     jq -n 'env' && \
#     printenv

FROM comfyui_base as comfyui_launcher
SHELL ["/bin/bash", "-l", "-c"]

ARG PATH_COMFY_BASE=/ComfyUI
ARG PATH_COMFY_INPUT=/ComfyUI_input
ARG PATH_COMFY_MODELS=/ComfyUI_models
ARG PATH_COMFY_OUTPUT=/ComfyUI_ouput
ARG PATH_COMFY_PY_DEPENDS=/ComfyUI_deps
ARG PATH_INIT_TOUCH_FILE=/ComfyUI_deps/touchme.comfyinit
ARG PYTHON_VERSION=3.11.9

ARG UseXPU=true
ARG NEOReadDebugKeys=1
ARG ClDeviceGlobalMemSizeAvailablePercent=100
ARG SYCL_PI_LEVEL_ZERO_SINGLE_THREAD_MODE=0
ARG SYCL_CACHE_PERSISTENT=1
ARG OverrideDefaultFP64Settings=1
ARG IGC_EnableDPEmulation=1
ARG IPEX_XPU_ONEDNN_LAYOUT=1
# set COMFYUI_MODELS_DOWNLOAD to 1 if want to run get_models.py if container 1st start,
#  --> you can override this in ../docker-compose.yaml and ignore this value
ARG COMFYUI_MODELS_DOWNLOAD=0
ARG UseXPU=true
# Set to the arguments you want to pass to ipexrun.
# Example for CPU: --multi-task-manager 'taskset' --memory-allocator ${ALLOCATOR}
# Example for XPU: --convert-fp64-to-fp32
ARG IPEXRUNArgs="--convert-fp64-to-fp32"
ARG UseIPEXRUN=true
ARG ALLOCATOR_LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc.so
ARG DPCPP_VER=2024.1.0-963
ARG MKL_VER=2024.1.0-691
ARG CMPLR_COMMON_VER=2024.1
ARG ComfyArgs=--normalvram --preview-method auto --listen --use-pytorch-cross-attention

# Set apt install to not be interactive
ENV DEBIAN_FRONTEND=noninteractive

ENV PATH_COMFY_BASE=$PATH_COMFY_BASE
ENV PATH_COMFY_INPUT=$PATH_COMFY_INPUT
ENV PATH_COMFY_MODELS=$PATH_COMFY_MODELS
ENV PATH_COMFY_OUTPUT=$PATH_COMFY_OUTPUT
ENV PATH_COMFY_PY_DEPENDS=$PATH_COMFY_PY_DEPENDS
ENV PATH_INIT_TOUCH_FILE=$PATH_INIT_TOUCH_FILE
ENV PYTHON_VERSION=$PYTHON_VERSION
ENV UseXPU=$UseXPU
ENV NEOReadDebugKeys=$NEOReadDebugKeys
ENV ClDeviceGlobalMemSizeAvailablePercent=$ClDeviceGlobalMemSizeAvailablePercent
# set COMFYUI_MODELS_DOWNLOAD to 1 if want to run get_models.py if container 1st start,
#  --> you can override this in ../docker-compose.yaml and ignore this value
ENV COMFYUI_MODELS_DOWNLOAD=$COMFYUI_MODELS_DOWNLOAD
# Set to the arguments you want to pass to ipexrun.
# Example for CPU: --multi-task-manager 'taskset' --memory-allocator ${ALLOCATOR}
# Example for XPU: --convert-fp64-to-fp32
ENV IPEXRUNArgs=$IPEXRUNArgs
ENV UseIPEXRUN=$UseIPEXRUN
# Force 100% available VRAM size for compute-runtime.
# See https://github.com/intel/compute-runtime/issues/586
ENV ClDeviceGlobalMemSizeAvailablePercent=$ClDeviceGlobalMemSizeAvailablePercent
#ENV LD_PRELOAD=$ALLOCATOR_LD_PRELOAD
ENV ComfyArgs="$ComfyArgs --output-directory $PATH_COMFY_OUTPUT --input-directory $PATH_COMFY_INPUT"
ENV ALLOCATOR_LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc.so
# Copy the startup script to the /bin/ folder and make executable.
COPY startup.sh /bin/
RUN chmod 755 /bin/startup.sh

# move to /ComfyUI at startup.sh
COPY requirements-ipex.txt $PATH_COMFY_PY_DEPENDS/requirements-ipex.txt
COPY requirements-comfy.txt $PATH_COMFY_PY_DEPENDS/requirements-comfy.txt

RUN mkdir $PATH_COMFY_PY_DEPENDS/scripts && chmod 755 $PATH_COMFY_PY_DEPENDS/scripts
COPY get_models.py $PATH_COMFY_PY_DEPENDS/scripts/get_models.py

COPY extra_model_paths.yaml /extra_model_paths.yaml

# Update system pip / setuptools
RUN pip --no-cache-dir install --upgrade \
    pip \
    setuptools

RUN echo "|____> env vars:" && \
    jq -n 'env'

# Set location and entrypoint of the image to the ComfyUI directory and the startup script.
WORKDIR ${PATH_COMFY_BASE}

ENTRYPOINT [ "/bin/bash", "-l", "-c", "startup.sh" ]
