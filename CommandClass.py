
## DEPENDANCIES  --------------------------------------------
import subprocess

## CLASS DEFINITIONS ----------------------------------------
class Command():
	def __init__(self, cmd, action):
		self.cmd = cmd;
		self.action = action;

	def __str__(self):
		return "Cmd: \"" + self.cmd + "\", Action:\"" + self.action + "\""

	def do(self):
		subprocess.call(self.action.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	def do_verbose(self):
		print subprocess.check_output(self.action.split(), shell=False)