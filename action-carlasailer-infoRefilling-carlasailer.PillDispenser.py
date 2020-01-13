#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *

from controls.ControlsCommunicator import get_stock_info
from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from utils.random_answer import get_random_answer

#conversion for weekdays
dic_weekdays = {0:'Montag', 1:'Dienstag', 2:'Mittwoch', \
                3:'Donnerstag', 4:'Freitag', 5:'Samstag', \
                6:'Sonntag', 7: 'Reserve'}
                
def start_infoRefilling(hermes, intent_message):
    """ Callback function for the intent "infoRefilling", gets called when intent is detected
    
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
        
    #get the stock information from the controls
    stock_info = get_stock_info()
    
    #get a random answer for constructing the final message to the TTS
    info_message = get_random_answer('infoRefilling', 'info') + 'Folgende Magazine sind noch voll: '
    single_message_stock = get_random_answer('infoRefilling', 'stock_info')
    single_message_empty = get_random_answer('infoRefilling', 'empty')
    
    #extract the information from stock_info and form the TTS message
    message_to_tts = ''
    for magazine_nr in range(0, len(stock_info)):
        
        if stock_info[magazine_nr] in [25, 50, 75]: 
            #magazines that are neither completely empty nor completely full
            message_to_tts += single_message_stock.format(dic_weekdays[magazine_nr], stock_info[magazine_nr])
            
        elif stock_info[magazine_nr] == 100:
            #magazines that are completely empty
            message_to_tts += single_message_empty.format(dic_weekdays[magazine_nr])
            
        else:
            #magazines that are completely full
            info_message += dic_weekdays[magazine_nr] + ', '
            
    message_to_tts = info_message[:-2] + '. ' + message_to_tts      
    
    # terminate the session by sending message to tts
    log_tts_output(message_to_tts)
    hermes.publish_end_session(intent_message.session_id, message_to_tts)
    
    
if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "infoRefilling" of the PillDispenser app
        h.subscribe_intent("carlasailer:infoRefilling", start_infoRefilling).start()
