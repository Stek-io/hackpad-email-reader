#!/usr/bin/env bash

# Get full path to the directory of this file
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null

VENV_NAME="venv"

LOGO="
====================================
=====   HackPad Email Parser   =====
====================================
"

# Print some intro
echo "$LOGO"

# Go into the app root directory
cd "$SCRIPTPATH/../"

# Activate Virtual Env
source "$VENV_NAME/bin/activate"

CONFIG_FILE=${1:-./config/config.yml}

# Run script
python3 ./app/fetch_credentials.py --config-file $CONFIG_FILE

deactivate