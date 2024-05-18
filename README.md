# img_gen_intel_arc_dGPU

## Usage

### image details

The consume folder allows you to use the built image, which is hosted on dockerhub.  This takes least time.

The 'comfyui' folder contains the docker-compose for the comfyui image.  This is a docker image that is built from the intel/intel-extension-for-pytorch image.

A github action workflow processes this, building and publishing the image referenced in the consume folder docker-compose.yml:

<https://hub.docker.com/repository/docker/karmaterminal/comfyui_intel_arc_gpu>

### consume

```bash
# check ./consume/comfyui_launcher.env for env vars
cd ./consume
docker compose up
```

### build

this is what is done in the github actions workflow 'docker-publish.yml' file.  it builds the comfyui image and pushes it to dockerhub.

You can use it directly to build the image locally:

```bash
# check ./comfyui/comfyui_launcher.env for env vars
# there's probably a better way to suck in args for the compose, but I repeat them.
# I repeat them in the Dockerfile itself, they'll be overridden by the compose file (as some might try to run the Dockerfile directly)
cd ./comfyui
docker compose build
docker compose up
```

## Notes on WSL2

I'd not run this as a persistent service in WSL2, getting it to startup with the machine, as opposed to user login and first launch (turning on WSL2 debugging helps see all this) would need
to be emulated with a service wrapping the wsl commands.

hyper-v isn't a good solution for gpu passing, it doesn't present an intel arc gpu to the VM, and there's no capability with intel arc gpus to virtualize / share a gpu between VMs.

a different hypervisor, and pciex passthrough of the gpu device might work better, but I want to keep the top of this box on windows at the moment, and I hear proxmox USB passthrough is not good (I have a lot of USB devices).

Regardless, there are a few things I did to WSL2 to get this working nicely.

### at the windows host level (in %userprofile%/.wslconfig)

```bash
[wsl2]
# https://learn.microsoft.com/en-us/windows/wsl/wsl-config
# default is 50% system RAM.
memory=16GB
# in practice mirroring mode did not work nicely for me when contending with VMs under hyper-v on the same nic, and it also stops being able to inspect netstat
# output from within the wsl2 host - they'll appear bound at the windows host but not in the wsl2 host.  Which I found confusing.
localhostForwarding=true

# default is 25% of available RAM
swap=16GB

# Sets swapfile path location, default is %USERPROFILE%\AppData\Local\Temp\swap.vhdx
swapfile=C:\\wsl-swap\\wsl-swap.vhdx

# Disable page reporting so WSL retains all allocated memory claimed from Windows and releases none back when free
#pageReporting=false

# default is true - nested virtualization
nestedVirtualization=true

# Turns on output console showing contents of dmesg when opening a WSL 2 distro for debugging
debugConsole=true

# Enable experimental features
[experimental]
sparseVhd=true
```

### at the WSL2 level (in /etc/wsl.conf within WSL2)

```bash
[boot]
systemd = true

[network]
hostname = some-meaningful-name

[automount]
# Automatically mount the fixed drives (C:) under /mnt.  note these will be slow to access
# I fix this in a startup script to mount vdhx virtual drives at wsl startup (see 'boot' section below)
enabled = true
# Sets the `/etc/fstab` file to be processed when a WSL distribution is launched.
mountFsTab = true

[boot]
command="/scripts/mount_wsl2.sh"
```

that 'mount_wsl2.sh' script is not in this repo, as its not directly related to the project.
It mounts the vhdx drives I use for the project at WSL2 startup.  You'll get better performance in wsl using VHDX files mounted in WSL2 than you will using the /mnt/c/... paths.

I found it most effective NOT to do this as a startup script or login script via task scheduler at the windows level, having tried several methods - they didn't work consistently.

However, you can communicate back to the windows host from within wsl2 - so this runs, and then a tolerant /etc/fstab entry for the mounted drives is processed at WSL2 startup.

```bash
/mnt/c/WINDOWS/system32/wsl.exe --distribution Ubuntu-24.04 --mount --vhd Z:\\vhdx\\some_meaningful_name_wsl2_z.vhdx --bare
/mnt/c/WINDOWS/system32/wsl.exe --distribution Ubuntu-24.04 --mount --vhd Y:\\vhdx\\some_meaningful_name_wsl2_y.vhdx --bare
```

My /etc/fstab looks like this - the easiest way to initially create the vhdx is from the hyper-v managment console:

```bash
# VHDX files created in windows file system, formatted ext4 then mounted here
# use e.g. wsl -d Ubuntu-24.04 --mount --vhd Y:\vhdx\some_meaningful_name_wsl2_y.vhdx --bare
# to create, then sudo mkfs.ext4 /dev/sde (presuming it ended up being /dev/sde)
# veryify you can see them with lsblk, and then get their UUID with blkid
# in the /etc/fstab file, use the UUIDs to mount them:
# NOTE: the last value is 2. this makes the fstab processing wait for the disks to be available.
# this happens via a startup script in our /etc/wsl.conf file in this example.
# Possible entries are 0, 1 and 2.
# The root file system should have the highest priority 1
# all other file systems you want to have checked should have a 2.
# File systems with a value 0 will not be checked by the fsck utility.
# I find this helpful in the WSL2 debug output, as it verifies the disks being mounted.
UUID=00000000-0000-0000-0000-000000000000 /f ext4 defaults 0 2
UUID=11111111-1111-1111-1111-111111111111 /e ext4 defaults 0 2
```

## ERRATA: setup for vhdx files

### create vhd file

(it's easiest to do this one off in disk management ui)

```powershell
New-VHD -Path "Y:\vhdx\some_meaningful_name_wsl2_z.vhdx" -SizeBytes 400GB -Dynamic -BlockSizeBytes 1MB
wsl -d Ubuntu-24.04 --mount --vhd Y:\vhdx\elliott_wsl2_y.vhdx --bare
```

### get the UUID of the disks

from within wsl2 distro you're using:

```bash
sudo lsblk

# -------------
# output will include /dev/sd* entries for the disks you mounted

NAME  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0   7:0    0 472.8M  1 loop /mnt/wsl/docker-desktop/cli-tools
loop1   7:1    0 145.2M  1 loop
loop2   7:2    0 411.1M  1 loop
sda     8:0    0 388.5M  1 disk
sdb     8:16   0     1T  0 disk /mnt/wsl/docker-desktop/docker-desktop-user-distro
sdc     8:32   0     1T  0 disk /mnt/wsl/docker-desktop-data/isocache
sdd     8:48   0     1T  0 disk /mnt/wslg/distro
                                /
sde     8:64   0   400G  0 disk /f
sdf     8:80   0   400G  0 disk /e
```

```bash

sudo blkid

# -------------
# output will incldude UUIDs for the disks you mounted, not the UUID of the disks
# ...rest of output removed
/dev/sdf: UUID="00000000-0000-0000-0000-000000000000" BLOCK_SIZE="4096" TYPE="ext4"
/dev/sde: UUID="11111111-1111-1111-1111-111111111111" BLOCK_SIZE="4096" TYPE="ext4"
```

### format ext4 (assuming devices sde and sdf from prior output)

```bash
sudo mkfs.ext4 /dev/sde
sudo mkfs.ext4 /dev/sdf
```

at this point you can use them in the startup script in /etc/wsl.conf, described above, without bother.

## quick todo

* [ ] get starter models from huggingface-cli as it lets you specify author / repo and is a git lfs interaction - though dunno how interacts with placement yet / i.e. detritus cleanup
  * [ ] ^ seems to want to use /$HOME/.cache/huggingface/hub/ for cache.  who knows.
* [ ] for the build process - somehow get setuptools-scm version into a tag for the docker image as it'll change the thing every time files change in the repo. need it to increment up so may need that and some pad logic in `_scripts_versions.py`
* [ ] for the built image - docker scout is pissy about several (~35 at time of writing: 2024-05-14) things in the image libs. see what you can do about that (without breaking it...)

## links

* homepage = <https://github.com/karmafeast/img_gen_intel_arc_dGPU>
* docker-image = <https://hub.docker.com/repository/docker/karmaterminal/comfyui_intel_arc_gpu/general>
* documentation = <https://github.com/karmafeast/img_gen_intel_arc_dGPU/blob/main/README.md>
* repository = <https://github.com/karmafeast/img_gen_intel_arc_dGPU>
* issue-tracker = <https://github.com/karmafeast/img_gen_intel_arc_dGPU/issues>
