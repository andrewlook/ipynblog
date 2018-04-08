# ipynblog

Utility for converting a jupyter/colab notebook into a publishable static site codebase

## Installation

```
# install latest directly f/ github
pip install git+https://github.com/andrewlook/ipynblog.git#egg=ipynblog
```

## Usage: Basic

```bash
ipynblog <template> [--colab-url <url> | --notebook-file <file>] [--name <name>]

export SVELTE_TEMPLATE=https://github.com/andrewlook/ipynblog-template-distill-svelte.git

#
# generates static site into ./deepdream-startup-breakfast from local file
#
ipynblog $SVELTE_TEMPLATE \
    --notebook-file deepdream-startup-breakfast.ipynb

# overriding the name, generating into ./startup-breakfast
ipynblog $SVELTE_TEMPLATE \
    --notebook-file deepdream-startup-breakfast.ipynb \
    --name startup-breakfast

#
# downloading ipynb from Google Colab, then generating into ./startup_breakfast
# (pydrive must be set up first).
#
export SAMPLE_COLAB_URL="https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO"

ipynblog $SVELTE_TEMPLATE \
    --colab-url $SAMPLE_COLAB_URL \
    --name startup_breakfast


cd startup_breakfast
npm install             # install JS dependencies
npm run serve           # run local webpack dev server (with hot reload for JS)
npm run build           # compile HTML/JS for static site deployment
```

## ipynblog templates

To generate a new static site repo for a converted jupyter notebook, the directory
structure of [ipynblog-template-distill-svelte](https://github.com/andrewlook/ipynblog-template-distill-svelte.git) looks roughly like this:
```
notebooks/
    test.ipynb             # sample jupyter notebook
nbconvert/
    distill_v2_svelte.tpl  # jinja2 template for jupyter's nbconvert
public/
    index.html             # result of converting test.ipynb
    index.bundle.js        # rendered webpack bundle, result of 'npm run build'
components/                # svelte custom web components go here
bundles/
    index.js               # module exporter for webpack
package.json
webpack.config.js
ipynblog.yaml              # tells ipynblog how to render notebook into generated proj
```

### ipynblog.yaml

Since different projects can have different structures, it may be necessary to use a
different jinja template for nbconvert (ex. to render plain HTML vs. custom JS
components, depending on how interactive the post is), or to render the notebook
into a differently-named file.

The contents of `ipynblog.yaml` look like this:
```yaml
ipynblog_template:
    nbconvert_template: ./nbconvert/distill_v2_svelte.tpl
    nbconvert_input: ./notebooks/test.ipynb
    nbconvert_output: ./public/index.html
    images_dir: ./public/images/
```

When a project is initialized from this template for `startup-breakfast.ipynb`,
we want to:
- replace the placeholder notebook `test.ipynb` with the input notebook,
- replace `index.html` with the generated output from `distill_v2_svelte.tpl`,
- extract any inline images from the jupyter notebook and storing them in
  `public/images`.


## Usage: Advanced

See [Subcommands](docs/subcommands.md):
- [ipynblog-render](docs/subcommands.md#ipynblog-render)
- [ipynblog-download](docs/subcommands.md#ipynblog-download)
- [ipynblog-cookiecutter](docs/subcommands.md#ipynblog-cookiecutter)

## Credentials Setup Instructions

See [PyDrive instructions](docs/pydrive.md)


## License

This project is distributed under the MIT license.
