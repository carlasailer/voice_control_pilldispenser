#!/usr/bin/env python3
# -*- encoding: iso-8859-15 -*-

""" resolve_alarm_spec
This script enables formatting of alarms as received from the database.

It contains the following functions:
	* get_alarm_for_weekday - format alarm for a specific weekday
	* get_alarm_for_next_day - format alarm for the following day
	
"""

import datetime

#conversion for weekdays
dic_weekdays = {0:'Montag', 1:'Dienstag', 2:'Mittwoch', \
                3:'Donnerstag', 4:'Freitag', 5:'Samstag', \
                6:'Sonntag'}
                
ALARMS = 		(	(1, 'sTD', 0, 1, 2, '2019-09-07 09:12:00', '2019-09-07 12:00:00', None, None),
					(2, 'sTD', 0, 1, 2, '2019-09-08 10:25:00', '2019-09-08 12:00:00', None, None),		
					(3, 'sTD', 0, 0, 2, None, '2019-09-09 13:00:00', None, None)
					)
                
def get_alarm_for_weekday(alarm_data, weekday):
	""" Format the alarm for a specific weekday
	
	Parameters
	----------
	alarm_data : tuple
		format same as in database of controls unit
	weekday : list
		day specified as integer (0: Monday, 1: Tuesday etc)
	
	Returns
	-------
	alarm_spec : dict
		alarms sorted by weekday
		
	"""
	print('Alarm Data: ', alarm_data)
	
	weekday = weekday[0]
	alarms = []
	
	#create a dictionary sorting the alarms by their weekday 
	alarms_by_days = {}
	for idx in range(0,7):
		alarms_by_days[idx] = []
		
	#flatten alarm_data
	alarm_data = [subelem for elem in alarm_data for subelem in elem]
	#fill the dictionary
	for item in alarm_data: 
		alarms_by_days[item.weekday()].append(item)
	print(alarms_by_days)
	
	#compare the required weekday and get alarms for it 
	if weekday in alarms_by_days.keys():
		alarms = alarms_by_days[weekday]
	else:
		alarms = None
	
	#extract time and day of alarm 
	alarm_spec = [[dic_weekdays[al.weekday()],datetime.time.strftime(al.time(), '%H:%M')]  for al in alarms]

	return alarm_spec
	
def get_alarm_for_next_day(alarm_data):
	""" Format the alarm for the following day
	
	Parameters
	----------
	alarm_data : tuple
		format same as in database of controls unit
	
	Returns
	-------
	alarm_day : string 
		day of the alarm as a string ('Montag', 'Dienstag', 'Mittwoch, ...)
	alarm_time : string
		'%H:%M' of alarm
		
	"""
		
	#compare the alarm to the current time and date and if still valid, save to next_alarms
	date_today = datetime.datetime.now()	
	next_alarms = [entry[0] for entry in alarm_data if len(entry) > 0 if date_today < entry[0]]
	
	#get the weekday of next alarm in German from the datetime object
	if next_alarms is not None:
		alarm_day = dic_weekdays[next_alarms[0].weekday()]
		alarm_time = datetime.time.strftime(next_alarms[0].time(), '%H:%M')
	
	else:
		alarm_day = None
		alarm_time = None
	
	return alarm_day, alarm_time 


if __name__ == '__main__':
	#only take the time stamps 
	alarms = [al[5:] for al in ALARMS]
	next_alarms = []
	for entry in alarms:
		#get valid alarms as datetime objects
		next_alarms.append([datetime.datetime.strptime(time_of_day, '%Y-%m-%d %H:%M:%S') for time_of_day in entry if time_of_day is not None])
	
	get_alarm_for_weekday(alarm_data=next_alarms, weekday=[5])
