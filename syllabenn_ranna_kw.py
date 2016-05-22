#!/usr/bin/python
# -*- coding: utf-8 -*-
# David Trethewey 06-05-2016 
# code is Open Source (GPL)
#
# A rough and ready hacked together segmentation of Cornish (Kernewek Kemmyn) text 
# to the syllable level using regular expressions. 
#
# This version makes a calculation of syllable length
# taking 1 unit as short vowel, 2 as a half-long, 3 as long
# 1 a normal consonant and 2 as a gemminated double consonant
# e.g. mm in kamm
# 
#
# This module is used by the module treuslytherenna.py to convert Kernewek Kemmyn
# text to the Standard Written Form
#
# Usage: python syllabenn_ranna_kw.py --test <inputfile>
# where <inputfile> is the path to an input file containing 
# text in Kernewek Kemmyn
# --test is an optional flag to run the test routines in profya()
# --fwd uses segmentation starting from the beginning of each word, rather than
# starting from the end and working backwards
# --short causes it to do a shorter reporting method simply listing each
# word and its number of syllables
# --line causes it to step through the input file line by line, and count the number of syllables
# in the whole line

from __future__ import print_function
import nltk
import sys
import re
import argparse
import codecs
import datageryow
reload(sys)
sys.setdefaultencoding('utf-8')

class kwKemmynRegExp:
    """
    holds the regular expressions to match Kernewek Kemmyn text
    """
    # perhaps replace these by using re.compile()?
    
    # syllabelRegExp should match syllable anywhere in a word
    # a syllable could have structure CV, CVC, VC, V
    # will now match traditional graphs c-, qw- yn syllable initial position
    syllabelRegExp = r'''(?x)
    ((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?\'?|dhr?\'?|dl|dr|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|sp?l?|Sp?l?|sm|Sm|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfjvlghmnprstwyzBCKDFJVLGHMNPRSTVWZY]) # consonant
    \'?(ay|a\'?w|eu|ey|ew|iw|oe|oy|ow|ou|uw|yw|[aeoiuy])\'? #vowel
(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|n?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gw|gl|gn|ld|lf|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgljmnpkrstvw])? #  optional const.
    )| # or
    (\'?(ay|a\'?w|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])\'? # vowel
    (lgh|ls|lt|bl|bb|kl|kr|kn|kwr?|kk|cch|n?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gw|gl|gn|ld|lf|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgljmnpkrstvw]\'?)?) # consonant (optional)
    '''
    # diwethRegExp matches a syllable at the end of the word
    diwetRegexp =  r'''(?x)
    ((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?\'?|dhr?\'?|dl|dr|Dl|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|sp?l?|Sp?l?|sm|Sm|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfjlghpmnrstvwyzBCKDFJLGHPMNRSTVWYZ]\'?)? #consonant or c. cluster
    \'?(ay|a\'?w|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|\'?[aeoiuyAEIOUY]\'?) # vowel
    (lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|cch|n?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gw|gl|gn|ld|lf|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgjklmnprstvw]\'?)? # optionally a second consonant or cluster ie CVC?
    (\-|\.|\,|;|:|!|\?|\(|\))*
    )$
    '''
    # kynsaRegexp matches syllable at beginning of a word
    # 1st syllable could be CV, CVC, VC, V
    kynsaRegexp =  r'''(?x)
    ^((\'?(bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?|dhr?|dl|dr|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|gwr?|gwl?|gl|gr|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|sp?l?|Sp?l?|sm|Sm|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfghjlmnprtvwyzBCKDFGHJLMNPRTVWYZ])\'?)? # optional C. 
    \'?(ay|a\'?w|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])\'? # Vowel
    (lgh|ls|lk|ld|lf|lt|bb?|kk?|cch|n?ch|n?dr|dh|dd?|ff?|vv?|ght|gg?h?|ll?|mp|mm?|nk|nd|nj|ns|nth?|nn?|pp?|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rj|rf|rs|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw]\'?)? # optional C.
    (\-|\.|\,|;|:|!|\?|\(|\))*
    )'''

    # these regular expressions below are not really used elsewhere
    # and may not be consistent with the above.
    
    # rising dipthongs
    dewson_sevel_re = r'ya|ye|yo|yu|wa|we|wi|wo|wy'
    # falling dipthongs
    dewson_kodha_re = r'ay|oy|ey|aw|ew|iw|ow|uw|yw'

    # word ending in vowels
    pennvog_re = r'^(.*?)(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ou|Ow|Uw|Yw|[aeoiuyAEIOUY])$'
    # word ending in consonants
    lostkess_re = r'^(.*?)(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk||cch|n?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gw|gl|gn|ld|lf|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgjklmnprstvw])$'
    # consonant-vowel sequence at the end
    lostKB_re =  r'(.*?)(bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kwr?|Kwr?|qwr?|Qwr?|ch|Ch|Dhr?\'?|dhr?\'?|dl|dr|Dl|Dr|fl|Fl|fr|Fr|vl|Vl|vr|Vr|vv|ll|gwr?|gwl?|gl|gr|gg?h|gn|Gwr?|Gwl?|Gl|Gr|Gn|hwr?|Hwr?|ph|Ph|pr|pl|Pr|Pl|shr?|Shr?|str?|Str?|skr?|Skr?|skw?|Skw?|sbr|Sbr|spr|Spr|sp?l?|Sp?l?|sm|Sm|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bckdfjlghpmnrstvwyzBCKDFJLGHPMNRSTVWYZ])(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])$'
    # vowel-consonant sequnce at the end
    lostBK_re = r'(.*?)(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(lgh|ls|lt|bl|br|bb|kl|kr|kn|kwr?|kk|cch|n?ch|dhr?|dl|n?dr|dd|fl|fr|ff|vl|vv|gg?ht?|gw|gl|gn|ld|lf|lk|ll|mm|mp|nk|nd|nj|ns|nth?|nn|ph|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rv|rm|rn|rr|rj|rf|rs|sh|st|sk|ss|sp?l?|tt?h|tt|[bdfgjklmnprstvw])$'
    # TODO: may need some more debugging checking which consonant clusters should be
    # considered 'single' and 'double' for the purposes of vowel length
    # vowel and single consonant
    lostBK_single =  r'(.*?)(ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(ch|dh|gh|ph|sh|st|sk|th|[bkdfgjlmnprstvw])$'
    # vowel and double consonant
    lostBK_double = r'(.*?)(ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(lgh|bl|br|bb|kl|kr|kn|kw|kk|nch|cch|dl|dr|dd|ff|vv|ggh|ll|mp|nj|mm|nk|nd|ns|nth?|nn|pr|pl|pp|rgh?|rdh?|rth?|rk|rl|rr|rv|rn|rj|rf|rs|ssh|ss|tth|tt|jj)$'

                        
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
        # use NLTK to split the input text into words
        geryow = nltk.word_tokenize(inputtext)
        # print(self.geryow)
        # go through and concatenate the 'words' beginning with apostrophes
        # to the previous word
        for i,g in enumerate(geryow[:-1]):
            if geryow[i+1] in apos_geryow:
                geryow[i] = geryow[i] + geryow[i+1]
                geryow[i+1] = ''
        self.geryow = geryow
            
	
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
            while ger:
                # print(ger)
                d = self.match_syl(ger,regexp)
                # print(d)
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
        use kynsaRegexp for 1st
        diwetRegexp for last
        """
        match_syl = ''
        msyl = re.search(regexp,ger)
        #print("An syllabenn matchys yw: {m}".format(m=msyl.group()))
        if msyl:
            match_syl = msyl.group()
        return match_syl

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

        print("\nList of (stem,last syllable): {l}".format(l=zip(stem,dsyl)))
        
        # Kavos an diwettha bogalenn ha kessonenn mars eus -BK orth penn an ger
        # i.e. match regular expression for vowel+consonant at end of the word
        lostBK = [re.findall(regexps.lostBK_re,g) for g in self.geryow if not(re.findall(regexps.lostBK_re,g)==[])]
        
        # get the stems, and last syllables out of the
        # list of lists containing tuples
        tuples = [d[0] for d in lostBK]
        stem = [t[0] for t in tuples]
        dsyl = [t[1]+t[2] for t in tuples]
        print("\nLast vowel+consonant: {l}".format(l=lostBK))
        print("\nList of (stem,last syllable): {l}".format(l=zip(stem,dsyl)))

        # create list of last syllables and first syllables of list of words 'geryow'
        dsls = [self.match_syl(g,regexps.diwetRegexp) for g in self.geryow if self.match_syl(g,regexps.diwetRegexp) != '']
        print("\nLast syllables of words in list: {d}".format(d=dsls))
        ksls = [self.match_syl(g,regexps.kynsaRegexp) for g in self.geryow if self.match_syl(g,regexps.kynsaRegexp) != ''] 
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
            if self.match_syl(g,regexps.kynsaRegexp) != '':
                nessasls.append(self.match_syl(g,regexps.kynsaRegexp))
            else:
                nessasls.append('')
        geryowk = [g for g in self.geryow if self.match_syl(g,regexps.kynsaRegexp) != ''] 
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
    def __init__(self,ger,rannans,fwds=False,regexps=kwKemmynRegExp):
        """ initialize Ger object
        """
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
            sls = rannans.ranna_syl(self.graph,regexps.kynsaRegexp,fwd=True,bwd=False)
        else:
            # go backwards from end 
            sls = rannans.ranna_syl(self.graph,regexps.diwetRegexp,fwd=False,bwd=True)

        # print(sls)
        self.sls = sls
        self.n_sls = len(sls)
        for s in self.sls:
            # create a Syllabenn object and append it to a list
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
        self.hirderGer = 0
        # update length arrays and total syllable length
        # after monosyl and stressed are set
        for syl in self.slsObjs:
            syl.lengtharray = syl.lengthSylParts()
            syl.syllableLength = sum(syl.lengtharray)
            self.hirderGer += syl.syllableLength

    def longoutput(self):
        """ return long output for each word"""
        line1 = "An ger yw: {g}".format(g=self.graph)
        line2 = "Niver a syllabennow yw: {n}".format(n=self.n_sls)
        line3 = "Hag yns i: {sls}".format(sls=[s.encode("ascii") for s in self.sls])
        outlines = [line1,line2,line3]
        # for each syllable, display its spelling - capitalized if stressed
        # structure (CVC/CV/VC/V)
        # list with length of syllable parts
        # total length syllable
        for i in range(self.n_sls):
            gr = self.slsObjs[i].grapheme
            struc = self.slsObjs[i].structure
            if self.slsObjs[i].stressed:
                gr = gr.upper()
            lenArray = self.slsObjs[i].lengtharray
            sylLength = self.slsObjs[i].syllableLength
            outlines.append("S{n}: {g}, {s}, hirder = {L}, hirder kowal = {t}".format(n=i+1,g=gr,s=struc, L = lenArray, t=sylLength))
        # total length of syllables in word
        outlines.append("Hirder ger kowal = {H}".format(H=self.hirderGer))
        return outlines
            
    def diskwedh(self):
        """ show output for each word """
        for l in self.longoutput():
            print(l)

    def shortoutput(self):
        """ return short output for each word 
        spelling: number of syllables """
        return "{g}:{n}  ".format(g=self.graph,n=self.n_sls)
    
    def diskwedhshort(self):
        """ show short output for each word """    
        print(self.shortoutput(),end="")
        
class Syllabenn:           
    """
    Class for syllable
    """
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
        # print(syl)
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
        lengtharray = range(len(self.sylparts))
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
    
def countSylsLine(linetext,fwd=False,mode='text'):
    """ count the total syllables in each line
    mode is either 'text', 'list' or 'nsyllist'
    to return either a string, list with words
    or just numbers of syllables """
    rannans = RannaSyllabenn(linetext)
    Nsls = 0
    outtext = ""
    outlist = []
    outnsyllist = []
    for i in rannans.geryow:
        g = Ger(i,rannans,fwd)
        # for each word, display it with number of syllables
        if g.graph != '':
            outtext += g.shortoutput()
            outlist.append((g.graph,g.n_sls))            
            Nsls += g.n_sls
            outnsyllist.append((g.n_sls))
    outtext += "\nNiver a sylabennow y'n linenn = {n}".format(n=Nsls)
    total = ("Sommenn",Nsls)
    if mode == 'list':
        return outlist, total
    elif mode == 'nsyllist':
        return outnsyllist, Nsls
    else:
        return outtext
    

def detailSylsText(intext,fwd=False,short=False):
    outtext = ""
    rannans = RannaSyllabenn(intext)
    punctchars = ".,;:!?()-"
    for i in rannans.geryow:
        g = Ger(i,rannans,fwd)
        # avoid printing 'words' that consist only of a
        # punctuation character
        if g.graph != '' and g.graph not in punctchars:
            if short:
                outtext += g.shortoutput()
            else:
                # print long form with syllable details
                outtext += "\n".join(g.longoutput())
                outtext += "\n\n"
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
    args = parser.parse_args()
    # Check that the input parameter has been specified.
    if args.inputfile == None:
        # Print an error message if not and exit.
        print("Error: No input file provided.")
        sys.exit()
        
    f = codecs.open(args.inputfile,"r",encoding="utf-8",errors="replace")
    if args.line:
            inputtext = f.readlines()
            for n,line in enumerate(inputtext):
                #line = line.encode('utf-8')
                print("Linenn {l}".format(l=n+1))
                rannans = RannaSyllabenn(line)
                # run test code if --test argument has been used
                if args.test:
                    rannans.profya()
                # count the total syllables in each line
                Nsls = 0
                for i in rannans.geryow:
                    g = Ger(i,rannans,args.fwd)
                    # for each word, display it with number of syllables
                    if g.graph != '':
                        g.diskwedhshort()
                        Nsls += g.n_sls
                print("\nNiver a sylabennow y'n linenn = {n}\n".format(n=Nsls))
    else:
        inputtext = f.read()
        #inputtext = inputtext.encode('utf-8')
        rannans = RannaSyllabenn(inputtext)
        # run test code if --test argument has been used
        if args.test:
            rannans.profya()

        punctchars = ".,;:!?()-"
        for i in rannans.geryow:
            g = Ger(i,rannans,args.fwd)
            # avoid printing 'words' that consist only of a
            # punctuation character
            if g.graph != '' and g.graph not in punctchars:
                if args.short:
                    # print short form word:nsyls
                    g.diskwedhshort()
                else:
                    # print long form with syllable details
                    g.diskwedh()
                    print('\n')
