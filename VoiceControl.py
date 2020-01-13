#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" VoiceControl

This scripts is the main script of the VoiceControl for the TANTUM pill dispenser.

It contains the class VoiceControl with the following methods:
	* session_ended - handle the reason why Hermes session ended, e.g. intent_not_recognized
	* subscribe_actions - subscribe to intents 
	* send_message_to_TTS - send a message to the speech synthesis module of Snips
	* get_MQTT_address - get host and port of MQTT broker
	
"""

import sys, os
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
import subprocess

from settings import SettingsManager
from controls import ControlsCommunicator
from logs import LoggingManager
from utils.add_user_contacts import add_doctors, add_emergency_contacts

class VoiceControl:
	""" Main class of the VoiceControl for the TANTUM pill dispenser.
	
	Attributes
	----------
	is_active : bool
		True if VoiceControl is active
	mqtt_address : string
		host and port of MQTT broker 
	user_ID : int 
		user as required by controls unit
	settingsmanager : SettingsManager
		instance of settingsmanager to control the Snips platform
	controlscommunicator : ControlsCommunicator
		instance of controlscommunicator to interact with controls unit
	
	Methods
	-------
	session_ended(hermes, intent_message)
		Handle the reason why Hermes session ended, e.g. intent_not_recognized
	subscribe_actions()
		Subscribe to intents 
	send_message_to_TTS(message)
		Send a message to the speech synthesis module of Snips
	
	"""
	
	def __init__(self, user_ID=None):
		#voice control can be activated or deactivated
		self.is_active = True
		
		#create MQTT address 
		MQTT_IP_ADDR = "localhost"
		MQTT_PORT = 1883
		self.mqtt_address = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

		#save the user that started the voicecontrol
		self.user_ID = user_ID

		#start the logging process
		LoggingManager.start_logging()
		LoggingManager.log_event('Start logging of incoming events...')
				
		#start SettingsManager and ControlsCommunicator
		self.settingsmanager = SettingsManager.SettingsManager(parent=self)
		self.settingsmanager.activate_voice_control()
		
		self.controlscommunicator = ControlsCommunicator.ControlsCommunicator(parent=self, user_ID=self.user_ID)
 		
		#add contacts to vocabulary
		add_doctors(self.user_ID)
		add_emergency_contacts(self.user_ID)
		
		#subscribe to master intent and intent not recognized
		#self.subscribe_actions()
		
		#reset alarm confirmation settings
		ControlsCommunicator.set_confirmation_started_by_voice(False)
		ControlsCommunicator.set_alarm_confirmed_by_voice(False)
		
	def master_intent_callback(self, hermes, intent_message):
		""" Callback that is called everytime an intent is detected
			
		Parameters
		----------
		hermes : <Hermes instance>
			current instance of the hermes broker 
		intent_message : <intent_message by Snips>     
			message created when intent was received

		"""
		pass
		
	def session_ended(self, hermes, intent_message):
		""" Callback function to handle reasons why a session has ended, 
		handle intent not recognized
		
		Parameters
		----------
		hermes : <Hermes instance>
			current instance of the hermes broker 
		intent_message : <intent_message by Snips>     
			message created when intent was received

		"""
		
		TERMINATION_REASONS = {	'TIMEOUT': 	0,
						'NOMINAL': 	1,
						'ERROR':	2,
						'ABORTED_BY_USER': 			3,
						'INTENT_NOT_RECOGNIZED': 	4,
						'COMPONENT_NOT_RESPONDING': 5
					   }

		reason = intent_message.termination.termination_type 
		if reason == TERMINATION_REASONS['INTENT_NOT_RECOGNIZED']:
			message_to_tts = 'Ich habe dich nicht verstanden. Bitte wiederhole die Spracheingabe.'
			self.send_message_to_TTS(message_to_tts)

		#elif reason == TERMINATION_REASONS['TIMEOUT']:
			#message_to_tts = 'Die Zeit ist abgelaufen.'
			
		#elif reason == TERMINATION_REASONS['ERROR']:
			#message_to_tts = 'Ein Fehler ist aufgetreten.'
			
		#elif reason == TERMINATION_REASONS['ABORTED_BY_USER'] or \
			 #reason == TERMINATION_REASONS['COMPONENT_NOT_RESPONDING']:  
			#message_to_tts = 'Wolltest du was sagen?'
			
		else:
			pass 
		
		
	def subscribe_actions(self):
		""" subscribe to the intent_not_recognized and session_ended intents """ 
		
		with Hermes(self.mqtt_address) as h:
			#handle SessionEndedMessages to look for unrecognized intents
			h.subscribe_session_ended(self.session_ended)
			#define what happens if any intent is recognized (master callback)
			h.subscribe_intents(self.master_intent_callback).start()
	
	def send_message_to_TTS(self, message):
		""" send the message to the speech synthesis module of Snips
		
		Parameters
		----------
		message : string
			message which will be output to the user
		
		"""

		#only allow tts output if voice control is active
		if self.is_active:
			with Hermes(self.mqtt_address) as h:
				#log the message to the output.log file and start the session
				LoggingManager.log_tts_output(message)
				h.publish_start_session_notification(None, message, None)
					

if __name__ == '__main__':
	pass
	#current_voice_control = VoiceControl(user_ID=16)
	#test the dual TTS
	#print('Enabling Dual TTS')
	#current_voice_control.settingsmanager.enable_dual_TTS()
	#voice = 'Marlene'
	#gender = 'FEMALE'
	#command = ['/var/lib/snips/skills/snips_app_pilldispenser/settings/amazon_tts.sh', '/var/lib/snips/skills/snips_app_pilldispenser/settings/1', 'amazon', 'de', 'DE', voice, gender, 'Der nächste Alarm ist um 15.00 Uhr.', '24000']	
	#subprocess.Popen(command)
	
	#current_voice_control.send_message_to_TTS("Der nächste Alarm ist am Montag um 15.00 Uhr.")

	
