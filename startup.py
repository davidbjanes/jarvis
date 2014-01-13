
## DEPENDANCIES  --------------------------------------------
import platform
import os
import sys
import subprocess
from ConfigFileManager import ConfigFileManager
from multiprocessing import Process
import main


## DEFINITIONS ----------------------------------------------
CONFIG_FILE_PATH = "config.ini"


# Run JARVIS
def startup():

	# Get Name of Operating System
	os_name = platform.system()

	# Initialize Configuration File
	configFile = ConfigFileManager(CONFIG_FILE_PATH)

	instance_ID = configFile.poll("Program", "instance_ID")

	# Don't allow multiple instances of Jarvis to run concurrently
	if not(isinstance(instance_ID,str) and instance_ID == "NaN"):
		print "Multiple Instances Running, Start-up Failure."
		return

	# Operating System Check
	if os_name == "Windows" or os_name == "Unix":
		print "Jarvis is Running!"

		# Initialize Configuration File
		configFile.update("Program", "status", "NaN")
		configFile.update("Program", "instance_id", "NaN")
		configFile.update("Program", "error_code", "NaN")

		command_str = "python main.py"

		if os_name == "Windows":
			process_obj = subprocess.Popen(command_str.split(), creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
			configFile.update("Program", "instance_ID", process_obj.pid)
			print "Windows Version Created!"

		else:
			# Create New Process Group
			os.setpgrp() 

			# spawn JARVIS
			process_obj = subprocess.Popen(command_str.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			configFile.update("Program", "instance_ID", process_obj.pid)

	else:
		print "I'm sorry, you are running " + os_name + ". I currently only run on Windows/Unix"
		return


# Default 'def' to start at
if __name__ == "__main__":
	startup()
