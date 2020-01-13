#!/bin/sh

#change the TTS engine to dual TTS provider

#go back to single TTS! comment the line
sudo sed -i '69 s/^/#/' /etc/snips.toml
sudo systemctl restart snips-tts
