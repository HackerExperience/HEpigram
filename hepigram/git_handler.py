import shutil
from hepigram.utils import call, get_extension


CLONE_PATH = '/tmp/hepigramgit'


class GitHandler:

    ORIGIN_PATH = ''

    def __init__(self):
        if not shutil.which('git'):
            raise Exception("You need to have git installed")

    def _verify_path(self):
        return True

    def clone(self, destination):

        print('Cloning into', destination)
        cmd = 'git clone {origin} {destination} > /dev/null 2>&1'.format(
            origin=self.ORIGIN_PATH, destination=destination
        )
        call(cmd, shell=True)


def is_git_uri(path):
    return '.' in path and get_extension(path) == 'git'
