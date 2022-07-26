#!/usr/bin/env bash

RASPI="dragon@192.168.1.38"
MAIN_DIR="/tmp/project"
SCRIPT_DIR="${MAIN_DIR}/scripts"

echo "${PWD}"

rsync -avu --exclude venv --exclude .idea --delete "${PWD}/" "${RASPI}:${MAIN_DIR}"


for fn in "$@"
do
    ssh "${RASPI}" "cd $MAIN_DIR; sh ${SCRIPT_DIR}/${fn}.sh"
done

ssh "${RASPI}" "python3 ${MAIN_DIR}/main.py"