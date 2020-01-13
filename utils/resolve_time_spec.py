#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-

""" resolve_time_spec
This script formats the slot values of the intent message to extract information 
about which weekday(s) where chosen by the user for the mobile mode. 

It contains the following functions:
	* check_days - converts to valid weekday integer
    * get_required_days_by_timespec - extract days from time specification
    * get_required_days_by_num - extract days from given number
    * get_required_days - parent function to choose either timespec or number extraction
    	
"""

import datetime
import numpy as np

#conversion for weekdays
dic_weekdays = {0:'Montag', 1:'Dienstag', 2:'Mittwoch', \
                3:'Donnerstag', 4:'Freitag', 5:'Samstag', \
                6:'Sonntag'}

#conversion from weekdays to numbers - reversed dictionary
dic_daynr = {day: nr for nr, day in dic_weekdays.items()}
                
def check_days(days):
    """ Converts list of days to valid list of days, only integers from 
    0 to 6
    
    Parameters
    ----------
    days : list
        weekdays as integers (0: Monday, 1: Tuesday etc)
        
    Returns
    -------
    valid_days : list
        formatted list of days
        
    """
    
    valid_days = np.asarray([(elem-7) if elem>=7 else elem for elem in days]) 
    return valid_days
        
def get_required_days_by_timespec(slot_vals, time_span_signal):	
    """ Extract required weekdays from slot values (time specification)
    
    Parameters
    ----------
    slot_vals : list
        values of the intent message
    time_span_signal : list
        values of the slot "time_span_signal"
    
    Returns
    -------
    days : list
        formatted list of days
        
    """
    
    days = []
    
    if 'bis' in time_span_signal:
        #first check for time span
        common_elem = [dic_daynr.get(key) for key in slot_vals]

        if len(common_elem)==2:
            #if exactly two weekdays are given
            if common_elem[0] < common_elem[1]:
                #e.g. 'Montag bis Mittwoch'
                days = list(range(common_elem[0], common_elem[1]+1))
                return days
             
            else:
                #e.g. 'Freitag bis Montag' - start of new week
                #get difference between numbers
                diff = common_elem[0] - common_elem[1]             
                days = list(range(common_elem[0], common_elem[0]+7-diff+1))    
                return check_days(days)
                
        elif len(common_elem)==1:
            #e.g. 'Ich brauche die Box bis Montag'
            #start from today until required day
            weekday_today = datetime.date.today().weekday()
            diff = weekday_today - common_elem[0]
            days = list(range(weekday_today, weekday_today+7-diff+1))
            return check_days(days)
            
        else:
            #something went wrong
            print('Not a time span.')
            return []
        
    elif 'heute' in slot_vals:
        days.append(datetime.date.today().weekday())
        return days

    elif 'morgen' in slot_vals:
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).weekday()
        days.append(tomorrow)
        return check_days(days)
 
    elif u'\xfcbermorgen' in slot_vals:
        day_tomorrow = (datetime.date.today() + datetime.timedelta(days=2)).weekday()
        days.append(day_tomorrow)
        return check_days(days)
        
    elif 'Wochenende' in slot_vals:
        #return values for saturday and sunday
        days = [5,6]
        return days
    
    elif (set(dic_weekdays.values()) & set(slot_vals)):
        #check for a specific weekday
        common_elem = list(set(dic_weekdays.values()) & set(slot_vals))
        days = [dic_daynr.get(key) for key in common_elem]
        return days
        
    elif (set([u'n\xe4chste', u'n\xe4chster', u'n\xe4chstes Mal', u'n\xe4chste Mal']) & set(slot_vals)):
        days = 8 
        return days
    
    else:
        print('Time spec could not be extracted. Quitting...')
        return []
    
def get_required_days_by_num(slot_vals):
    """ Extract required weekdays from slot values (number of days)
    
    Parameters
    ----------
    slot_vals : list
        values of the intent message
    
    Returns
    -------
    required_days_num : list
        formatted list of days
        
    """
    #get current weekday
    weekday_today = datetime.date.today().weekday()
    
    #create a list of required days by counting the days from today + desired days
    required_days_num = list(range(weekday_today+1, weekday_today+1+slot_vals[0]))
    required_days_num = check_days(required_days_num)
    
    return required_days_num
    
def get_required_days(slots):
    """ Handle correct extraction of weekdays from all slot values
    
    Parameters
    ----------
    slots : < intent_message.slots as in Snips >
        slot values of the intent message
   
    Returns
    -------
    required_days : list
        formatted list of days
        
    """
    
    slots_time_spec = []
    slots_time_nr = []
    slots_time_span_signal = []
    
    #store slot values in a list    
    if slots.time_spec.all() is not None:
        for item in slots.time_spec.all():
            slots_time_spec.append(item.value)
            
    if slots.number_days.all() is not None:
        for item in slots.number_days.all():
            slots_time_nr.append(int(item.value))
    
    if slots.time_span_signal.all() is not None:
        for item in slots.time_span_signal.all():
            slots_time_span_signal.append(item.value)
                
    if len(slots.number_days) != 0:
        #user defined for how many days mobile mode is needed,
        #e.g. 'Für die nächsten 2 Tage'
        required_days = get_required_days_by_num(slots_time_nr)
        return required_days
    
    elif len(slots.time_spec) != 0:
        #user gave weekdays or time_spec values, e.g. 'Für Montag und Dienstag'
        #time span
        required_days = get_required_days_by_timespec(slots_time_spec, slots_time_span_signal)
        return required_days
