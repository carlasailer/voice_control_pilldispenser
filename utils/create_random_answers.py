  #!/usr/bin/env python3
# -*- encoding: utf-8 -*-

""" create_random_answers

Run this script to create the file of possible answers of the speech synthesis (TTS) engine.

"""

import json

filename = '/var/lib/snips/skills/snips_app_pilldispenser/utils/answers.txt'

#ae:  u'\xe4'
#oe:  u'\xf6'
#ue:  u'\xfc'
#AE:  u'\xc4'

#adaptVolume
dic_adaptVolume = 			{'adapt':	[u'Die Lautst\xe4rke wurde angepasst.',
										u'Lautst\xe4rke erfolgreich ge\xe4ndert.',
										u'\xe4nderung der Lautst\xe4rke erfolgreich.',
										u'\xe4nderung der Lautst\xe4rke erfolgreich durchgef\xfchrt.'],
							'error':	[u'Lautst\xe4rke konnte nicht angepasst werden.']
							}
#confirmTaking
dic_confirmTaking = 		{'start':				[u'Bitte die Entnahme per Knopfdruck, auf dem Bildschirm oder per Sprache best\xe4tigen.',
													u'Bitte bestätigen Sie die Entnahme per Knopfdruck, auf dem Bildschirm oder per Sprache.',
													u'Es ist Zeit für die Medikamentenentnahme. Bitte per Knopfdruck, auf dem Bildschirm oder per Sprache best\xe4tigen.'],
							'confirm':				[u'Danke f\xfcr die Best\xe4tigung der Entnahme.',
													u'Danke f\xfcr die Best\xe4tigung',
													u'Best\xe4tigung vollst\xe4ndig.', 
													u'Best\xe4tigung erfolgreich.', 
													'Vielen Dank. Entnahme ist beendet.']
							}
							
#contact
dic_contact = 				{'call': 		[u'Ich werde folgende Person f\xfcr dich anrufen: {} ', 
											'Ich starte einen Anruf an: {}', 
											'{} wird angerufen.'],
							'suggestDoc': 	[u'Folgende \xc4rzte habe ich in der Datenbank gefunden: ',
											u'Folgende \xc4rzte sind in der Datenbank hinterlegt: ',
											u'Folgende \xc4rzte stehen zur Auswahl: '],
							'notSuccess': 	[u'Wen soll ich anrufen?', 'Wenn soll ich kontaktieren?', 'Wen meintest du?']
							}
				
#durationMobilemode
dic_durationMobilemode = 	{'active': 		['Mobile Einheit aktiv! Folgende Magazine sind vorbereitet: {}', 
											'Die mobile Box ist bereit. Bitte folgende Magazine entnehmen: {}', 
											'Wechsel in den mobilen Modus. Bitte die Tagesmagazine für {} mitnehmen.']
							}

#getHistory
dic_getHistory = 			{'info': 		[u'Ich informiere dich \xfcber die bisherigen Entnahmen.',
											u'Du erh\xe4lst nun Auskunft \xfcber die bisherigen Entnahmen.',
											u'Hier ist die Entnahme-Historie.',
											u'Ich informiere dich \xfcber die Historie der Entnahmen.'],
							'nonCorrects': [u'Die Anzahl fehlerhafter Entnahmen ist: {}',
											'Es gab {} fehlerhafte Entnahmen.',
											'{} Entnahmen waren fehlerhaft.' ],
							'infoHistory': [u'Bitte \xfcberpr\xfcfen: {} {}.',
											u'Am {} war die Entnahme am {} nicht korrekt.',
											u'Am {] gab es es am {} eine fehlerhafte Entnahme.']
							}
						
#infoMedication
dic_infoMedication = 		{'next':	[u'Ich gebe dir gerne Informationen zur n\xe4chsten Einnahme. Tag: {}, Uhrzeit: {}',
										u'Tag und Uhrzeit der n\xe4chsten Entnahme: {} {}',
										u'Die n\xe4chste Entnahme ist am {} um {}.'],
							'days':		[u'Folgende Alarme sind f\xfcr {} gespeichert: ', 
										u'Ich teile dir die Entnahmezeiten f\xfcr {} mit: ']
							}

#infoRefilling
dic_infoRefilling = 		{'info':		[u'Ich gebe dir den aktuellen F\xfcllzustand der einzelnen Magazine. ', 
											u'Hier die Best\xe4nde. '],
							'stock_info': 	[u'Magazin für {} ist zu {} % leer. ', 
											'Das {}s-Magazin ist zu {} % leer. ', 
											'{}: {} % leer. '],
							'empty': 		['Magazin für {} ist komplett leer. ', 
											'Das {}s-Magazin ist komplett leer. ', 
											'{}: komplett leer. ']
							}

#repeat
dic_repeat = 				{'last_asr': 	['Die letzte Spracheingabe war: {}',
											'Ich habe folgenden Satz verstanden: {}',
											'Die letzte Eingabe per Sprache lautete: {}',
											'Ich wiederhole die letzte Aufforderung: {}'],
							'last_tts':		['Die letzte Sprachausgabe war: {}',
											'Meine letzte Ausgabe war: {}',
											'Die letzte Ausgabe war: {}',
											'Ich wiederhole meine letzte Sprachausgabe: {}'],
							}
#startMobilemode
dic_startMobilemode = 		{'askTimespec': ['An welchen Tagen brauchst du die mobile Einheit?', 
											u'Teile mir die gew\xfcnschten Tage mit.',
											'Wann bist du unterwegs?',
											u'F\xfcr wie lange bist du weg?',
											u'F\xfcr welche Tage soll ich die mobile Box vorbereiten?'
											]
							}

#save all intents to one dict						
dic_answers = 	{'adaptVolume':			dic_adaptVolume,
				'confirmTaking': 		dic_confirmTaking,
				'contact':	 			dic_contact,
				'durationMobilemode': 	dic_durationMobilemode,
				'getHistory':			dic_getHistory,
				'infoMedication':		dic_infoMedication,
				'infoRefilling': 		dic_infoRefilling,
				'repeat':				dic_repeat,
				'startMobilemode': 		dic_startMobilemode				
				}

with open(filename, 'w') as f:
	f.write(json.dumps(dic_answers))#, ensure_ascii=False))

print('Creating answers was successful.')
