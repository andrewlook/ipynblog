#!/bin/bash -x

SAMPLE_COLAB_URL="https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO"
SAMPLE_COOKIECUTTER_REPO="git@github.com:andrewlook/cookiecutter-svelte-template.git"

NOTEBOOKS_DIR=$(pwd)/notebooks

jupyter2distill download ${SAMPLE_COLAB_URL} -o ${NOTEBOOKS_DIR}

NOTEBOOK_PATH=${NOTEBOOKS_DIR}/$(ls ./notebooks | grep -v ".meta" | head -n1)

jupyter2distill repo --notebook ${NOTEBOOK_PATH} ${SAMPLE_COOKIECUTTER_REPO} 
