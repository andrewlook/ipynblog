#!/usr/bin/env python
import io
import os
from pprint import pprint

import yaml
from cookiecutter.main import cookiecutter


def generate_cookiecutter(cookiecutter_url, metadata_file=None):
    notebook_metadata = {}
    if metadata_file and os.path.isfile(metadata_file):
        with io.open(metadata_file) as fd:
            notebook_metadata = yaml.load(fd)
    notebook_fname = metadata_file.replace('.yaml', '')
    project_slug = notebook_metadata['project_slug']
    print('metadata loaded from notebook: ' + notebook_fname)
    print('generating to output dir: ' + project_slug)
    print('metadata to be passed to cookiecutter as extra_context:')
    pprint(notebook_metadata)

    #
    # Use notebook metadata to preload the cookiecutter config options:
    # http://cookiecutter.readthedocs.io/en/latest/advanced/suppressing_prompts.html
    #
    cookiecutter(cookiecutter_url, extra_context=notebook_metadata)
    return project_slug


"""
def run_template():
    parser = ArgumentParser()
    parser.add_argument('-t', '--type',
                        help='Type of nbconvert template to include')
    parser.add_argument('-o', '--output',
                        help='Template dest dir')
    args = parser.parse_args(sys.argv)
    dirname = os.path.dirname(__file__)
    templates_dir = os.path.join(dirname, 'templates')
    template_fname = '%s.tpl' % args.type
    template_path = os.path.join(templates_dir, template_fname)
    if not os.path.isfile(template_path):
        raise ValueError('invalid template type "%s"; file note found: %s' %
                         (args.type, template_path))
    if not os.path.isdir(args.output):
        raise ValueError('output directory "%s" does not exist' % output)

    dest_path = os.path.join(args.output, template_fname)
    shutil.copy2(template_path, dest_path)
"""


def main():
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Sets up a new template using cookiecutter')
    parser.add_argument('cookiecutter',
                        help='Cookiecutter repo URL')
    parser.add_argument('-m', '--metadata',
                        help='Path to downloaded notebook\'s yaml metadata file')
    args = parser.parse_args(sys.argv[1:])
    project_slug = generate_cookiecutter(cookiecutter_url=args.cookiecutter,
                                         metadata_file=args.metadata)
    print('generated cookiecutter template from {u} to {s}'
          .format(u=args.cookiecutter, s=project_slug))


if __name__ == '__main__':
    main()
