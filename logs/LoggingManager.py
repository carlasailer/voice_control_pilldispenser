 #!/usr/bin/env python3
# -*- encoding: utf-8 -*-

""" Logging Manager 

This script contains all relevant functions for logging events of the 
VoiceControl using the logging library in standard python. 

It contains the following functions:
	* start_logging - format and file settings for the logging process
	* check_max_entries - checks if a given maximum of entries is exceeded
	* log_received_intent - saves the name of the intent to a file (+ timestamp)
	* log_event - log other info to a file  
	* log_asr_input - log the transcribed user speech input to file
	* log_tts_output - log created speech synthesis message to file
	* main - use for testing the script
"""

import logging
import os

#names of the loggers
logger_intents = logging.getLogger('intents')
logger_input = logging.getLogger('input')
logger_output = logging.getLogger('output')

#filenames of log files 
FILENAME_INTENTS 	= '/var/lib/snips/skills/snips_app_pilldispenser/logs/intents.log'
FILENAME_INPUT 		= '/var/lib/snips/skills/snips_app_pilldispenser/logs/input.log'
FILENAME_OUTPUT 	= '/var/lib/snips/skills/snips_app_pilldispenser/logs/output.log'

#maximum allowed entries per log file
MAX_ENTRIES = 80
	
def start_logging():
	""" Setup of logging incl specification of file location and name, 
	and logging format
	
	"""
	
	#setup for intents logger
	logger_intents.setLevel(logging.INFO)	
	fileHandler_intents = logging.FileHandler(FILENAME_INTENTS)
	formatter_intents = logging.Formatter('%(asctime)s %(message)s ', '%Y-%m-%d %H:%M:%S')
	fileHandler_intents.setFormatter(formatter_intents)
	logger_intents.addHandler(fileHandler_intents)
	
	#setup for input logger (coming from Speech Recognition - ASR)
	logger_input.setLevel(logging.INFO)
	fileHandler_input = logging.FileHandler(FILENAME_INPUT)
	formatter_input = logging.Formatter('%(asctime)s %(message)s ', '%Y-%m-%d %H:%M:%S')
	fileHandler_input.setFormatter(formatter_input)
	logger_input.addHandler(fileHandler_input)
	
	#setup for output logger (coming from Speech Synthesis - TTS)
	logger_output.setLevel(logging.INFO)
	fileHandler_output = logging.FileHandler(FILENAME_OUTPUT)
	formatter_output = logging.Formatter('%(asctime)s %(message)s ', '%Y-%m-%d %H:%M:%S')
	fileHandler_output.setFormatter(formatter_output)
	logger_output.addHandler(fileHandler_output)
			
def check_max_entries(filename=None):
	""" removes first entries in a file if maximum number of log entries is exceeded
	
	Parameters
	----------
	filename : String
		location of the file to be checked
	
	"""
	
	#open the file and read the lines
	lines = []
	lines_new = []
	with open(filename, 'r') as f:
		lines = [line for line in f]
		previous = len(lines)
		
		#check if maximum is exceeded and get only last max_entries lines
		if previous > MAX_ENTRIES:
			diff = previous - MAX_ENTRIES
			lines_new = lines[diff:]
		else:
			lines_new = lines
	
	#write lines back to file 
	if lines_new is not None:
		with open(filename, 'w') as f:
			f.writelines(lines_new)	
			
def log_received_intent(intent_message='No intent transmitted.'):
	""" logs the name of the received intent to the log file
	
	Parameters
	----------
	intent_message: <intent_message by Snips>     
        message created when intent was received
	
	"""
	
	#check if log file is full
	check_max_entries(FILENAME_INTENTS)
	
	#log intent
	intent_name = intent_message.intent.intent_name.split(':')
	log_msg = '[Received] intent: {}'.format(intent_name[1])
	logger_intents.info(log_msg.encode("utf-8"))
    
def log_event(msg='No message received.'):
	""" logs a message other than intent name to the log file
	
	Parameters
	----------
	msg: String 
		message to be logged
		
	"""
	
	#check if log file is full
	check_max_entries(FILENAME_INTENTS)
	
	#log event
	logger_intents.info(msg.encode("utf-8"))

def log_asr_input(msg='Error'):
	""" logs captured ASR text to specified log file
	
	Parameters
	----------
	msg: String 
		message to be logged
		
	"""
	
	#check if log file is full
	check_max_entries(FILENAME_INPUT)
	
	#log input
	logger_input.info(msg.encode("utf-8"))

def log_tts_output(msg='Error'):
	""" logs produced TTS output to specified log file
	
	Parameters
	----------
	msg: String 
		message to be logged
		
	"""
	#log output
	logger_output.info(msg.encode("utf-8"))
	
	#check if log file is full
	check_max_entries(FILENAME_OUTPUT)
	
if __name__ == '__main__':
	start_logging()
	log_tts_output('What an amazing day!')
