## Main Code Base for JARVIS
## Written by David Bjanes
## contact: public@davidbjanes.com

## DEPENDANCIES  --------------------------------------------
import ConfigParser
import subprocess
import time
import sys
import signal
import ast
import Logger
from CommandClass import Command
from ConfigFileManager import ConfigFileManager
from shutdown import shutdown


## Global Constants  ----------------------------------------
CONFIG_FILE_PATH = "config.ini"
LOG_FILE_PATH = "log.txt"
STATE_ON = True
STATE_OFF = False


## Global MESSAGE Constants  ----------------------------------------
MSG_STARTUP = "Jarvis is booting up ----------------------------------"
MSG_RUNNING = "Running..."
MSG_ENDING = "Jarvis is powering down."
MSG_ERROR_1 = "User Killed Jarvis, powering down."
MSG_ERROR_2 = "Unknown Error Killed Jarvis, powering down."


## Global Variables  ----------------------------------------
verbose = True


## Main Function   ------------------------------------------
def main_loop():

	configFile = ConfigFileManager(CONFIG_FILE_PATH)

	commandList = configFile.buildCommandList()

	configFile.update("Program", "status", STATE_ON)
	stateMachine = STATE_ON

	logFile = Logger.Logger(LOG_FILE_PATH)
	logFile.log(MSG_STARTUP)

	try:
		while (stateMachine == STATE_ON):

			# Check for given commands
			pendingCommandList = configFile.getPendingCommandList()

			# Execute Commands
			# commandList[0].do()
			for pendingCommand in pendingCommandList:
				text == pendingCommand.do()

			# Check Status in Config File
			value = configFile.poll("Program", "status")
			stateMachine = ast.literal_eval(value)

			# Dummy Command
			logFile.log(MSG_RUNNING)
			time.sleep(1)

		# stateMachine has ended loop
		logFile.log(MSG_ENDING)
		shutdown()



	except (KeyboardInterrupt, SystemExit, signal.SIGINT, OSError):
		logFile.log(MSG_ERROR_1)
		shutdown(1)
		raise

	except:
		logFile.log(MSG_ERROR_2)
		shutdown(2)
		raise



# Default 'def' to start at
if __name__ == "__main__":
	main_loop()



