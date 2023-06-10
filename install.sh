mkdir -p ~/.local/share/dpm
rm -rf ~/.local/share/dpm/src
cp -r ./src ~/.local/share/dpm
pip install pyrinth
sudo cp ./dpm.sh /usr/bin/dpm
sudo chmod +x /usr/bin/dpm