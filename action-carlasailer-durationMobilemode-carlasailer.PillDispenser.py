#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-
import io
import json
import numpy as np

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *

from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from utils.resolve_time_spec import get_required_days
from utils.random_answer import get_random_answer

#conversion for weekdays
dic_weekdays = {0:'Montag', 1:'Dienstag', 2:'Mittwoch', \
                3:'Donnerstag', 4:'Freitag', 5:'Samstag', \
                6:'Sonntag'}

#conversion from weekdays to numbers - reversed dictionary
dic_daynr = {day: nr for nr, day in dic_weekdays.items()}
      
def continue_durationMobilemode(hermes, intent_message):
    """ Callback function for the intent "durationMobilemode", gets called when intent is detected
    
    Parameters
    ----------
    hermes : <Hermes instance>
        current instance of the hermes broker 
    intent_message : <intent_message by Snips>     
        message created when intent was received
        
    """ 
    #log the input and the received intent
    start_logging()
    log_asr_input(intent_message.input)
    log_received_intent(intent_message)
        
    #get required days based on slot values in intent message
    required_days = get_required_days(intent_message.slots)
        
    #convert numbers to weekdays and format for output message 
    required_days_str = ''
    if required_days is not None:
        for key in required_days:
            required_days_str += dic_weekdays.get(key) + ', '
    
        #no action in control unit! 
    
        #log 
        log_msg = '    started mobile dispenser: {}'.format(required_days_str[:-2])   
        log_event(log_msg)
    
        #get a randomly chosen answer from a list of possible answers
        message_to_tts = get_random_answer('durationMobilemode').format(required_days_str[:-2])
        log_tts_output(message_to_tts)
        
    else:
        #error occurred during extraction of required days
        message_to_tts = 'Mobilmodus konnte nicht gestartet werden. Bitte erneut versuchen.'
    
    #end the session by sending the message to the tts
    hermes.publish_end_session(intent_message.session_id, message_to_tts)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    #start_logging()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "durationMobilemode" of the PillDispenser app
        h.subscribe_intent("carlasailer:durationMobilemode", continue_durationMobilemode).start()
