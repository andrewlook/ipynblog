import yaml

class TemplateConfig(yaml.YAMLObject):
    yaml_tag = u'!TemplateConfig'
    ipynblog_template = None

    def __init__(self, ipynblog_template=None):
        self.ipynblog_template = ipynblog_template


class IpynbTemplate(yaml.YAMLObject):
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


class NotebookMetadata(yaml.YAMLObject):
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


