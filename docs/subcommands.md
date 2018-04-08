## ipynblog subcommands

There are several individual versions of the commands for those wishing to
download / render separately.

### ipynblog-render

Running the nbconvert template `distill_v2_svelte.tpl` on `test.ipynb`:
```bash
ipynblog-render  ./notebooks/test.ipynb  <cookiecutter_repo_root>/public/index.html \
    --template <cookiecutter_repo_root>/nbconvert/distill_v2_svelte.tpl \
    --images-dir <cookiecutter_repo_root>/public/images
```

Alternatively, from a directory already containing a template's `ipynblog.yaml`:
```bash
ipynblog-render --config ./ipynblog.yaml
```

### ipynblog-download

Here's a way to download notebooks from Google Colab and extract some metadata in the
process (author, modified date, etc) to be used when rendering the templates. This
metadata can be stored as JSON alongside the downloaded notebook file.

**Note:** Be sure to complete the [PyDrive setup](docs/pydrive.md) before running
this:

```bash
ipynblog-download <url> [ --dir ./notebooks ]
```

Or, from an already-initialized ipynblog template repo,
```bash
# re-downloads <colab_url> to <nbconvert_input>
ipynblog-download --config ipynblog.yaml
```

### ipynblog-cookiecutter 

```bash
ipynblog-cookiecutter <cookiecutter_url> [ --metadata ./notebooks/test.ipynb.yaml ]
```

For example:
```bash
export COOKIECUTTER_URL=git@github.com:andrewlook/ipynblog-cookiecutter-svelte-template.git

ipynblog-cookiecutter $COOKIECUTTER_URL
```


