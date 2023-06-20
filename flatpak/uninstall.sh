#shellcheck shell=sh

pacman -Rs flatpak

rm /usr/lib/flatpak-system-helper_mymod
rm /etc/polkit-1/rules.d/org.freedesktop.Flatpak.rules

rm /usr/lib/flatpak-chown_noroot
rm /usr/lib/revokefs-fuse_noroot

rm /usr/lib/systemd/system/flatpak-rm-nomod.service
rm /usr/lib/systemd/system/flatpak-rm-nomod.path
systemctl daemon-reload


groupdel lxr
userdel fak

chown -hR root:root /var/lib/flatpak/
if mount | grep '/mnt/LinEx'; then chown -hR root:root /mnt/LinEx/Root/*/flatpak/
else echo '!> LinEx not mounted; do chown -hR root:root /mnt/LinEx/Root/*/flatpak/ after mount'; fi
