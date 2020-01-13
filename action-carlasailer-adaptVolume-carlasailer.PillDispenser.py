#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from settings.SettingsManager import change_volume
from utils.resolve_volume_spec import get_required_volume
from utils.random_answer import get_random_answer           

def start_adaptVolume(hermes, intent_message):    
    """ Callback function for the intent "adaptVolume", gets called when intent is detected

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
        
    #extract the desired volume value from the intent message and adapt the volume
    volume_value = get_required_volume(intent_message.slots)
    
    if volume_value is None:
        #volume value not valid
        #get a randomly chosen answer from a list of possible answers
        message_to_tts = get_random_answer('adaptVolume', 'error')

    else:
        #volume value is valid
        change_volume(volume_value)
        #log the event of changing the volume
        log_msg = '    changed output volume to: {} '.format(str(volume_value))
        log_event(log_msg)
    
        #get a randomly chosen answer from a list of possible answers
        message_to_tts = get_random_answer('adaptVolume', 'adapt')
    
    #end by sending a message to the tts and logging
    log_tts_output(message_to_tts)
    hermes.publish_end_session(intent_message.session_id, message_to_tts)

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "adaptVolume" of the PillDispenser app
        h.subscribe_intent("carlasailer:adaptVolume", start_adaptVolume).start()
