#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-

import io
from datetime import datetime, timedelta

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *

from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from controls.ControlsCommunicator import ControlsCommunicator
from controls.ControlsCommunicator import set_alarm_confirmed_by_voice
from utils.random_answer import get_random_answer
        
def start_confirmTaking(hermes, intent_message): 
    """ Callback function for the intent "confirmTaking", gets called when intent is detected
    
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
    
    #send successful alarm confirmation to controls communicator
    set_alarm_confirmed_by_voice(True)
    
    #get a randomly chosen answer from a list of possible answers
    message_to_tts = get_random_answer('confirmTaking', 'confirm')
    log_tts_output(message_to_tts)
    hermes.publish_end_session(intent_message.session_id, message_to_tts)


   
if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "confirmTaking" of the PillDispenser app
        h.subscribe_intent("carlasailer:confirmTaking", start_confirmTaking).start()
