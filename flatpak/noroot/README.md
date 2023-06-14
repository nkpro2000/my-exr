# No root access for flatpak

Only flatpak-system-helper in Flatpak uses privileged access (to install flatpak in
system-wide locations).

## Making flatpak-system-helper run as 'fak' not 'root' user
> there is already 'flatpak' system account user, but i don't know what it is for.
>> `flatpak:x:972:972:Flatpak system helper:/:/usr/bin/nologin`

### Create system account User ('fak')
So, chown all the system wide location to 'fak'.
```bash
sudo useradd -MrUc 'Flatpak system-wide dirs' -d / -s /usr/bin/nologin fak
```
> ```
> ~ sh> sudo cat /etc/passwd | grep fak
> fak:x:954:954:Flatpak system-wide dirs:/:/usr/bin/nologin
> ~ sh> sudo cat /etc/shadow | grep fak
> fak:!:19521::::::
> ~ sh> sudo cat /etc/gshadow | grep fak
> fak:!::
> ~ sh> sudo cat /etc/group | grep fak                         
> fak:x:954:
> ```

### Modifying SystemD service
To run flatpak-system-helper as 'fak' user.
```bash
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/flatpak-system-helper.service.sed \
                        -i /usr/lib/systemd/system/flatpak-system-helper.service
```
> */usr/lib/systemd/system/flatpak-system-helper.service*
> ```diff
>  [Unit]
> -Description=flatpak system helper
> +Description=flatpak system helper (mymod)
>  
>  [Service]
> +User=fak
> +Group=fak
> +
>  BusName=org.freedesktop.Flatpak.SystemHelper
>  Environment=XDG_DATA_DIRS=/var/lib/flatpak/exports/share/:/usr/local/share/:/usr/share/
> -ExecStart=/usr/lib/flatpak-system-helper
> +ExecStart=/usr/lib/flatpak-system-helper_mymod
>  Type=dbus
>  IOSchedulingClass=idle
> ```

### Modifying DBus related files
```bash
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/org.freedesktop.Flatpak.SystemHelper.conf.sed \
                     -i /usr/share/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/org.freedesktop.Flatpak.SystemHelper.service.sed \
              -i /usr/share/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
```
> */usr/share/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf*
> ```diff
> @@ -8,7 +8,7 @@
>    <!-- This configuration file specifies the required security policies
>         for the the flatpak system helper to work. -->
>  
> -  <policy user="root">
> +  <policy user="fak">
>      <allow own="org.freedesktop.Flatpak.SystemHelper"/>
>    </policy>
>  
> ```
> */usr/share/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service*
> ```diff
>  [D-BUS Service]
>  Name=org.freedesktop.Flatpak.SystemHelper
> -Exec=/usr/lib/flatpak-system-helper
> +Exec=/usr/lib/flatpak-system-helper_mymod
>  SystemdService=flatpak-system-helper.service
> -User=root
> +User=fak
> ```

### Modifying Polkit .policy file of Flatpak
Adding 'fak' user as action owner, so no more this vVV error.
> Only trusted callers (e.g. uid 0 or an action owner) can use CheckAuthorization()
>> https://stackoverflow.com/questions/75573959/ask-for-authentication-when-calling-a-dbus-method-on-a-non-root-other-users-da

```bash
sudo sed \
    -f /var/lxr/$USER/LinExRoot_git/flatpak/noroot/org.freedesktop.Flatpak.policy.sed \
                    -i /usr/share/polkit-1/actions/org.freedesktop.Flatpak.policy
```
> */usr/share/polkit-1/actions/org.freedesktop.Flatpak.policy*
> ...
> ```diff
> @@ -289,6 +293,7 @@
>        <allow_inactive>auth_admin</allow_inactive>
>        <allow_active>yes</allow_active>
>      </defaults>
> +    <annotate key="org.freedesktop.policykit.owner">unix-user:fak</annotate>
>    </action>
>    <action id="org.freedesktop.Flatpak.modify-repo">
>      <!-- SECURITY:
> @@ -342,6 +347,7 @@
>        <allow_inactive>auth_admin</allow_inactive>
>        <allow_active>yes</allow_active>
>      </defaults>
> +    <annotate key="org.freedesktop.policykit.owner">unix-user:fak</annotate>
>    </action>
>    <action id="org.freedesktop.Flatpak.install-bundle">
>      <!-- SECURITY:
> ```
> ...

## Chown system-wide flatpak installations locations to 'fak'
So, flatpak-system-helper can work in these locations

```bash
sudo chown -hR fak:fak /path/of/the/folder # Eg. /var/lib/flatpak
```
```
~ >>> ls -ld /var/lib/flatpak
drwxr-xr-x 8 fak fak 4096 Jun 14 12:21 /var/lib/flatpak
```
