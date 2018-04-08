import unicodedata
import yaml

# From https://docs.python.org/2/library/unicodedata.html#unicodedata.normalize:
#   "The normal form KD (NFKD) will apply the compatibility decomposition, i.e.
#   replace all compatibility characters with their equivalents. The normal form
#   KC (NFKC) first applies the compatibility decomposition, followed by the
#   canonical composition."
UNICODE_NORMALIZATION = 'NFKD'


def dump_yaml(dest_path, attrs):
    """
    Dumps out a yaml object as a map, converting any unicode strings to ascii
    to prevent pyyaml from including '!!python/unicode' at the start of each
    field.

    TODO consider custom YAML objects for ser/de:
    - http://pyyaml.org/wiki/PyYAMLDocumentation#constructors-representers-resolvers

    :param dest_path:   output file path
    :param attrs:       python dict to save
    :return:            dest_path
    """
    to_dump = {}
    for k, v in attrs.items():
        if type(v) == unicode:
            to_dump[k] = unicodedata.normalize(UNICODE_NORMALIZATION, v)\
                .encode('ascii', 'ignore')
        else:
            to_dump[k] = v

    with open(dest_path, 'w+') as outfile:
        yaml.dump(to_dump, outfile, default_flow_style=False, tags=None)

    return dest_path