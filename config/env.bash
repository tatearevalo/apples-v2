#!/bin/bash

###############################################################################
#                                                                             #
#  env.bash                                                                   #
#                                                                             #
#     Creates and activates virtual python environment                        #
#                                                                             #
###############################################################################

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
HOME_DIR=/home/$(whoami)
ENV_DIR=$HOME_DIR/venv

if [ -d $ENV_DIR ]
then
	echo Virtual python environment "venv" already exists
else
	echo Creating virtual environment
	python3 -m venv $HOME_DIR/venv
fi

echo 
echo 1. Activate the environment
echo --- $ source $ENV_DIR/bin/activate
echo 
echo 2. Upgrade pip
echo --- $ pip install -U pip
echo
echo 3. Install requirements
echo --- $ pip install -r $DIR/requirements.txt