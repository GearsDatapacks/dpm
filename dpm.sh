#! /usr/bin/bash

DIR=$(pwd)

cd ~/.local/share/dpm/src/dpm

python dpm.py $@ --dir "$DIR"
