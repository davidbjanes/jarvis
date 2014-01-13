
## DEPENDANCIES  --------------------------------------------
import ConfigParser
from CommandClass import Command

## CLASS DEFINITIONS ----------------------------------------
class ConfigFileManager():
	def __init__(self, CONFIG_FILE_PATH):
		self.configFile = ConfigParser.ConfigParser()
		self.CONFIG_FILE_PATH = CONFIG_FILE_PATH
		self.configFile.read(CONFIG_FILE_PATH)

	# Interface for Configuration File
	def update(self, section, option, value = "NaN"):

		# Update Configuration File
		self.configFile.read(self.CONFIG_FILE_PATH)

		# Get/Set Value
		self.configFile.set(section, option, value)
		cfgfile = open(self.CONFIG_FILE_PATH,'w')
		self.configFile.write(cfgfile)
		cfgfile.close()

	def poll(self, section, option):

		# Update Configuration File
		self.configFile.read(self.CONFIG_FILE_PATH)

		# Get/Set Value
		return self.configFile.get(section, option)

	# build Command List
	def buildCommandList(self):

		# Initialize Variables
		commandList = []

		# Update Configuration File
		self.configFile.read(self.CONFIG_FILE_PATH)

		# Iterate through command pairs
		options = self.configFile.options("CommandDefinition")
		for option in options:
			try:
				output = self.configFile.get("CommandDefinition", option)
				pair = output.split(",")
				commandList.append(Command(pair[0], pair[1]));
				print "DEBUGGING:" + str(commandList[len(commandList)-1])

			except Exception as exception:
				print "ERROR:" + "Invalid Command in Configuration File"
				return -1

		return commandList


	# read Pending Command List
	def getPendingCommandList(self):

		# Initialize Variables
		commandList = []

		# Update Configuration File
		self.configFile.read(self.CONFIG_FILE_PATH)

		# Iterate through command pairs
		options = self.configFile.options("PendingCommands")
		for option in options:
			try:
				output = self.configFile.get("PendingCommands", option)
				pair = output.split(",")
				commandList.append(Command(pair[0], pair[1]));
				print "DEBUGGING:" + str(commandList[len(commandList)-1])

			except Exception as exception:
				print "ERROR:" + "Invalid Command in Configuration File"
				return -1

		return commandList

