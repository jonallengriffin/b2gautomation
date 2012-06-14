#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

PYTHON=$1
VENV_DIR="postbuildresults_venv"

if [ -z "${PYTHON}" ]
then
    echo "No python found"
    exit 1
fi

# delete any existing venv
if [ -d "${VENV_DIR}" ]
then
   rm -rf ${VENV_DIR}
fi

# create a virtual env
curl https://raw.github.com/pypa/virtualenv/develop/virtualenv.py | ${PYTHON} - ${VENV_DIR} 
cd ${VENV_DIR}
. bin/activate

# set up mozautolog
hg clone http://hg.mozilla.org/automation/mozautolog/
cd mozautolog
python setup.py develop
cd ..

# set up tailer
easy_install tailer

# run the postbuildresults script
cd ..
python postbuildresults.py

