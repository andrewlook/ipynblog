from __future__ import absolute_import
from __future__ import print_function

import logging
import os
import shutil
import sys
import tempfile

from argparse import ArgumentParser

from ipynblog.config import TemplateConfig
from ipynblog.download import download_colab
from ipynblog.render import convert_and_save
from ipynblog.repo import git_clone
from ipynblog.repo import git_init

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def main():
    parser = ArgumentParser()
    # required: the template to use to convert jupyter NB
    parser.add_argument('template',
                        help='Git repo URL of post template')
    parser.add_argument('--name', help='Name of generated project (defaults to notebook name)')
    parser.add_argument('--skip-cleanup', action='store_true',
                        help='Name of generated project (defaults to notebook name)')

    # either/or: Google Colab URL, or local jupyter file
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--colab-url')
    group.add_argument('--notebook-file')

    args = parser.parse_args(sys.argv[1:])


    project_name = args.name if args.name else 'temp_proj'
    proj_root = os.path.join(os.getcwd(), project_name)
    temp_proj_root = None

    if not args.name:
        _ipynblog_temp_dir = tempfile.mkdtemp(prefix="ipynblog_")
        temp_proj_root = os.path.join(_ipynblog_temp_dir, project_name)
        LOG.debug('Using temporary directory {d}'.format(d=temp_proj_root))
        os.makedirs(temp_proj_root)
    else:
        # TODO clean this logic upp...
        temp_proj_root = proj_root
        LOG.debug('Using directory {d}'.format(d=temp_proj_root))

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
        ipynblog_yaml_path = os.path.join(temp_proj_root, 'ipynblog.yaml')
        t = TemplateConfig.load_from(ipynblog_yaml_path)
        cfg = t.ipynblog_template

        # find the folder in the generated project structure containing the example notebook.
        # this is where the input notebook will get copied into the repo.
        notebooks_dir = os.path.dirname(cfg.nbconvert_input_abspath(temp_proj_root))

        if args.colab_url:
            # record the colab notebook's url in the YAML config, in case sync needed.
            cfg.colab_url = args.colab_url
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
        if not args.name:
            # if project name wasn't available before NB download, update it now.
            proj_root = os.path.join(os.getcwd(), project_name)
            LOG.debug('updating proj_root to {d}'.format(d=proj_root))

        assert notebook_fname, 'notebook_fname must be set'
        # update config's pointer to which notebook needs to be converted.
        LOG.info('updating config[nbconvert_input] from {f} to {t}'
                 .format(f=cfg.nbconvert_input, t=notebook_fname))
        cfg.nbconvert_input = notebook_fname  #### .replace(temp_proj_root, '')
        # update the YAML file in the generated repo
        t.dump(ipynblog_yaml_path)

        convert_and_save(local_fname=notebook_fname,
                         output=cfg.nbconvert_output_abspath(temp_proj_root),
                         template=cfg.nbconvert_template_abspath(temp_proj_root),
                         images_dir=cfg.images_dir_abspath(temp_proj_root))

        # if everything converted properly, copy the temporary dir into CWD() and rename it
        if not args.name:
            LOG.info('moving generated project from temp dir " {t} " to dest dir " {d} " '
                     .format(t=temp_proj_root, d=proj_root))
            print('mv --> ', temp_proj_root, proj_root)
            shutil.move(temp_proj_root, os.path.join(os.getcwd(), project_name))
    finally:
        # be sure to clean up temp dir:
        # - after it has been copied in case of success
        # - in case of failure also clean it up
        if temp_proj_root and os.path.exists(temp_proj_root):
            LOG.debug('temp_proj_root found: {t}'.format(t=temp_proj_root))
            if args.skip_cleanup:
                LOG.info('skipping cleanup')
                return
            LOG.info('cleaning up temp_dir {t}'.format(t=temp_proj_root))
            shutil.rmtree(temp_proj_root)

    LOG.info('finished generated project in dest dir " {d} " '.format(d=proj_root))


if __name__ == '__main__':
    main()
