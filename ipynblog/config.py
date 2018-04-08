import io
import yaml


class YAMLConfigBase(yaml.YAMLObject):
    def dump(self, **kwargs):
        return yaml.dump(self, default_flow_style=False, **kwargs)

    @classmethod
    def load(cls, *args, **kwargs):
        return yaml.load(*args, **kwargs)

    @classmethod
    def load_file(cls, fname):
        with io.open(fname, encoding='utf-8') as fd:
            return yaml.load(fd)


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


