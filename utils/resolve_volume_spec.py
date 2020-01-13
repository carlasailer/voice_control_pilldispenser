#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-

""" resolve_volume_spec
This script handles formatting the slot values of the intent message to 
extract information about the volume to set the output volume of the RPi alsamixer. 

It contains the following functions:
	* check_valid_volume - volume has to be between 0 and 100
    * get_required_volume - extract days from slot values 
    	
"""

def check_valid_volume(value):
    """ Check if the value is between 0 and 100 as required for a
    specification of volume level in %
    
    Parameters
    ----------
    value : string
        value as extracted from the slot values in the intent message
    
    Returns
    -------
    value : string
        original value if valid, else []
    
    """
    
    if int(value) in range(0,101):
        return value
    else:
        return [] 
        
def get_required_volume(slots):
    """ Handle correct extraction of volume for speaking louder or less loud
    from all slot values
    
    Parameters
    ----------
    slots : < intent_message.slots as in Snips >
        slot values of the intent message
   
    Returns
    -------
    required_volume : string
        extracted valid volume to be send to alsamixer
        
    """
    
    slots_volume_relative = []
    slots_volume_nr = []
    slots_volume_relative_signal = []
    
    #store slot values in a list    
    if slots.volume_relative_signal.all() is not None:
        for item in slots.volume_relative_signal.all():
            slots_volume_relative_signal.append(item.value)
            
    if slots.volume_relative.all() is not None:
        for item in slots.volume_relative.all():
            slots_volume_relative.append(item.value)
    
    if slots.volume_value.all() is not None:
        for item in slots.volume_value.all():
            slots_volume_nr.append(int(item.value))
    
    #find required volume specification
    if len(slots.volume_value) == 0:        
        #user did not give a volume value,
        #default is +-15%, e.g. 'Mach lauter'
        
        if 'lauter' in slots_volume_relative:
            #turn volume up by default value
            required_volume = '15%+'
            return required_volume
        
        elif 'leiser' in slots_volume_relative:
            #turn volume down by default value
            required_volume = '15%-'
            return required_volume
    
    elif len(slots.volume_relative_signal) == 0:
        #user defined a volume and it is absolute value, 
        #e.g. 'Stell die Lautstaerke auf 50%'
        required_volume = slots_volume_nr[0]
        required_volume = check_valid_volume(required_volume)
        return str(int(required_volume)) + '%'
    
    elif (len(slots.volume_relative_signal) != 0) & (len(slots.volume_value) != 0):
        #user defined a relative volume,
        #e.g. 'Sprich um 10 Prozent lauter'
        required_volume = check_valid_volume(slots_volume_nr[0])
        
        if 'lauter' in slots_volume_relative:
            #turn volume up by value
            required_volume = str(int(required_volume)) + '%+'
            print(required_volume)

            return required_volume
        
        elif 'leiser' in slots_volume_relative:
            #turn volume down by value
            required_volume = str(int(required_volume)) + '%-'
            print(required_volume)
            return required_volume
            
    else:
        #error occured
        return None
