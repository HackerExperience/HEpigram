import subprocess
import os


def call(cmd, shell=False):
    return subprocess.call(cmd, shell=shell)


def absolutify(relative_path):
    """If a relative path is given, this function will return the absolute
    path instead."""
    if relative_path.startswith('/') or \
            relative_path.split('://')[0] in ['git', 'http', 'https']:
        return relative_path
    return os.getcwd() + '/' + relative_path


def get_extension(file):
    return file.split('.')[-1]
