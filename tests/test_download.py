from __future__ import absolute_import

# import pytest

from ipynblog.download import colab_gdrive_id

COLAB_URL = 'https://colab.research.google.com/drive/' \
            '1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO'


def test_colab_gdrive_id():
    assert colab_gdrive_id(COLAB_URL) == '1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB'
