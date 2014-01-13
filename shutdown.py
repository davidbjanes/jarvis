
## DEPENDANCIES  --------------------------------------------
import ConfigParser
import os
import sys
from ConfigFileManager import ConfigFileManager


## Global Constants  ----------------------------------------
CONFIG_FILE_PATH = "config.ini"
STATE_ON = True
STATE_OFF = False


# Turn off Jarvis
def shutdown(error_code = 0):

	# Initialize Configuration File
	configFile = ConfigFileManager(CONFIG_FILE_PATH)

	configFile.update("Program", "instance_ID", "NaN")
	configFile.update("Program", "status", STATE_OFF)
	configFile.update("Program", "error_code", error_code)


# Default 'def' to start at
if __name__ == "__main__":
	shutdown()