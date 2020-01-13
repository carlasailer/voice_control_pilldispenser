#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

from controls.ControlsCommunicator import get_alarm_info
from logs.LoggingManager import start_logging, log_event, log_received_intent, log_asr_input, log_tts_output
from utils.resolve_time_spec import get_required_days 
from utils.random_answer import get_random_answer

#conversion for weekdays
dic_weekdays = {0:'Montag', 1:'Dienstag', 2:'Mittwoch', \
                3:'Donnerstag', 4:'Freitag', 5:'Samstag', \
                6:'Sonntag'}
                
def create_msg_for_one_day(alarms):
    """ Sets up the message for one required day
    
    Parameters
    ----------
    alarms : list
        alarms from the database for the required day
        
    """
    alarm_day = alarms[0][0]
    msg = get_random_answer('infoMedication', 'days').format(alarm_day) + ' ' 
    for item in alarms:
        msg += item[1] + ', '     
    return msg[:-2], alarm_day
    
def start_infoMedication(hermes, intent_message):
    """ Callback function for the intent "infoMedication", gets called when intent is detected

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
        
    #extract the days to be informed about from slot values
    global alarm_day
    
    required_days = get_required_days(intent_message.slots)
    print(required_days)
    if required_days is None:
        required_days = []
        
    #get day and time of next alarm according to alarm settings
    if required_days == 8:
        #info about next alarm
        [alarm_day, alarm_time] = get_alarm_info()
        message_to_tts = get_random_answer('infoMedication', 'next').format(alarm_day, alarm_time)
        
    elif required_days != 8 and len(required_days) == 1:
        #info about alarms for one specific weekday
        alarms = get_alarm_info(required_days)
        print(alarms)
        if alarms == []:
            #no alarms found for that day
            alarm_day = None
            message_to_tts = 'Keine Alarme für {} hinterlegt.'.format(dic_weekdays[required_days[0]])
        else:     
            [message_to_tts, alarm_day] = create_msg_for_one_day(alarms)
          
    else:
        #info about alarms for multiple days
        total_alarms = []
        message_to_tts = ''
        for day in required_days:
            alarms = get_alarm_info([day])
            if alarms != []:
                [day_msg, d] = create_msg_for_one_day(alarms)
                alarm_day = required_days
                total_alarms.append(alarms)
            else:
                day_msg = 'Für {} sind keine Alarme hinterlegt. '.format(dic_weekdays[day])
            message_to_tts += day_msg
        
        alarm_day = None
            
        #ToDo: multiple days!
        pass
            
    #log 
    if alarm_day is not None:
        log_msg = '    info about next alarm for: {}'.format(alarm_day)   
    else:
        log_msg = '    info about next alarm for: '
            
    log_event(log_msg)
    
    #end the session by sending message to tts    
    log_tts_output(message_to_tts)
    hermes.publish_end_session(intent_message.session_id, message_to_tts)  

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        #subscribe to the intent "infoMedication" of the PillDispenser app
        h.subscribe_intent("carlasailer:infoMedication", start_infoMedication) \
         .start()
