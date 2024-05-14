# img_gen_intel_arc_dGPU

## links

homepage = "<https://github.com/karmafeast/img_gen_intel_arc_dGPU>"
docker-image = "<https://hub.docker.com/repository/docker/karmaterminal/comfyui_intel_arc_gpu/general>"
documentation = "<https://github.com/karmafeast/img_gen_intel_arc_dGPU/blob/main/README.md>"
repository = "<https://github.com/karmafeast/img_gen_intel_arc_dGPU>"
issue-tracker = "<https://github.com/karmafeast/img_gen_intel_arc_dGPU/issues>"

rough, not nice yet. working on ARC A770m.

I'm using this as a base image for my Intel Arc dGPU (using a A770m) -
image: <https://hub.docker.com/r/intel/intel-extension-for-pytorch>
from: <https://github.com/intel/ai-containers>

you can run the built image (what gets built in './comfyui by github actions) and put to docker hub with:

* note that env stuff is in `./consume/comfyui_launcher.env`

```bash
cd ./consume
docker compose up
```

you can build it locally from the `./comfyui` docker-compose as well, should you like.

## quick todo

* [ ] get starter models from huggingface-cli as it lets you specify author / repo and is a git lfs interaction - though dunno how interacts with placement yet / i.e. detritus cleanup
  * [ ] ^ seems to want to use /$HOME/.cache/huggingface/hub/ for cache.  who knows.
* [ ] for the build process - somehow get setuptools-scm version into a tag for the docker image as it'll change the thing every time files change in the repo. need it to increment up so may need that and some pad logic in `_scripts_versions.py`
* [ ] for the built image - docker scout is pissy about several (~35 at time of writing: 2024-05-14) things in the image libs. see what you can do about that (without breaking it...)
