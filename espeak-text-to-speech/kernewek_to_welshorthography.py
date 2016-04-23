# coding=utf-8
import sys
import string
#
# Author: David Trethewey
# This program does not pretend to produce an orthographically
# sensible result, but rather in conjunction with the shell scripts
# kows_kernewek_tofile.sh or kows_kernewek_speaker.sh
# use espeak TTS software with its Welsh voice
# produce an attempt at Cornish text to speech
#
# takes first argument as input text, second as output
#

def towelsh(inputtext,newline=False):
    outputtext = ""    
    for w in inputtext:
        w = w.lower()
        w = w.replace("f","ff")
        w = w.replace("sya","sja")
        w = w.replace("y","i")
        w = w.replace("ll","l")
        w = w.replace("ch","tj")
        w = w.replace("gh","ch")
        w = w.replace("sh","si")
        w = w.replace("wra","wrà")
        w = w.replace("wr","r")
        w = w.replace("eu","w")
        w = w.replace("ou","ŵ")
        w = w.replace("oe","oo")
        w = w.replace("u","i")
        w = w.replace("dh","dd")
        if newline:
            outputtext += w + "\n"
        else:
            outputtext += w
    return outputtext

if __name__ == "__main__":
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    #print inputtext_words
    inputtext = file(inputfile).readlines()
    outputtext = towelsh(inputtext,True)
    outputtext = outputtext.replace(" .",".")
    outputtext = outputtext.replace(" - ","-")
    outputtext = outputtext.replace(" ' ","'")
    outputtext = outputtext.replace("' ","'")
    outputtext = outputtext.replace("'","")
    # print towelsh
    out = file(outputfile,"w")
    out.write(outputtext)



