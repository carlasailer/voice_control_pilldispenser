import sys
sys.path.append(r'/var/lib/snips/skills/snips_app_pilldispenser')

from VoiceControl import VoiceControl
from settings import SettingsManager
import time

if __name__ == '__main__':
	test_voiceControl = VoiceControl()
	
	#create a settingsmanager instance
	#test_settingsManager = SettingsManager.SettingsManager()
	
	#enable dual TTS
	test_voiceControl.settingsmanager.enable_dual_TTS()
	time.sleep(3)
	test_voiceControl.send_message_to_TTS('Die Sprachausgabe wurde angepasst.')
