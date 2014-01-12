
import os
import subprocess

destination_language = "en"
masters_name = "David"
voice_modules_name = "Jarvis"

# DEFINITIONS -----------------------------------------------------------------$
class command():
	def __init__(self, speech, cmd):
		self.speech = speech;
		self.cmd = cmd;

# Speak "phrase"
def speakKnownPhrase(phrase_num = 1):
	if phrase_num == 1:
		subprocess.call(["mplayer", "-ao", "alsa:device=hw=0.0", "audio/helpyou.mp3"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def speakDestinationText(phrase):
	googleSpeechURL = "http://translate.google.com/translate_tts?tl=" + destination_language +"&q=" + phrase
	subprocess.call(["mplayer", "-ao", "alsa:device=hw=0.0", googleSpeechURL], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Record User's Speech (Run Bash file and save output to text file)
def getText(record_time = 3):
	# Recorder User's response
	os.system("./speech2Text.sh %s" % record_time)
	# Read Text file with synthesized text
	fileHandle = open ( 'speech2Text.txt', 'r' )
	text = fileHandle.read()
	fileHandle.close()
	text.strip()
	return (text[:-1])


# Main Program ----------------------------------------------------------------$
confirm_command_text = "no"
while confirm_command_text != "yes":
	text = ""
	while not text:
		speakKnownPhrase(1)
		text = getText(3)
		if not text:
			speakDestinationText("I couldn't hear you.")

	# Confirm Command
	speakDestinationText("Did you say: %s?" % text)
	# Get responses
	confirm_command_text = getText()
	if confirm_command_text == "cancel":
		speakDestinationText("Good Bye!")
		sys.exit()

speakDestinationText("Ok!")

commandList = []
commandList.append(command("text my iPhone", "python send_SMS.py"));

completedAction = False
for cmd in commandList:
	#print(cmd.speech)
	if text == cmd.speech:
		os.system(cmd.cmd)
		completedAction = True;
		break

if completedAction:
	speakDestinationText("Great!  It is done!")
else:
	speakDestinationText("I am sorry, I could not find the command.")


