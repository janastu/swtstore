#!/bin/bash

# NOOB Install: Script to install opinonated defaults and setup swtstore
# Right now works only Debian-based systems
# BSD License: swtstore authors. See LICENSE file for details.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DEPENDENCIES=( postgresql postgresql-server-dev-all python-dev python-pip )

cd $DIR

is_installed() {
  req=$1
  # To find out a program is installed from shell script might not be
  # straightforward and consistent. See this answer for more details:
  # http://stackoverflow.com/questions/592620/how-to-check-if-a-program-exists-from-a-bash-script#677212
  if $(command -v "$req" > /dev/null); then # if found
    return 0
  else
    return 1
  fi
}

install_deps() {
  echo "Installing ${DEPENDENCIES[@]}.."
  echo "sudo apt-get install ${DEPENDENCIES[@]}"

  sudo apt-get install "${DEPENDENCIES[@]}"
}

install_venv() {
  echo "Installing virtualenv.."
  if ! $(is_installed virtualenv); then
    echo "sudo pip install virtualenv"
    sudo pip --proxy="$http_proxy" install virtualenv
  else
    sudo pip --proxy="$http_proxy" --upgrade virtualenv
  fi
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
#activate_venv && install_swtstore
