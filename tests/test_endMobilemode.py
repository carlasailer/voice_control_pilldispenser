import sys
sys.path.append(r'/var/lib/snips/skills/snips_app_pilldispenser')

from VoiceControl import VoiceControl

#locations of the magazine
ERROR = 0
AT_STATIONARY = 1
AT_MOBILE = 2

if __name__ == '__main__':
	#create a voice control instance
	test_voicecontrol = VoiceControl(user_ID=16)

	###dummy data: 'Magazine' defines where the magazine is located
	MAGAZINE_LIST = {}
	MAGAZINE_LIST[0] = {'Day': 'Mon', 'Magazine': 1, 'No': 0, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
	MAGAZINE_LIST[1] = {'Day': 'Tue', 'Magazine': 1, 'No': 1, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 1, 'empty': 1, 'AlreadyDetected': 'no'}
	MAGAZINE_LIST[2] = {'Day': 'Wed', 'Magazine': 1, 'No': 2, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 1, 'ni': 1, 'empty': 1, 'AlreadyDetected': 'no'}
	MAGAZINE_LIST[3] = {'Day': 'Thu', 'Magazine': 1, 'No': 3, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
	MAGAZINE_LIST[4] = {'Day': 'Fri', 'Magazine': 1, 'No': 4, 'h': 0, 'm': 0, 'sT': 0, 'mo': 1, 'mi': 1, 'a': 1, 'ni': 1, 'empty': 0, 'AlreadyDetected': 'no'}
	MAGAZINE_LIST[5] = {'Day': 'Sat', 'Magazine': 1, 'No': 5, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
	MAGAZINE_LIST[6] = {'Day': 'Sun', 'Magazine': 1, 'No': 6, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
	MAGAZINE_LIST[7] = {'Day': 'Res', 'Magazine': 1, 'No': 7, 'h': 0, 'm': 0, 'sT': 0, 'mo': 0, 'mi': 0, 'a': 0, 'ni': 0, 'empty': 0, 'AlreadyDetected': 'no'}
	
	#magazines for thursday and friday at mobile
	MAGAZINE_LIST[3]['Magazine'] = AT_MOBILE
	MAGAZINE_LIST[4]['Magazine'] = AT_MOBILE
	
	#test the voice control for end of mobile mode
	test_voicecontrol.controlscommunicator.receive_stop_mobilemode(MAGAZINE_LIST)
	
	#'return' the two magazines to the stationary 
	MAGAZINE_LIST[3]['Magazine'] = AT_STATIONARY
	MAGAZINE_LIST[4]['Magazine'] = AT_STATIONARY
	
	#test the voice control for end of mobile mode
	test_voicecontrol.controlscommunicator.receive_stop_mobilemode(MAGAZINE_LIST)
