import sys

from argparse import ArgumentParser

USAGE = "Usage: jupyter2distill download|repo|template|render [OPTIONS]"


def run_download(url, output):
    print('url = %s, output = %s' % (url, output))


def run_repo(notebook, metadata, cookiecutter_url):
    print('notebook = %s, metadata = %s, cookiecutter_url = %s' %
          (notebook, metadata, cookiecutter_url))


def run_template(type, output):
    print('type = %s, output = %s' % (type, output))


def run_render(input, output, notebooks_dir, images_dir):
    print('input = %s, output = %s, notebooks_dir = %s, images_dir = %s'
          % (input, output, notebooks_dir, images_dir))


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    command = sys.argv[1]
    parser = ArgumentParser()
    remaining_args = sys.argv[2:] if len(sys.argv) > 2 else []

    if command == 'download':
        parser.add_argument('-u', '--url', help='URL of colab notebook')
        parser.add_argument('-o', '--output', help='Download dest dir')
        args = parser.parse_args(remaining_args)
        return run_download(args.url, args.output)
    elif command == 'repo':
        parser.add_argument('-n', '--notebook',
                            help='Path to downloaded notebook')
        parser.add_argument('-m', '--metadata',
                            help='Path to notebook metadata')
        parser.add_argument('-c', '--cookiecutter',
                            help='Cookiecutter repo URL')
        args = parser.parse_args(remaining_args)
        return run_repo(args.notebook, args.metadata, args.cookiecutter)
    elif command == 'template':
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
        parser.add_argument('--notebooks-dir',
                            help='Path to copy unrendered notebook to')
        parser.add_argument('--images-dir',
                            help='Path to extract image assets to')
        args = parser.parse_args(remaining_args)
        return run_render(args.input, args.output, args.notebooks_dir,
                          args.images_dir)
    else:
        print('command "%s" not recognized\n\n%s' % (command, USAGE))
        sys.exit(1)


if __name__ == '__main__':
    main()
