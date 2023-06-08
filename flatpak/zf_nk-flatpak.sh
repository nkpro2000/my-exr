# To avoid LXR dirs from $XDG_DATA_DIRS, which is updated by
# /etc/profile.d/flatpak.sh (to make the App s available from menu).
# Will be copied to /etc/profile.d/ by setup-lxr.py and run by /etc/profile 
# like `for profile in /etc/profile.d/*.sh; do test -r "$profile" && . "$profile"; done`.
# /etc/profile is sourced by all SHELLs, after initialized by login (which by init).

# shellcheck shell=sh
:

export XDG_DATA_DIRS
XDG_DATA_DIRS="$(echo $XDG_DATA_DIRS | sed 's/[^:]*\/mnt\/LinEx\/Root[^:]*//g' | sed 's/::\+/:/g')"
