# img_gen_intel_arc_dGPU

rough, not nice yet.

I'm using this as a base image for my Intel Arc dGPU (using a A770m) -
image: https://hub.docker.com/r/intel/intel-extension-for-pytorch
from: https://github.com/intel/ai-containers


## quick todo
- [ ] get starter models from huggingface-cli as it lets you specify author / repo and is a git lfs interaction - though dunno how interacts with placement yet / i.e. detritus cleanup
- [ ] ^ seems to want to use /$HOME/.cache/huggingface/hub/ for cache.  who knows.