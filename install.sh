#! /usr/bin/bash
echo "#! /usr/bin/bash

BASE_DIR=\$(pwd)

cd ~/.local/share/dpm

DIR=\$(pwd)

function installDP() {
  python install.py \"\$1\"

  for FILE in \$(ls \"\$DIR/downloaded\")
  do
    mv \"\$DIR/downloaded/\$FILE\" \"\$BASE_DIR/\$FILE\"
  done

  rm -rf \"\$DIR/downloaded\"
}

if [ \"\$1\" == \"install\" ]
then
  installDP \"\$2\"
else
  echo \"Error: unknown option \\\"\$1\\\"\"
  exit 1
fi
" > /usr/bin/dpm
chmod +x /usr/bin/dpm
cd ~/.local/share
git clone git@github.com:GearsDatapacks/dpm.git