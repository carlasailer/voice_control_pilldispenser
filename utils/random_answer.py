#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-

""" random_answer

This scripts is available for choosing randomly one of the available TTS answers.

It contains the following functions:
	* get_random_answer - choose answer from file
	
"""
import json
import random

filename = '/var/lib/snips/skills/snips_app_pilldispenser/utils/answers.txt'

def get_random_answer(intent_name=None, key_name=None):
	""" Open the file with possible TTS answers and choose a random answer for the desired intent
	
	Parameters
	----------
	intent_name : string
	 	name of the intent that needs the answer
	key_name : string
		key within intent if multiple keys available, check answers.txt for all keys
		
	Returns
	-------
	random_answer : string
		answer which will be returned to the intent callback function
	
	"""
	
	with open(filename, 'r') as json_file:
		data = json.load(json_file)
		answers = [data[key] for key in data.keys() if key == intent_name][0]
	
		if key_name is not None:
			possible_answers = answers[key_name]
			
		else: 
			possible_answers = answers[list(answers.keys())[0]]

	random_answer = possible_answers[random.randint(0, len(possible_answers)-1)]

	return random_answer
	
	
if __name__ == '__main__':
	#get_random_answer('contact', 'anrufen')
	rnd_answer = get_random_answer('contact')
	
	print(rnd_answer)	
