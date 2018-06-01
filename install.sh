#!/bin/bash -e

SRC_DIR=$PWD
INS_DIR=/usr/local/bin

for file in $(find $SRC_DIR/bin -type f); do 
    ln -s $file $INS_DIR/$(basename $file)
done
