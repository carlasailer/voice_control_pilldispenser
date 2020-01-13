#!/bin/sh

#change the TTS engine to dual TTS provider

#in this case: enable the dual TTS! uncomment the line
sudo sed -i '69 s/^#//' /etc/snips.toml
sudo systemctl stop snips-tts
sudo systemctl restart snips-*
sudo systemctl stop snips-tts
#sudo systemctl start snips-tts
