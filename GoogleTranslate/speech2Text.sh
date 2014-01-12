# This Bash Script Queries Google for Speech to Text. Input Arg1 is number of
# seconds to record and listen for speech

#echo "Recording your Speech (3 Seconds of Text)"
arecord -d ${1:-3} -D plughw:0,0 -q -f cd -t wav -r 16000 | flac - -f --best --sample-rate 16000 -s -o audio/speech.flac;

#echo "Converting Speech to Text..."
wget -q -U "Mozilla/5.0" --post-file audio/speech.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v1/recognize?lang=en-us&client=chromium" | cut -d\" -f12  > speech2Text.txt

#echo "You Said:"
#value=`cat speech2Text.txt`
#echo "$value"
