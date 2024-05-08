# SPDX-License-Identifier: Apache-2.0
ARG UBUNTU_VERSION=22.04
#FROM ubuntu:${UBUNTU_VERSION} AS oneapi-lib-installer

FROM intel/intel-extension-for-pytorch:2.1.30-xpu

# Install prerequisites to install oneAPI runtime libraries.
RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    ca-certificates \
    gnupg2 \
    gpg-agent \
    unzip \
    wget \
    htop \
    ubuntu-image \
    libjpeg-turbo-progs \
    libjpeg-turbo8 \
    libpng16-16 && \
    ldconfig && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define and install oneAPI runtime libraries for less space.
ARG DPCPP_VER=2024.1.0-963
ARG MKL_VER=2024.1.0-691
ARG CMPLR_COMMON_VER=2024.1

# Set apt install to not be interactive for things like tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Install certificate authorities to get access to secure connections to other places for downloads.
RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    ca-certificates \
    fonts-noto \
    gnupg2 \
    gpg-agent \
    software-properties-common && \
    apt-get upgrade -y --no-install-recommends --fix-missing && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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

# Copy the startup script to the /bin/ folder and make executable.
COPY startup.sh /bin/
RUN chmod 755 /bin/startup.sh

# move to /ComfyUI at startup.sh
COPY requirements-ipex.txt /requirements-ipex.txt
COPY requirements-comfy.txt /requirements-comfy.txt

RUN mkdir /scripts && chmod 755 /scripts
COPY get_models.py /scripts/get_models.py

COPY extra_model_paths.yaml /extra_model_paths.yaml

# Setup location of Python virtual environment and make sure LD_PRELOAD contains the path of the allocator chosen.
ENV VENVDir=/deps/venv
ENV LD_PRELOAD=${ALLOCATOR_LD_PRELOAD}

# Force 100% available VRAM size for compute-runtime.
# See https://github.com/intel/compute-runtime/issues/586
ENV NEOReadDebugKeys=1
ENV ClDeviceGlobalMemSizeAvailablePercent=100

# Enable SYCL variables for cache reuse and single threaded mode.
# See https://github.com/intel/llvm/blob/sycl/sycl/doc/EnvironmentVariables.md
ENV SYCL_CACHE_PERSISTENT=1
ENV SYCL_PI_LEVEL_ZERO_SINGLE_THREAD_MODE=1

# Enable double precision emulation just in case.
# See https://github.com/intel/compute-runtime/blob/master/opencl/doc/FAQ.md#feature-double-precision-emulation-fp64
ENV OverrideDefaultFP64Settings=1
ENV IGC_EnableDPEmulation=1

# Set variable for better training performance in case.
# See https://github.com/intel/intel-extension-for-pytorch/issues/296#issuecomment-1461118993
ENV IPEX_XPU_ONEDNN_LAYOUT=1

# Set to false if CPU is to be used to launch ComfyUI. XPU is default.
ARG UseXPU=true
ENV UseXPU=${UseXPU}

# Set to true if ipexrun is to be used to launch ComfyUI. Off by default.
ARG UseIPEXRUN=false
ENV UseIPEXRUN=${UseIPEXRUN}

# Set to the arguments you want to pass to ipexrun.
# Example for CPU: --multi-task-manager 'taskset' --memory-allocator ${ALLOCATOR}
# Example for XPU: --convert-fp64-to-fp32
ARG IPEXRUNArgs=""
ENV IPEXRUNArgs=${IPEXRUNArgs}

# Pass in ComfyUI arguments as an environment variable so it can be used in startup.sh which passes it on.
ARG ComfyArgs=""
ENV ComfyArgs=${ComfyArgs}

# Set location and entrypoint of the image to the ComfyUI directory and the startup script.
WORKDIR /ComfyUI

ENTRYPOINT [ "startup.sh" ]
