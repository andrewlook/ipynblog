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

#### Plain git templates way

```
ipynblog repo git@github.com:andrewlook/ipynblog-template-distill-svelte.git
```

#### (TODO Deprecate) The Cookiecutter way
```bash
ipynblog cookiecutter <cookiecutter_url> [ --notebook ./notebooks/test.ipynb ]
```

For example:
```bash
ipynblog cookiecutter git@github.com:andrewlook/ipynblog-cookiecutter-svelte-template.git
```

TODOs:
- github integration?

### Producing an Example Template for Jupyter nbconvert

It's likely that the jupyter nbconvert template may need some tweaks. So we recommend
dumping the nbconvert template into the repo and making any necessary modifications
in the template. This can streamline the process of re-rendering from a notebook.

```bash
ipynblog template \
    --type distill_v2 \
    --output ./templates

# outputs to './templates/distill_v2.tpl'
```

TODOs:
- add reference for where to learn about nbconvert formatting, reference `basic.tpl`

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
