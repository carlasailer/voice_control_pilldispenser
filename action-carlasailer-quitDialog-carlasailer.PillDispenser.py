#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output

def start_quitDialog(hermes, intent_message):
    """ Callback function for the intent "quitDialog", gets called when intent is detected
    
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
        
    #log the intent of the user
    log_msg = '     User quits.'
    log_event(log_msg)
    
    #end the session with sending an empty message to the tts
    message_to_tts = ' ' 
    hermes.publish_end_session(intent_message.session_id, message_to_tts)

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "contact" of the PillDispenser app
        h.subscribe_intent("carlasailer:quitDialog", start_quitDialog).start()
