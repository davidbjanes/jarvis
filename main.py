## Main Code Base for JARVIS
## Written by David Bjanes
## contact: public@davidbjanes.com

## DEPENDANCIES  --------------------------------------------
import time
import sys
import os
import platform
import subprocess
import ConfigParser


## Global Constants  ----------------------------------------
STATE_STOP = 0
STATE_RUNNING = 1
STATE_ERROR = -1
CONFIG_FILE_PATH = "config.ini"


## Global Variables  ----------------------------------------
verbose = True
stateMachine = STATE_STOP
configFile = []


## Main Function 
def main_loop():

	# Initialize Variables
	global stateMachine
	global configFile

	try:
		while (stateMachine != 0):
			# Check for new commands

			# Execute New Commands

			# Check Status in Config File
			value = updateConfigFile("Program", "status")
			stateMachine = int(value)

			# Dummy Command
			print "Running..."
			time.sleep(1)

		# stateMachine has ended loop
		stop()

	except (KeyboardInterrupt, SystemExit):
		stateMachine = STATE_ERROR
		stop("User Killed Jarvis, powering down.")
		raise



# Boot up Jarvis
def startup():

	# Initialize Variables
	global stateMachine
	global configFile

	# Get Name of Operating System
	os_name = platform.system()

	# Initalize Configuration File
	configFile = ConfigParser.ConfigParser()

	num_instances_running = updateConfigFile("Program", "Number_Of_Instances")
	num_instances_running = int(num_instances_running)

	# Don't allow multiple instances of Jarvis to run concurrently
	if num_instances_running > 0:
		print "Multiple Instances Running, Startup Failure."
		return

	# Operating System Check
	if os_name == "Other":
		stop("I'm sorry, but I currently only run on \"Linux\".")
		return

	else: 
		print "Jarvis is Running!"

		#Initialize State Machine
		stateMachine = STATE_RUNNING
		updateConfigFile("Program", "status", stateMachine)
		updateConfigFile("Program", "Number_Of_Instances", num_instances_running+1)

		# Run Main Loop
		main_loop()


# Interface for Configuration File
def updateConfigFile(section, option, value = "getValue"):

	# Initialize Variables
	global configFile

	# Update Configuration File
	configFile.read(CONFIG_FILE_PATH)

	# Get/Set Value
	if value == "getValue":
		return configFile.get(section, option)
	else:
		configFile.set(section, option, value)

		cfgfile = open(CONFIG_FILE_PATH,'w')
		configFile.write(cfgfile)
		cfgfile.close()

		return


# Turn off Jarvis
def stop(error_msg = "Jarvis is powering down."):

	global stateMachine

	num_instances_running = updateConfigFile("Program", "Number_Of_Instances")
	updateConfigFile("Program", "Number_Of_Instances", int(num_instances_running)-1)
	updateConfigFile("Program", "status", stateMachine)

	print error_msg


# Default 'def' to start at
if __name__ == "__main__":
	startup()



