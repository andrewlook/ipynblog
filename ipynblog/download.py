#!/usr/bin/env python

# Avoid python 2/3 nonsense from urllib:
# - http://python-future.org/compatible_idioms.html#urllib-module
from six.moves.urllib.parse import urlparse

import os
import tempfile

import yaml
from dateutil import parser as dt_parser


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
        'env vars must be set: PYDRIVE_SETTINGS_YAML '\
        'or PYDRIVE_CLIENT_CONFIG_FILE '\
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


def save_colab_gfile(colab_file, notebook_dir='./notebooks', overwrite=True):
    """ Downloads an ipynb fmor google colab.
        refs:
        - http://pythonhosted.org/PyDrive/filemanagement.html
        - http://pythonhosted.org/PyDrive/pydrive.html
    """
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


def download_colab(url, notebook_dir=_ipynblog_temp_dir):
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

    dt = extract_updated_dt(colab_file)
    author_email, author_name = extract_last_modified_user(colab_file)
    colab_fname = colab_file['title']
    colab_extension = colab_file['fileExtension']

    project_name = colab_fname.replace('.'+colab_extension, '')
    project_slug = project_name.lower().replace(' ', '_').replace('-', '_')

    notebook_fname = save_colab_gfile(colab_file, notebook_dir=notebook_dir)
    metadata = dict(
        project_name=project_name,
        project_slug=project_slug,
        colab_url=url,
        author_name=author_name,
        author_email=author_email,
        dt=dt,
    )
    metadata_fname = notebook_fname + '.yaml'
    with open(metadata_fname, 'w+') as outfile:
        yaml.dump(metadata, outfile, indent=2)
    return notebook_fname, metadata_fname


def main():
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Downloads Google Colab notebooks')
    parser.add_argument('url', help='URL of colab notebook')
    parser.add_argument('-d', '--dir', help='Download dest dir',
                        default=_ipynblog_temp_dir)
    args = parser.parse_args(sys.argv)

    notebook_fname, metadata_fname = download_colab(url=args.url,
                                                    notebook_dir=args.output)
    print('Downloaded notebook to {n}, saved metadata to: {m}'
          .format(n=notebook_fname, m=metadata_fname))


if __name__ == '__main__':
    main()
