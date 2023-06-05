#TODO add shebang with proper python env.
# This is the first file to run after cloning so that all are configured as intended.
# See comments ######### for steps involved in this process done by this script.
# Will be run user like `python setup-lxr.py` after cloning this repo in /mnt/LinEx/Root .

import os
import sys
import re
import shutil

LINEXROOT = '/mnt/LinEx/Root/'
LINEXROOT_GIT = '/var/lxr/'+ os.environ['USER'] +'/LinExRoot_git/'
LINEXROOT_OUT = '/var/lxr/'+ os.environ['USER'] +'/LinExRoot_out/'
LINEXROOT_TMP = '/var/lxr/tmp/'+ os.environ['USER'] +'/'

LINEXROOT_GIT = '/home/nkpro/nk/Lobby/my-exr/'

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
##└── 5Boxes
snk.set_folder_icon(LINEXROOT_GIT+'.directory', '0_ExtensionRoot_git.png')
if os.path.isfile(LINEXROOT+'.directory'):
    shutil.copyfile(LINEXROOT+'.directory', LINEXROOT_OUT+'.directory')
snk.set_folder_icon(LINEXROOT_OUT+'.directory', '0_ExtensionRoot.png')
for dir in enumerate('Tux,Wine,Darling,Droid,Boxes'.split(',')):
    os.mkdir(dir_path:=LINEXROOT_OUT+f'{dir[0]+1}{dir[1]}/')
    if os.path.isfile(LINEXROOT+f'{dir[0]+1}{dir[1]}/.directory'):
        shutil.copyfile(LINEXROOT+f'{dir[0]+1}{dir[1]}/.directory', dir_path+'.directory')
        # To avoid overwriting other contents in .directory file.
    snk.set_folder_icon(dir_path+'.directory', f'{dir[0]+1}_{dir[1]}.png')
## Copy assets to LINEXROOT_TMP
shutil.copytree(LINEXROOT_GIT+'.assets/', LINEXROOT_TMP+'.assets/', dirs_exist_ok=True)


# Creating/Updating tree in LINEXROOT
######################################
script = r'''# shellcheck shell=sh

cd '''+ LINEXROOT_OUT + r''' || (echo 'no LinExRoot_out' && exit)
LXR='''+ LINEXROOT + r'''
THIS_USER='''+ os.environ['USER'] +r'''

for file in $(find ./ -type d | cut -d. -f2-); do
    # shellcheck disable=SC2174
    mkdir -m "$(stat -c '%a' .$file)" -p ${LXR}$file
    file_user=$(stat -c '%U' .$file)
    file_group=$(stat -c '%G' .$file)
    if test $file_user = $THIS_USER; then
        file_user=root
    fi
    if test $file_group = $THIS_USER; then
        file_group=root
    fi
    chown ${file_user}:${file_group} ${LXR}$file
done
for file in $(find ./ -type f | cut -d. -f2-); do
    if test ".$file" = './update-lxr.sh'; then
        continue
    fi
    cat .$file > ${LXR}$file
    chmod "$(stat -c '%a' .$file)" ${LXR}$file
    file_user=$(stat -c '%U' .$file)
    file_group=$(stat -c '%G' .$file)
    if test $file_user = $THIS_USER; then
        file_user=root
    fi
    if test $file_group = $THIS_USER; then
        file_group=root
    fi
    chown ${file_user}:${file_group} ${LXR}$file
done

'''
with open(LINEXROOT_OUT+'update-lxr.sh', 'w') as f:
    f.write(script)
os.system('sudo bash '+ LINEXROOT_OUT+'update-lxr.sh')
os.system('sudo -K')
