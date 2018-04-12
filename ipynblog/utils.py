import io
import os

import yaml
import unicodedata
from six import string_types


def load_yaml(path_or_fd_or_blob):
    if not path_or_fd_or_blob:
        raise ValueError('path_or_fd must be provided to load YAML from')

    # if the argument is not a string, assume its a file-like and start reading
    if not isinstance(path_or_fd_or_blob, string_types):
        fd = path_or_fd_or_blob
        return yaml.load(stream=fd)

    # if path_or_fd is an actual path (so if a YAML string blob is passed in we can parse it?)
    if os.path.isfile(path_or_fd_or_blob):
        path = path_or_fd_or_blob
        with io.open(path, encoding='utf-8') as fd:
            return yaml.load(stream=fd)

    # otherwise, assume the provided string is the encoded YAML, and load it
    blob = path_or_fd_or_blob
    return yaml.load(stream=blob)  # stream = io.BytesIO(.encode(encoding='utf-8'))


def dump_yaml(obj, path_or_fd=None):
    """
    Saves contents as YAML. Dump to string if no 'stream' argument is provided.

    :param path_or_fd:  where to dump data (accepts either path or file descriptor)
    :return:            YAML as string (or None if 'stream' was provided)
    """
    if not path_or_fd:
        return _dump_formatted_yaml(obj)

    if not isinstance(path_or_fd, string_types):
        return _dump_formatted_yaml(obj, stream=path_or_fd)

    with io.open(path_or_fd, 'w+') as fd:
        return _dump_formatted_yaml(obj, stream=fd)


def _dump_formatted_yaml(obj, stream=None):
    """
    Helper to minimize duplication of YAML args needed to format data consistently.

    :param stream:  optional FD for YAML to dump to
    :return:        string repr of YAML (if no stream provided)
    """
    return yaml.dump(data=_dict2ascii(obj),     # ensure no "!! python/unicode" preamble ends up in the config files
                     default_flow_style=False,  # YAML flow style is totally different (and ugly AF)
                     stream=stream)


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
    # TODO verify that non-dict objects are actually YAMLObject?
    if not isinstance(obj, dict):
        obj = obj.__dict__

    def __ascii(v):
        return v \
            if type(v) != unicode \
            else unicodedata.normalize(UNICODE_NORMALIZATION, v).encode('ascii', 'ignore')

    return {k: __ascii(v) for k, v in obj.items()}


class YAMLConfigBase(yaml.YAMLObject):
    """
    Base object handling de/serialization for all config objects
    """

    def dump(self, path_or_fd=None):
        return dump_yaml(self, path_or_fd=path_or_fd)

    @classmethod
    def load_from(cls, path_or_fd):
        # TODO this doesnt really need to be a classmethod since YAML will internally figure out which class to resolve
        return load_yaml(path_or_fd_or_blob=path_or_fd)