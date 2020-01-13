#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

from controls.ControlsCommunicator import get_history
from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from utils.random_answer import get_random_answer

def start_getHistory(hermes, intent_message):   
    """ callback function for the intent "getHistory", gets called when intent is detected
    
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
        
    #get history of medications as a dict
    [non_corrects, history] = get_history()
    
    #choose parts of the TTS message randomly
    final_message = get_random_answer(intent_name='getHistory', key_name='info') + ' ' 
    history_msg = get_random_answer(intent_name='getHistory', key_name='nonCorrects') 
    
    #create complete TTS message based on received history
    final_message = final_message + history_msg.format(non_corrects)
    print(final_message)
        
    #terminate the session by sending message to tts    
    log_tts_output(final_message)
    hermes.publish_end_session(intent_message.session_id, final_message)
    

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "getHistory" of the PillDispenser app
        h.subscribe_intent("carlasailer:getHistory", start_getHistory).start()
