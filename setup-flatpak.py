#TODO add shebang with proper python env.
# This script will install and setup flatpak with my modifications.
# Will be run user like `python /var/lxr/$USER/LinExRoot_git/setup-flatpak.py`.

import os
import sys
import shutil

LINEXROOT_FAKPKG = '/mnt/LinEx/Root/1Tux/'+os.environ['USER']+'/flatpak_pkg/'
LINEXROOT_GIT = '/var/lxr/'+ os.environ['USER'] +'/LinExRoot_git/'
LINEXROOT_FAKMOD = LINEXROOT_GIT+'flatpak/mymod/'
LINEXROOT_FAKNRO = LINEXROOT_GIT+'flatpak/noroot/'
LINEXROOT_BACKUP = LINEXROOT_GIT+'data/backup/'

MAKEPKG_CMD = 'makepkg -Lfs'

# Check LinEx is mounted
if (ec:=os.system("mount | grep '/mnt/LinEx'")) != 0:
    print('?> LinEx not mounted')
    sys.exit(ec)

os.makedirs(LINEXROOT_FAKPKG, exist_ok=True)
os.makedirs(LINEXROOT_BACKUP, exist_ok=True)


# Compile a modified flatpak-system-helper
## This modified version of flatpak-system-helper will pass all the parameters
## https://docs.flatpak.org/en/latest/libflatpak-api-reference.html#gdbus-org.freedesktop.Flatpak.SystemHelper
## passed to these^ methods to polkit_details_insert, so we can get that parameters
## in /etc/polkit-1/rules.d/org.freedesktop.Flatpak.rules by action.lookup("parameters");
## with these we can manage flatpak action more perfectly (for LinExRoot).

print('I> To compile a modified flatpak-system-helper')
pwd = os.getcwd()
os.chdir(LINEXROOT_FAKPKG)

if not os.path.isdir(LINEXROOT_FAKPKG+'flatpak/'):
    print('|> cloning https://gitlab.archlinux.org/archlinux/packaging/packages/flatpak')
    if (ec:=os.system("git clone https://gitlab.archlinux.org/archlinux/packaging/packages/flatpak")) != 0:
        os.chdir(pwd)
        sys.exit(ec)
    os.chdir(LINEXROOT_FAKPKG+'flatpak/')
else:
    print('|> pulling https://gitlab.archlinux.org/archlinux/packaging/packages/flatpak')
    os.chdir(LINEXROOT_FAKPKG+'flatpak/')
    if (ec:=os.system("git pull")) != 0:
        os.chdir(pwd)
        sys.exit(ec)

print('|> appling patch Apply-MyMod-for-Flatpak-system-helper-while-building.patch')
if (ec:=os.system("git apply -3 "+ LINEXROOT_FAKMOD+"Apply-MyMod-for-Flatpak-system-helper-while-building.patch")) != 0:
    os.chdir(pwd)
    sys.exit(ec)
# This^ patch is used to modify PKGBUILD of arch flatpak pkg, to apply my modifications
# on flatpak_git/system-helper/flatpak-system-helper.c while `makepkg -Lfs`.
os.system('cp '+ LINEXROOT_FAKMOD+'MyMod-of-Flatpak-system-helper-polkit_details_insert-installation.patch ./')

print('|> appling patch Apply-NoRoot-for-Flatpak-system-helper-while-building.patch')
if (ec:=os.system("git apply -3 "+ LINEXROOT_FAKNRO+"Apply-NoRoot-for-Flatpak-system-helper-while-building.patch")) != 0:
    os.chdir(pwd)
    sys.exit(ec)
# This^ patch is used to modify PKGBUILD of arch flatpak pkg, to apply my modifications
# on flatpak_git/system-helper/flatpak-system-helper.c while `makepkg -Lfs`.
os.system('cp '+ LINEXROOT_FAKNRO+'Using-flatpak-chown_noroot-instead-of-unistd-chown-so-noroot.patch ./')

print('|> making flatpak pkg (using archlinux PKGBUILD file)')
ec=os.system(MAKEPKG_CMD)
while ec!=0:
    print('x> makepkg exited with exitcode',ec)
    i_ = input('   Enter r:to_retry|R:to_retry_with_flags|x:cancel|*:to_procede_anyway >')
    if i_ == 'r':
        ec=os.system(MAKEPKG_CMD)
    elif i_ == 'R':
        ec=os.system(MAKEPKG_CMD+input('>>>'+MAKEPKG_CMD))
    elif i_ == 'x':
        os.chdir(pwd)
        sys.exit(ec)
    else: break

print('|> extracting files from pkg')
os.chdir(LINEXROOT_FAKPKG)
if (ec:=os.system('cp ./flatpak/flatpak-1*.pkg.tar.zst flatpak.pkg.tar.zst')) != 0:
    os.chdir(pwd)
    sys.exit(ec)

shutil.rmtree(LINEXROOT_FAKPKG+'fak/', ignore_errors=True)
os.makedirs(LINEXROOT_FAKPKG+'fak/')
os.system('unzstd flatpak.pkg.tar.zst')
os.system('tar -xvf flatpak.pkg.tar -C ./fak')

os.chdir(pwd)


# Updating files of Flatpak
############################
script = r'''# shellcheck shell=sh

cd '''+ LINEXROOT_FAKPKG + r''' || (echo 'no LinExRoot_FlatpAKPKG' && exit)
FAKM='''+ LINEXROOT_FAKMOD + r'''
FAKN='''+ LINEXROOT_FAKNRO + r'''
BKUP='''+ LINEXROOT_BACKUP + r'''
THIS_USER='''+ os.environ['USER'] +r'''

pacman -Sy flatpak

cp /usr/lib/systemd/system/flatpak-system-helper.service "$BKUP"
cp /usr/share/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service "$BKUP"
mv /usr/lib/flatpak-system-helper "$BKUP"

sed -f "$FAKM"flatpak-system-helper.service.sed -i /usr/lib/systemd/system/flatpak-system-helper.service
sed -f "$FAKM"org.freedesktop.Flatpak.SystemHelper.service.sed \
    -i /usr/share/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
cp ./fak/usr/lib/flatpak-system-helper /usr/lib/flatpak-system-helper_mymod

cp "$FAKM"org.freedesktop.Flatpak.rules /etc/polkit-1/rules.d/

cp /usr/share/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf "$BKUP"
cp /usr/share/polkit-1/actions/org.freedesktop.Flatpak.policy "$BKUP"

sed -f "$FAKN"flatpak-system-helper.service.sed -i /usr/lib/systemd/system/flatpak-system-helper.service
sed -f "$FAKN"org.freedesktop.Flatpak.SystemHelper.service.sed \
    -i /usr/share/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
sed -f "$FAKN"org.freedesktop.Flatpak.SystemHelper.conf.sed \
    -i /usr/share/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf

sed -f "$FAKN"org.freedesktop.Flatpak.policy.sed \
    -i /usr/share/polkit-1/actions/org.freedesktop.Flatpak.policy

cp "$FAKM"to_avoid_unmod-flatpak/flatpak-rm-nomod.service /usr/lib/systemd/system/
cp "$FAKM"to_avoid_unmod-flatpak/flatpak-rm-nomod.path /usr/lib/systemd/system/
systemctl daemon-reload
systemctl enable --now flatpak-rm-nomod.path

groupadd lxr
usermod --append --group lxr "$THIS_USER"

useradd -MrUc 'Flatpak system-wide dirs' -d / -s /usr/bin/nologin fak
chown -hR fak:fak /var/lib/flatpak/
chown -hR fak:fak /mnt/LinEx/Root/*/flatpak/

'''
with open(LINEXROOT_FAKPKG+'update-flatpak.sh', 'w') as f:
    f.write(script)
print('I> To run bash Script to add/remove/replace some files of Flatpak package')
print('I> to apply my modifications. So, we can use Flatpak for LXR in our own way.')
print('|> $ sudo bash '+ LINEXROOT_FAKPKG+'update-flatpak.sh # Ctrl+D to skip')
os.system('sudo bash '+ LINEXROOT_FAKPKG+'update-flatpak.sh')
os.system('sudo -K')
