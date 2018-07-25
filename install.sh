#!/bin/bash -e

# Bash installer for tkldev-tools

. lib/bash-common

check_root

SRC_PATH=$PWD
BASE_PATH=/usr/local
BIN_PATH=${BASE_PATH}/bin
LIB_PATH=${BASE_PATH}/lib
ETC_PATH=/etc/tkldev-tools
CONF=${ETC_PATH}/conf
CONF_EX=${SRC_PATH}/etc/conf.example

for file in $(find ${SRC_PATH}/bin -executable -type f); do
    ln -s ${file} ${BIN_PATH}/$(basename ${file})
done
for file in $(find ${SRC_PATH}/lib -type f); do
    ln -s ${file} ${LIB_PATH}/$(basename ${file})
done
mkdir -p ${ETC_PATH}
if [[ ! -f ${CONF} ]]; then
    cp ${CONF_EX} ${CONF}
else
    grep LIB_PATH ${CONF} >/dev/null || warning "LIB_PATH not set in conf"
    warning "${CONF} already exists, please check that it is compatible with ${CONF_EX}"
fi
