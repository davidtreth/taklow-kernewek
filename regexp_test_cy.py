# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 20:53:26 2017

@author: davydh
"""
import re
import sys
from syllabenn_ranna_kw import cyRegExp as CYre
import imp
imp.reload(sys)
if sys.version_info[0] < 3:
    print("Best run in Python3 to print output containing non-ASCII characters")
    sys.setdefaultencoding('utf-8')    

def getTestWord():
    if sys.version_info[0] < 3:
        w = raw_input('Gorr ger arbrov mar pleg: ')
    else:
        w = input('Gorr ger arbrov mar pleg: ')
    return w

def deleteFinal(word, finalsylregexp):
    """ word is the string containing the word """
    syl = re.findall(finalsylregexp, word)
    #syl should be a list containing one tuple 
    #intended to be output of re.findall(word, diwetRegExp)
    print("Final syllable regexp match tuple: {S}".format(S=syl))
    if syl[0][0]:
        finalrev = syl[0][0][::-1]
    else:
        # where one of the vowels with umlaut is used
        finalrev = syl[0][5][::-1]
    w_notfinal = word[::-1].replace(finalrev, "", 1)[::-1]
    return w_notfinal, finalrev[::-1]

sylRE = CYre.syllabelRegExp
diwetRE = CYre.diwetRegExp 
kynsaRE = CYre.kynsaRegExp
#print(sylRE)

#testwords = [t.title() for t in testwords]             
testwords = ["Noswaith", "da", "gweld", "mae'r", "cwrdd", "nghariad",
             "mrawd", "caeëdig", "glöwr", "adeiladwr", "efallai",
             "llongyfarchiadau", "Aberystwyth",
             "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch"]
#testword = ""
testword = "test"
print("Gorrewgh geryow arbrov mar pleg. Pan vydh an rol leun, gwra gweskel 'Enter'.")

while testword:             
    testword = getTestWord()
    testword = testword.strip()
    #testword = testword.encode('utf-8')
    if testword:
        testwords.append(testword)

print("arbrovya syllabelRegExp")
for t in testwords:    
    m = re.findall(sylRE, t)
    print("{w}:\n".format(w=t))
    sylstrs = []
    for i, s in enumerate(m):
        print("S{i}: {s}".format(i=i+1, s=s))
        sylstr = s[0] + s[4] + s[7]
        sylstrs.append(sylstr)
    print("")
    print("{w}: {n} syllables:".format(w=t, n=len(sylstrs)))
    for i, s in enumerate(sylstrs):
        print("{i}:{s} ".format(i=i+1, s=s), end="")
    print("\n")
    
print("arbrovya diwetRegExp")
for t in testwords:
    m = re.findall(diwetRE, t)
    print("{w}:\nFinalSyl:{sls}\n".format(w=t, sls=m))


print("arbrovya diwetRegExp (recursive)")
for t in testwords:
    syls = []
    word = t
    while word:
        print("{w}:".format(w=word))
        word2, finalsyl = deleteFinal(word, diwetRE)
        print("FinalSyl:{f}\n".format(f=finalsyl))
        word = word2
        syls.append(finalsyl)
    syls.reverse()
    print("{w}: matching backwards {n} syllables:".format(w=t, n=len(syls)))
    for i, s in enumerate(syls):
        print("{i}:{s} ".format(i=i+1, s=s), end="")
    print("\n")
    
print("arbrovya kynsaRegExp")
for t in testwords:
    m = re.findall(kynsaRE, t)
    print("{w}:\nFirstSyl:{sls}\n".format(w=t, sls=m))    
"""    
print("arbrovya dewson_sevel_re")
print("ger: REmatches")
for t in testwords:
    m = re.findall(dewson_sev, t)
    print("{w}:\nCY:{sls}\n".format(w=t, sls=m))    

print("arbrovya dewson_kodha_re")
print("ger: REmatches")
for t in testwords:
    m = re.findall(dewson_kodha, t)
    print("{w}:\nCY:{sls}".format(w=t, sls=m))    
"""
