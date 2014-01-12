## Main Code Base for JARVIS
## Written by David Bjanes
## email: public@davidbjanes.com

## DEPENDANCIES  --------------------------------------------
import time
import sys
import os
import platform

## Global Variables  ----------------------------------------
verbose = True



## Main Function 
def main():

	os = platform.system()

	# Operating System Check
	if os == "Windows":
		print "I'm sorry, but I currently only run on \"Linux\"."
	else: 
		print "Jarvis is Running!"
	
	#while (True):

		#Get Inputs



if __name__ == "__main__":
	main()