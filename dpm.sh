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

BASE_DIR=$(pwd)

#cd ~/.local/share/dpm/dpm
cd ~/Desktop/learnweb/python/dpm

DIR=$(pwd)

cd src/dpm

map "$@"

python dpm.py "$ARGS"

for FILE in $(ls "$DIR/downloaded")
do
  mv "$DIR/downloaded/$FILE" "$BASE_DIR/$FILE"
done

rm -rf "$DIR/downloaded"
