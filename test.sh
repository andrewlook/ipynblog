#!/bin/bash -x

SAMPLE_COLAB_URL="https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO"
SAMPLE_COOKIECUTTER_REPO="git@github.com:andrewlook/cookiecutter-svelte-template.git"

NOTEBOOKS_DIR=$(pwd)/notebooks

jupyter2distill download ${SAMPLE_COLAB_URL} -o ${NOTEBOOKS_DIR}

NOTEBOOK_NAME=$(ls ./notebooks | grep -v ".meta" | head -n1)
NOTEBOOK_SLUG=$(echo ${NOTEBOOK_NAME} | tr '-' '_' | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
NOTEBOOK_PATH=${NOTEBOOKS_DIR}/${NOTEBOOK_NAME}

jupyter2distill repo --notebook ${NOTEBOOK_PATH} ${SAMPLE_COOKIECUTTER_REPO} 

ls -l ${NOTEBOOK_SLUG}/

GEN_NOTEBOOKS_DIR=${NOTEBOOK_SLUG}/notebooks
GEN_PUBLIC_DIR=${NOTEBOOK_SLUG}/public

jupyter2distill template -t distill_v2 -o ${GEN_NOTEBOOKS_DIR} 

TEMPLATE_PATH=${GEN_NOTEBOOKS_DIR}/distill_v2.tpl

jupyter2distill render \
    -i ${NOTEBOOK_PATH} \
    -o ${GEN_PUBLIC_DIR}/index.html \
    --notebooks-dir ${GEN_NOTEBOOKS_DIR} \
    --images-dir ${GEN_PUBLIC_DIR}/images \
    --template ${TEMPLATE_PATH}
