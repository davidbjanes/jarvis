
## DEPENDANCIES  --------------------------------------------
import ConfigParser
import os
from ConfigFileManager import ConfigFileManager


## Global Constants  ----------------------------------------
CONFIG_FILE_PATH = "config.ini"
STATE_ON = True
STATE_OFF = False


# Turn off Jarvis
def stop(error_msg = "Jarvis is powering down."):

	# Initialize Configuration File
	configFile = ConfigFileManager(CONFIG_FILE_PATH)

	configFile.update("Program", "instance_ID", "NaN")
	configFile.update("Program", "status", STATE_OFF)

	print error_msg