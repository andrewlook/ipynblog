from __future__ import print_function

import subprocess


def call(x, **kwargs):
    subprocess.check_call(x.split(), **kwargs)


def git_clone(url, project_root):
    print('git clone --depth 1 {url} {name}'.format(url=url, name=project_root))
    call('git clone --depth 1 {url} {name}'.format(url=url, name=project_root))
    call('rm -rf {name}/.git/'.format(name=project_root))


def git_init(project_root):
    call('git init', cwd=project_root)
    call('git add -f .', cwd=project_root)
    call('git commit -m init', cwd=project_root)

