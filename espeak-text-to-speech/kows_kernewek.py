## usage: python kows_kernewek.py <input text> <output sound file>
# In Linux I have generally used the kows_kernewek_*.sh scripts
# to call espeak at the command line
# In windows it is possible to use this Python script to process the files
#
# this script assumes we are in the same directory
# as the command line espeak.exe file

import sys
import os

# not used at present. This could be prepended to the espeakcommand
espeakpath = "C:\\Program Files (x86)\\eSpeak\\command-line\\"

# convert Cornish text (first command line argument) to the Welsh spelling system
os.system("python kernewek_to_welshorthography.py "+sys.argv[1]+" kows_workingfile.txt")
# adapt this if you wish to output to audio out rather than to file
espeakcommand = "espeak.exe"+" -vcy"+" -f "+" kows_workingfile.txt " + " -w "+sys.argv[2]
print(espeakcommand)
# run espeak with the welsh voice using the converted text as input
# and the second command line argument to specify the output sound file
os.system(espeakcommand)
