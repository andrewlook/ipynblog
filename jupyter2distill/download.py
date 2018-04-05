#!/usr/bin/env python
import json
import os
from dateutil import parser as dt_parser
from pprint import pprint

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#
# Avoid python 2/3 nonsense from urllib:
# - http://python-future.org/compatible_idioms.html#urllib-module
#
from six.moves.urllib.parse import urlparse


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
    gauth = GoogleAuth()
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
    # assert '.ipynb' in fname
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


def download_colab(url, notebook_dir=None):
    drive = get_gdrive()
    colab_file = fetch_colab_gfile(drive, url)

    dt = extract_updated_dt(colab_file)
    author_email, author_name = extract_last_modified_user(colab_file)

    colab_fname = colab_file['title']

    colab_extension = colab_file['fileExtension']
    # assert colab_extension == 'ipynb', \
    # 'extension should be ipynb but is: "%s"' % colab_extension

    project_name = colab_fname.replace('.'+colab_extension, '')
    project_slug = project_name.lower().replace(' ', '_').replace('-', '_')

    local_fname = save_colab_gfile(colab_file, notebook_dir=notebook_dir)
    metadata = dict(
        project_name=project_name,
        project_slug=project_slug,
        colab_url=url,
        local_fname=local_fname,
        author_name=author_name,
        author_email=author_email,
        dt=dt,
    )
    local_metadata_fname = local_fname + '.meta'
    with open(local_metadata_fname, 'w+') as outfile:
        json.dump(metadata, outfile)

    print('Downloaded notebook to {f}, saved metadata to: {m}'
          .format(f=local_fname, m=local_metadata_fname))
    pprint(metadata)
    return metadata
