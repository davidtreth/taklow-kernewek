#!/bin/bash
python keskows5.py --writetofile --onesent --english 
python kernewek_to_welshorthography.py lavar_k.txt kows_workingfile.txt
espeak -vcy -f kows_workingfile.txt --ipa
espeak -ven-uk -f lavar_e.txt
