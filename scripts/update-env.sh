#!/usr/bin/env bash

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

PYENV=`pyenv -v`

if [ -z "$PYENV" ]
then
    rm -r "${HOME}/.pyenv"
    sh scripts/pyenv-installation.sh
fi

pyenv virtualenv 3.9.2 dragon
pyenv activate dragon

pip install -r requirements.txt