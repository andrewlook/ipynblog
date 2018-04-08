from __future__ import absolute_import

import os

from ipynblog.config import *

author_email = 'andrew.m.look@gmail.com'
author_name = 'Andrew Look'
colab_url = 'https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO'
dt = '2018-04-05'
project_name = 'deepdream--startup-breakfast--final'
project_slug = 'deepdream__startup_breakfast__final'

notebook_yaml = u"""
!NotebookMetadata
author_email: {author_email}
author_name: {author_name}
colab_url: {colab_url}
dt: '{dt}'
project_name: {project_name}
project_slug: {project_slug}
""".format(author_email=author_email,
           author_name=author_name,
           colab_url=colab_url,
           dt=dt,
           project_name=project_name,
           project_slug=project_slug)

nbconvert_template = './nbconvert/distill_v2_svelte.tpl'
nbconvert_input = './notebooks/test.ipynb'
nbconvert_output = './public/index.html'
images_dir = './public/images/'

default_template_yaml = u"""
!TemplateConfig
ipynblog_template: !IpynbTemplate
  nbconvert_template: {nbconvert_template}
  nbconvert_input: {nbconvert_input}
  nbconvert_output: {nbconvert_output}
  images_dir: {images_dir}
""".format(nbconvert_template=nbconvert_template,
           nbconvert_input=nbconvert_input,
           nbconvert_output=nbconvert_output,
           images_dir=images_dir)

updated_nbconvert_input = os.path.join('./notebooks', project_name)
colab_template_yaml = u"""
!TemplateConfig
ipynblog_template: !IpynbTemplate
  nbconvert_template: {nbconvert_template}
  nbconvert_input: {nbconvert_input}
  nbconvert_output: {nbconvert_output}
  images_dir: {images_dir}
  colab_url: {colab_url}
""".format(nbconvert_template=nbconvert_template,
           nbconvert_input=updated_nbconvert_input,
           nbconvert_output=nbconvert_output,
           images_dir=images_dir,
           colab_url=colab_url)

def __load_dump(y):
    return yaml.dump(yaml.load(y), default_flow_style=False)

def test_dump_notebook():
    nb = NotebookMetadata(author_email, author_name, colab_url,
                          dt, project_name, project_slug)
    assert __load_dump(notebook_yaml) == yaml.dump(nb, default_flow_style=False)


def test_load_notebook():
    n = yaml.load(notebook_yaml)
    assert n.author_email == author_email


def test_dump_template_config():
    c = TemplateConfig(ipynblog_template=IpynbTemplate(
        nbconvert_template=nbconvert_template,
        nbconvert_input=updated_nbconvert_input,
        nbconvert_output=nbconvert_output,
        images_dir=images_dir,
        colab_url=colab_url,
    ))
    assert __load_dump(colab_template_yaml) == yaml.dump(c, default_flow_style=False)


def test_load_and_dump_template_config():
    c = yaml.load(default_template_yaml)
    t = c.ipynblog_template
    assert t.nbconvert_template == nbconvert_template
    assert t.nbconvert_input == nbconvert_input
    assert t.nbconvert_output == nbconvert_output
    assert t.images_dir == images_dir
    assert t.colab_url == None

    t.colab_url = colab_url
    t.nbconvert_input = updated_nbconvert_input

    assert __load_dump(colab_template_yaml) == yaml.dump(c, default_flow_style=False)
