#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" resolve_contact_info
This script formats the intent message to extract information about 
the person to make contact with.

It contains the following functions:
	* get_person - extract the person from the slot values
	
"""

def get_person(intent_message=None):
    """ Extracts the person from the slot values of the intent message
    
    Parameters
    ----------
    intent_message : <intent_message by Snips>     
        message created when intent was received
        
    Returns
    -------
    person : string
        name of the person or doctor
    person_type : string
        'medical_staff' or 'emergency_contact'
    state : bool
        True if person could be extracted
        
    """ 
    
    state = 'success'  
    print(intent_message.input)
    
    #extract medical staff 
    if intent_message.slots.medical_staff.all() is not None:
        person_type = 'medical_staff'
        
        #raw value of slot:     intent_message.slots.medical_staff[0].raw_value
        #matched value of slot: intent_message.slots.medical_staff.first().value

        raw_val = intent_message.slots.medical_staff[0].raw_value
        current_doctor = intent_message.input.split(' ')

        if raw_val in current_doctor:
            idx = current_doctor.index(raw_val)
            person = ' '.join(current_doctor[idx:idx+2])
     
        else:
            person = str(intent_message.slots.medical_staff.first().value)
        
        
    #extract saved contacts
    elif intent_message.slots.saved_contact.all() is not None:
        person_type = 'emergency_contact'
                
        #raw value of slot:     intent_message.slots.saved_contact[0].raw_value
        #matched value of slot: intent_message.slots.saved_contact.first().value

        person = str(intent_message.slots.saved_contact.first().value)
      
        
    else:
        person_type = None
        person = None 
        state = 'fail'
        
    return person, person_type, state 

