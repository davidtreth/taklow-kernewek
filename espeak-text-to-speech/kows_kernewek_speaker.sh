#!/bin/bash
# usage: ./kows_kernewek_speaker.sh <input Cornish text file>
python kernewek_to_welshorthography.py $1 kows_workingfile.txt
espeak -vcy -f kows_workingfile.txt --ipa 
