#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import json 
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *

from controls.ControlsCommunicator import make_contact
from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from utils.random_answer import get_random_answer
from utils.resolve_contact_info import get_person

def continue_contact(hermes, intent_message, names=None):
    """ No specific person was found for 'contact', send a message to the TTS
    
    Parameters
    ----------
    hermes : <Hermes instance>
        current instance of the hermes broker 
    intent_message : <intent_message by Snips>     
        message created when intent was received
    names : list
        possible doctors if any where found
        
    """
    #log the input and the received intent
    start_logging()
    log_asr_input(intent_message.input)
    log_received_intent(intent_message)
        
    if names is not None:
        #user tried to call a doctor, name was not given
        #suggest possible doctors to be called
        message_to_tts = get_random_answer('contact', 'suggestDoc')
        for name in names:
            message_to_tts += name + ', '
        message_to_tts  = message_to_tts[:-2] + '. ' + get_random_answer('contact', 'notSuccess')
    
    else:
        #no success in extracting person 
        message_to_tts = "Leider konnte ich keine Person ermitteln. " + get_random_answer('contact', 'notSuccess')
    
    #continue the session but only allow intent contact and quitDialog
    INTENT_FILTER_CONTACT = ["carlasailer:contact", "carlasailer:quitDialog"]

    #log the tts output
    log_tts_output(message_to_tts)
    hermes.publish_continue_session(intent_message.session_id, message_to_tts, INTENT_FILTER_CONTACT)
    log_event('    contact: could not be extracted')
    
def end_contact(hermes, intent_message, person):
    """ Person (emergency contact or doctor) could be extracted, send a message to the TTS
   
    Parameters
    ----------
    hermes : <Hermes instance>
        current instance of the hermes broker 
    intent_message : <intent_message by Snips>     
        message created when intent was received
    person : string
        name of the person to be called
        
    """
    # terminate the session by sending message to tts
    # get a randomly chosen answer from a list of possible answers
    message_to_tts = get_random_answer('contact', 'call').format(person)
    
    #log the tts output
    log_tts_output(message_to_tts)
    hermes.publish_end_session(intent_message.session_id, message_to_tts)
    log_event('    contacted: {}'.format(person))
    
def start_contact(hermes, intent_message):    
    """ callback function for the intent "contact", gets called when intent is detected
    
    Parameters
    ----------
    hermes : <Hermes instance>
        current instance of the hermes broker 
    intent_message : <intent_message by Snips>     
        message created when intent was received
        
    """ 
    #extract the person from the intent_message 
    [person, person_type, state] = get_person(intent_message)
        
    if state == 'success':        
        #start the call to the person
        [success, names] = make_contact(person, person_type)
        if success:
            end_contact(hermes, intent_message, person)
        else:
            continue_contact(hermes, intent_message, names)
    else:
        continue_contact(hermes, intent_message)
        

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "contact" of the PillDispenser app
        h.subscribe_intent("carlasailer:contact", start_contact).start()
