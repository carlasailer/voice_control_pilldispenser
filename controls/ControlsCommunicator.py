#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" ControlsCommunicator

This script handles all functionality concerning receiving and sending 
information to and from the controls unit of the tablet dispenser. 

It contains the class ControlsCommunicator with the following methods:
	* start_confirmation - start the alarm confirmation process
	* receive_stop_mobilemode - handle the end of mobile mode
	
It contains the following functions:
	* get_history - compare alarms and extractions and return to the intent callback
	* make_contact - extract phone number for person from database and start call
	* get_alarm_info - format alarms for user from control unit 
	* get_stock_info - format stock info for user
	* start_mobilemode - informs the control unit which days where chosen for mobile mode
	* get_alarm_confirmed_by_voice - access runtime_variables.json to see if alarm has been confirmed
	* set_alarm_confirmed_by_voice - save state of alarm confirmation to runtime_variables.json
	* get_confirmation_started_by_voice - access runtime_variables.json to see if alarm confirmation already started
	* set_confirmation_started_by_voice - save state of alarm confirmation started to runtime_variables.json
	* get_current_user_ID - access runtime_variables.json to retrieve current user ID
	* set_current_user_ID - save current user ID to runtime_variables.json
	
"""

import sys
sys.path.insert(0, '/home/pi/Dev/std_project/tantumDev/tantum_dev_unist/TablettIAS_HardwareControl/')
sys.path.insert(0, '/var/lib/snips/skills/snips_app_pilldispenser/')

import collections
import datetime
import json

#imports from voice control unit
from logs.LoggingManager import start_logging, log_event
from utils.random_answer import get_random_answer
from utils import resolve_alarm_spec

#imports from the control unit
from ConnectionDatabase import ConnectionDatabase

#create global variables
USER_ID = None
ALARM_CONFIRMED = False
MAGAZINELIST = None

#conversion for weekdays
dic_weekdays = {0:'Montag', 1:'Dienstag', 2:'Mittwoch', \
                3:'Donnerstag', 4:'Freitag', 5:'Samstag', \
                6:'Sonntag', 7: 'Reserve'}

#locations of the magazine
ERROR = 0
AT_STATIONARY = 1
AT_MOBILE = 2

#filename where runtime vars are saved
FILENAME_RUNTIME = '/var/lib/snips/skills/snips_app_pilldispenser/controls/runtime_variables.json'

###dummy data
#MAGAZINE_LIST = {}
#MAGAZINE_LIST[0] = {'Day': 'Mon', 'Magazine': 1, 'No': 0, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
#MAGAZINE_LIST[1] = {'Day': 'Tue', 'Magazine': 2, 'No': 1, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 1, 'empty': 1, 'AlreadyDetected': 'no'}
#MAGAZINE_LIST[2] = {'Day': 'Wed', 'Magazine': 2, 'No': 2, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 1, 'ni': 1, 'empty': 1, 'AlreadyDetected': 'no'}
#MAGAZINE_LIST[3] = {'Day': 'Thu', 'Magazine': 1, 'No': 3, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
#MAGAZINE_LIST[4] = {'Day': 'Fri', 'Magazine': 1, 'No': 4, 'h': 0, 'm': 0, 'sT': 0, 'mo': 1, 'mi': 1, 'a': 1, 'ni': 1, 'empty': 0, 'AlreadyDetected': 'no'}
#MAGAZINE_LIST[5] = {'Day': 'Sat', 'Magazine': 1, 'No': 5, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
#MAGAZINE_LIST[6] = {'Day': 'Sun', 'Magazine': 1, 'No': 6, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
#MAGAZINE_LIST[7] = {'Day': 'Res', 'Magazine': 1, 'No': 7, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}

#ALARMS = 		(	(1, 'sTD', 0, 1, 2, '2019-09-08 09:12:00', '2019-09-08 12:00:00', None, None),
					#(2, 'sTD', 0, 1, 2, '2019-09-16 10:25:00', '2019-09-16 12:00:00', None, None),		
					#(3, 'sTD', 0, 0, 2, None, '2019-09-18 13:00:00', None, None)
					#)
					
#EXTRACTIONS =  	(	(47, 2, '2019-09-08 09:12:00', None, None, None, 'sTD'),
					#(48, 2, None, '2019-09-14 13:00:00', None, None, 'sTD')
					#)
					
#DOCTOR = 	( (1, 'Helmut', 'Schneider', '07122 23223', 'doctor1@gmx.de'),
			  #(2, 'Chrissi', 'Weitmann', '07123 12312', 'doctor2@gmx.de')
			#)
			
#EMERGENCY_CONTACT = ( (1, 2, 'Claudia', 'Sailer', '07123 1', 'claudia@gmx.de'),
					  #(2, 2, 'Helena', 'Sailer', '07123 2', 'helena@gmx.de'),
					  #(3, 2, 'Franca', 'Sailer', '07123 3', 'franca@gmx.de')
					 #)

class ControlsCommunicator:
	""" Class to handle functionality concerning communication with 
	controls unit modules
	
	Attributes
	----------
	parent : VoiceControl
		instance of VoiceControl by which it was called
	user_ID : int
		user_ID in database for which VoiceControl was called
	
	Methods 
	-------
	start_confirmation()
		Start the alarm confirmation process
	receive_stop_mobilemode(MagazineList)
		Handle the end of mobile mode
		
	"""
	def __init__(self, parent=None, user_ID=None):
		self.parent = parent

		#save user that started voice control for calls to database
		self.user_ID = user_ID
		#set_current_user_ID(user_ID)

		start_logging()
		
	def start_confirmation(self):
		""" Handles the start of the alarm confirmation process via 
		VoiceControl by starting with a TTS message
		
		Returns
		-------
		confirmation_started : bool
			True if voice_control is active and TTS message was sent
		"""
		
		confirmation_started = False
		
		if self.parent.is_active:
			
			# only start speech synthesis if voice control is active
			log_event('Starting confirmation... ')
			INTENT_FILTER_CONFIRMTAKING = ["carlasailer:confirmTaking", "carlasailer:quitDialog"]
			self.parent.send_message_to_TTS(message=get_random_answer(intent_name='confirmTaking', key_name='start'))#,  
											#intent_filter=INTENT_FILTER_CONFIRMTAKING)
			confirmation_started = True
		
		#TODO: delete next line
		confirmation_started = True
		
		return confirmation_started
		
	def receive_stop_mobilemode(self, MagazineList):
		""" Informs the user about the end of mobilemode, gets called with 
		MagazineList from the Controls and depending on the state of it, 
		sends message to TTS
		
		Parameters
		----------
		MagazineList : dict
			input data of type MagazineList as used by the Controls unit of the stationary dispenser
			'Magazine': 0 if error, 1 if at stationary, 2 if at mobile dispenser	
			e.g. 	MAGAZINE_LIST = {}
			MAGAZINE_LIST[0] = {'Day': 'Mon', 'Magazine': 1, 'No': 0, 'h': 0, 'm': 0, 'sT': 0, 
								'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
								
		"""
		
		#if voice control is active: 
		if self.parent.is_active:
                        
			#extract the missing magazines from MagazineList: 
			missing_days = [nr for nr in range(0, len(MagazineList)) if MagazineList[nr]['Magazine'] == AT_MOBILE]
		
			if len(missing_days) != 0:
				#if magazines are missing, tell the user to put them back in
				print('Missing Magazines: ', missing_days)
				log_event('[end mobileMode]		Missing magazines: {}'.format(missing_days))
				
				#convert numbers to weekdays and format for output message 
				missing_days_str = ''
				if missing_days is not None:
					for key in missing_days:
						missing_days_str += dic_weekdays.get(key) + ', '
			
				self.parent.send_message_to_TTS('Mobilmodus noch nicht beendet. Bitte folgende Magazine einstecken: {}.'.format(missing_days_str))
		
			else:
				#if no magazines are missing, mobilemode can be stopped
				self.parent.send_message_to_TTS('Mobilmodus wurde beendet.')
				log_event('[end mobileMode]  	No missing magazines. Switch to stationary mode.')
				
def get_history():
	""" Compares alarms to extractions (from database)
	to create information about adherence
	
	
	Returns
	-------
	count_non_corrects : int
		number of non correctly taken medications
	history : list
		information about non correctly taken medications 
		
	"""
		
	#contact the controls to get the info about previous medication withdrawals
	DB = ConnectionDatabase() 
	ExtrData = DB.load_extraction(userID=get_current_user_ID())
	AlarmData = DB.load_alarmdata(userID=get_current_user_ID())
        
	#only take the time stamps 
	alarms = [al[5:] for al in AlarmData]
	extractions = [extr[2:6] for extr in ExtrData]

	history  = []
	state = ''
	#count not correctly taken medications - either forgotten or additional medications
	count_non_corrects = 0

	#iterate over days
	for counter in range(0, len(extractions)):
		daily_history = []
		
		#iterate over the four possible times of the day
		for time_of_day in range(0,4):
			current_alarm = alarms[counter][time_of_day]
			current_extraction = extractions[counter][time_of_day]
			
			#compare alarm and extraction
			if current_extraction is not None and current_alarm is None:
				#entnommen, obwohl kein Alarm
				state = 'Fehler - extra Entnahme'
				count_non_corrects += 1 
			elif current_alarm is not None and current_extraction is None:
				#nicht genommen, obwohl Alarm
				state = 'Fehler - vergessen'
				count_non_corrects += 1 
			elif current_alarm is not None and current_extraction is not None:
				#korrekte Entnahme
				state = 'korrekt - korrekte Entnahme'
			else:
				#keine Entname, kein Alarm
				state = 'korrekt - keine Entnahme erwartet'
				
			#get date of the extraction
			if current_extraction is not None:
				current_date = datetime.datetime.strftime(current_extraction, '%Y-%m-%d %H:%M:%S')
			else:
				current_date = None
			
			daily_history.append([current_date, state])
			
		history.append(daily_history)
	
	return count_non_corrects, history
		
def make_contact(person=None, person_type=None):
	""" Get the required phone number for the person from the database 
	and start the call (really starting the call not implemented, 
	just print a line to cmd)
	
	Parameters
	----------
	person : string
		name of the person to be contacted
	person_type : string
		'medical_staff' or 'emergency_contact'
	
	Returns
	-------
	success : bool
		True if corresponding person was found in database
	doc_names : list
		list of names of doctors found in the database returned to intent callback function		
	
	"""
	
	#contact the control unit to get saved contacts and doctors
	DB = ConnectionDatabase() 
	DoctorData = DB.load_doctors(userID=get_current_user_ID())
	ContactData = DB.load_emergency_contacts(userID=get_current_user_ID())
	
	success = False
	doc_names = None
	
	if person_type == 'medical_staff':
		
		if len(person) == 1:
			pass
		try: 
			#find the doctor's telephone number in the database
			dr = person.split(' ')[1].capitalize()
			call_nr = [DoctorData[idx][3] for idx in range(0, len(DoctorData)) if dr in DoctorData[idx]]
			if len(call_nr) != 0:
				print('Calling: ', call_nr[0])
				success = True
				
		except IndexError:
			#make a suggestion about calling a doctor from the database
			doc_names = [('Doktor ' + DoctorData[idx][2]) for idx in range(0, len(DoctorData))]
			print('Possible Doctors: ', doc_names)
			#success not set to True!
			
	elif person_type == 'emergency_contact':
		contact = person.capitalize()
		#find nr of emergency contact in database
		call_nr = [ContactData[idx][4] for idx in range(0, len(ContactData)) if contact in ContactData[idx]]
		if len(call_nr) == 1:
			print('Calling: ', call_nr[0])
			success = True
		
	else:
		pass
	
	return success, doc_names 

def get_alarm_info(days=None):
	""" Retrieve alarms from database and format for a specific day,
	if no day is specified get the next alarm 
	
	Parameters 
	----------
	days : list 
		weekdays, in integer format (0: Monday 1: Tuesday etc)
	
	Returns 
	-------
	alarms : list
		alarms for given weekday(s)
	
	alarm_day : int
		weekday in integer format as above
	
	alarm_time: string
		time of the next alarm, '%H:%M'
		
	"""
	#contact the control unit to get info about desired withdrawals 
	DB = ConnectionDatabase() 
	AlarmData = DB.load_alarmdata(userID=get_current_user_ID())
	
	#only take the time stamps 
	alarms = [al[5:] for al in AlarmData]
	next_alarms = []
	for entry in alarms:
		#get valid alarms as datetime objects
		next_alarms.append([time_of_day for time_of_day in entry if time_of_day is not None])

	if days is None:
		#get next alarm
		[alarm_day, alarm_time] = resolve_alarm_spec.get_alarm_for_next_day(alarm_data=next_alarms)
		return alarm_day, alarm_time 
		
	else:
		alarms = resolve_alarm_spec.get_alarm_for_weekday(alarm_data=next_alarms, weekday=days)
		return alarms

def get_stock_info():
	""" Calculate the information about magazine filling state in percent, 
	(0, 25% , 50% , 75% or 100% empty) for each magazine
	
	Returns
	-------
	stock_state : dict
		filling rate for each magazine 
		
	"""
	global MAGAZINELIST
	MagazineList = MAGAZINELIST

	time_of_day = ['mo', 'no', 'ev', 'ni']
	stock_state = {}	
	
	#iterate over dictionary entries and count if one of the time_of_day keys is 1 (means compartment is empty!)
	for magazine in range(0, len(MagazineList)):
	
		#save stock state in percent for the correct magazine
		stock_state[magazine] = int(float(sum([MagazineList[magazine][idx] for idx in time_of_day]))/float(len(time_of_day))*100)
	
	return stock_state

def get_alarm_confirmed_by_voice():
	""" Get the status whether the alarm has been confirmed by voice 
	
	Returns
	----------
	alarm_confirmed : boolean
		True if alarm has been confirmed, False otherwise
	
	"""
	
	with open(FILENAME_RUNTIME, 'r') as f:
		runtime_data = json.load(f)
		alarm_confirmed = runtime_data['alarm_conf']
	
	return alarm_confirmed

def set_alarm_confirmed_by_voice(state):
	""" Save alarm_confirmed state to the controlscommunicator, 
	can be retrieved by controls unit
	
	Parameters
	----------
	state : boolean
		True if alarm has been confirmed, False otherwise
	
	"""
	
	with open(FILENAME_RUNTIME, 'r') as f:
		global runtime_data
		runtime_data = json.load(f)
		
	with open(FILENAME_RUNTIME, 'w') as f:
		runtime_data['alarm_conf'] = state
		json.dump(runtime_data, f)

def get_confirmation_started_by_voice():
	""" Get the status whether the alarm has been confirmed by voice 
	
	Returns
	----------
	confirm_state : boolean
		True if alarm has been confirmed, False otherwise
	
	"""
	with open(FILENAME_RUNTIME, 'r') as f:
		runtime_data = json.load(f)
		confirm_state = runtime_data['conf_started']

	return confirm_state

def set_confirmation_started_by_voice(state):
	""" Save alarm_confirmed state to the controlscommunicator, 
	can be retrieved by controls unit
	
	Parameters
	----------
	state : boolean
		True if alarm has been confirmed, False otherwise
	
	"""
	
	with open(FILENAME_RUNTIME, 'r') as f:
		global runtime_data
		runtime_data = json.load(f)
		
	with open(FILENAME_RUNTIME, 'w') as f:
		runtime_data['conf_started'] = state
		json.dump(runtime_data, f)
		
def set_current_user_ID(user_ID):
	""" save user_ID to runtime_variables.json during runtime
	
	Parameters
	----------
	user_ID : int
		ID in the database for the user that is logged in
			
	"""
	
	#save the user_ID to file 
	with open(FILENAME_RUNTIME, 'r') as f:
		runtime_data = json.load(f)
		
	with open(FILENAME_RUNTIME, 'w') as f:
		runtime_data['user_ID'] = user_ID[0]
		json.dump(runtime_data, f)
	
def get_current_user_ID():
	""" Get the status whether the alarm has been confirmed by voice 
	
	Returns
	----------
	user_ID : int
		ID in the database for the user that is logged in
	
	"""
	
	with open(FILENAME_RUNTIME, 'r') as f:
		runtime_data = json.load(f)
		user_ID = runtime_data['user_ID']

	return int(user_ID)
	
	
if __name__ == '__main__':
	print(get_alarm_confirmed_by_voice())
	pass
