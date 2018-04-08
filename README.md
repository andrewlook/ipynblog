# ipynblog

Utility for converting a jupyter/colab notebook into a publishable static site codebase

## Installation

```
# install latest directly f/ github
pip install git+https://github.com/andrewlook/ipynblog.git#egg=ipynblog

```

TODO:
- publish to pypi

## Usage: Basic


## Usage: Advanced

There are several individual versions of the commands for those wishing to
download / render separately.

### ipynblog-download

Here's a way to download notebooks from Google Colab and extract some metadata in the
process (author, modified date, etc) to be used when rendering the templates. This
metadata can be stored as JSON alongside the downloaded notebook file.

**Note:** Be sure to complete the [PyDrive setup](docs/pydrive.md) before running
this:

```bash
ipynblog-download <url> [ --dir ./notebooks ]
```

### Initializing a Static Site Repository

Often we'll want to bootstrap a git repository into which we can download our notebook
and run the conversion.

#### Initializing with Git Repos

```
ipynblog repo git@github.com:andrewlook/ipynblog-template-distill-svelte.git
```

#### Initializing with Cookiecutter

```bash
ipynblog-cookiecutter <cookiecutter_url> [ --metadata ./notebooks/test.ipynb.yaml ]
```

For example:
```bash
export COOKIECUTTER_URL=git@github.com:andrewlook/ipynblog-cookiecutter-svelte-template.git

ipynblog-cookiecutter $COOKIECUTTER_URL
```

### Rendering the Jupyter Notebook

Finally, actually running the renderer.

```bash
ipynblog render \
    --input ./notebooks/test.ipynb \
    --output <cookiecutter repo root>/public/index.html \
    --notebooks-dir <cookiecutter repo root>/notebooks/ \
    --images-dir <cookiecutter repo root>/public/images
```

## Credentials Setup Instructions

See [PyDrive instructions](docs/pydrive.md)


## License

This project is distributed under the MIT license.
