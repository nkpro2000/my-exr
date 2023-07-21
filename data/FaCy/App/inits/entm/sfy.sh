# shellcheck shell=sh
mount_cryfs () {
    cryfs "/mnt/LinEx/Root/1Tux/nkpro/FaCyApp/.CryFs/entm/sfy/" "/mnt/LinEx/Root/1Tux/nkpro/.~/entm/.var/app/com.spotify.Client/" &&     ln -sfT "/mnt/LinEx/Root/1Tux/nkpro/.~/entm/.var/.cache/app/com.spotify.Client/cache" "/mnt/LinEx/Root/1Tux/nkpro/.~/entm/.var/app/com.spotify.Client/cache" &&     file "/mnt/LinEx/Root/1Tux/nkpro/.~/entm/.var/app/com.spotify.Client/cache"
}
run_flatpak () {
    echo "<> Enter b:to block spotify ADs | *:to use spotify with no modifications"
    read -r ad
    if test "$ad" = "b"; then
        echo "I> Blocking AD using https://github.com/abba23/spotify-adblock"
        cmd='eval "$(cat /app/bin/spotify |'
        cmd="$cmd"' sed s~LD_PRELOAD=~LD_PRELOAD=/mnt/LinEx/Root/1Tux/nkpro/FaCyApp/.HOMEs/entm/.spotify-adblock/spotify-adblock.so:~g |'
        cmd="$cmd"' sed s/'"'"'"$@" \+&'"'"'/'"'"'& sfy_pid=$!'"'"'/g)$(printf "\nwait \$sfy_pid")"'
        XDG_DATA_DIRS="/mnt/LinEx/Root/1Tux/nkpro/.~/entm/.local/share/flatpak/exports/share:/mnt/LinEx/Root/1Tux/flatpak/exports/share:/home/nkpro/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/" \
            HOME="/mnt/LinEx/Root/1Tux/nkpro/.~/entm/" flatpak --installation=lxr \
            --command=sh run com.spotify.Client -c "$cmd" /app/bin/spotify_mymod \
            --cache-path=/mnt/LinEx/Root/1Tux/nkpro/FaCyApp/.HOMEs/entm/.spotify-cache/ --show-console "$@"
    else
        XDG_DATA_DIRS="/mnt/LinEx/Root/1Tux/nkpro/.~/entm/.local/share/flatpak/exports/share:/mnt/LinEx/Root/1Tux/flatpak/exports/share:/home/nkpro/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/" \
            HOME="/mnt/LinEx/Root/1Tux/nkpro/.~/entm/" flatpak --installation=lxr \
            run com.spotify.Client --cache-path=/mnt/LinEx/Root/1Tux/nkpro/FaCyApp/.HOMEs/entm/.spotify-cache/ --show-console "$@"
    fi
}
# Give permission to app for "/mnt/LinEx/Root/1Tux/nkpro/.~/entm/.var/.cache/app/com.spotify.Client/cache/" , needed in some cases.
