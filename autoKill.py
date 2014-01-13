
## DEPENDANCIES  --------------------------------------------
import os
import signal
import ctypes
from ConfigFileManager import ConfigFileManager

## Global Constants  ----------------------------------------
CONFIG_FILE_PATH = "config.ini"

## Code -----------------------------------------------------
configFile = ConfigFileManager(CONFIG_FILE_PATH)
pid = configFile.poll("Program", "instance_id")

PROCESS_TERMINATE = 1
handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
ctypes.windll.kernel32.TerminateProcess(handle, -1)
ctypes.windll.kernel32.CloseHandle(handle)
