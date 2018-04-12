from __future__ import absolute_import

import os

from ipynblog.utils import YAMLConfigBase


class TemplateConfig(YAMLConfigBase):
    yaml_tag = u'!TemplateConfig'
    ipynblog_template = None

    def __init__(self, ipynblog_template=None):
        self.ipynblog_template = ipynblog_template


class IpynbTemplate(YAMLConfigBase):
    yaml_tag = u'!IpynbTemplate'
    nbconvert_template = None
    nbconvert_input = None
    nbconvert_output = None
    images_dir = None
    colab_url = None

    def __init__(self,
                 nbconvert_template=None,
                 nbconvert_input=None,
                 nbconvert_output=None,
                 images_dir=None,
                 colab_url=None):
        self.nbconvert_template = nbconvert_template
        self.nbconvert_input = nbconvert_input
        self.nbconvert_output = nbconvert_output
        self.images_dir = images_dir
        self.colab_url = colab_url

    def nbconvert_template_abspath(self, dir):
        return self._to_abs(dir, self.nbconvert_template)

    def nbconvert_input_abspath(self, dir):
        return self._to_abs(dir, self.nbconvert_input)

    def nbconvert_output_abspath(self, dir):
        return self._to_abs(dir, self.nbconvert_output)

    def images_dir_abspath(self, dir):
        return self._to_abs(dir, self.images_dir)

    def _to_abs(self, dir, rel_path):
        assert os.path.isdir(dir), '{d} is not a directory'.format(d=dir)
        return os.path.join(dir, rel_path.replace('./', ''))


class NotebookMetadata(YAMLConfigBase):
    yaml_tag = u'!NotebookMetadata'
    author_email = None
    author_name = None
    colab_url = None
    dt = None
    project_name = None
    project_slug = None

    def __init__(self,
                 author_email=None,
                 author_name=None,
                 colab_url=None,
                 dt=None,
                 project_name=None,
                 project_slug=None):
        self.author_email = author_email
        self.author_name = author_name
        self.colab_url = colab_url
        self.dt = dt
        self.project_name = project_name
        self.project_slug = project_slug


