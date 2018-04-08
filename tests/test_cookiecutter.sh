#!/bin/bash -x

SAMPLE_COLAB_URL="https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO"
SAMPLE_COOKIECUTTER_REPO="git@github.com:andrewlook/ipynblog-cookiecutter-svelte-template.git"

NOTEBOOKS_DIR=$(pwd)/notebooks

ipynblog-download ${SAMPLE_COLAB_URL} -d ${NOTEBOOKS_DIR}

NOTEBOOK_NAME=$(ls ./notebooks | grep -v ".meta" | head -n1)
NOTEBOOK_SLUG=$(echo ${NOTEBOOK_NAME} | tr '-' '_' | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
NOTEBOOK_PATH=${NOTEBOOKS_DIR}/${NOTEBOOK_NAME}
NOTEBOOK_META=${NOTEBOOK_PATH}.yaml

ipynblog-cookiecutter --metadata ${NOTEBOOK_META} ${SAMPLE_COOKIECUTTER_REPO}

ls -l ${NOTEBOOK_SLUG}/

GEN_NOTEBOOKS_DIR=${NOTEBOOK_SLUG}/notebooks
GEN_PUBLIC_DIR=${NOTEBOOK_SLUG}/public

ipynblog-render ${NOTEBOOK_PATH} ${GEN_PUBLIC_DIR}/index.html \
    --images-dir ${GEN_PUBLIC_DIR}/images \
    --template ${GEN_NOTEBOOKS_DIR}/nbconvert.tpl
