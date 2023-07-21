# shellcheck shell=sh
mount_cryfs () {
    cryfs "/mnt/LinEx/Root/1Tux/nkpro/FaCyApp/.CryFs/comm/dc/" "/mnt/LinEx/Root/1Tux/nkpro/.~/comm/.var/app/com.discordapp.Discord/" &&     ln -sfT "/mnt/LinEx/Root/1Tux/nkpro/.~/comm/.var/.cache/app/com.discordapp.Discord/cache" "/mnt/LinEx/Root/1Tux/nkpro/.~/comm/.var/app/com.discordapp.Discord/cache" &&     file "/mnt/LinEx/Root/1Tux/nkpro/.~/comm/.var/app/com.discordapp.Discord/cache"
}
run_flatpak () {
    XDG_DATA_DIRS="/mnt/LinEx/Root/1Tux/nkpro/.~/comm/.local/share/flatpak/exports/share:/mnt/LinEx/Root/1Tux/flatpak/exports/share:/home/nkpro/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/"     HOME="/mnt/LinEx/Root/1Tux/nkpro/.~/comm/" flatpak --installation=lxr run com.discordapp.Discord  "$@"
}
# Give permission to app for "/mnt/LinEx/Root/1Tux/nkpro/.~/comm/.var/.cache/app/com.discordapp.Discord/cache/" , needed in some cases.
