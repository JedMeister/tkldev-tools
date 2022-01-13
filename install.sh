#!/bin/bash -eu

# Bash installer for tkldev-tools

. lib/bash-common

check_root

deps="devscripts"

to_install=""
for dep in $deps; do
    dpkg -s $dep >/dev/null 2>&1 || to_install="$to_install $dep"
done
if [[ -n "$to_install" ]]; then
    info "Please wait while apt indexes are updated and packages installed."
    apt update -qq
    DEBIAN_FRONTEND=noninteractive apt-get install -y $to_install
fi

SRC_PATH=$PWD
BASE_PATH=/usr/local
BIN_PATH=${BASE_PATH}/bin
LIB_PATH=${BASE_PATH}/lib
ETC_PATH=/etc/tkldev-tools
CONF=${ETC_PATH}/conf
CONF_EX=${SRC_PATH}/etc/conf.example

for file in $(find ${SRC_PATH}/bin -executable -type f); do
    ln -fs ${file} ${BIN_PATH}/$(basename ${file})
done
for file in $(find ${SRC_PATH}/lib -type f); do
    ln -fs ${file} ${LIB_PATH}/$(basename ${file})
done
mkdir -p ${ETC_PATH}
if [[ ! -f ${CONF} ]]; then
    cp ${CONF_EX} ${CONF}
else
    if ! diff ${CONF_EX} ${CONF} >/dev/null 2>&1; then
        warning "${CONF} already exists, please check that it is compatible with ${CONF_EX}"
    fi
fi
info "install complete."
