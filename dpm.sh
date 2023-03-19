#! /usr/bin/bash

ARGS=""

function map () {
  for ARG in "$@"
  do
    case "$ARG" in
      [iI] | [iI][nN][sS][tT][aA][lL][lL])
        ARGS="$ARGS --install"
      ;;
      
      [pP][uU][bB][lL][iI][sS][hH])
        ARGS="$ARGS --publish"
      ;;
      *)
        ARGS="$ARGS $ARG"
      ;;
    esac
  done
}

DIR=$(pwd)

cd ~/.local/share/dpm/src/dpm

map "$@"

python dpm.py $ARGS --dir "$DIR"
