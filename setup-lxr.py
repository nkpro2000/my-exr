#TODO add shebang with proper python env.
# This is the first file to run after cloning so that all are configured as intended.
# See comments ######### for steps involved in this process done by this script.
# Will be run by user like `python setup-lxr.py`, after cloning this repo (follow README.md).

import os
import sys
import re
import shutil

LINEXROOT = '/mnt/LinEx/Root/'
LINEXROOT_GIT = '/var/lxr/'+ os.environ['USER'] +'/LinExRoot_git/'
LINEXROOT_OUT = '/var/lxr/'+ os.environ['USER'] +'/LinExRoot_out/'
LINEXROOT_TMP = '/var/lxr/tmp/'+ os.environ['USER'] +'/'

# Check LinEx is mounted
if (ec:=os.system("mount | grep '/mnt/LinEx'")) != 0:
    print('?> LinEx not mounted'+str(ec))
    sys.exit(ec)

os.makedirs(LINEXROOT_TMP, exist_ok=True)

import types
snk = types.ModuleType(
    'from setup-nk',
    'Parsed only Functions from https://github.com/nkpro2000/my-dir/blob/master/setup-nk.py '
    # Because i am lazy to refactor setup-nk.py (if so simple import is enough).
)
sys.modules['snk'] = snk
PYFUNCTION = re.compile(r'(?<=\n)def .*\n(?: .*\n|\n)+')
with open(LINEXROOT_GIT + '.sub/my-dir/setup-nk.py') as f:
    code = f.read()
code = '\n\n'.join(PYFUNCTION.findall(code))
code = compile(code, 'Part of setup-nk.py', 'exec')
exec (
    code,
    {
        **globals(),
        'NK_DIR':LINEXROOT_TMP, # set_folder_icon uses icons from NK_DIR+'.assets/'+icon_path .
    },
    snk.__dict__
)


# Cleaning LinExRoot_out
shutil.rmtree(LINEXROOT_OUT, ignore_errors=True)
os.makedirs(LINEXROOT_OUT, exist_ok=True)


# Making Dirs and adding icons
###############################
##├── 1Tux
##├── 2Wine
##├── 3Darling
##├── 4Droid
##├── 5Boxes
##├── 6Games
##└── 7Temps
shutil.copytree( # Copy assets to LINEXROOT_TMP, before adding icons to dirs.
    LINEXROOT_GIT+'.assets/', LINEXROOT_TMP+'.assets/',
    dirs_exist_ok=True
)
snk.set_folder_icon(LINEXROOT_GIT+'.directory', '0_ExtensionRoot_git.png')
if os.path.isfile(LINEXROOT+'.directory'):
    shutil.copyfile(LINEXROOT+'.directory', LINEXROOT_OUT+'.directory')
snk.set_folder_icon(LINEXROOT_OUT+'.directory', '0_ExtensionRoot.png')
for dir in enumerate('Tux,Wine,Darling,Droid,Boxes,Games,Temps'.split(',')):
    os.mkdir(dir_path:=LINEXROOT_OUT+f'{dir[0]+1}{dir[1]}/')
    if os.path.isfile(LINEXROOT+f'{dir[0]+1}{dir[1]}/.directory'):
        shutil.copyfile(LINEXROOT+f'{dir[0]+1}{dir[1]}/.directory', dir_path+'.directory')
        # To avoid overwriting other contents in .directory file.
    if os.path.isfile(LINEXROOT_TMP+'.assets/'+f'{dir[0]+1}_{dir[1]}.png'):
        snk.set_folder_icon(dir_path+'.directory', f'{dir[0]+1}_{dir[1]}.png')
    # for Flatpak
    os.mkdir(dir_path+'flatpak')
    os.mkdir(dir_path+os.environ['USER'], mode=0o700)
    os.makedirs(dir_path+os.environ['USER']+'/.local/share/flatpak/overrides/', exist_ok=True)
    with open(dir_path+os.environ['USER']+'/.local/share/flatpak/overrides/com.github.tchx84.Flatseal','w') as f:
        f.write(
            '[Context]\nfilesystems=!xdg-data/flatpak/app;!/var/lib/flatpak/app;'+\
                #'/etc/flatpak/installations.d/:ro;'+\
                'host-etc:ro;'+ #github.com/flatpak/flatpak/issues/4525 \
                LINEXROOT+f'{dir[0]+1}{dir[1]}/flatpak/app:ro\n'
        )


# Creating/Updating tree in LINEXROOT
######################################
script = r'''# shellcheck shell=sh

cd '''+ LINEXROOT_OUT + r''' || (echo 'no LinExRoot_out' && exit)
LXR='''+ LINEXROOT + r'''
THIS_USER='''+ os.environ['USER'] +r'''

mkdir -p "$LXR"
for file in $(find ./ -type d | cut -d. -f2-); do
    # shellcheck disable=SC2174
    mkdir -m "$(stat -c '%a' ".$file")" -p "${LXR}$file"
    file_user=$(stat -c '%U' ".$file")
    file_group=$(stat -c '%G' ".$file")
    case ".$file" in *"/$THIS_USER/"*);; *"/$THIS_USER");; *) #Look4Doc#
        if test "$file_user" = "$THIS_USER"; then
            file_user=root
        fi
        if test "$file_group" = "$THIS_USER"; then
            file_group=root
        fi
    esac
    chown "${file_user}:${file_group}" "${LXR}$file"
done
for file in $(find ./ -type f | cut -d. -f2-); do
    if test ".$file" = './update-lxr.sh'; then
        continue
    fi
    cat ".$file" > "${LXR}$file"
    chmod "$(stat -c '%a' ".$file")" "${LXR}$file"
    file_user=$(stat -c '%U' ".$file")
    file_group=$(stat -c '%G' ".$file")
    case ".$file" in *"/$THIS_USER/"*);; *)
        if test "$file_user" = "$THIS_USER"; then
            file_user=root
        fi
        if test "$file_group" = "$THIS_USER"; then
            file_group=root
        fi
    esac
    chown "${file_user}:${file_group}" "${LXR}$file"
done

mkdir -p /etc/flatpak/installations.d/
cp '''+ LINEXROOT_GIT +r'''flatpak/LXR-*.conf /etc/flatpak/installations.d/

cp '''+ LINEXROOT_GIT +r'''flatpak/zf_nk-flatpak.sh /etc/profile.d/

''' #Look4Doc#
with open(LINEXROOT_OUT+'update-lxr.sh', 'w') as f:
    f.write(script)
print('I> To run bash Script to apply changes to '+LINEXROOT)
print('I> this will only update specific file/dir, other are left unchanged.')
print('|> $ sudo bash '+ LINEXROOT_OUT+'update-lxr.sh # Ctrl+D to skip')
os.system('sudo bash '+ LINEXROOT_OUT+'update-lxr.sh')
os.system('sudo -K')
