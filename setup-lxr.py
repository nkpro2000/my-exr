#TODO add shebang with proper python env.
# This is the first file to run after cloning so that all are configured as intended.
# See comments ######### for steps involved in this process done by this script.
# Will be run user like `python setup-lxr.py` after cloning this repo in /mnt/LinEx/Root .

import os
import re
import sys

LINEXROOT = '/mnt/LinEx/Root/'
LINEXROOT = '/home/nkpro/nk/Lobby/my-exr/'

import types
snk = types.ModuleType(
    'from setup-nk',
    'Parsed only Functions from https://github.com/nkpro2000/my-dir/blob/master/setup-nk.py '
    # Because i am lazy to refactor setup-nk.py (if so simple import is enough).
)
sys.modules['snk'] = snk
PYFUNCTION = re.compile(r'(?<=\n)def .*\n(?: .*\n|\n)+')
with open(LINEXROOT + '.sub/my-dir/setup-nk.py') as f:
    code = f.read()
code = '\n\n'.join(PYFUNCTION.findall(code))
code = compile(code, 'Part of setup-nk.py', 'exec')
exec (
    code,
    {**globals(), 'NK_DIR':LINEXROOT},
    snk.__dict__
)

for dir in enumerate('Tux,Wine,Darling,Droid,Boxes'.split(',')):
    os.mkdir(f'/tmp/test/{dir[0]+1}{dir[1]}')
    snk.set_folder_icon(f'/tmp/test/{dir[0]+1}{dir[1]}/.directory', f'{dir[0]+1}_{dir[1]}.png')

