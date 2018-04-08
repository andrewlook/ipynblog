import json
import os

from cookiecutter.main import cookiecutter
from pprint import pprint


def generate_cookiecutter(cookiecutter_url, metadata_file=None):
    notebook_metadata = {}
    if metadata_file and os.path.isfile(metadata_file):
        with open(metadata_file) as fd:
            notebook_metadata = json.load(fd)
    notebook_fname = notebook_metadata['local_fname']
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
