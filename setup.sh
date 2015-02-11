#!/bin/bash

# NOOB Install: Script to install opinonated defaults and setup swtstore
# Right now works only Debian-based systems
# BSD License: swtstore authors. See LICENSE file for details.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DEPENDENCIES=( postgresql-9.4 postgresql-server-dev-9.4 python-dev python-pip )

cd $DIR

install_deps() {
  echo "Installing ${DEPENDENCIES[@]}.."
  echo "sudo apt-get install ${DEPENDENCIES[@]}"

  sudo apt-get update && sudo apt-get install "${DEPENDENCIES[@]}"
}

install_venv() {
  echo "Installing virtualenv.."
  echo "sudo pip install virtualenv"
  sudo pip install virtualenv
}

activate_venv() {
  virtualenv venv && source venv/bin/activate
}

install_swtstore() {
  python setup.py install
  cp swtstore/sample_config.py swtstore/config.py
  mkdir logs
}

install_deps && install_venv && activate_venv && install_swtstore
