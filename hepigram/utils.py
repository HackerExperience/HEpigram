import subprocess
import os
from threading import Thread


def call(cmd, shell=False):
    return subprocess.call(cmd, shell=shell)


def absolutify(relative_path):
    """If a relative path is given, this function will return the absolute
    path instead."""
    if relative_path.startswith('/') or \
            relative_path.split('://')[0] in ['git', 'http', 'https', 'ssh']:
        return relative_path
    return os.getcwd() + '/' + relative_path


def get_extension(file):
    return file.split('.')[-1]


def path_exists(path):
    return os.path.exists(path)


def walk(path, **kwargs):
    return os.walk(path, **kwargs)


def thread(cmd, args):
    t = Thread(target=cmd, args=args)
    t.start()
    t.join()
    return t
