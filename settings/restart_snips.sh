#!/bin/sh

#manually restart all snips components

sudo systemctl restart snips-asr
sudo systemctl restart snips-audio-server
sudo systemctl restart snips-dialogue
sudo systemctl restart snips-hotword
sudo systemctl restart snips-nlu
sudo systemctl restart snips-skill-server
sudo systemctl restart snips-tts

gnome-terminal -e snips-skill-server
