from __future__ import print_function

import subprocess
import io
import yaml
import os


def call(x, **kwargs):
    subprocess.check_call(x.split(), **kwargs)


def git_clone(url, project_root):
    print('git clone --depth 1 {url} {name}'.format(url=url, name=project_root))
    call('git clone --depth 1 {url} {name}'.format(url=url, name=project_root))
    call('rm -rf {name}/.git/'.format(name=project_root))


def find_yaml_config(project_root):
    yaml_fname = os.path.join(project_root, 'ipynblog.yaml')
    if not os.path.isfile(yaml_fname):
        raise ValueError('{yaml_fname} not found from template at {url}'
                         .format(yaml_fname=yaml_fname))
    with io.open(yaml_fname) as yaml_fd:
        ipynblog_config = yaml.load(yaml_fd)
    return ipynblog_config


def git_init(project_root):
    call('git init', cwd=project_root)
    call('git add -f .', cwd=project_root)
    call('git commit -m init', cwd=project_root)

