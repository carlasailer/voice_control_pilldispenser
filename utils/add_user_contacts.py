#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-
import json
import subprocess

#imports from the control unit
from ConnectionDatabase import ConnectionDatabase

""" add_user_contacts

This scripts supports adding of names of user contacts to the vocabulary of Snips
	
It contains the following functions:
	* perform_injection - add the values to the vocabulary
	* add_doctors - get names of doctors from database and format
	* add_emergency_contacts - get names of contact persons and format
	
"""

DOCTOR = 	( (1, 'Helmut', 'Schneider', '07122 23223', 'doctor1@gmx.de'),
			  (2, 'Chrissi', 'Weitmann', '07123 12312', 'doctor2@gmx.de')
			)
			
EMERGENCY_CONTACT = ( (1, 2, 'Claudia', 'Sailer', '07123 1', 'claudia@gmx.de'),
					  (2, 2, 'Helena', 'Sailer', '07123 2', 'helena@gmx.de'),
					  (3, 2, 'Miri', 'Schäfer', '07123 3', 'nada@gmx.de')
					)
					
def perform_injection(values):
	""" Adds the values specified to the vocabulary of Snips ASR and NLU
	
	Parameters
	----------
	values : dict
		values to be added, in the format required by Snips Entities Injection Feature
	
	"""
	
	filename = '/var/lib/snips/skills/snips_app_pilldispenser/utils/new_values.json'
	
	#save values to a file
	with open(filename, 'w') as f:
		json.dump(values, f)
		
	command = ['mosquitto_pub', '-t', 'hermes/injection/perform', '-f', '/var/lib/snips/skills/snips_app_pilldispenser/utils/new_values.json']
	subprocess.Popen(command)
	
def add_doctors(user_ID=None):
	""" Get doctors names from database, format and start injection 
	
	Parameters
	----------
	user_ID : int
		user_ID in database for which VoiceControl was called
	
	"""
	
	#contact the control unit to get saved contacts and doctors
	DB = ConnectionDatabase() 
	DoctorData = DB.load_doctors(user_ID)
	
	#format the doctors names 	
	doctors = [DoctorData[idx][2] for idx in range(0, len(DoctorData))]
	
	#format expected for the entities injection feature of the snips platform
	values_to_add = { "operations": [[ "add", {"medical_staff": doctors } ] ] }
	
	#add the values to Snips vocabulary
	perform_injection(values_to_add)	

def add_emergency_contacts(user_ID=None):
	""" Get emergency contacts from database, format and start injection 
	
	Parameters
	----------
	user_ID : int
		user_ID in database for which VoiceControl was called
	
	"""
	
	#load emergency contacts from database and format them 
	DB = ConnectionDatabase() 
	ContactData = DB.load_emergency_contacts(user_ID)
	contacts = [ContactData[idx][2] for idx in range(0, len(ContactData))]
	
	#format expected for the entities injection feature of the snips platform
	values_to_add = { "operations": [[ "add", {"saved_contact": contacts } ] ] }
	
	#add the values to Snips vocabulary
	perform_injection(values_to_add)	

if __name__ == '__main__':
	add_doctors(user_ID=16)
	add_emergency_contacts(user_ID=16)
