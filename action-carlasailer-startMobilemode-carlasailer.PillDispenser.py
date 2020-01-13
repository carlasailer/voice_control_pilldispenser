#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-

import logging
from datetime import date 

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *

#from controlsCommunicator.ControlsCommunicator import start_mobilemode
from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from utils.random_answer import get_random_answer

def start_startMobilemode(hermes, intent_message):
    """ Callback function for the intent "startMobilemode", gets called when intent is detected
    
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
        
    
    #continue the session by sending a message to the tts, allowing only two intents
    INTENT_FILTER_MOBILEMODE = ["carlasailer:durationMobilemode", "carlasailer:quitDialog"]
        
    message_to_tts = get_random_answer('startMobilemode')
    log_tts_output(message_to_tts)
    hermes.publish_continue_session(intent_message.session_id, message_to_tts, INTENT_FILTER_MOBILEMODE)
 
    
if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    #start_logging()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent startMobilemode of the PillDispenser app
        h.subscribe_intent("carlasailer:startMobilemode", start_startMobilemode).start()
