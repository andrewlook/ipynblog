import os
import shutil
import sys

from argparse import ArgumentParser

USAGE = "Usage: ipynblog template|render [OPTIONS]"


def run_template(type, output):
    print('type = %s, output = %s' % (type, output))
    dirname = os.path.dirname(__file__)
    templates_dir = os.path.join(dirname, 'templates')
    template_fname = '%s.tpl' % type
    template_path = os.path.join(templates_dir, template_fname)
    if not os.path.isfile(template_path):
        raise ValueError('invalid template type "%s"; file note found: %s' %
                         (type, template_path))
    if not os.path.isdir(output):
        raise ValueError('output directory "%s" does not exist' % output)

    dest_path = os.path.join(output, template_fname)
    shutil.copy2(template_path, dest_path)


def run_render(local_fname, output, template, notebooks_dir, images_dir):
    print('local_fname = %s, output = %s, template = %s, '
          'notebooks_dir = %s, images_dir = %s'
          % (local_fname, output, template, notebooks_dir, images_dir))
    from ipynblog.convert import convert_and_save
    convert_and_save(local_fname, output, template, notebooks_dir, images_dir)


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    command = sys.argv[1]
    parser = ArgumentParser()
    remaining_args = sys.argv[2:] if len(sys.argv) > 2 else []

    if command == 'template':
        parser.add_argument('-t', '--type',
                            help='Type of nbconvert template to include')
        parser.add_argument('-o', '--output',
                            help='Template dest dir')
        args = parser.parse_args(remaining_args)
        return run_template(args.type, args.output)
    elif command == 'render':
        parser.add_argument('-i', '--input',
                            help='Path to downloaded notebook')
        parser.add_argument('-o', '--output',
                            help='Path to render notebook to')
        parser.add_argument('--template',
                            help='Path to nbconvert template to use')
        parser.add_argument('--notebooks-dir',
                            help='Path to copy unrendered notebook to')
        parser.add_argument('--images-dir',
                            help='Path to extract image assets to')
        args = parser.parse_args(remaining_args)
        return run_render(args.input, args.output, args.template,
                          args.notebooks_dir, args.images_dir)
    else:
        print('command "%s" not recognized\n\n%s' % (command, USAGE))
        sys.exit(1)


if __name__ == '__main__':
    main()
