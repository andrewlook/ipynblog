#!/usr/bin/env python

# Avoid python 2/3 nonsense from urllib:
# - http://python-future.org/compatible_idioms.html#urllib-module
from six.moves.urllib.parse import urlparse

import os
import tempfile

from dateutil import parser as dt_parser

from ipynblog import utils
from ipynblog.config import TemplateConfig

_ipynblog_temp_dir = tempfile.mkdtemp(prefix="ipynblog_")


def colab_gdrive_id(url):
    parse_result = urlparse(url)
    assert parse_result.netloc == 'colab.research.google.com', \
        'URL should be from colab.research.google.com'
    path_parts = parse_result.path.strip().split('/')
    assert len(path_parts) == 3, \
        'URL should look like https://colab.research.google.com/drive/<ID>'
    assert path_parts[0] == '', \
        'URL should look like https://colab.research.google.com/drive/<ID>'
    assert path_parts[1] == 'drive', \
        'URL should look like https://colab.research.google.com/drive/<ID>'
    return path_parts[2]


def get_gdrive():
    settings_yaml = os.getenv('PYDRIVE_SETTINGS_YAML')
    client_config_file = os.getenv('PYDRIVE_CLIENT_CONFIG_FILE')
    saved_credentials_file = os.getenv('PYDRIVE_SAVED_CREDENTIALS_FILE')

    assert (client_config_file and saved_credentials_file) or settings_yaml, \
        'env vars must be set: PYDRIVE_SETTINGS_YAML ' \
        'or PYDRIVE_CLIENT_CONFIG_FILE ' \
        'and PYDRIVE_SAVED_CREDENTIALS_FILE'

    # import these only if function gets called, so non-colab users don't need to
    # install/configure PyDrive if they're not going to download f/ Colab.
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    if settings_yaml:
        gauth = GoogleAuth(settings_file=settings_yaml)
    else:
        gauth = GoogleAuth()
        gauth.settings['client_config_backend'] = 'file'
        gauth.settings['client_config_file'] = client_config_file
        gauth.settings['save_credentials'] = True
        gauth.settings['save_credentials_backend'] = 'file'
        gauth.settings['save_credentials_file'] = saved_credentials_file
        gauth.settings['get_refresh_token'] = True
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    return drive


def fetch_colab_gfile(drive, url):
    gdrive_id = colab_gdrive_id(url)
    colab_file = drive.CreateFile({'id': gdrive_id})
    colab_file.FetchMetadata()
    return colab_file


def save_colab_gfile(colab_file, notebook_dir='./notebooks', overwrite=True,
                     fname=None):
    """ Downloads an ipynb fmor google colab.
        refs:
        - http://pythonhosted.org/PyDrive/filemanagement.html
        - http://pythonhosted.org/PyDrive/pydrive.html
    """
    if not fname:
        fname = colab_file['title']
    print('fname = %s, notebook_dir=%s' % (fname, notebook_dir))
    if not os.path.isdir(notebook_dir):
        os.makedirs(notebook_dir)

    local_fname = os.path.join(notebook_dir, fname)
    print('local_fname = %s' % local_fname)
    if os.path.exists(local_fname) and not overwrite:
        raise Exception("%s already exists" % local_fname)

    colab_file.GetContentFile(local_fname)
    return local_fname


def extract_updated_dt(gfile):
    if 'modifiedDate' not in gfile:
        return ''
    utc_iso_timestamp = gfile['modifiedDate']
    utc_datetime = dt_parser.parse(utc_iso_timestamp)
    return utc_datetime.strftime("%Y-%m-%d")


def extract_last_modified_user(gfile):
    """ Extractors for the gfile metadata
    https://developers.google.com/drive/v2/reference/files#resource-representations
    :param gfile:
    :return:
    """
    if 'lastModifyingUser' not in gfile:
        return ''
    user = gfile['lastModifyingUser']
    email = ''
    if 'emailAddress' in user:
        email = user['emailAddress']
    name = ''
    if 'displayName' in user:
        name = user['displayName']
    return (email, name)


def download_colab(url, notebook_dir=_ipynblog_temp_dir, fname=None):
    """
    Downloads google colab notebook and saves the ipynb file in 'notebook_dir'.
    Extracts GDrive metadata (name, modified timestamp, username) and saves as
    yaml alongside the notebook.

    :param url:             URL of Google Colab notebook
    :param notebook_dir:    Directory in which to save (defaults to temp dir)
    :return:                File paths of downloaded notebook and yaml metadata
    """
    drive = get_gdrive()
    colab_file = fetch_colab_gfile(drive, url)

    colab_extension = colab_file['fileExtension']
    dt = extract_updated_dt(colab_file)
    author_email, author_name = extract_last_modified_user(colab_file)

    notebook_path = save_colab_gfile(colab_file, notebook_dir=notebook_dir,
                                     fname=fname)
    colab_fname = os.path.basename(notebook_path)
    project_name = colab_fname.replace('.' + colab_extension, '')
    project_slug = project_name.lower().replace(' ', '_').replace('-', '_')

    metadata = dict(
        project_name=project_name,
        project_slug=project_slug,
        colab_url=url,
        author_name=author_name,
        author_email=author_email,
        dt=dt,
    )
    metadata_fname = utils.dump_yaml(dest_path=notebook_path + '.yaml', attrs=metadata)
    return notebook_path, metadata_fname, metadata


def main():
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Downloads Google Colab notebooks')
    parser.add_argument('url', help='URL of colab notebook')
    parser.add_argument('-d', '--dir', help='Download dest dir',
                        default=_ipynblog_temp_dir)
    parser.add_argument('-c', '--config',
                        help='YAML config. If provided, overrides args'
                             'using generated ipynblog.yaml')
    args = parser.parse_args(sys.argv[1:])
    print(args.url)

    url = args.url
    notebook_dir = args.dir
    notebook_fname = None

    if args.config:
        cfg = TemplateConfig.load_file(args.config).ipynblog_template
        url = cfg.colab_url
        notebook_dir = os.path.dirname(cfg.nbconvert_input)
        # ensure the notebook gets downloaded to a file of the same name,
        # since its possible for that to change within colab since last sync.
        notebook_fname = os.path.basename(cfg.nbconvert_input)

    notebook, meta, _ = download_colab(url=url, notebook_dir=notebook_dir,
                                       notebook_fname=notebook_fname)
    print('Downloaded notebook to {n}, saved metadata to: {m}'
          .format(n=notebook, m=meta))


if __name__ == '__main__':
    main()
