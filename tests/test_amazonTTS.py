import sys
sys.path.append(r'/var/lib/snips/skills/snips_app_pilldispenser')

import subprocess
from VoiceControl import VoiceControl
from settings import SettingsManager
import time

if __name__ == '__main__':
	current_voice_control = VoiceControl(user_ID=16)
	
	time.sleep(5)
	#test the dual TTS
	print('Enabling Dual TTS')
	current_voice_control.settingsmanager.enable_dual_TTS()
	voice = 'Marlene'
	gender = 'FEMALE'
	command = ['/var/lib/snips/skills/snips_app_pilldispenser/settings/amazon_tts.sh', '/var/lib/snips/skills/snips_app_pilldispenser/settings/1', 'amazon', 'de', 'DE', voice, gender, 'Der nächste Alarm ist um 15.00 Uhr.', '24000']	
	subprocess.Popen(command)
