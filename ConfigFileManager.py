
## DEPENDANCIES  --------------------------------------------
import ConfigParser

## CLASS DEFINITIONS ----------------------------------------
class ConfigFileManager():
	def __init__(self, CONFIG_FILE_PATH):
		self.file = ConfigParser.ConfigParser()
		self.CONFIG_FILE_PATH = CONFIG_FILE_PATH

	# Interface for Configuration File
	def update(self, section, option, value = "getValue"):

		# Update Configuration File
		self.file.read(self.CONFIG_FILE_PATH)

		# Get/Set Value
		self.file.set(section, option, value)
		cfgfile = open(self.CONFIG_FILE_PATH,'w')
		self.file.write(cfgfile)
		cfgfile.close()

	def poll(self, section, option):

		# Update Configuration File
		self.file.read(self.CONFIG_FILE_PATH)

		# Get/Set Value
		return self.file.get(section, option)