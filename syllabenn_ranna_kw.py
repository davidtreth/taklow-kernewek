#!/usr/bin/python
# -*- coding: utf-8 -*-
# David Trethewey 06-05-2016 
# code is Open Source (GPL)
# Fenten Igor yw an kodenn ma (GPL)
#
# A rough and ready hacked together segmentation of Cornish (Kernewek Kemmyn or SWF) text 
# to the syllable level using regular expressions. 
#
# Rannans tekst Kernewek nebes hakkys yn garow (Kernewek Kemmyn po FSS) dhe syllabennow
# 'regular expressions' (pyth yw henna yn Kernewek?)
#
# This version makes a calculation of syllable length
# in Kernewek Kemmyn taking 1 unit as short vowel, 2 units for a half-long, 3 as long
# 1 a normal consonant and 2 as a gemminated double consonant
# e.g. mm in kamm
# in SWF there are no half-long vowels or gemminated consonants, therefore 
# 1 is a short vowel and 2 is a long vowel, and all consonants have length 1 
#
# An vershyon ma a wra amontyans hirder an syllabenn
# yn Kernewek Kemmyn bogalenn verr yw 1 unses, bogalenn hanter hir yw 2 unses, hag onan hir
# yw 3 unses.
# Yma 1 unses yn kessonenn normal ha 2 yn kessonenn gemmynheys
# kepar ha mm yn kamm
# Yn FSS nag eus bogalennow hanterhir po kesson gemmynheys, ytho unses yw dhe
# vogalenn verr ha 2 dhe vogalenn hir, ha hirder a 1 yw gans pub kessonenn
#
# This module is used by the module treuslytherenna.py to convert Kernewek Kemmyn
# text to the Standard Written Form
#
# Usys yw an modul gans modul treuslytherenna.py dhe dreylya tekst Kernewek Kemmyn
# bys dhe'n Furv Skrifys Savonek
#
# Usage: python syllabenn_ranna_kw.py --test <inputfile>
# where <inputfile> is the path to an input file containing 
# text in Kernewek Kemmyn (or FSS or Welsh if the relevant options are used)
# --test is an optional flag to run the test routines in profya()
# --fwd uses segmentation starting from the beginning of each word, rather than
# starting from the end and working backwards
# --short causes it to do a shorter reporting method simply listing each
# word and its number of syllables
# --line causes it to step through the input file line by line, and count the number of syllables
# in the whole line
# --fssregexp causes the Standard Written Form regular expressions to be use
# these aim to match either SWF Main or Traditional forms, but not yet Late
# --cyregexp uses the (experimental) regular expressions to match Welsh text
# this will override --fssregexp

# Usyans: python syllabenn_ranna_kw.py --test <inputfile>
# hag <inputfile> yw hyns dhe restrenn ynworrans gans tekst yn Kernewek Kemmyn
# po FSS po Kembrek mars yw an dewisyansow usys
# --test yw baner dewisel rag dhe eksekutya kodenn arbrov yn profya()
# --fwd a wra rannans diworth dalleth pub ger, yn le dalleth a'n lost hag oberi 
# a-dhelergh
# --short a wra eskorrans berra gans pub ger ha niver syllabennow
# --line a wra kemmer an restrenn dre linennow, hag amontya niver a syllabennow
# yn pub linenn
# --fssregexp a war usya regexps a wra aswonn tekst yn Furv Skrifys Savonek
# yn furv savonek po hengovek, mes na Diwedhes hwath.
# --cyregexp a wra usya regexp (arbrovel) dhe aswonn tekst Kembrek
# henna a wra gorrewlya --fssregexp 

from __future__ import print_function
from collections import defaultdict
import sys
import re
import argparse
import codecs
import datageryow
import imp
imp.reload(sys)
if sys.version_info[0] < 3:
    sys.setdefaultencoding('utf-8')
try:
    import nltk
except ImportError:
    print("NLTK not available. Download from www.nltk.org if not on the system.")

def keyvaltups_group5_text(kvtup):
    lenKV = len(kvtup)
    maxA = lenKV // 5
    kvtext = ""
    for i in range(maxA):
        kv5 = str(kvtup[i*5:(i*5)+5])[1:-1]
        kv5text = "{kvt}\n".format(kvt=kv5)
        kvtext += kv5text
    return kvtext
            
class CountAllSyls:
    def __init__(self):
        """ initialize CountAllSyls object
        """
        # keep track of total number of syllables
        self.NSylTotal = 0
        self.NWords = 0
        # have dictionaries to count the syllables
        self.AllSyllablesDict = defaultdict(int)
        self.AllSyllablesDict_nopunct = defaultdict(int)
        self.StartWordSyllablesDict = defaultdict(int)
        self.EndWordSyllablesDict = defaultdict(int)
        self.MonoSylsDict = defaultdict(int)
        self.StressedNonFinalSylsDict = defaultdict(int)
        self.AllSyllablesStructDict = defaultdict(int)
        # tuple (stressd, monosyl, structure, nSylsGer, final)
        self.AllSyllablesTupleDict = defaultdict(int)
    
    def keyvaltups(self):
        # remove punctuation characters
        self.AllSyllablesDict_nopunct = self.remove_punctchars(self.AllSyllablesDict)
        AllSyllablesDictkv = [(k,v) for (k,v) in self.AllSyllablesDict_nopunct.items()]
        # sort by decreasing frequency
        self.AllSyllablesDSort = sorted(AllSyllablesDictkv,
                                  key=lambda AllSyllablesDictkv: AllSyllablesDictkv[1],
                                  reverse=True)
        StartWordSyllablesDictkv = [(k,v) for (k,v) in self.StartWordSyllablesDict.items()]
        # sort by decreasing frequency
        self.StartWordSyllablesDSort = sorted(StartWordSyllablesDictkv,
                                  key=lambda StartWordSyllablesDictkv: StartWordSyllablesDictkv[1],
                                  reverse=True)
        EndWordSyllablesDictkv = [(k,v) for (k,v) in self.EndWordSyllablesDict.items()]
        # sort by decreasing frequency
        self.EndWordSyllablesDSort = sorted(EndWordSyllablesDictkv,
                                  key=lambda EndWordSyllablesDictkv: EndWordSyllablesDictkv[1],
                                  reverse=True)
        MonoSylsDictkv = [(k,v) for (k,v) in self.MonoSylsDict.items()]
        # sort by decreasing frequency
        self.MonoSylsDSort = sorted(MonoSylsDictkv,
                                  key=lambda MonoSylsDictkv: MonoSylsDictkv[1],
                                  reverse=True)
        StressedNonFinalSylsDictkv = [(k,v) for (k,v) in self.StressedNonFinalSylsDict.items()]
        # sort by decreasing frequency
        self.StressedNonFinalSylsDSort = sorted(StressedNonFinalSylsDictkv,
                                  key=lambda StressedNonFinalSylsDictkv: StressedNonFinalSylsDictkv[1],
                                  reverse=True)
        # create multiline strings with 5 on each line
        self.AllSyllablesDSortText = keyvaltups_group5_text(self.AllSyllablesDSort)
        self.StartWordSyllablesDSortText = keyvaltups_group5_text(self.StartWordSyllablesDSort)
        self.EndWordSyllablesDSortText = keyvaltups_group5_text(self.EndWordSyllablesDSort)
        self.MonoSylsDSortText = keyvaltups_group5_text(self.MonoSylsDSort)
        self.StressedNonFinalSylsDSortText = keyvaltups_group5_text(self.StressedNonFinalSylsDSort)
        
    def remove_punctchars(self, sylsdict):
        """
        remove all punctation characters from syllable dictionaries
        """
        punctchars = "'.,;:!?()-\"" 
        sylsdict_textonly = defaultdict(int)
        for s in sylsdict:
            s0 = s
            for p in punctchars:
                s = s.replace(p,"")
            sylsdict_textonly[s] += sylsdict[s0]
        return sylsdict_textonly

def preprocess2ASCII(inputtext):
    """
    replace any of apostrophe, backtick, or open/close single quote
    with apostrophe
    
    similarly replace possible other double quote characters 
    with ASCII double quote "
    and various hyphen characters with ASCII hyphen -    
    based on http://www.cs.sfu.ca/~ggbaker/reference/characters/
    """
    if sys.version_info[0] < 3:
        inputtext = inputtext.encode('utf-8')    
    singlequotechars = ['`','‘','’','′']
    doublequotechars = ['“','”','″','〃']
    hyphenchars = ['‐','–','—','−','‑','⁃']
    for h in hyphenchars:
        if h in inputtext:
            inputtext = inputtext.replace(h,'-')
    for d in doublequotechars:
        if d in inputtext:
            inputtext = inputtext.replace(d,'"')
    for s in singlequotechars:
        #print(s)
        if s in inputtext:
            inputtext = inputtext.replace(s,"'")
    #print(inputtext)
    return inputtext
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

class kwKemmynRegExp:
    """
    holds the regular expressions to match Kernewek Kemmyn text
    """
    # these are written using re.compile() in kwKemmynDevRegExp
    # Skrifys yns dre re.compile yn kwKemmynDevRegExp
    
    # syllabelRegExp should match syllable anywhere in a word
    # a syllable could have structure CV, CVC, VC, V
    # will now match traditional graphs c-, qw- yn syllable initial position
    syllabelRegExp = r'''(?x)
    (\'?(bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?\'?|dhr?\'?|dl|dr|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|s[pt]?l?|S[pt]?l?|s[mnw]|S[mn]|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfjvlghmnprstwyzBCKDFJVLGHMNPRSTVWZY]) # consonant
    \'?(a\'?y|a\'?w|eu|e\'?y|e\'?w|iw|oe|oy|ow|ou|uw|yw|[aeoiuy])\'? #vowel
(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gw|gl|gn|ld|lf|lk|ll|lm|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgljmnpkrstvw])? #  optional const.
    )| # or
    (\'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])\'? # vowel
    (lgh|ls|lt|lv|bl|bb|kl|kr|kn|kwr?|kk|cch|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gg|gw|gl|gn|ld|lf|lk|ll|lm|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|r\'?s|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgljmnpkrstvw]\'?)?) # consonant (optional)
    '''
    # diwethRegExp matches a syllable at the end of the word
    diwetRegExp =  r'''(?x)
    (\'?(bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?\'?|dhr?\'?|dl|dr|Dl|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|s[pt]?l?|S[pt]?l?|s[mnw]|S[mn]|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfjlghpmnrstvwyzBCKDFJLGHPMNRSTVWYZ]\'?)? #consonant or c. cluster
    \'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ow|Ou|Uw|Yw|\'?[aeoiuyAEIOUY])\'? # vowel
    (lgh|ls|lt|lv|bl|br|bb|kl|kr|kn|kwr?|kk|cch|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gg|gw|gl|gn|ld|lf|lk|ll|lm|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|r\'?s|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgjklmnprstvw]\'?)? # optionally a second consonant or cluster ie CVC?
    (\-|\.|\,|;|:|\'|!|\?|\(|\))*
    )$
    '''
    # kynsaRegExp matches syllable at beginning of a word
    # 1st syllable could be CV, CVC, VC, V
    kynsaRegExp =  r'''(?x)
    ^((\'?(bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?|dhr?|dl|dr|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|gwr?|gwl?|gl|gr|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|s[pt]?l?|S[pt]?l?|s[mnw]|S[mn]|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfghjlmnprtvwyzBCKDFGHJLMNPRTVWYZ])\'?)? # optional C. 
    \'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])\'? # Vowel
    (lgh|ls|lk|ld|lf|lt|lv|lm|bb?|kk?|cch|[nr]?ch|n?dr|dh|dd?|ff?|vv?|ght|gg?h?|ll?|mp|mm?|nk|nd|nj|ns|nth?|nn?|pp?|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rj|rf|r\'?s|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw]\'?)? # optional C.
    (\-|\.|\,|;|:|\'|!|\?|\(|\))*
    )'''
    # TODO: may need some more debugging checking which consonant clusters should be
    # considered 'single' and 'double' for the purposes of vowel length
    # vowel and single consonant
    lostBK_single =  r'(.*?)(a\'?y|aw|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(ch|dh|gh|ph|sh|st|sk|th|[bkdfgjlmnprstvw])$'
    # vowel and double consonant
    lostBK_double = r'(.*?)(a\'?y|aw|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(lgh|bl|br|bb|kl|kr|kn|kw|kk|nch|cch|dl|dr|dd|ff|vv|ggh?|ll|mp|nj|mm|nk|nd|ns|nth?|nn|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rr|rv|rn|rj|rf|rs|ssh|ss|tth|tt|jj)$'

    # these regular expressions below are not really used elsewhere
    # and may not be consistent with the above.
    
    # rising dipthongs
    dewson_sevel_re = r'ya|ye|yo|yu|wa|we|wi|wo|wy'
    # falling dipthongs
    dewson_kodha_re = r'a\'?y|oy|e\'?y|aw|e\'?w|iw|ow|uw|yw'

    # word ending in vowels
    pennvog_re = r'^(.*?)(a\'?y|aw|e\'?y|eu|e\'?w|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ou|Ow|Uw|Yw|[aeoiuyAEIOUY])$'
    # word ending in consonants
    lostkess_re = r'^(.*?)(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk||cch|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|s[pt]?l?|tt?h|tt|[bdfgjklmnprstvw])$'
    # consonant-vowel sequence at the end
    lostKB_re =  r'(.*?)\'?(bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?\'?|dhr?\'?|dl|dr|Dl|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|s[pt]?l?|S[pt]?l?|s[mnw]|S[mn]|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfjlghpmnrstvwyzBCKDFJLGHPMNRSTVWYZ])(a\'?y|aw|e\'?y|eu|e\'?w|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])$'
    # vowel-consonant sequnce at the end
    lostBK_re = r'(.*?)(a\'?y|aw|e\'?y|eu|e\'?w|iw|oe|oy|ow|ou|uw|yw|A\'?y|Aw|E\'?y|Eu|E\'?w|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|cch|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgjklmnprstvw])$'

class kwKemmynDevRegExp:
    """
    holds the regular expressions to match Kernewek Kemmyn text
    
    this is a development version which will improve the way the regular expressions
    are structured
    """
    # perhaps replace these by using re.compile()?
    
    # syllabelRegExp should match syllable anywhere in a word
    # a syllable could have structure CV, CVC, VC, V
    # will now match traditional graphs c-, qw- yn syllable initial position
    syllabelRegExp = re.compile(r'''
    (\'?(bl|br|kl|kr|kn|kwr?|qwr?|ch|dhr?\'?|
    dl|dr|fl|fr|vl|vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|
    hwr?|ph|pr|pl|cy|shr?|str?|skr?|
    skw?|sbr|spr|s[pt]?l?|s[mnw]|tth|thr?|tr|tl|
    wr|wl|[bckdfjvlghmnprstwyz]) # consonant
    \'?(a\'?y|a\'?w|eu|e\'?y|e\'?w|iw|oe|oy|ow|ou|uw|yw|[aeoiuy])\'? #vowel
    (lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|
    gg?ht?|gw|gl|gn|ld|lf|lv|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|
    rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|
    [bdfgljmnpkrstvw])? # optional const.
    )| # or
    (\'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|[aeoiuy])\'? # vowel
    (lgh|ls|lt|bl|bb|kl|kr|kn|kwr?|kk|cch|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|
    gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|lm|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|
    rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|r\'?s|sh|st|sk|ss|sp?l?|tt?h|tt|
    [bdfgljmnpkrstvw]\'?)?) # consonant (optional)
    ''', re.X + re.I)
    
    # diwethRegExp matches a syllable at the end of the word
    diwetRegExp =  re.compile(r'''
    (\'?(bl|br|kl|kr|kn|kwr?|qwr?|ch|dhr?\'?|
    dl|dr|fl|fr|vl|vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|hwr?|ph|pr|pl|shr?|str?
    |skr?|skw?|sbr|spr|s[pt]?l?|s[mnw]|tth|thr?|tr|tl|wr|wl|[bckdfjlghpmnrstvwyz]\'?)? #consonant or c. cluster
    \'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|\'?[aeoiuy])\'? # vowel
    (lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|cch|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|
    gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|lm|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|
    rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|r\'?s|sh|st|sk|ss|sp?l?|tt?h|tt|
    [bdfgjklmnprstvw]\'?)? # optionally a second consonant or cluster ie CVC?
    (\-|\.|\,|\'|;|:|!|\?|\(|\))*
    )$
    ''', re.X + re.I)
    # kynsaRegExp matches syllable at beginning of a word
    # 1st syllable could be CV, CVC, VC, V
    kynsaRegExp =  re.compile(r'''
    ^((\'?(bl|br|kl|kr|kn|kwr?|qwr?|ch|dhr?|dl|dr|fl|fr|vl|vr|gwr?|gwl?|gl|gr|
    gn|hwr?|ph|pr|pl|shr?|str?|skr?|skw?|sbr|spr|s[pt]?l?|s[mnw]|tth|thr?|tr|tl|
    wr|wl|[bckdfghjlmnprtvwyz])\'?)? # optional C. 
    \'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|[aeoiuy])\'? # Vowel
    (lgh|ls|lk|ld|lf|lv|lt|bb?|kk?|cch|[nr]?ch|n?dr|dh|dd?|ff?|vv?|ght|gg?h?|ll?|lm|
    mp|mm?|nk|nd|nj|ns|nth?|nn?|pp?|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rj|rf|r\'?s|rr?|
    sh|st|sk|sp|ss?|tt?h|tt?|[jw]\'?)? # optional C.
    (\-|\.|\,|\'|;|:|!|\?|\(|\))*
    )''', re.X + re.I)
    
    # TODO: may need some more debugging checking which consonant clusters should be
    # considered 'single' and 'double' for the purposes of vowel length
    # vowel and single consonant
    lostBK_single =  re.compile(r'''(.*?)(a\'?y|aw|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|
    [aeoiuy])(ch|dh|gh|ph|sh|st|sk|th|[bkdfgjlmnprstvw])$''', re.X + re.I)
    # vowel and double consonant
    lostBK_double = re.compile(r'''(.*?)(a\'?y|aw|eu|e\'?w|e\'?y|iw|oe|oy|ow|ou|uw|yw|
    [aeoiuy])(lgh|bl|br|bb|kl|kr|kn|kw|kk|nch|cch|dl|dr|dd|ff|vv|ggh?|ll|
    mp|nj|mm|nk|nd|ns|nth?|nn|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rr|rv|rn|rj|rf|rs|
    ssh|ss|tth|tt|jj)$''', re.X + re.I)
    
    # these regular expressions below are not really used elsewhere
    # and may not be consistent with the above.
    
    # rising dipthongs
    dewson_sevel_re = re.compile(r'ya|ye|yo|yu|wa|we|wi|wo|wy', re.X)
    # falling dipthongs
    dewson_kodha_re = re.compile(r'a\'?y|oy|e\'?y|aw|e\'?w|iw|ow|uw|yw', re.X)

    # word ending in vowels
    pennvog_re = re.compile(r'''^(.*?)(a\'?y|aw|e\'?y|eu|e\'?w|iw|oe|oy|ow|ou|
    uw|yw|[aeoiuy])$''', re.X + re.I)
    # word ending in consonants
    lostkess_re = re.compile(r'''^(.*?)(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|
    cch|[nr]?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|mm|mp|
    nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|
    sh|st|sk|ss|s[pt]?l?|tt?h|tt|[bdfgjklmnprstvw])$''', re.X + re.I)
    # consonant-vowel sequence at the end
    lostKB_re =  re.compile(r'''(.*?)\'?(bl|br|kl|kr|kn|kwr?|qwr?|ch|
    dhr?\'?|dl|dr|fl|fr|vl|vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|hwr?|ph|pr|pl|
    shr?|str?|skr?|skw?|sbr|spr|s[pt]?l?|S[pt]?l?|s[mnw]|tth|thr?|tr|tl|wr|wl|
    [bckdfjlghpmnrstvwyz])
    (a\'?y|aw|e\'?y|eu|e\'?w|iw|oe|oy|ow|ou|uw|yw|[aeoiuy])$''', re.X + re.I)
    # vowel-consonant sequnce at the end
    lostBK_re = re.compile(r'''(.*?)(a\'?y|aw|e\'?y|eu|e\'?w|iw|oe|oy|ow|ou|
    uw|yw|[aeoiuy])(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|cch|[nr]?ch|dhr?|dl|n?dr|
    dd|fl|fr|ff|vl|vv|gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|
    pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|
    tt|[bdfgjklmnprstvw])$''', re.X + re.I)


class kwFSSRegExp:
    """
    will hold the regular expressions to match Standard Writen Form (Main) text
    placeholder at present
    
    it should be possible I think to match either Main or Traditional variants
    """
    
    # needs debugging FSS regexes
    
    syllabelRegExp = re.compile(r'''
    (\'?([ck][lrn]|[kq]wr?|ch|dhr?\'?|
    [bdfv][lr]|vv|ll|gwr?|gwl?|g[lr]|gg?h|gn|
    hwr?|whr?|p[hrl]|cy|shr?|str?|s[ck]r?|
    skw?|sqw|sbr|spr|s[pt]?l?|s[mnw]|tth|thr?|
    [tw][rl]|[bckdfjvlghmnprstwyz]) # consonant
    \'?(a\'?y|a\'?w|eu|e\'?y|e\'?w|iw|oo|oy|ow|ou|uw|yw|[aeoiuy])\'? #vowel
    (lgh|ls|lt|[bdfv][lr]|bb|[ck][lrn]|[ck]k|[kq]wr?|[nr]?ch|dhr?|n?dr|dd|ff|vv|
    gg?ht?|gw|gl|gn|ld|lf|lv|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|p[hrlp]|rgh?|
    rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|cy|sh|st|s[ck]|ss|sp?l?|tt?h|tt|
    [bdfglhmnpkrstvw])? # optional const.
    )| # or
    (\'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oo|oy|ow|ou|uw|yw|[aeoiuy])\'? # vowel
    (lgh|ls|lt|[bdfv][lr]|bb|[ck][lrn]|[ck]k|[kq]wr?|[nr]?ch|dhr?|n?dr|dd|ff|vv|
    gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|lm|mm|mp|nk|nd|nj|ns|nth?|nn|p[hrlp]|rgh?|
    rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|r\'?s|cy|sh|st|s[ck]|ss|sp?l?|tt?h|tt|
    [bdfglhmnpkrstvw]\'?)?) # consonant (optional)
    ''', re.X + re.I)
    
    
    # diwethRegExp matches a syllable at the end of the word
    diwetRegExp =  re.compile(r'''
    (\'?(ck[lr]|[bckdfv][lr]|[ck]n|[kq]wr?|ch|dhr?\'?|
    [dfv][lr]|vv|ll|gwr?|gwl?|g[lr]|gg?h|gn|hwr?|whr?|p[hrl]|cy|shr?|str?
    |s[ck]r?|skw?|sqw|sbr|spr|s[pt]?l?|s[mnw]|tth|thr?|[tw][rl]|ck|[bckdfjlghpmnrstvwyz]\'?)? #consonant or c. cluster
    \'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oo|oy|ow|ou|uw|yw|\'?[aeoiuy])\'? # vowel
    (lgh|ls|lt|[bdfk][lr]|bb|[ck][lrn]|[ck]k|[kq]wr?|cch|[nr]?ch|dhr?|n?dr|dd|ff|vl|vv|
    gg?ht?|gg|gw|gl|gn|ld|lf|lv|lk|ll|lm|mm|mp|nk|nd|nj|ns|nth?|nn|p[hrlp]|rgh?|
    rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|r\'?s|cy|sh|st|s[ck]|ss|sp?l?|tt?h|tt|
    [bdfgjklmnprstvw]\'?)? # optionally a second consonant or cluster ie CVC?
    (\-|\.|\,|\'|;|:|!|\?|\(|\))*
    )$
    ''', re.X + re.I)
    
    # kynsaRegExp matches syllable at beginning of a word
    # 1st syllable could be CV, CVC, VC, V
    kynsaRegExp =  re.compile(r'''
    ^((\'?(b[lr]|[ck][lrn]|[kq]wr?|ch|dhr?|[dfv][lr]|gwr?|gwl?|g[lrn]|
    hwr?|whr?|p[hrl]|cy|shr?|str?|s[ck]r?|s[kq]w|sbr|spr|s[pt]?l?|s[mnw]|tth|thr?|[tw][rl]|
    [bckdfghjlmnprtvwyz])\'?)? # optional C. 
    \'?(a\'?y|a\'?w|eu|e\'?w|e\'?y|iw|oo|oy|ow|ou|uw|yw|[aeoiuy])\'? # Vowel
    (lgh|ls|lk|ld|lf|lv|lt|[bdf][lr]|bb?|[ck][lrn]|c?k|kk|[kq]wr?|cch|[nr]?ch|n?dr|dh|
    dd?|ff?|vv?|ght|gg?h?|ll?|lm|
    mp|mm?|nk|nd|nj|ns|nth?|nn?|pp?|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rj|rf|r\'?s|rr?|
    cy|sh|st|sk|sp|ss?|tt?h|tt?|[jw]\'?)? # optional C.
    (\-|\.|\,|\'|;|:|!|\?|\(|\))*
    )''', re.X + re.I)
    
    # TODO: may need some more debugging checking which consonant clusters should be
    # considered 'single' and 'double' for the purposes of vowel length
    # may need revising for FSS
    # vowel and single consonant    
    lostBK_single =  re.compile(r'''(.*?)(a\'?y|aw|eu|e\'?w|e\'?y|iw|oo|oy|ow|ou|uw|yw|
    [aeoiuy])(ch|dh|gh|ph|cy|sh|st|sk|th|[bkdfgjlmnrsvw])$''', re.X + re.I)
    # vowel and double consonant
    lostBK_double = re.compile(r'''(.*?)(a\'?y|aw|eu|e\'?w|e\'?y|iw|oo|oy|ow|ou|uw|yw|
    [aeoiuy])(lgh|bl|br|bb|kl|kr|kn|kw|[ck]k|nch|cch|dl|dr|dd|ff|vv|ggh?|ll|ls|
    mp|nj|mm|nk|nd|ns|nth?|nn|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rr|rv|rn|rj|rf|rs|
    ssh|ss|tth|tt|jj|[pt])$''', re.X + re.I)    
    
    
class kwFSSLateRegExp:
    """
    will hold the regular expressions to match Standard Writen Form (Late) text
    placeholder at present
    
    similarly to the FSS, could either have 'main' or 'trad' spellings 
    """
    
class cyRegExp:
    """
    will hold the regular expressions to match Welsh text    

    not sure how to deal with ambiguity of w sometimes being
    semi-vowel and sometimes a vowel
    similarly i can be semi-vowel
    not sure whether all the acute and grave accented vowels actually exist    
    """
    
    syllabelRegExp = re.compile(r'''
    (\'?(c[lrn]|chl?|cwr?|si|ddr?|
    [bdfmtw][lr]|ff|ff[lr]|ll|n?gwr?|n?gwl?|g[lr]|gn|ng?h?|mh|
    chw?r?|p[hrl]|rh|si|str?|scr?|sgr?|
    sgw?|sbr|spr|s[pt]?l?|s[mnw]|th?r?|tl|w[rl]|
    [bcdfjlghmnprstwiz]) # consonant 
    \'?(ae|ai|au|aw|ei|ew|iw|oe|oi|ow|uw|[wŵ]y|yw|[aâáàeêéèoôóòiîíìuûúùyŷýỳwŵẃẁ])\'? #vowel
    (lch|ls|lt|[bdftw][lr]|bb|c[lrn]|cwr?|ddr?|n?dr|ff|
    cht?|gw|gl|gn|ld|lff?|lc|lg|llt?|mm|mp|nc|nd|ns|nth?|nn|p[hrlp]|rch?|
    rdd?|rth?|rc|rl|rff?|rh|rm|rn|rr|rs|st|sc|sg|ss|sp?l?|th|tt|
    [bcdfglhmnprstwiz])? # optional const.
    )| # or
    (\'?(ae|ai|au|aw|ei|eu|ew|iw|oe|oi|ow|uw|[wŵ]y|yw|[aâáàeêéèoôóòiîíìuûúùyŷýỳwŵẃẁ])\'? # vowel
    (lch|ld|ls|lt|[bdftw][lr]|bb|c[lrn]|cwr?|ddr?|n?dr|ff|
    cht?|gw|gl|gn|ld|lff?|lc|lg|llt?|mm|mp|nc|nd|ns|nth?|nn|p[hrlp]|rch?|
    rdd?|rth?|rc|rl|rff?|rh|rm|rn|rr|rs|st|sc|sg|ss|sp?l?|th|tt|
    [bcdfglhmnprstwiz]\'?)? # consonant (optional)
    )| # or
    (\'?(c[lrn]|chl?|cwr?|si|ddr?|
    [bdftw][lr]|ff|ff[lr]|ll|n?gwr?|n?gwl?|g[lr]|gn|ng|nh|ngh|mr|mh|
    chwr?|p[hrl]|rh|shr?|str?|scr?|sgr?|
    sgw?|sbr|spr|s[pt]?l?|s[mnw]|th?r?|tl|w[rl]|
    [bcdfjlghmnprstwiz])? # consonant
    \'?([äëïöüẅÿ])\'?) # vowel with umlaut
    ''', re.X + re.I + re.U)
    
    
    # diwethRegExp matches a syllable at the end of the word
    diwetRegExp =  re.compile(r'''
    (\'?([bcdmftw][lr]|cn|cwr?|chl?|ddr?|
    ff|ll?|n?gwr?|n?gwl?|g[lr]|gn|ng?h?|mh|chw?r?|p[hrl]|si|str?|
    s[cg]r?|sgw?|sbr|spr|s[pt]?l?|s[mnw]|th?r?|tl|w[rl]|
    [bcdfghpmnrstwiz]\'?)? #consonant or c. cluster
    \'?(ae|ai|au|aw|ei|eu|ew|iw|oe|oi|ow|uw|[wŵ]y|yw|
    \'?[aâáàeêéèoôóòiîíìuûúùyŷýỳwŵẃẁ])\'? # vowel
    (lch|ls|lt|[bdftw][lr]|bb|c[lrn]|cwr?|ddr?|n?dr|ff|
    cht?|gw|gl|gn|ld|lff?|lc|lg|llt?|mm|mp|nc|ng|nd|ns|nth?|nn|p[hrlp]|rch?|
    rdd?|rth?|rc|rg|rl|rff?|rm|rn|rr|rs|st|sc|sg|ss|sp?l?|th|tt|
    [bcdfgjlmnprstwz]\'?)? # optionally a second consonant or cluster ie CVC?
    (\-|\.|\,|\'|;|:|!|\?|\(|\))*
    )$| #or
    ((\'?(c[lrn]|chl?|cwr?|si|ddr?|
    [bdftw][lr]|ff|ff[lr]|ll|n?gwr?|n?gwl?|g[lr]|gn|ng|nh|ngh|mr|mh|
    chwr?|p[hrl]|rh|shr?|str?|scr?|sgr?|
    sgw?|sbr|spr|sp?l?|s[mnw]|th?r?|tl|w[rl]|
    [bcdfjlghmnprstwiz])\'?)? # consonant (optional)
    \'?[äëïöüẅÿ]\'? # vowel with umlaut
    (\-|\.|\,|\'|;|:|!|\?|\(|\))*
    )$''', re.X + re.I + re.U)
    
    # kynsaRegExp matches syllable at beginning of a word
    # 1st syllable could be CV, CVC, VC, V
    kynsaRegExp =  re.compile(r'''
    ^((\'?([bdm][lr]|c[lrn]|cwr?|chl?|ddr?|ff|ff?[lr]|ll|
    n?gwr?|n?gwl?|g[lrn]|ng?h?|
    chw?r?|p[hrl]|rh|si|str?|scr?|sgw?|sbr|spr|s[pt]?l?|s[mnw]|th?r?|[tw][rl]|
    [bcdfghjlmnprstwiz])\'?)? # optional C. 
    \'?(ae|ai|au|aw|ei|eu|ew|iw|oe|oi|ow|uw|[wŵ]y|yw|
    \'?[aâáàeêéèoôóòiîíìuûúùyŷýỳwŵẃẁ]\'?) # Vowel
    (lch|ls|ld|lf|ll?t?|[bdf][lr]|bb?|c[lrn]|cwr?|n?dr|
    dd?|ff?|cht?|gg?|mp|mm?|n[cg]|nd|nj|ns|nth?|nn?|pp?|
    rch?|rdd?|rth?|r[cg]|rl|rm|rn|rj|rff?|rs|rr?|
    st|s[cg]|s[bp]|ss?|tt?h?|[jwz]\'?)? # optional C.
    (\-|\.|\,|;|:|!|\?|\(|\))*
    )| #or
    ^((\'?(c[lrn]|chl?|cwr?|si|ddr?|
    [bdftw][lr]|ff|ff[lr]|ll|n?gwr?|n?gwl?|g[lr]|gn|ng|nh|ngh|mr|mh|
    chwr?|p[hrl]|rh|shr?|str?|scr?|sgr?|
    sgw?|sbr|spr|s[pt]?l?|s[mnw]|th?r?|tl|w[rl]|
    [bcdfjlghmnprstwiz])\'?) # consonant
    \'?[äëïöüẅÿ]\'? # vowel with umlaut
    (\-|\.|\,|\'|;|:|!|\?|\(|\))*
    )''', re.X + re.I + re.U)
    
    # TODO: may need some more debugging checking which consonant clusters should be
    # considered 'single' and 'double' for the purposes of vowel length
    # may need revising for FSS
    # vowel and single consonant    
    lostBK_single =  re.compile(r'''(.*?)(ae|ai|au|aw|ei|eu|ew|iw|oe|oi|ow|
    uw|[wŵ]y|yw|
    \'?[aâáàeêéèoôóòiîíìuûúùyŷýỳwŵẃẁ]\'?)
    (ch|dd|ph|st|s[cg]|th|ff|[bcdfgjlmnrswz])$''', re.X + re.I + re.U)
    # vowel and double consonant
    lostBK_double = re.compile(r'''(.*?)(ae|ai|au|aw|ei|eu|ew|iw|oe|oi|ow|
    uw|[wŵ]y|yw|
    \'?[aâáàeêéèoôóòiîíìuûúùyŷýỳwŵẃẁ]\'?)
    (lch|bl|br|bb|[cg]l|cr|cn|cw|dl|dr|ll|ls|
    mp|nj|mm|n[cg]|nd|ns|nth?|nn|pr|pl|pp|rch?|rdd?|rth?|
    r[cg]|rl|rr|rff?|rn|rj|rs|
    ss|tth|tt|jj|[pt])$''', re.X + re.I + re.U)    

    
class RannaSyllabenn:
    """
    RannaSyllabenn is a class containing methods for syllable segmentation
    """
    
    def __init__(self, inputtext):
        """
        initialize RannaSyllabenn object
        """
        # print(inputtext)
        self.inputtext = inputtext
        # nltk.word_tokenize puts these in separate words
        apos_geryow = ["'m","'s","'th"]
        # for certain words containing apostrophes like 'n
        # the apostrophe ends up in its own word
        # e.g. a-dhia'n --> ['a-dhia', "'", 'n']
        apos_geryow2 = ["n", "w", "y", "l"]
        # use NLTK to split the input text into words
        try:
            geryow = nltk.word_tokenize(inputtext)
        except AttributeError:
            print("nltk.word_tokenize() not available. Use nltk.download() in the Python shell to download Punkt Tokenizer Models.")
        # print(self.geryow)
        # go through and concatenate the 'words' beginning with apostrophes
        # to the previous word
        geryow2 = []
        for g in geryow:
            if re.search('[a-zA-Z]\-[a-zA-Z]', g):
                ### 2022-04-07 decided to remove this to
                ### avoid separating hypenated words
                ### i.e. to treat as one word
                # if there is a hyphen in the middle of the word
                # separate it to two words
                #span = re.search('[a-zA-Z]\-[a-zA-Z]', g).span()
                #index = span[1]-1
                #ger1 = g[:index]
                #ger2 = g[index:]
                #geryow2.append(ger1)
                #geryow2.append(ger2)
                geryow2.append(g)
            else:
                geryow2.append(g)
        # fix words with 'm 's 'th
        for i,g in enumerate(geryow2[:-1]):
            if geryow2[i+1] in apos_geryow:
                geryow2[i] = geryow2[i] + geryow2[i+1]
                geryow2[i+1] = ''
        # fix words with 'n 'w 'y 'l
        for i,g in enumerate(geryow2[:-2]):
            if geryow2[i+1]=="'" and geryow2[i+2] in apos_geryow2:
                geryow2[i] = geryow2[i] +"'" + geryow2[i+2]
                geryow2[i+1] = ''
                geryow2[i+2] = ''
        self.geryow = geryow2
            
    
    def ranna_syl(self,ger,regexp,fwd=True,bwd=False):
        """ divide a word into a list of its syllables
        and return this as a list of plain text strings
        """
        syl_list = []
        if fwd:
            # go forwards through the word
            while ger:
            # print(ger)
                k = self.match_syl(ger,regexp)
            # print("kynsa syl:{k}".format(k=k))
            # add the syllable to the list
                if k != '':
                    syl_list.append(k)
                if k != '' and len(ger.split(k,1))>1:
                # if there is more of the word after the
                # 1st syllable
                # remove the 1st syllable
                    ger = ger.split(k,1)[1]

                else: 
                    ger = ''
        if bwd:
            # go backwards from the end through the word
            ger0 = ger
            while ger:
                # print(ger)
                d = self.match_syl(ger,regexp)
                # print(d)
                
                # check if the syllable starts with a y followed by
                # a vowel, i.e. a semi-vowel y, and the previous syllable
                # fails to match
                semivowel_y = r'''^y[aeiou]'''
                initial_hw = r'''^hw[aeiouy]'''
                # consonants that can precede h in terminating a syllable
                # if the syllable in question starts with semi-vowel y
                if re.search(semivowel_y, d):
                    #print("semi-vowel y begins syllable {s} in word {g}".format(s=d, g=ger0))
                    ger_dalleth = ger.rsplit(d,1)[0]
                    d2 = self.match_syl(ger_dalleth, regexp)
                    if not(d2):
                        #print("failure to match regexp to {gd} in word {g}".format(gd=ger_dalleth, g=ger0))
                        #print("deleting y from beginning of syllable")
                        d = d[1:]
                elif re.search(initial_hw, d):
                    #print("hw begins syllable {s} in word {g}".format(s=d, g=ger0))
                    # without the last syllable
                    ger_dalleth = ger.rsplit(d,1)[0]
                    d2 = self.match_syl(ger_dalleth, regexp)
                    if not(d2) and ger_dalleth.strip() != "":
                        #print("failure to match regexp to {gd} in word {g}".format(gd=ger_dalleth, g=ger0))                    
                        #print("delete h from beginning of the syllable")
                        d = d[1:]
                # add the syllable to the list
                if d != '':
                    syl_list.insert(0,d)
                if d != '' and len(ger.rsplit(d,1))>1:
                # if there is more of the word before the
                # last syllable
                # remove the last syllable
                    ger = ger.rsplit(d,1)[0]
                else: 
                    ger = ''
        # this is returning
        # a list of plain text
        # not Syllabenn objects
        return syl_list

    def match_syl(self, ger, regexp):
        """ find a syllable of word
        with regexp
        use kynsaRegExp for 1st
        diwetRegExp for last
        """
        match_syl = ''
        msyl = re.search(regexp,ger)
        #print("An syllabenn matchys yw: {m}".format(m=msyl.group()))
        if msyl:
            match_syl = msyl.group()
        return match_syl
        
    def match_syl_all(self, ger, regexp, fwd=True):
        """ find all possible first or last syllables of a word
        with regexp = kynsaRegExp for 1st syllables
        regexp = diwetRegExp for last syllables
        """
        msyls = []
        match_syl = ''        
        msyl = re.search(regexp,ger)
        if msyl:
            match_syl = msyl.group()
            msyls.append(match_syl)
            while msyl:
                if fwd:
                    ger = match_syl[:-1]
                else:
                    ger = match_syl[1:]
                msyl = re.search(regexp,ger)
                if msyl:
                    match_syl = msyl.group()
                    msyls.append(match_syl)
        return msyls
        
    def diwettha_lytherenn(self,ger):
        """ return last letter of a word
        """
        d_l = ''
        if ger[-1].isalpha():
            d_l = ger[-1]
        return d_l

    def profya(self,regexps=kwKemmynRegExp):
        """ test code
        Mostly deprecated
        """
        # removya an dashow -
        # geryow = [g.replace("-","") for g in geryow]

        # Kavos an diwettha bogalenn yn pub ger yn rol mars eus bogalenn orth penn an ger 
        # i.e. match regular expression for vowel at the end of the word for a list of words
        pennvog =  [re.findall(regexps.pennvog_re,g) for g in self.geryow if (not(re.findall(regexps.pennvog_re,g)) ==[])]
        # Kavos an diwettha kessonenn yn pub ger yn rol mars eus kessonenn orth penn an ger
        # i.e. match regular expression for consonant at the end of the word for a list of words
        lostkess = [re.findall(regexps.lostkess_re,g) for g in self.geryow if (not(re.findall(regexps.lostkess_re,g))==[])]
        # Kavos an diwettha kessonenn ha bogalenn mars eus -KB orth penn an ger rag pub ger yn rol
        # i.e. match regular expression for consonant+vowel at end of the word for each word in a list
        lostKB = [re.findall(regexps.lostKB_re,g) for g in self.geryow if not(re.findall(regexps.lostKB_re,g)==[])]
        
        # this prints a list of lists of which each has one tuple as an element
        # [[(stem,lastv)],[(stem,lastv)],[(stem,lastv)]]
        # where lastv is the vowle/dipthong that ends a word
        # and stem is the rest of the word
        print("Last vowels: {p}".format(p=pennvog))
        # similarly for words that end in a consonant
        # or consonant cluster
        print("\nLast consonants: {l}".format(l=lostkess))

        # the format of lostKB is
        # [[(stem,const,lastv)],[(stem,const,lastv)]]
        # where const is a consonant cluster followed by vowel/dipthong lastv
        # and stem is the rest of the word
        print("\nLast consonant+vowel: {l}".format(l=lostKB))

        # get the stems, and last syllables out of the
        # list of lists containing tuples
        tuples = [d[0] for d in lostKB]
        stem = [t[0] for t in tuples]
        dsyl = [t[1]+t[2] for t in tuples]

        print("\nList of (stem,last syllable): {l}".format(l=list(zip(stem,dsyl))))
        
        # Kavos an diwettha bogalenn ha kessonenn mars eus -BK orth penn an ger
        # i.e. match regular expression for vowel+consonant at end of the word
        lostBK = [re.findall(regexps.lostBK_re,g) for g in self.geryow if not(re.findall(regexps.lostBK_re,g)==[])]
        
        # get the stems, and last syllables out of the
        # list of lists containing tuples
        tuples = [d[0] for d in lostBK]
        stem = [t[0] for t in tuples]
        dsyl = [t[1]+t[2] for t in tuples]
        print("\nLast vowel+consonant: {l}".format(l=lostBK))
        print("\nList of (stem,last syllable): {l}".format(l=list(zip(stem,dsyl))))

        # create list of last syllables and first syllables of list of words 'geryow'
        dsls = [self.match_syl(g,regexps.diwetRegExp) for g in self.geryow if self.match_syl(g,regexps.diwetRegExp) != '']
        print("\nLast syllables of words in list: {d}".format(d=dsls))
        ksls = [self.match_syl(g,regexps.kynsaRegExp) for g in self.geryow if self.match_syl(g,regexps.kynsaRegExp) != ''] 
        print("\nFirst syllables of words in list: {k}\n".format(k=ksls))
        # make a list of all the remainders of the words after the 1st syllable
        slserell = []
        for k,g in zip(ksls,self.geryow):
            if len(g.split(k,1)) > 1:
                slserell.append(g.split(k,1)[1])
            else:
                slserell.append('')
        # make a list of the second syllables of each word in list of words geryow
        nessasls = []
        for g in slserell:
            if self.match_syl(g,regexps.kynsaRegExp) != '':
                nessasls.append(self.match_syl(g,regexps.kynsaRegExp))
            else:
                nessasls.append('')
        geryowk = [g for g in self.geryow if self.match_syl(g,regexps.kynsaRegExp) != ''] 
        # print(zip(ksls,geryowk))
        for k,n,e,g in zip(ksls,nessasls,slserell,geryowk):
             print("Ger: {g}, an kynsa syllabenn yw: {k}, an syllabennow erell yw: {e}, an nessa syllabenn yw: {n}".format(g=g,k=k,e=e,n=n))
        print("\nWords containing rising dipthongs:")
        print([(g, re.findall(regexps.dewson_sevel_re,g)) for g in self.geryow if re.findall(regexps.dewson_sevel_re,g) != []])
        print("\nWords containing falling dipthongs:")
        print([(g, re.findall(regexps.dewson_kodha_re,g)) for g in self.geryow if re.findall(regexps.dewson_kodha_re,g) != []])
        
class Ger:
    """
    class for a word of Cornish text
    """
    def __init__(self,ger,rannans, counts, fwds=False,regexps=kwKemmynRegExp, FSSmode=False,
                 CYmode = False, gwarnya=False):
        """ initialize Ger object
        """
        if CYmode:
            self.CYmode = True # used to ensure warning displayed in Welsh if segmentation doesn't use all of input
        else:
            self.CYmode = False
        self.graph = ger # an ger kowal
        # dilea an dashow -
        # self.grapheme = self.grapheme.replace("-","")
        # dilea an . ; , ?
        # strip out punctuation characters
        #self.graph = self.graph.replace(".","")
        #self.graph = self.graph.replace(";","")
        #self.graph = self.graph.replace(",","")
        #self.graph = self.graph.replace("?","")
        #self.graph = self.graph.replace("'","")
        #self.graph = self.graph.replace(" ","")
        # print(ger)
        
        self.n_sls = 0 # niver syllabennow
        self.sls = []  # rol a syllabennow yn furv tekst
        self.slsObjs = [] # rol a daklennow syllabennow
        
        if fwds:
            # go forwards
            sls = rannans.ranna_syl(self.graph,regexps.kynsaRegExp,fwd=True,bwd=False)
        else:
            # go backwards from end 
            sls = rannans.ranna_syl(self.graph,regexps.diwetRegExp,fwd=False,bwd=True)

        # print(sls)
        self.segmented_word = ''.join(sls)
        if self.segmented_word != ger:
            if gwarnya:
                print("warning: segmentation has not processed all of input '{g}'.\nGwarnyans: ny wrug an rannans argerdhes oll an ynworrans '{g}'".format(g=ger))
                print("segmentation only processed '{s}'\nNy wrug an rannans argerdhes marnas '{s}'".format(s=self.segmented_word))
            self.completeseg = False
        else:
            self.completeseg = True
        
        self.sls = sls
        self.n_sls = len(sls)
        for s in self.sls:
            # create a Syllabenn object and append it to a list
            if CYmode:
                self.slsObjs.append(CYSyllabenn(s, rannans))
            elif FSSmode:
                self.slsObjs.append(FSSSyllabenn(s,rannans))
            else:
                self.slsObjs.append(Syllabenn(s,rannans))
        #print ("len(self.slsObjs) = {l}".format(l=len(self.slsObjs)))
        for i,s in enumerate(self.slsObjs):
            # store number of syllables in word, position in word
            # and spelling of word in attributes of the Syllabenn object
            s.nSylsGer = self.n_sls
            s.position = i+1
            s.graphGer = self.graph
            if i == self.n_sls -1:
                # check if it is the last syllable of the word
                # and flag it if it is
                s.final = True
                
        # find out which syllable is stressed        
        if len(self.slsObjs) == 1:
            # monosyllables are stressed except for a few particles etc.
            # which do not carry stress
            # print("setting stressed and monosyl")
            if self.graph.lower() in datageryow.unstressed_monosyls:
               self.slsObjs[0].stressed = False
            else:
                self.slsObjs[0].stressed = True
            # flag monosyllables
            self.slsObjs[0].monosyl = True
            # add to grand total dict
            counts.MonoSylsDict[self.graph.lower()] += 1
        elif len(self.slsObjs) > 1:
            # test for exceptions
            if self.graph[:2] == "di" and self.n_sls == 2:
                # 2 syllable words starting with di- are stressed
                # on second syllable except for a list of words
                # which are stressed on di- which is penultimate
                if not(self.graph.lower() in datageryow.words_di_stress1):
                    self.slsObjs[-1].stressed = True            
            elif self.graph.lower() in datageryow.final_syl_stress_words:
                self.slsObjs[-1].stressed = True                
            elif self.graph.lower() in datageryow.first_syl_stress_words:
                self.slsObjs[0].stressed = True
            elif self.graph.lower() in datageryow.second_syl_stress_words:
                self.slsObjs[1].stressed = True
            else:
                # penultimate stress
                self.slsObjs[-2].stressed = True
        
        # counter for total syllable length in word
        # and grand total for numbers of words
        self.hirderGer = 0
        counts.NWords += 1
        # update length arrays and total syllable length
        # after monosyl and stressed are set
        for syl in self.slsObjs:
            syl.lengtharray = syl.lengthSylParts()
            syl.syllableLength = sum(syl.lengtharray)
            self.hirderGer += syl.syllableLength
            syl.makeTupleDesc()
            # update grand total counters
            counts.NSylTotal += 1
            counts.AllSyllablesDict[syl.grapheme.lower()] += 1
            counts.AllSyllablesStructDict[syl.structure] += 1
            totalsTuple = (syl.stressed, syl.monosyl, syl.structure,
                           syl.nSylsGer, syl.final)
            counts.AllSyllablesTupleDict[totalsTuple] += 1
            if len(self.slsObjs) > 1:
                # non-monosyllable
                if syl.stressed and not(syl.final):
                    counts.StressedNonFinalSylsDict[syl.grapheme.lower()] += 1
        if len(self.slsObjs) >= 1:
            counts.StartWordSyllablesDict[self.slsObjs[0].grapheme.lower()] += 1
            counts.EndWordSyllablesDict[self.slsObjs[-1].grapheme.lower()] += 1
        
    def longoutput(self, gwarnya=False):
        """ return long output for each word"""
        line1 = "An ger yw: {g}".format(g=self.graph)
        line2 = "Niver a syllabennow yw: {n}".format(n=self.n_sls)
        line3 = "\nHag yns i: {sls}".format(sls=[s for s in self.sls])
        #line3 = "Hag yns i: {sls}".format(sls=self.sls)
        if not(gwarnya) or self.graph == self.segmented_word:
            outlines = [line1,line2,line3]
        else:
            line1point5 = self.gwarnyans(lang='bi')
            outlines = [line1,line1point5,line2,line3]
        # for each syllable, display its spelling - capitalized if stressed
        # structure (CVC/CV/VC/V)
        # list with length of syllable parts
        # total length syllable
        wholeword = ""
        for i in range(self.n_sls):
            gr = self.slsObjs[i].grapheme
            struc = self.slsObjs[i].structure
            textdesc = self.slsObjs[i].textdesc
            if self.slsObjs[i].stressed:
                gr = gr.upper()
            lenArray = self.slsObjs[i].lengtharray
            sylLength = self.slsObjs[i].syllableLength
            outlines.append("S{n}: {g}, {s}, hirder = {L}, hirder kowal = {t}. {d}".format(n=i+1,g=gr,s=struc, L = lenArray, t=sylLength, d=textdesc))
            wholeword = wholeword + gr
        # total length of syllables in word
        outlines.append("Hirder ger kowal = {H}".format(H=self.hirderGer))
        outlines.append("\n{wword}\n".format(wword=wholeword))
        return outlines
    
    def gwarnyans(self, lang="kw"):
        """ return warning if not all of word consumed """
        if not(self.completeseg):
            # not all of word consumed by regexp
            if self.CYmode:
                outtext = "Rhybudd: dydy y rhaniad ddim wedi defnyddio y gair '{g}' yn cyfan. Mae'r rhaniad wedi defnyddio dim ond '{s}'"  
            elif lang == "bi":
                outtext = "Warning: segmentation has not processed all of input '{g}'.\nGwarnyans: ny wrug an rannans argerdhes oll an ynworrans '{g}'.\nSegmentation only processed '{s}'\nNy wrug an rannans argerdhes marnas '{s}'"
            elif lang == "en":
                outtext = "Warning: segmentation has not processed all of input '{g}'. Segmentation only processed '{s}'"
            else:
                outtext = "Gwarnyans: ny wrug an rannans argerdhes oll an ynworrans '{g}'. Ny wrug an rannans argerdhes marnas '{s}'"
            outtext = outtext.format(g=self.graph, s=self.segmented_word)
            return outtext
        else:
            return ''
            
    
    def diskwedh(self, gwarnya=False):
        """ show output for each word """
        if gwarnya:
            print(self.gwarnyans(lang='bi'))        
        for l in self.longoutput():
            print(l)
        

    
    def shortoutput(self, gwarnya=False):
        """ return short output for each word 
        spelling: number of syllables """
        if gwarnya and not self.completeseg:
            return"{g}:{n}:{w}  ".format(g=self.graph, n=self.n_sls, w=self.gwarnyans(lang='kw'))
        else:
            return "{g}:{n}  ".format(g=self.graph,n=self.n_sls)
    
    def diskwedhshort(self, gwarnya=False):
        """ show short output for each word """    
        print(self.shortoutput(gwarnya=gwarnya),end="")
        
class Syllabenn(object):           
    """
    Class for syllable
    """
    def outputLabelShort(t):
        """ take tuple of the form
        (Stressed, Monosyllable, Structure, nSylsGer, Final)
        and make this into a short text string """
        if t[0]:
            stress = "S"
        else:
            stress = "s"
        if t[1]:
            mono = "M"
        else:
            mono = "m"
        struct = t[2]
        nsyls = str(t[3])
        if t[4]:
            final = "F"
        else:
            final = "f"
        outlabel = stress + mono + struct + nsyls + final
        return outlabel
            
    def __init__(self,graph,rannans,regexps=kwKemmynRegExp):
        """
        Initialize Syllabenn object
        """
        # spelling
        self.grapheme = graph
        # stressed ?
        self.stressed = False
        # monosyllable ?
        self.monosyl = False
        # rannans is the RannaSyllabenn object containing the regexp methods
        self.rannans = rannans
        # structure of syllable (CVC/VC/CV/V)
        self.structure = ''
        # match the regular expression syllabelRegExp
        syl = re.findall(regexps.syllabelRegExp,graph)        
        self.syl = syl        
        self.nSylsGer = 0
        self.position = 0
        self.final = False
        self.graphGer = ''
        self.sylparts = []
        #print(syl)
        # slice syl list to get the syllable parts
        # i.e. consonant clusters + vowels
        if len(syl) > 0:
            if syl[0][0] != '':
            # if there is a consonant at start
                sylparts = syl[0][1:4]
                # print(sylparts)
                if sylparts[2] == '': # CV i.e. no second consonant
                    sylparts = sylparts[0:2]
                    self.structure = 'CV'
                else:
                    self.structure = 'CVC'
            elif syl[0][4] != '':
            # initial vowel
                sylparts = syl[0][5:7]
                # print(sylparts)
                if sylparts[1] == '': #V alone
                    sylparts = sylparts[0:1]
                    self.structure = 'V'
                else:
                    self.structure = 'VC'
            self.sylparts = sylparts
            self.lengtharray = self.lengthSylParts()
            self.syllableLength = sum(self.lengtharray)


    def lengthSylParts(self,regexps=kwKemmynRegExp):
        """ find the lengths of each part of the syllable
        and the syllable as a whole """
        # initialise elements of lengtharray to 1
        lengtharray = list(range(len(self.sylparts)))
        lengtharray = [i*0 + 1 for i in lengtharray]
        punctchars = "'.,;:!?()-"
        graph_nopunct = self.grapheme
        for c in punctchars:
            graph_nopunct = graph_nopunct.replace(c,"")
        #print("self.structure={s}".format(s=self.structure))
        if self.structure == 'CVC':
            lengtharray[0] = 1  # hirder an kynsa kessonenn
            #print("self.monosyl={m}".format(m=self.monosyl))
            if self.monosyl:
            # mars yw unnsyllabenn:
                if re.search(regexps.lostBK_single,graph_nopunct):
                    lengtharray[1] = 3
                    #    mars yw kessonenn unnplek: bogalenn hir 
                    # ha kessonenn verr
                    lengtharray[2] = 1
                else:
                    if re.search(regexps.lostBK_double,graph_nopunct):
                        lengtharray[1] = 1
                        #    mars yw kessonenn dewblek: bogalenn verr
                        # ha kessonenn hir
                        lengtharray[2] = 2
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    if re.search(regexps.lostBK_single,graph_nopunct):
                        # mars yw kessonenn unnplek: boglenn hanterhir
                        # ha kessonenn verr
                        lengtharray[1] = 2
                        lengtharray[2] = 1
                    else:
                        if re.search(regexps.lostBK_double,graph_nopunct):
                            # mars yw kessonenn dewblek: bogalenn verr
                            # ha kessonenn hir
                            lengtharray[1] = 1
                            lengtharray[2] = 2
                        
                else:
                    # mars yw liessyllabelenn anpoesys:
                    #    bogalenn verr ha kessonenn verr
                    lengtharray[1] = 1
                    lengtharray[2] = 1

        if self.structure == 'CV':
            lengtharray[0] = 1  # hirder an kynsa kessonenn
            if self.monosyl:
                # mars yw unnsyllabenn:
                #   bogalenn hir
                lengtharray[1] = 3
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    #   bogalenn hanterhir
                    lengtharray[1] = 2
                else:
                    # mars yw liessyllabenn anpoesys:
                    #   bogalenn verr 
                    lengtharray[1] = 1

        if self.structure == 'VC':
            if self.monosyl:
                # mars yw unnsyllabenn:
                if re.search(regexps.lostBK_single,graph_nopunct):
                    lengtharray[0] = 3
                    #    mars yw kessonenn unnplek: bogalenn hir 
                    # ha kessonenn berr
                    lengtharray[1] = 1
                else:
                    if re.search(regexps.lostBK_double,graph_nopunct):
                        lengtharray[0] = 1
                        #    mars yw kessonenn dewblek: bogalenn verr
                        # ha kessonenn hir
                        lengtharray[1] = 2
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    if re.search(regexps.lostBK_single,graph_nopunct):
                        # mars yw kessonenn unnplek: boglenn hanterhir
                        lengtharray[0] = 2
                        lengtharray[1] = 1
                    else:
                        if re.search(regexps.lostBK_double,graph_nopunct):
                            # mars yw kessonenn dewblek: bogalenn berr
                            lengtharray[0] = 1
                            lengtharray[1] = 2


                else:
                    # mars yw liessyllabenn anpoesys:
                    #    bogalenn berr
                    lengtharray[0] = 1
                    lengtharray[1] = 1

        if self.structure == 'V':            
            if self.monosyl:
            # mars yw unnsyllabenn:
            # bogalenn hir
                lengtharray[0] = 3
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    # bogalenn hanterhir
                    lengtharray[0] = 2
                else:
                    # mars yw liessyllabenn anpoesys:
                    # bogalenn verr
                    lengtharray[0] = 1

        # TO DO
        # probably needs a bit of debugging to make sure 
        # regular expressions pick up single/double consts properly
        # maybe some ambiguity in how words are segmented?
        return lengtharray
        
    def makeTupleDesc(self):
        # tuple description
        tuple_desc = (self.stressed, self.monosyl, self.structure, self.nSylsGer, self.final)
        # convert to text
        self.textdesc = Syllabenn.outputLabelShort(tuple_desc)


class FSSSyllabenn(Syllabenn):     
    """
    Class for a syllable in FSS mode
    will override lengthSylParts method
    to calculate length for standard written form
    """
    
    def __init__(self, graph, rannans, regexps=kwFSSRegExp):
        """ inherit from Syllabenn class """
        # syllable structure not determined correctly at present
        # needs debugging FSS regexes
        super(FSSSyllabenn, self).__init__(graph, rannans, regexps=regexps)
        self.lengtharray = self.lengthSylParts()
        self.syllableLength = sum(self.lengtharray)
        
    def lengthSylParts(self, regexps=kwFSSRegExp):
        """ find the lengths of each part of the syllable
        and the syllable as a whole """
        # TO be written
        # initialise elements of lengtharray to 1
        lengtharray = list(range(len(self.sylparts)))
        lengtharray = [i*0 + 1 for i in lengtharray]
        punctchars = "'.,;:!?()-"
        graph_nopunct = self.grapheme
        for c in punctchars:
            graph_nopunct = graph_nopunct.replace(c,"")
        #print("self.structure={s}".format(s=self.structure))
        if self.structure == 'CVC':
            lengtharray[0] = 1  # hirder an kynsa kessonenn
            #print("self.monosyl={m}".format(m=self.monosyl))
            if self.monosyl:
            # mars yw unnsyllabenn:
                if re.search(regexps.lostBK_single,graph_nopunct):
                    lengtharray[1] = 2
                    # mars yw kessonenn unnplek: bogalenn hir 
                    # ha kessonenn verr
                    # yn FSS nyns eus bogalennow hanterhir
                    # ytho hirder yw 2 yn le 3
                    lengtharray[2] = 1
                else:
                    if re.search(regexps.lostBK_double,graph_nopunct):
                        lengtharray[1] = 1
                        # mars yw kessonenn dewblek: bogalenn verr
                        # ha kessonenn verr
                        # nyns yw geminates yn FSS
                        lengtharray[2] = 1
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    if re.search(regexps.lostBK_single,graph_nopunct):
                        # mars yw kessonenn unnplek: boglenn hir
                        # ha kessonenn verr
                        lengtharray[1] = 2
                        lengtharray[2] = 1
                    else:
                        if re.search(regexps.lostBK_double,graph_nopunct):
                            # mars yw kessonenn dewblek: bogalenn verr
                            # ha kessonenn verr
                            # nag yw geminate yn FSS
                            lengtharray[1] = 1
                            lengtharray[2] = 1
                        
                else:
                    # mars yw liessyllabelenn anpoesys:
                    #    bogalenn verr ha kessonenn verr
                    lengtharray[1] = 1
                    lengtharray[2] = 1

        if self.structure == 'CV':
            lengtharray[0] = 1  # hirder an kynsa kessonenn
            if self.monosyl:
                # mars yw unnsyllabenn:
                # bogalenn hir
                # mes 2 yn le 3 yn FSS
                lengtharray[1] = 2
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    # bogalenn hir
                    lengtharray[1] = 2
                else:
                    # mars yw liessyllabenn anpoesys:
                    # bogalenn verr 
                    lengtharray[1] = 1

        if self.structure == 'VC':
            if self.monosyl:
                # mars yw unnsyllabenn:
                if re.search(regexps.lostBK_single,graph_nopunct):
                    lengtharray[0] = 2
                    # mars yw kessonenn unnplek: bogalenn hir 
                    # mes 2 yn le 3
                    # ha kessonenn berr
                    lengtharray[1] = 1
                else:
                    if re.search(regexps.lostBK_double,graph_nopunct):
                        lengtharray[0] = 1
                        # mars yw kessonenn dewblek: bogalenn verr
                        # ha kessonenn verr
                        lengtharray[1] = 1
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    if re.search(regexps.lostBK_single,graph_nopunct):
                        # mars yw kessonenn unnplek: boglenn hir
                        lengtharray[0] = 2
                        lengtharray[1] = 1
                    else:
                        if re.search(regexps.lostBK_double,graph_nopunct):
                            # mars yw kessonenn dewblek: bogalenn verr
                            lengtharray[0] = 1
                            lengtharray[1] = 1


                else:
                    # mars yw liessyllabenn anpoesys:
                    #    bogalenn berr
                    lengtharray[0] = 1
                    lengtharray[1] = 1

        if self.structure == 'V':            
            if self.monosyl:
            # mars yw unnsyllabenn:
            # bogalenn hir
            # 2 yn le 3 yn FSS
                lengtharray[0] = 2
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    # bogalenn hir
                    lengtharray[0] = 2
                else:
                    # mars yw liessyllabenn anpoesys:
                    # bogalenn verr
                    lengtharray[0] = 1

        # TO DO
        # probably needs a bit of debugging to make sure 
        # regular expressions pick up single/double consts properly
        # maybe some ambiguity in how words are segmented?        
        return lengtharray        


class CYSyllabenn(FSSSyllabenn):     
    """
    Class for a syllable in Welsh
    subclasses the FSS mode
    placeholder

    will also need to write data in datageryow.py with 
    abnormally stressed words in Welsh
    and tell the Ger class to use it
    """
    def __init__(self, graph, rannans, regexps=cyRegExp):
        """ inherit from FSSSyllabenn class """
        # needs debugging FSS regexes
        super(CYSyllabenn, self).__init__(graph, rannans, regexps=regexps)

        # print(syl)
        # slice syl list to get the syllable parts
        # i.e. consonant clusters + vowels
        if len(self.syl) > 0:
            if self.syl[0][0] != '':
            # if there is a consonant at start
                sylparts = self.syl[0][1:4]
                # print(sylparts)
                if sylparts[2] == '': # CV i.e. no second consonant
                    sylparts = sylparts[0:2]
                    self.structure = 'CV'
                else:
                    self.structure = 'CVC'
            elif self.syl[0][7] != '':
                # syllabel uses a vowel with umlaut
                sylparts = self.syl[8:10]
                if sylparts[0] == '': # V only
                    sylparts = sylparts[1:]
                    self.structure = 'V'
                else:
                    self.structure = 'CV'
                
            elif self.syl[0][4] != '':
            # initial vowel
                sylparts = self.syl[0][5:7]
                # print(sylparts)
                if sylparts[1] == '': # V only
                    sylparts = sylparts[0:1]
                    self.structure = 'V'
                else:
                    self.structure = 'VC'
            self.sylparts = sylparts
            self.lengtharray = self.lengthSylParts()
            self.syllableLength = sum(self.lengtharray)
            
    def lengthSylParts(self, regexps=cyRegExp):
        """ find the lengths of each part of the syllable
        and the syllable as a whole """
        # needs to be rewritten and tested for Welsh
        # initialise elements of lengtharray to 1
        lengtharray = list(range(len(self.sylparts)))
        lengtharray = [i*0 + 1 for i in lengtharray]
        punctchars = "'.,;:!?()-"
        graph_nopunct = self.grapheme
        for c in punctchars:
            graph_nopunct = graph_nopunct.replace(c,"")
        #print("self.structure={s}".format(s=self.structure))
        if self.structure == 'CVC':
            lengtharray[0] = 1  # hirder an kynsa kessonenn
            #print("self.monosyl={m}".format(m=self.monosyl))
            if self.monosyl:
            # mars yw unnsyllabenn:
                if re.search(regexps.lostBK_single,graph_nopunct):
                    lengtharray[1] = 2
                    # mars yw kessonenn unnplek: bogalenn hir 
                    # ha kessonenn verr
                    # yn FSS nyns eus bogalennow hanterhir
                    # ytho hirder yw 2 yn le 3
                    lengtharray[2] = 1
                else:
                    if re.search(regexps.lostBK_double,graph_nopunct):
                        lengtharray[1] = 1
                        # mars yw kessonenn dewblek: bogalenn verr
                        # ha kessonenn verr
                        # nyns yw geminates yn FSS
                        lengtharray[2] = 1
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    if re.search(regexps.lostBK_single,graph_nopunct):
                        # mars yw kessonenn unnplek: boglenn hir
                        # ha kessonenn verr
                        lengtharray[1] = 2
                        lengtharray[2] = 1
                    else:
                        if re.search(regexps.lostBK_double,graph_nopunct):
                            # mars yw kessonenn dewblek: bogalenn verr
                            # ha kessonenn verr
                            # nag yw geminate yn FSS
                            lengtharray[1] = 1
                            lengtharray[2] = 1
                        
                else:
                    # mars yw liessyllabelenn anpoesys:
                    #    bogalenn verr ha kessonenn verr
                    lengtharray[1] = 1
                    lengtharray[2] = 1

        if self.structure == 'CV':
            lengtharray[0] = 1  # hirder an kynsa kessonenn
            if self.monosyl:
                # mars yw unnsyllabenn:
                # bogalenn hir
                # mes 2 yn le 3 yn FSS
                lengtharray[1] = 2
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    # bogalenn hir
                    lengtharray[1] = 2
                else:
                    # mars yw liessyllabenn anpoesys:
                    # bogalenn verr 
                    lengtharray[1] = 1

        if self.structure == 'VC':
            if self.monosyl:
                # mars yw unnsyllabenn:
                if re.search(regexps.lostBK_single,graph_nopunct):
                    lengtharray[0] = 2
                    # mars yw kessonenn unnplek: bogalenn hir 
                    # mes 2 yn le 3
                    # ha kessonenn berr
                    lengtharray[1] = 1
                else:
                    if re.search(regexps.lostBK_double,graph_nopunct):
                        lengtharray[0] = 1
                        # mars yw kessonenn dewblek: bogalenn verr
                        # ha kessonenn verr
                        lengtharray[1] = 1
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    if re.search(regexps.lostBK_single,graph_nopunct):
                        # mars yw kessonenn unnplek: boglenn hir
                        lengtharray[0] = 2
                        lengtharray[1] = 1
                    else:
                        if re.search(regexps.lostBK_double,graph_nopunct):
                            # mars yw kessonenn dewblek: bogalenn verr
                            lengtharray[0] = 1
                            lengtharray[1] = 1


                else:
                    # mars yw liessyllabenn anpoesys:
                    #    bogalenn berr
                    lengtharray[0] = 1
                    lengtharray[1] = 1

        if self.structure == 'V':            
            if self.monosyl:
            # mars yw unnsyllabenn:
            # bogalenn hir
            # 2 yn le 3 yn FSS
                lengtharray[0] = 2
            else:
                if self.stressed:
                    # mars yw liessyllabenn poesys:
                    # bogalenn hir
                    lengtharray[0] = 2
                else:
                    # mars yw liessyllabenn anpoesys:
                    # bogalenn verr
                    lengtharray[0] = 1

        # TO DO
        # probably needs a bit of debugging to make sure 
        # regular expressions pick up single/double consts properly
        # maybe some ambiguity in how words are segmented?
        return lengtharray        
        
        
def countSylsLine(linetext,fwd=False,mode='text',regexps=kwKemmynRegExp,
                  FSSmode=False, CYmode=False, gwarnya=False):
    """ count the total syllables in each line
    mode is either 'text', 'list' or 'nsyllist'
    to return either a string, list with words
    or just numbers of syllables """
    rannans = RannaSyllabenn(linetext)
    Nsls = 0
    outtext = ""
    outtext2 = "" #the words with stress indicted by capitalisation
    outlist = []
    outnsyllist = []
    for i in rannans.geryow:
        g = Ger(i,rannans,counts, fwd,regexps=regexps, FSSmode=FSSmode, CYmode=CYmode)
        # for each word, display it with number of syllables
        if g.graph != '':
            outtext += g.shortoutput(gwarnya=gwarnya)
            outlist.append((g.graph,g.n_sls))                        
            Nsls += g.n_sls
            outnsyllist.append((g.n_sls))
        for s in range(g.n_sls):
            gr = g.slsObjs[s].grapheme            
            if g.slsObjs[s].stressed:
                gr = gr.upper()
            else:
                gr = gr.lower()
            outtext2 += gr        
        outtext2 += " " # add space at end of each word
    
    if Nsls > 0:
        # write out number of syllables in line
        outtext += "\nNiver a sylabennow y'n linenn = {n}\n".format(n=Nsls)
        outtext += outtext2
    else:
        # except if its a completely empty line
        outtext += "\n\n"
    
    total = ("Sommenn",Nsls)
    if mode == 'list':
        return outlist, total
    elif mode == 'nsyllist':
        return outnsyllist, Nsls
    else:
        return outtext
    
def detailSylsText(intext,fwd=False,short=False,regexps=kwKemmynRegExp,
                   FSSmode=False, CYmode=False, gwarnya=False):
    outtext = ""
    rannans = RannaSyllabenn(intext)
    punctchars = ".,;:!?()-"
    for i in rannans.geryow:
        g = Ger(i,rannans,fwd, counts, regexps=regexps, FSSmode=FSSmode, CYmode=CYmode)
        # avoid printing 'words' that consist only of a
        # punctuation character
        if g.graph != '' and g.graph not in punctchars:
            if short:
                outtext += g.shortoutput(gwarnya=gwarnya)
            else:
                # print long form with syllable details
                outtext += "\n".join(g.longoutput(gwarnya=gwarnya))
                outtext += "\n\n"
    return outtext

def totalcountsOutput(counts):
    outtext = ""
    # sort dictionaries
    counts.keyvaltups()
    
    outtext += "\n\nTotal number of syllables = {t}\n".format(t = counts.NSylTotal)
    outtext += "\nAll syllables = \n{A}\n".format(A = counts.AllSyllablesDSortText)
    outtext += "\nSyllables starting a word = \n{S}\n".format(S = counts.StartWordSyllablesDSortText)
    outtext += "\nSyllables ending a word = \n{E}\n".format(E = counts.EndWordSyllablesDSortText)
    outtext += "\nMonosyllables = \n{M}\n".format(M = counts.MonoSylsDSortText)
    outtext += "\nStressed non-final syllables = \n{s}\n".format(s = counts.StressedNonFinalSylsDSortText)
    return outtext
    
    

if __name__ == '__main__':
    """
    If invoked at the command-line
    """
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    # take the input from a file specified
    # by a command line argument
    parser.add_argument("inputfile", type=str,
                         help="Specify the input text file containing Cornish text.")
    parser.add_argument("--test",action="store_true",
                        help="Test mode. Run test code.")
    parser.add_argument("--fwd",action="store_true",
                        help="Use forward segmentation. Default is backward, starting from end of word.")
    parser.add_argument("--line",action="store_true",
                        help="Line by line mode. Counts syllables in each line, and uses shorter reporting of each word.")
    parser.add_argument("--short",action="store_true",
                        help="Short output for each word, i.e. only number of syllables, rather than details and syllable lengths")
    parser.add_argument("--devregexp", action="store_true",
                        help="Use the development KK regular expressions rather than standard")
    parser.add_argument("--fssregexp", action="store_true",
                        help="Use the FSS/Standard Written form regular expressions rather than standard. takes priority over --devregexp.")
    parser.add_argument("--cyregexp", action="store_true",
                        help="Use Welsh regular expressions. Takes priority over other regexp options.")
    parser.add_argument("--warn", action="store_true",
                        help="Display warnings if words not fully consumed by regular expressions. Default is not to do so")
    parser.add_argument("--totalcounts", action="store_true",
                        help="Display the grand total numbers of syllables etc.")
    args = parser.parse_args()
    # Check that the input parameter has been specified.
    if args.inputfile == None:
        # Print an error message if not and exit.
        print("Error: No input file provided.")
        sys.exit()
        
    f = codecs.open(args.inputfile,"r",encoding="utf-8",errors="replace")
    if args.cyregexp:
        if sys.version_info[0] < 3:
            print("Python 3 advised for Welsh text, to correctly process non-ASCII letters")
        regexps = cyRegExp
    elif args.fssregexp:
        regexps = kwFSSRegExp
    elif args.devregexp:
        regexps = kwKemmynDevRegExp
    else:
        regexps = kwKemmynRegExp
    # create object to count all syllables
    counts = CountAllSyls()
    # create list of Ger objects
    listGer = []
    # list of lists of Ger objects
    listGer_lines = []
    if args.line:
            inputtext = f.readlines()            
            for n,line in enumerate(inputtext):
                line = preprocess2ASCII(line)
                #line = line.encode('utf-8')
                print("Linenn {l}".format(l=n+1))
                rannans = RannaSyllabenn(line)
                # run test code if --test argument has been used
                if args.test:
                    rannans.profya()
                # count the total syllables in each line
                Nsls = 0
                # list of Ger objets
                listGer_line = []
                for i in rannans.geryow:
                    g = Ger(i,rannans, counts, args.fwd, regexps=regexps,
                            FSSmode=args.fssregexp,
                            CYmode=args.cyregexp, gwarnya=args.warn)
                    listGer_line.append(g)
                    listGer.append(g)
                    # for each word, display it with number of syllables
                    if g.graph != '':
                        g.diskwedhshort(gwarnya=args.warn)
                        Nsls += g.n_sls                        
                print("\nNiver a sylabennow y'n linenn = {n}\n".format(n=Nsls))
                listGer_lines.append(listGer_line)
    else:
        inputtext = f.read()
        inputtext = preprocess2ASCII(inputtext)
        #inputtext = inputtext.encode('utf-8')
        rannans = RannaSyllabenn(inputtext)
        # run test code if --test argument has been used
        if args.test:
            rannans.profya()

        punctchars = ".,;:!?()-"
        for i in rannans.geryow:
            g = Ger(i,rannans, counts, args.fwd, regexps=regexps,
                    FSSmode=args.fssregexp,
                    CYmode=args.cyregexp, gwarnya=args.warn)
            # avoid printing 'words' that consist only of a
            # punctuation character
            if g.graph != '' and g.graph not in punctchars:
                listGer.append(g)
                if args.short:
                    # print short form word:nsyls
                    g.diskwedhshort(gwarnya=args.warn)
                else:
                    # print long form with syllable details
                    g.diskwedh(gwarnya=args.warn)
                    print('\n')
    if args.totalcounts:
        print(totalcountsOutput(counts))
        
