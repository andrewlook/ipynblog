#!/usr/bin/env python
import os
from argparse import ArgumentParser

from cookiecutter.main import cookiecutter

from convert import convert_and_save
from download import download_colab

SVELTE_COOKIECUTTER = 'git@github.com:andrewlook/cookiecutter-svelte-template.git'


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--colab-url')
    parser.add_argument('--notebooks-dir', default='./notebooks')
    args = parser.parse_args()

    notebook_metadata = download_colab(url=args.colab_url, notebook_dir=args.notebooks_dir)
    notebook_fname = notebook_metadata['local_fname']
    project_slug = notebook_metadata['project_slug']
    print(notebook_metadata)

    #
    # Use notebook metadata to preload the cookiecutter config options:
    # - http://cookiecutter.readthedocs.io/en/latest/advanced/suppressing_prompts.html
    #
    cookiecutter(SVELTE_COOKIECUTTER, extra_context=notebook_metadata)

    gen_dir = os.path.join(os.getcwd(), project_slug)
    convert_and_save(basedir=gen_dir,
                     local_fname=notebook_fname)

