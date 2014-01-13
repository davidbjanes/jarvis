
## DEPENDANCIES  --------------------------------------------
import time

## CLASS DEFINITIONS ----------------------------------------
class Logger():
	def __init__(self, LOG_FILE_PATH):
		self.LOG_FILE_PATH = LOG_FILE_PATH

	def log(self, msg = ""):
		logFile = open(self.LOG_FILE_PATH, 'a', 0)
		time_str = time.strftime("%Y.%m.%d_%H.%M.%S:")
		print >> logFile, time_str + msg
		logFile.close()