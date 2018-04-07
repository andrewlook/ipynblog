import os
from io import open
from shutil import copy2  # include metadata when copying

import nbformat
from traitlets.config import Config
from nbconvert import HTMLExporter


def convert_notebook(notebook_file, template_file='basic'):
    notebook = nbformat.read(notebook_file, as_version=4)
    c = Config()
    c.HTMLExporter.preprocessors = [
            'nbconvert.preprocessors.ExtractOutputPreprocessor',
    ]
    c.HTMLExporter.template_file = template_file
    html_exporter = HTMLExporter(config=c)
    html_exporter.preprocessors
    body, resources = html_exporter.from_notebook_node(notebook)
    return body, resources


def save_images(img_dir, resources):
    if 'outputs' not in resources:
        return
    outputs = resources['outputs']
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    for filename, rawdata in outputs.items():
        img_fname = os.path.join(img_dir, filename)
        with open(img_fname, 'wb+') as outfile:
            outfile.write(rawdata)
        print('wrote ' + img_fname)


def convert_and_save(local_fname, output, template, notebooks_dir, images_dir):
    # paths relative to root of generated project directory
    gen_nb_dir = notebooks_dir  # os.path.join(basedir, 'notebooks')
    gen_nb_tpl = template  # os.path.join(gen_nb_dir, 'nbconvert.tpl')
    html_path = output  # os.path.join(basedir, 'public/index.html')
    gen_img_dir = images_dir  # os.path.join(basedir, 'public/images')

    base_fname = os.path.basename(local_fname)

    # 1. copy in the notebook
    dest_notebook_path = os.path.join(gen_nb_dir, base_fname)
    copy2(local_fname, dest_notebook_path)

    # 2. run nbconvert
    body, res = convert_notebook(local_fname, template_file=gen_nb_tpl)

    # 3. replace src/index.ejs with the generated post
    print('converting html to: %s' % html_path)
    with open(html_path, mode='w+', encoding='utf-8') as outfile:
        outfile.write(body)

    # 4. Save the images into public/images
    save_images(gen_img_dir, res)
