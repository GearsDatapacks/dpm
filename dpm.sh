#! /usr/bin/bash

BASE_DIR=$(pwd)

cd ~/.local/share/dpm/dpm

DIR=$(pwd)

function installDP() {
  cd src/dpm
  python dpm.py --download "$1"

  for FILE in $(ls "$DIR/downloaded")
  do
    mv "$DIR/downloaded/$FILE" "$BASE_DIR/$FILE"
  done

  rm -rf "$DIR/downloaded"
}

if [ "$1" == "install" ]
then
  installDP "$2"
else
  echo "Error: unknown option \"$1\""
  exit 1
fi
