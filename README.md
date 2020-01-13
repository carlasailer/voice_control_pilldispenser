# Voice Control for an Intelligent Pill Dispensing System using the Snips Voice Platform (https://snips.ai/)

This repository provides Python code for a voice control system. It is composed of the action code as expected by the 'snips-skill-server' (`action-*.py`). One such file is generated per intent supported. These are standalone executables and will perform a connection to MQTT and register on the given intent using the `hermes-python` helper lib. Additional Python scripts ensure a modular structure of the code. 
All the scripts are coded to run on a Raspberry Pi Model 3B. 

Intents for the following use cases of a pill dispenser are supported:
- call a doctor / an emergency contact
- get information about future medication withdrawals
- get information about previous faulty medication withdrawals 
- support the medication withdrawal
- enter and stop mobile mode (mobile unit of the pill dispenser) 

Other functionalities concerning the Snips Voie Platform are:
- three wake words available: "Tantum", "privater Bereich" and "Hey Snips"
- add names of contact persons and doctors to vocabulary of VoiceControl (Dynamic Entities Injection Feature)
- log all intents, inputs to the asr and outputs to the tts in separate files
- ask Snips to speak louder or less loud (using alsamixer)
- ask Snips to repeat what was said before

## Setup

This app requires some python dependencies to work properly, these are
listed in the `requirements.txt`. You can use the `setup.sh` script to
create a python virtualenv that will be recognized by the skill server
and install them in it.
