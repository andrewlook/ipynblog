import io
import unicodedata

import yaml
from six import string_types


class YAMLConfigBase(yaml.YAMLObject):
    """
    Base object handling de/serialization for all config objects
    """

    def dump(self, path_or_fd=None):
        """
        Saves contents as YAML. Dump to string if no 'stream' argument is provided.

        :param path_or_fd:  where to dump data (accepts either path or file descriptor)
        :return:            YAML as string (or None if 'stream' was provided)
        """
        if not path_or_fd:
            return self._dump_formatted_yaml()

        if not isinstance(path_or_fd, string_types):
            return self._dump_formatted_yaml(stream=path_or_fd)

        with io.open(path_or_fd, 'w+') as fd:
            return self._dump_formatted_yaml(stream=fd)

    def _dump_formatted_yaml(self, stream=None):
        """
        Helper to minimize duplication of YAML args needed to format data consistently.

        :param stream:  optional FD for YAML to dump to
        :return:        string repr of YAML (if no stream provided)
        """
        return yaml.dump(data=_dict2ascii(self), default_flow_style=False, stream=stream)

    @classmethod
    def load(cls, *args, **kwargs):
        return yaml.load(*args, **kwargs)

    @classmethod
    def load_file(cls, fname):
        with io.open(fname, encoding='utf-8') as fd:
            return yaml.load(fd)


def _dict2ascii(obj):
    """
    HACK: pyYAML is pretty verbose about datatypes, and if a unicode string is used this is what happens:

        !TemplateConfig
        ipynblog_template: !IpynbTemplate
          colab_url: https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO
          images_dir: ./public/images/
          nbconvert_input: !!python/unicode './notebooks/deepdream--startup-breakfast--final'
          nbconvert_output: ./public/index.html
          nbconvert_template: ./nbconvert/distill_v2_svelte.tpl

    Instead, I want this:

        !TemplateConfig
        ipynblog_template: !IpynbTemplate
          colab_url: https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO
          images_dir: ./public/images/
          nbconvert_input: ./notebooks/deepdream--startup-breakfast--final
          nbconvert_output: ./public/index.html
          nbconvert_template: ./nbconvert/distill_v2_svelte.tpl

    So I'm converting everything to ascii first. Though supporting unicode isn't really a priority, I figure it's
    at least worth making an effort to do ascii-folding.

    :param obj: dictionary or object
    :return:    dictionary of field names to their values, with any string values converted to ascii encoding.
    """

    # From https://docs.python.org/2/library/unicodedata.html#unicodedata.normalize:
    #   "The normal form KD (NFKD) will apply the compatibility decomposition, i.e.
    #   replace all compatibility characters with their equivalents. The normal form
    #   KC (NFKC) first applies the compatibility decomposition, followed by the
    #   canonical composition."
    UNICODE_NORMALIZATION = 'NFKD'
    # if an object (YAML config object) was passed in, convert it to dictionary representation
    if not isinstance(obj, dict):
        obj = obj.__dict__

    def __ascii(v):
        return v \
            if type(v) != unicode \
            else unicodedata.normalize(UNICODE_NORMALIZATION, v).encode('ascii', 'ignore')

    return {k: __ascii(v) for k, v in obj.items()}


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


