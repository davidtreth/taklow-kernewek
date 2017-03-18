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
    sys.setdefaultencoding('utf-8')

def getTestWord():
    if sys.version_info[0] < 3:
        w = raw_input('Gorr ger arbrov mar pleg: ')
    else:
        w = input('Gorr ger arbrov mar pleg: ')
    return w
    
sylRE = CYre.syllabelRegExp
diwetRE = CYre.diwetRegExp 
kynsaRE = CYre.kynsaRegExp

#testwords = [t.title() for t in testwords]             
testwords = []
testword = "test"
print("Gorrewgh geryow arbrov mar pleg. Pan vydh an rol leun, gwra gweskel 'Enter'.")
while testword:             
    testword = getTestWord()
    testword = testword.strip()
    testword = testword.encode('utf-8')
    if testword:
        testwords.append(testword)

print("arbrovya syllabelRegExp")
print("ger: REmatches")
for t in testwords:    
    m = re.findall(sylRE, t)
    print("{w}:\nCY:{sls}\n".format(w=t, sls=m))

print("arbrovya diwetRegExp")
print("ger: REmatches")
for t in testwords:
    m = re.findall(diwetRE, t)
    print("{w}:\nCY:{sls}\n".format(w=t, sls=m))
    
print("arbrovya kynsaRegExp")
print("ger: REmatches")
for t in testwords:
    m = re.findall(kynsaRE, t)
    print("{w}:\nCY:{sls}\n".format(w=t, sls=m))    
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
