import sys
sys.path.append(r'/var/lib/snips/skills/snips_app_pilldispenser')

from VoiceControl import VoiceControl

if __name__ == '__main__':
	#create a voice control instance
	test_voicecontrol = VoiceControl()

	#deactivate snips components manually 
	test_voicecontrol.settingsmanager.deactivate_voice_control()

