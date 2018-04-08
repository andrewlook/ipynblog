class TemplateConfig(object):
    ipynb_template = None

    def __init__(self, ipynb_template=None):
        self.ipynb_template = ipynb_template


class IpynbTemplate(object):
    nbconvert_template = None
    nbconvert_input = None
    nbconvert_output = None
    images_dir = None

    def __init__(self,
                 nbconvert_template=None,
                 nbconvert_input=None,
                 nbcovnert_output=None,
                 images_dir=None):
        self.nbconvert_template = nbconvert_template
        self.nbconvert_input = nbconvert_input
        self.nbconvert_output = nbcovnert_output
        self.images_dir = images_dir


class NotebookMetadata(object):
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
