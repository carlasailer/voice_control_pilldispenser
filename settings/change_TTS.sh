#!/bin/sh

#change the TTS engine depending on online-state 
#which is handed as param (1 for online, 0 for offline)

state="$1"

if [["$1" -eq "1"]]; then
	sudo sed -i -e 's/provider = "picotts"/provider = "customtts"/' /etc/snips.toml
	sudo systemctl stop snips-asr
	sudo systemctl start snips-asr-google
else 
	sudo sed -i -e 's/provider = "customtts"/provider = "picotts"/' /etc/snips.toml
	sudo systemctl stop snips-asr-google
	sudo systemctl start snips-asr
fi

sudo systemctl restart snips-*