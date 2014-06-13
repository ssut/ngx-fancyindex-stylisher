import subprocess
import shlex

from shutil import copy
from sys import argv, stdout, stderr, exit
from platform import dist
from os import getuid, path

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Formatter:
    def __init__(self, fp=None, fmt=[]):
        self.fp = fp
        self.fmt = fmt

    def write(self, text):
        _text = ''
        for i in self.fmt:
            _text += i if len(i) > 0 else text
        self.fp.write(_text)

_stderr = stderr
stderr = Formatter(fp=_stderr, fmt=[Color.FAIL, '', Color.ENDC])

def _check_uid(uid=0):
    """
    check user unique id
    """
    return (uid == getuid())

def _check_dist(distribution='ubuntu'):
    """
    check linux distribution
    """
    current_dist = dist()
    return (distribution == current_dist[0].lower()
            if len(current_dist) > 0 else False)

def _check_apt(package, print_err=False):
    """
    check installed a package from dpkg list
    """
    command = ' '.join(['dpkg', '-L', package])
    command = shlex.split(command)
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if err or 'not installed' in out.lower():
        if print_err:
            print >> stderr, ('Cannot find {0} package ' +
                              'in your aptitude package list. ') \
                .format(package)
        return False

    return True

def install():
    """
    install fancyindex conf
    """
    if not path.isfile('/etc/nginx/fancyindex.conf'):
        copyfile('fancy/fancyindex.conf', '/etc/nginx/fancyindex.conf')



def template():
    """
    copy fancyindex template file to specify directory
    """


def main():
    if not _check_uid():
        print >> stderr, 'only root can run this script. ' + \
                         'recommend: run this script via sudo.'
        exit(1)

    if not _check_dist():
        print >> stderr, 'ubuntu only'
        exit(1)

    if not ((_check_apt('nginx') & _check_apt('nginx-extras')) |
            _check_apt('nginx-full')) or not path.isdir('/etc/nginx'):
        print >> stderr, 'Cannot find nginx, nginx-extras or nginx-full' + \
                         'package in your ubuntu aptitude package list.'
        exit(1)

    command = 'install' if len(argv) < 2 else argv[1]
    try:
        func = globals()[command]
    except KeyError:
        print >> stderr, 'unknown command: ', command
    else:
        func()

if __name__ == '__main__':
    main()
