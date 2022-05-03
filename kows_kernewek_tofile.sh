#!/bin/bash
# usage: ./kows_kernewek_tofile.sh <input Cornish text file> <output sound file>
python kernewek_to_welshorthography.py $1 kows_workingfile.txt
espeak -vcy -w $2 -f kows_workingfile.txt 
