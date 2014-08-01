# Inspired by http://eli.thegreenplace.net/2013/04/20/bootstrapping-virtualenv/
from __future__ import print_function
import sys
import subprocess
from subprocess import PIPE


VENV_VERSION = '1.11.6'
PYPI_VENV_BASE = 'https://pypi.python.org/packages/source/v/virtualenv'
INITIAL_ENV = '.env'


def exec_cmd(cmd, echo=False):
    """Run 'cmd' and return its stdout.
    """
    if echo:
        print('[cmd] {0}'.format(cmd))
    out = subprocess.check_output(cmd, stderr=PIPE, shell=True)
    if echo:
        print(out)
    return out

if len(sys.argv) > 1:
    PYTHON = sys.argv[1]
else:
    PYTHON = 'python'

dirname = 'virtualenv-' + VENV_VERSION
tgz_file = dirname + '.tar.gz'

venv_url = PYPI_VENV_BASE + '/' + tgz_file

exec_cmd('curl -O {0}'.format(venv_url))
exec_cmd('tar xzf {0}'.format(tgz_file))
exec_cmd('{0} {1}/virtualenv.py {2}'.format(PYTHON, dirname, INITIAL_ENV))
exec_cmd('{0}/bin/pip install {1}'.format(INITIAL_ENV, tgz_file))
exec_cmd('rm -rf {0} {1}'.format(dirname, tgz_file))
