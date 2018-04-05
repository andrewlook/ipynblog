# jupyter2distill

Utility for converting a jupyter/colab notebook into a publishable static site codebase

## Installation

```
pip install jupyter2distill

# install latest directly f/ github
pip install git+https://github.com/andrewlook/jupyter2distill.git#egg=jupyter2distill
```

## Usage

### Downloading Notebooks from Google Colab

Here's a way to download notebooks from Google Colab and extract some metadata in the
process (author, modified date, etc) to be used when rendering the templates. This
metadata can be stored as JSON alongside the downloaded notebook file.

First, you must have a set of credentials from the google API's console. Follow the
instructions in the [pydrive quickstart](http://pythonhosted.org/PyDrive/quickstart.html)
to get your credentials file.

Next, set up some environment variables to tell `jupyter2distill` where to find your
google API configuration files. You'll need 2 env vars:
- `PYDRIVE_CLIENT_CONFIG_FILE`: location of the `client_secrets.json` file provided
  by Google API console.
- `PYDRIVE_SAVED_CREDENTIALS_FILE`: location to store API tokens of authenticated users
  (so you don't need to go through the whole OAuth flow every time you use the script).

You may want to define these in your `.bash_profile` like so:
```bash
#!/bin/bash

export PYDRIVE_CLIENT_CONFIG_FILE=${HOME}/.gcloud_client_secrets.json
export PYDRIVE_SAVED_CREDENTIALS_FILE=${HOME}/.gcloud_drive_credentials.json
```

When you're done (and have either opened a new terminal or done `source ~/.bash_profile`),
you should see something like the following when you check `env`:
```bash
$ env | grep PY
PYDRIVE_CLIENT_CONFIG_FILE=${HOME}/.gcloud_client_secrets.json
PYDRIVE_SAVED_CREDENTIALS_FILE=${HOME}/.gcloud_drive_credentials.json
```

```bash
jupyter2distill download <url> [ --output ./notebooks ]
```


### Initializing a Static Site Repository

Often we'll want to bootstrap a git repository into which we can download our notebook
and run the conversion.

```bash
jupyter2distill repo <cookiecutter_url> [ --notebook ./notebooks/test.ipynb ]
```

For example:
```bash
jupyter2distill repo git@github.com:andrewlook/cookiecutter-svelte-template.git
```

TODOs:
- github integration?

### Producing an Example Template for Jupyter nbconvert

It's likely that the jupyter nbconvert template may need some tweaks. So we recommend
dumping the nbconvert template into the repo and making any necessary modifications
in the template. This can streamline the process of re-rendering from a notebook.

```bash
jupyter2distill template \
    --type distill_v2 \
    --output ./templates

# outputs to './templates/distill_v2.tpl'
```

TODOs:
- add reference for where to learn about nbconvert formatting, reference `basic.tpl`

### Rendering the Jupyter Notebook

Finally, actually running the renderer.

```bash
jupyter2distill render \
    --input ./notebooks/test.ipynb \
    --output <cookiecutter repo root>/public/index.html \
    --notebooks-dir <cookiecutter repo root>/notebooks/ \
    --images-dir <cookiecutter repo root>/public/images
```

## License

This project is distributed under the MIT license.
