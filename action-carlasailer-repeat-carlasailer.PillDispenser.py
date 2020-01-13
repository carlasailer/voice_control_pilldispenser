#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from utils.random_answer import get_random_answer           

def get_last_log_entry(keyword='output'):
    """ Retrieves the last log entry of either input or output log as defined in keyword
    
    Parameters
    ----------
    keyword: string
        'input' (ASR) or 'output' (TTS)
    
    Returns
	-------
	last_log : string
		last entry in the chosen log file 
                
    """
    
    if keyword == 'output':
        filename_log = '/var/lib/snips/skills/snips_app_pilldispenser/logs/output.log'
    else:
        filename_log = '/var/lib/snips/skills/snips_app_pilldispenser/logs/input.log'
    
    with open(filename_log, 'r') as f:
        lines = f.readlines()
        #take the last log and format it
        last_log = lines[-1].split(' ')
        last_log = ' '.join(last_log[2:])
        return last_log
    
def start_repeat(hermes, intent_message):
    """ Callback function for the intent "repeat", gets called when intent is detected
    
    Parameters
    ----------
    hermes : <Hermes instance>
        current instance of the hermes broker 
    intent_message : <intent_message by Snips>     
        message created when intent was received
    
    """ 
    
    #extracting relevant information from the slot values
    if intent_message.slots.you_me.all() is not None:
        direction = intent_message.slots.you_me.first().value
        
        if direction == 'du':
            #user wants to know last tts output
            log = get_last_log_entry(keyword='output')    
            message_to_tts = get_random_answer('repeat', 'last_tts').format(log)
        
            
        elif direction == 'ich':
            #user wants to know last asr input
            log = get_last_log_entry(keyword='input')
            message_to_tts = get_random_answer('repeat', 'last_asr').format(log)
  
    else:
        #error occured, default: repeat last tts
        log = get_last_log_entry(keyword='output')
        message_to_tts = get_random_answer('repeat', 'last_tts').format(log)
     
     #end the session by sending the message to the tts
    log_tts_output(message_to_tts)
    hermes.publish_end_session(intent_message.session_id, message_to_tts)
    

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "repeat" of the PillDispenser app
        h.subscribe_intent("carlasailer:repeat", start_repeat).start()

