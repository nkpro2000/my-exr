# No root access for flatpak

Only flatpak-system-helper in Flatpak uses privileged access (to install flatpak in
system-wide locations).

## Making flatpak-system-helper run as 'fak' not 'root' user
> there is already 'flatpak' system account user, but i don't know what it is for.

### Create system account User ('fak')
So, chown all the system wide location to 'fak'.
```bash
sudo useradd -MrUc 'Flatpak system-wide dirs' -d / -s /usr/bin/nologin fak
```

### Modifying SystemD service
To run flatpak-system-helper as 'fak' user.
```bash
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/flatpak-system-helper.service.sed \
                        -i /usr/lib/systemd/system/flatpak-system-helper.service
```

### Modifying DBus related files
```bash
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/org.freedesktop.Flatpak.SystemHelper.conf.sed \
                     -i /usr/share/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/org.freedesktop.Flatpak.SystemHelper.service.sed \
              -i /usr/share/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
```

### Modifying Polkit .policy file of Flatpak
Adding 'fak' user as action owner, so no more this vVV error.
> Only trusted callers (e.g. uid 0 or an action owner) can use CheckAuthorization()
>> https://stackoverflow.com/questions/75573959/ask-for-authentication-when-calling-a-dbus-method-on-a-non-root-other-users-da

```bash
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/org.freedesktop.Flatpak.policy.sed \
                    -i /usr/share/polkit-1/actions/org.freedesktop.Flatpak.policy
```
