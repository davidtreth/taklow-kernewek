# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 20:53:26 2017

@author: davydh
"""
import re
from syllabenn_ranna_kw import kwKemmynRegExp as KKre
from syllabenn_ranna_kw import kwKemmynDevRegExp as KKre_dev

sylRE = KKre.syllabelRegExp
diwetRE = KKre.diwetRegExp 
kynsaRE = KKre.kynsaRegExp
dewson_sev = KKre.dewson_sevel_re
dewson_kodha = KKre.dewson_kodha_re

sylRE2 = KKre_dev.syllabelRegExp
diwetRE2 = KKre_dev.diwetRegExp 
kynsaRE2 = KKre_dev.kynsaRegExp
dewson_sev2 = KKre_dev.dewson_sevel_re
dewson_kodha2 = KKre_dev.dewson_kodha_re


testwords = ['penn', 'pennskol', 'penneglos', 'penneglosow',
             'an', 'androw', 'anaswonnys']
print("arbrovya syllabelRegExp")
print("ger: REmatches REDevmatches")
for t in testwords:    
    m = re.findall(sylRE, t)
    m2 = re.findall(sylRE2, t)
    print("{w}: {sls} {sls2}".format(w=t, sls=m, sls2=m2))

print("arbrovya diwetRegExp")
print("ger: REmatches REDevmatches")
for t in testwords:
    m = re.findall(diwetRE, t)
    m2 = re.findall(diwetRE2, t)
    print("{w}: {sls} {sls2}".format(w=t, sls=m, sls2=m2))
    
print("arbrovya kynsaRegExp")
print("ger: REmatches REDevmatches")
for t in testwords:
    m = re.findall(kynsaRE, t)
    m2 = re.findall(kynsaRE2, t)
    print("{w}: {sls} {sls2}".format(w=t, sls=m, sls2=m2))    
    
print("arbrovya dewson_sevel_re")
print("ger: REmatches REDevmatches")
for t in testwords:
    m = re.findall(dewson_sev, t)
    m2 = re.findall(dewson_sev2, t)
    print("{w}: {sls} {sls2}".format(w=t, sls=m, sls2=m2))    

print("arbrovya dewson_kodha_re")
print("ger: REmatches REDevmatches")
for t in testwords:
    m = re.findall(dewson_kodha, t)
    m2 = re.findall(dewson_kodha2, t)
    print("{w}: {sls} {sls2}".format(w=t, sls=m, sls2=m2))    

