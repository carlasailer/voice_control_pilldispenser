#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" SettingsManager

This scripts handles all interactions concerning settings of the Snips Voice platform. 

It contains the class SettingsManager with the following methods:
	* activate_voice_control - activate Snips components
	* deactivate_voice_control - deactivate Snips components
	* change_TTS_engine - change the TTS engine used by Snips
	* enable_dual_TTS - allow dual TTS (one for online, one for offline)
	* disable_dual_TTS - do not allow dual TTS
	* setup_audio - choose correct input and output devices for Snips
	
It contains the following functions:
	* change_volume - terminal command to change the volume of the speakers of the RPi
	
"""

import os
import subprocess
import requests

class SettingsManager:
	""" Class to handle changes in settings of Snips Voice Platform and 
	the RaspberryPi 
	
	Attributes
	----------
	parent : VoiceControl
		instance of VoiceControl by which it was called
	isActiveDualTTS : bool
		True if dual TTS is enabled
		
	Methods 
	-------
	activate_voice_control() 
		Activate Snips components
	deactivate_voice_control()
		Deactivate Snips components
	change_TTS_engine()
		Change the TTS engine used by Snips
	enable_dual_TTS()
		Allow dual TTS (one for online, one for offline)
	disable_dual_TTS()
		Do not allow dual TTS
	setup_audio()
		Choose correct input and output devices for Snips
		
	"""
	def __init__(self, parent=None):
		self.parent = parent
		self.isActiveDualTTS = False
		self.setup_audio()
	
	def activate_voice_control(self):
		""" Calls a bash script to manually restart all snips components,
		activate the voice control and the detection of hotword
		
		"""
		
		path_to_file = '/var/lib/snips/skills/snips_app_pilldispenser/settings/restart_snips.sh'
		subprocess.call([path_to_file])
		print('Voice control restarted.')

		#set is_active of voice control instance to true and tell the user
		self.parent.is_active = True
		self.parent.send_message_to_TTS("Die Sprachsteuerung ist aktiv.")
		
	def deactivate_voice_control(self):
		""" Makes a command line command to stop all snips components,
		deactivate the voice control and the detection of hotword
		
		"""
		
		command = ['sudo', 'systemctl', 'stop', 'snips-*']
		subprocess.Popen(command)
		print('Voice control stopped.')
		
		#set is_active of voice control instance to false and tell the user
		self.parent.is_active = False
		self.parent.send_message_to_TTS("Die Sprachsteuerung ist nicht mehr aktiv.")
		
	def change_TTS_engine(self):
		""" Calls a bash script to change the used Snips TTS engine
		if this option is enabled
		
		"""
		
		if self.isActiveDualTTS:
			#dual TTS
			path_to_file = '/var/lib/snips/skills/snips_app_pilldispenser/settings/dual_TTS.sh'
			subprocess.call([path_to_file])
			print('Dual TTS is enabled. Using Amazon Polly TTS in case of internet connection, else use offline Picotts TTS.')
			
		else:
			#go back to single offline Picotts TTS
			path_to_file = '/var/lib/snips/skills/snips_app_pilldispenser/settings/single_TTS.sh'
			subprocess.call([path_to_file])
			print('Dual TTS is disabled. Using offline Picotts TTS regardless of internect connection.')
			
	def enable_dual_TTS(self):
		""" Activates the option of dual TTS depending on internet connection 
		"""
		
		self.isActiveDualTTS = True
		self.change_TTS_engine()
		
	def disable_dual_TTS(self):
		""" Deactivates the option of dual TTS depending on internet connection 
		"""
		
		self.isActiveDualTTS = False
		self.change_TTS_engine()
		
	def setup_audio(self):
		""" Calls a bash script that sets the correct audio devices 
		(USB sound card)
		
		"""
		
		path_to_file = '/var/lib/snips/skills/snips_app_pilldispenser/settings/setup_audio.sh'
		subprocess.call([path_to_file])

def change_volume(value):
	""" Change the output volume of the device via alsamixer
	
	Parameters 
	----------
	value : int 
		value to which the alsamixer volume should be set
		
	"""
	
	print('received val:', value)
	
	command = ['amixer', '--card', '1', 'set', 'Speaker', value]	
	subprocess.Popen(command)
		
		
if __name__ == '__main__':
	#pass
	testSettingsManager = SettingsManager()	
	
	testSettingsManager.enable_dual_TTS()
	
	#volume_value = '50%'
	#change_volume(volume_value)
	
