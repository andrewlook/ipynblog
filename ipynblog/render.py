#!/usr/bin/env python
import os
import io

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


def convert_and_save(local_fname, output, template, images_dir):
    # run nbconvert
    body, res = convert_notebook(local_fname, template_file=template)

    # replace placeholder public/index.html with the generated post
    print('converting html to: %s' % output)
    with io.open(output, mode='w+', encoding='utf-8') as outfile:
        outfile.write(body)

    # Save the images into public/images
    save_images(images_dir, res)


def main():
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input',
                        help='Path to downloaded notebook')
    parser.add_argument('output',
                        help='Path to render notebook to')
    parser.add_argument('--template',
                        help='Path to nbconvert template to use')
    parser.add_argument('--images-dir',
                        help='Path to extract image assets to')
    args = parser.parse_args(sys.argv)

    convert_and_save(local_fname=args.input,
                     output=args.output,
                     template=args.template,
                     images_dir=args.images_dir)


if __name__ == '__main__':
    main()