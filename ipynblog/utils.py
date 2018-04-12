from __future__ import print_function

import io
import os
import sys

import six
import yaml
import unicodedata


def load_yaml(path_or_fd_or_blob):
    if not path_or_fd_or_blob:
        raise ValueError('path_or_fd must be provided to load YAML from')

    # if the argument is not a string, assume its a file-like and start reading
    if not isinstance(path_or_fd_or_blob, six.string_types):
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

    if not isinstance(path_or_fd, six.string_types):
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


# From https://docs.python.org/2/library/unicodedata.html#unicodedata.normalize:
#   "The normal form KD (NFKD) will apply the compatibility decomposition, i.e.
#   replace all compatibility characters with their equivalents. The normal form
#   KC (NFKC) first applies the compatibility decomposition, followed by the
#   canonical composition."
UNICODE_NORMALIZATION = 'NFKD'


def _dict2ascii(obj):
    """
    pyYAML is pretty verbose about datatypes, and if a unicode string is used this is what happens:
    ```
    nbconvert_input: !!python/unicode './notebooks/deepdream--startup-breakfast--final'
    ```

    Instead I'm converting all string values to ascii first. Though supporting unicode-valued
    config options isn't really a priority, I figure it's at least worth making an effort to do ascii-folding.

    :param obj: dictionary or object
    :return:    dictionary of field names to their values, with any string values converted to ascii encoding.
    """

    # if the argument was a unicode object, convert it to string first
    if isinstance(obj, six.string_types):
        # no need to use the decoded object, but if the string-like isn't ascii-friendly it
        # will raise an exception.
        if sys.version_info.major < 3 and isinstance(obj, unicode):
            return unicodedata.normalize(UNICODE_NORMALIZATION, obj).encode('ascii', 'ignore')
        return obj
    elif isinstance(obj, YAMLConfigBase):
        # if the argument was a config object that should first be converted to a dictionary,
        # convert it so that the tail recursion call will use this dict.
        obj = obj.__dict__
    elif not isinstance(obj, dict):
        # if it was anything besides a dict, no recursive call needed, just return 'obj' as-is
        return obj

    # this tail recursion call should only take place if 'obj' was a dict,
    # or subclassed YAMLConfigBase.
    return {k: _dict2ascii(v) for k, v in obj.items()}


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