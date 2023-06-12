# my-exr

**To Setup :**
```bash
sudo mkdir -m u=rwx,g=,o= -p /var/lxr/$USER
sudo chown $USER:$USER /var/lxr/$USER
sudo mkdir -m 777 -p /var/lxr/tmp
sudo chmod +t /var/lxr/tmp

git clone https://github.com/nkpro2000/my-exr.git /var/lxr/$USER/LinExRoot_git
git -C /var/lxr/$USER/LinExRoot_git submodule init
git -C /var/lxr/$USER/LinExRoot_git submodule update

# Mount /mnt/LinEx/Root/
python /var/lxr/$USER/LinExRoot_git/setup-lxr.py

sudo -K
```


### Tux
* Flatpak
* Distrobox

### Wine
* WineHQ
  * Winetricks
* Bottles

### Darling
* DarlingHQ

### Droid
* Waydroid
* Anbox
* ARC Welder

### Boxes
* QEMU
* Podman (, Buildah, and Skopeo)
* Kubernetes
* Docker


> Move https://github.com/nkpro2000/my-WineDarlingDroid to here.
