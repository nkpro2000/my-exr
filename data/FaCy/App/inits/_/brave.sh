# shellcheck shell=sh
mount_cryfs () {
    cryfs "/mnt/LinEx/Root/1Tux/nkpro/FaCyApp/.CryFs/_/brave/" "/mnt/LinEx/Root/1Tux/nkpro/.~/_/.var/app/com.brave.Browser/" &&     ln -sfT "/mnt/LinEx/Root/1Tux/nkpro/.~/_/.var/.cache/app/com.brave.Browser/cache" "/mnt/LinEx/Root/1Tux/nkpro/.~/_/.var/app/com.brave.Browser/cache" &&     file "/mnt/LinEx/Root/1Tux/nkpro/.~/_/.var/app/com.brave.Browser/cache"
}
run_flatpak () {
    XDG_DATA_DIRS="/mnt/LinEx/Root/1Tux/nkpro/.~/_/.local/share/flatpak/exports/share:/mnt/LinEx/Root/1Tux/flatpak/exports/share:/home/nkpro/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/"     HOME="/mnt/LinEx/Root/1Tux/nkpro/.~/_/" flatpak --installation=lxr run com.brave.Browser  "$@"
}
# Give permission to app for "/mnt/LinEx/Root/1Tux/nkpro/.~/_/.var/.cache/app/com.brave.Browser/cache/" , needed in some cases.
