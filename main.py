## Main Code Base for JARVIS
## Written by David Bjanes
## contact: public@davidbjanes.com

## DEPENDANCIES  --------------------------------------------
import ConfigParser
import subprocess
import time
import sys
import signal
from CommandClass import Command
from ConfigFileManager import ConfigFileManager
from stop import stop


## Global Constants  ----------------------------------------
CONFIG_FILE_PATH = "config.ini"
LOG_FILE_PATH = "log.txt"
STATE_ON = True
STATE_OFF = False

## Global Variables  ----------------------------------------
verbose = True


## Main Function   ------------------------------------------
def main_loop():

	logFile = open(LOG_FILE_PATH, 'a')
	sys.stdout = logFile
	print time.strftime("%Y.%m.%d_%H.%M.%S:") + "Jarvis is booting up ----------------------------------"

	configFile = ConfigFileManager(CONFIG_FILE_PATH)

	commandList = buildCommandList(configFile)

	configFile.update("Program", "status", STATE_ON)
	stateMachine = STATE_ON

	try:
		#while (stateMachine != 0):
		for x in range(0,20):

			time_str = time.strftime("%Y.%m.%d_%H.%M.%S:")

			# Check for given commands

			# Execute Commands
			commandList[0].do_verbose()

			# Check Status in Config File
			stateMachine = configFile.poll("Program", "status")

			# Dummy Command
			print time_str + "Running..."
			time.sleep(1)

		# stateMachine has ended loop
		stop()

	except (KeyboardInterrupt, SystemExit, signal.SIGINT, OSError):
		configFile.update("Program", "error_code", 1)
		stop(time_str + "User Killed Jarvis, powering down.")
		raise

	except:
		configFile.update("Program", "error_code", 2)
		stop(time_str + "Unknown Error Killed Jarvis, powering down.")
		raise


# build Command List
def buildCommandList(configFile):

	# Initialize Variables
	commandList = []

	# Update Configuration File
	configFile.file.read(configFile.CONFIG_FILE_PATH)

	# Iterate through command pairs
	options = configFile.file.options("Commands")
	for option in options:
		try:
			output = configFile.file.get("Commands", option)
			pair = output.split(",")
			commandList.append(Command(pair[0], pair[1]));
			print commandList[len(commandList)-1]

		except:
			print "Invalid Command in Configuration File"
			return

	return commandList


# Default 'def' to start at
if __name__ == "__main__":
	main_loop()



