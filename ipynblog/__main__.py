from __future__ import absolute_import
from __future__ import print_function

import os
import shutil
import sys
import tempfile

from argparse import ArgumentParser

from ipynblog.repo import git_clone
from ipynblog.repo import find_yaml_config
from ipynblog.repo import git_init
from ipynblog.download import download_colab


def main():
    parser = ArgumentParser()
    # required: the template to use to convert jupyter NB
    parser.add_argument('template',
                        help='Git repo URL of post template')
    parser.add_argument('--name', help='Name of generated project (defaults to notebook name)')

    # either/or: Google Colab URL, or local jupyter file
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--colab-url')
    group.add_argument('--notebook-file')

    args = parser.parse_args(sys.argv[1:])

    project_name = args.name if args.name else 'temp_proj'

    _ipynblog_temp_dir = tempfile.mkdtemp(prefix="ipynblog_")
    temp_proj_root = os.path.join(_ipynblog_temp_dir, project_name)
    os.makedirs(temp_proj_root)

    try:
        git_clone(url=args.template, project_root=temp_proj_root)
        git_init(temp_proj_root)
        """
        Example Template Config YAML:
        -----------------------------
        ipynblog_template:
            nbconvert_template: ./nbconvert/distill_v2_svelte.tpl
            nbconvert_input: ./notebooks/test.ipynb
            nbconvert_output: ./public/index.html
            images_dir: ./public/images/
        """
        t = find_yaml_config(temp_proj_root)['ipynblog_template']

        nbconvert_template = os.path.join(temp_proj_root, t['nbconvert_template'])
        nbconvert_input = os.path.join(temp_proj_root, t['nbconvert_input'])
        nbconvert_output = os.path.join(temp_proj_root, t['nbconvert_output'])
        images_dir = os.path.join(temp_proj_root, t['images_dir'])

        # find the folder in the generated project structure containing the example notebook.
        # this is where the input notebook will get copied into the repo.
        notebooks_dir = os.path.basename(nbconvert_input)

        if args.colab_url:


            notebook_fname, _, metadata = download_colab(args.colab_url, notebook_dir=notebooks_dir)

            if not args.name:
                project_name = metadata['project_name']

        elif args.notebook_file:
            fname = os.path.basename(args.notebook_file)
            # filename of the path in generated project to copy notebook to
            notebook_fname = os.path.join(notebooks_dir, fname)
            shutil.copy2(args.notebook_file, notebook_fname)

            if not args.name:
                project_name = fname.replace('.ipynb', '')
        else:
            raise ValueError()

        assert project_name, 'project_name must be set'
        assert notebook_fname, 'notebook_fname must be set'

        from ipynblog.render import convert_and_save

        from pprint import pprint
        pprint(dict(local_fname=notebook_fname,
                         output=nbconvert_output,
                         template=nbconvert_template,
                         images_dir=images_dir))

        convert_and_save(local_fname=notebook_fname,
                         output=nbconvert_output,
                         template=nbconvert_template,
                         images_dir=images_dir)

        # if everything converted properly, copy the temporary dir into CWD() and rename it
        print('mv --> ', temp_proj_root, os.path.join(os.getcwd(), project_name))
        shutil.move(temp_proj_root, os.path.join(os.getcwd(), project_name))

    finally:
        # be sure to clean up temp dir:
        # - after it has been copied in case of success
        # - in case of failure also clean it up
        print('cleaning up temp_dir {t}'.format(t=temp_proj_root))
        shutil.rmtree(temp_proj_root)


if __name__ == '__main__':
    main()
