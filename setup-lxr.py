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

LINEXROOT_GIT = '/home/nkpro/nk/Lobby/my-exr/'

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
        'NK_DIR':LINEXROOT_GIT, # set_folder_icon uses icons from NK_DIR+'.assets/'+icon_path .
    },
    snk.__dict__
)


shutil.rmtree(LINEXROOT_OUT, ignore_errors=True)
os.makedirs(LINEXROOT_OUT, exist_ok=True)

for dir in enumerate('Tux,Wine,Darling,Droid,Boxes'.split(',')):
    os.mkdir(dir_path:=LINEXROOT_OUT+f'{dir[0]+1}{dir[1]}/')
    if os.path.isfile(LINEXROOT+f'{dir[0]+1}{dir[1]}/.directory'):
        shutil.copyfile(LINEXROOT+f'{dir[0]+1}{dir[1]}/.directory', dir_path+'.directory')
        # To avoid overwriting other contents in .directory file.
    snk.set_folder_icon(dir_path+'.directory', f'{dir[0]+1}_{dir[1]}.png')

