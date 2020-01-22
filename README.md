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

## Abstract
More than three-quarters of the German population takes at least one pill every day. Additionally, the number of prescribed pills a patient has to ingest increases with age. The  correct  taking  can  pose  an  insurmountable  obstacle  for  those  with  cognitive 
impairment  due  to  age.  The  pill  dispenser  developed  in  the  TANTUM  project  is  an intelligent medication system, which supports old and chronically ill people with their daily medication taking. To increase acceptance in the target group, the user interface of the pill dispenser is extended with voice control. 

The aim of this work is the conception and prototypical implementation of such voice control. One requirement for user interfaces in Ambient Assisted Living (AAL) systems is to  focus  on  practical  use  cases  during  the  development  process.  Therefore,  the  use 
cases “Confirm pill taking”, “Get information about future medications”, “Contact”, “Start mobile  mode”,  “End  mobile  mode”,  “Get  information  about  magazine  stock”,  “Get information about discrepancies” and “Give power warning” were modeled.  

After a comparison of different approaches, the Snips Voice Platform was chosen for the prototypical  implementation.  This  platform  offers  the  chance  to  define  the  scope  of application of a voice assistant online and to perform the training online. The components of  the  voice  control  such  as  ASR,  NLU,  and  TTS  are  provided  by  the  Snips  Voice Platform,  are  capable  of  running  on  edge  device  with  limited  resources  and  do  not depend on internet connection.  

Finally,  the  implemented  voice  control  was  analyzed  in  terms  of  elderly-appropriate design.  The  identified  and  implemented  measures  that  render  the  system  elderly-appropriate include the adaptability of the speech output volume, the possibility to repeat 
information, the flexibility in speech input, and the speech input with a decreased rate of speaking. 
