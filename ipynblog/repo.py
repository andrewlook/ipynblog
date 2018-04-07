import json
import os

from cookiecutter.main import cookiecutter
from pprint import pprint


def generate_repo(cookiecutter_url, metadata_file=None):
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
