#!/bin/bash -eu

# Bash installer for tkldev-tools

. lib/bash-common

check_root

deps="devscripts" # includes dch which we leverage for tkldev-changelog
deps="$deps python3-colorama" # required for turnkey-bugs

to_install=""
for dep in $deps; do
    dpkg -s $dep >/dev/null 2>&1 || to_install="$to_install $dep"
done
if [[ -n "$to_install" ]]; then
    info "Please wait while apt indexes are updated and packages installed."
    apt update -qq
    DEBIAN_FRONTEND=noninteractive apt-get install -y $to_install
fi

[[ "$0" == "./install.sh" ]] || fatal "Must be run from within the base dir."
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

ENV="$HOME/.bashrc.d/tkldev-tools"
VARS="DEBFULLNAME DEBEMAIL FULLNAME EMAIL"
unset _mail _name
if [[ ! -f "$ENV" ]]; then
    cat > $ENV <<EOF
# tkldev-tools (dch specifcially) requires env vars

# will check DEBFULLNAME & DEBEMAIL first
#export DEBFULLNAME=""
#export DEBEMAIL=""

# will fallback to these if above not set
#export FULLNAME="Jeremy Davis"
#export EMAIL="jeremy@turnkeylinux.org"
EOF
    chmod +x $ENV
    msg="Env file ($ENV) created, please edit it and uncomment and update"
    warning "$msg relevant values"
else
    msg="Env file ($ENV) exists, skipping creation. Be sure to set"
    msg="$msg DEBFULLNAME/FULLNAME and DEBEMAIL/EMAIL for tkldev-changelog"
    warning "$msg"
fi

mkdir -p ${ETC_PATH}
if [[ ! -f ${CONF} ]]; then
    cp ${CONF_EX} ${CONF}
else
    if ! diff ${CONF_EX} ${CONF} >/dev/null 2>&1; then
        warning "${CONF} already exists, please check that it is compatible with ${CONF_EX}"
    fi
fi
info "install complete."
