#!/usr/bin/python
# -*- coding: utf-8 -*-
# David Trethewey 03-04-2015 Open Source GPL
#
# A rough and ready hacked together segmentation of Cornish (Kernewek Kemmyn) text 
# to the syllable level using regular expressions. 
#
# 
# In future I will try to make one for the Standard Written Form of Cornish
# with an idea to use this to do transliteration between the orthographies.
#
# Usage: python sylabelenn_ranna_kw.py --test <inputfile>
# where <inputfile> is the path to an input file containing 
# text in Kernewek Kemmyn
# --test is an optional flag to run the test routines in profya()
import nltk
import sys
import string
import re
import copy
import argparse

class RannaSyllabelenn:
    def __init__(self, inputtext):
	    # syllabelRegExp should match syllable anywhere
        # a syllable could be CV, CVC, VC, V
	self.syllabelRegExp = r'''(?x)
((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kw|Kw|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gg?h|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|hw?|Hw?|pr|pl?|Pr|Pl?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bkdjlmnrtwyBKDJLMNRTVWY]) #consonant or c cluster
(ay|aw|eu|ey|ew|iw|oe|oy|ow|ou|uw|yw|[aeoiuy]) #vowel
(lgh|bl|br|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tt?|[jw])? #optionally a second consonant or cluster ie CVC?
)| #or VC:
((ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])#vowel
(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tt?|[jw])? #consonant
	'''
	self.diwetRegexp =  r'''(?x)
(((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kw|Kw|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gg?h|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|hw?|Hw?|pr|pl?|Pr|Pl?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bkdjlmnrtwyBKDJLMNRTVWY]) #consonant or c cluster
(ay|aw|eu|ey|ew|iw|oe|oy|ow|ou|uw|yw|[aeoiuy]) #vowel
(lgh|bl|br|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tt?|[jw])? #optionally a second consonant or cluster ie CVC?
)| #or
((ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])#vowel
(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tt?|[jw])?))$ #should be the same as before  but just match at end of string
'''
        # 1st syllable could be CV, CVC, VC, V
	self.kynsaRegexp =  r'''(?x)
(^((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kw|Kw|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|hw?|Hw?|pr|pl?|Pr|Pl?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bkdjlmnrtwyBKDJLMNRTVWY]) #C
(ay|aw|eu|ey|ew|iw|oe|oy|ow|ou|uw|yw|[aeoiuy]) #V
(lgh|bl|br|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tl|tt?|[jw])?#optional C
))| #or
(^((ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY]))(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tl|tt?|[jw])? #VC?
)|(\-)(.*?)'''	
        self.dewson_sevel_re = r'ya|ye|yo|yu|wa|we|wi|wo|wy'
        self.dewson_kodha_re = r'ay|oe|oy|ey|aw|ew|iw|ow|uw|yw'
        self.pennvog_re = r'^(.*?)(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ou|Ow|Uw|Yw|[aeoiuyAEIOUY])$'
        self.lostkess_re = r'^(.*?)(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tt?|[jw])$'
        self.lostKB_re =  r'(.*?)(bl|br|Bl|Br|bb?|kl|Kl|kr|Kr|kn|Kn|kw|Kw|kk?|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|dd?|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gg?h|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|ll?|mm?|nd|ns|nn?|hw?|Hw?|pr|pl?|Pr|Pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|thr?|Thr?|tr|Tr|tl|Tl|tt?|wr|Wr|wl|Wl|[jwyBKDLJMNRTVWY])(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])$'
        self.lostBK_re = r'(.*?)(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|th|tt?|[jw])$'
        #print inputtext
        self.geryow = nltk.word_tokenize(inputtext)
        #print geryow
	
    def ranna_syl(self,ger):
        # divide a word into a list of its syllables
        # and return this
        syl_list = []
        while ger:
            # print ger
            k = kynsa_syl(ger,self.kynsaRegexp)
            syl_list.append(k)
            if len(ger.split(k,1))>1:
                ger = ger.split(k,1)[1]
            else: 
                ger = ''
        return syl_list

    def diwettha_syl(self,ger, regexp):
        # find last syllable of a word
        diwettha_syl = ''
        # take off a trailing hyphen 
        if ger[-1] == '-':
            ger = ger[:-1]
        dsyl = re.findall(regexp,ger) 
        print dsyl
        if not(dsyl == []):
            diwettha_syl=dsyl[0][1]
        return diwettha_syl

    def kynsa_syl(self, ger, regexp):
        # find 1st syllable of word
        kynsa_syl = ''
        # print ger
        # take off an initial hyphen from the syllable
        if ger != '' and ger[0] == '-':
            ger = ger[1:]
        # print ger
        ksyl = re.findall(regexp,ger)
        # print "An kynsa sylabellen yw:", ksyl
        if not(ksyl == []):
            kynsa_syl = ksyl[0][1]+ksyl[0][5]
        return kynsa_syl

    def diwettha_lytherenn(self,ger):
        # return last letter of a word
        d_l = ''
        if ger[-1].isalpha():
            d_l = ger[-1]
        return d_l

    def profya(self, geryow):
        # removya an dashow -
        #geryow = [g.replace("-","") for g in geryow]
        # Kavos an diwettha bogalenn yn ger mars eus bogalenn orth penn an ger 
        # i.e. match regular expression for vowel at the end of the word for a list of words
        pennvog =  [re.findall(self.pennvog_re,g) for g in geryow if (not(re.findall(self.pennvog_re,g)) ==[])]
        # Kavos an diwettha kessonenn yn ger mars eus kessonenn orth penn an ger
        # i.e. match regular expression for consonant at the end of the word for a list of words
        lostkess = [re.findall(self.lostkess_re,g) for g in geryow if (not(re.findall(self.lostkess_re,g))==[])]
        # Kavos an diwettha kessonenn ha bogalenn mars eus -KB orth penn an ger
        # i.e. match regular expression for consonant+vowel at end of the word
        lostKB = [re.findall(self.lostKB_re,g) for g in geryow if not(re.findall(self.lostKB_re,g)==[])]
        #print pennvog
        #print lostkess
        tuples = [d[0] for d in lostKB]
        stem = [t[0] for t in tuples]
        dsyl = [t[1]+t[2] for t in tuples]
        #print lostkessvog
        #print zip(stem,dsyl)
        # Kavos an diwettha bogalenn ha kessonenn mars eus -BK orth penn an ger
        # i.e. match regular expression for vowel+consonant at end of the word
        lostBK = [re.findall(self.lostBK_re,g) for g in geryow if not(re.findall(self.lostBK_re,g)==[])]
        tuples = [d[0] for d in lostBK]
        stem = [t[0] for t in tuples]
        dsyl = [t[1]+t[2] for t in tuples]
        #print lostvogkess
        #print zip(stem,dsyl)
        # create list of last syllables and first syllables of list of words geryow
        dsls = [self.diwettha_syl(g,self.diwetRegexp) for g in geryow if self.diwettha_syl(g,self.diwetRegexp) != '']
        print dsls
        ksls = [self.kynsa_syl(g,self.kynsaRegexp) for g in geryow if self.kynsa_syl(g,self.kynsaRegexp) != ''] 
        print ksls
        # make a list of all the remainders of the words after the 1st syllable
        slserell = []
        for k,g in zip(ksls,geryow):
            if len(g.split(k,1)) > 1:
                slserell.append(g.split(k,1)[1])
            else:
                slserell.append('')
        # make a list of the second syllables of each word in list of words geryow
        nessasls = []
        for g in slserell:
            if self.kynsa_syl(g,self.kynsaRegexp) != '':
                nessasls.append(self.kynsa_syl(g,self.kynsaRegexp))
            else:
                nessasls.append('')

        print slserell
        print nessasls
        geryowk = [g for g in geryow if self.kynsa_syl(g,self.kynsaRegexp) != ''] 
        #print zip(ksls,geryowk)
        for k,n,e,g in zip(ksls,nessasls,slserell,geryowk):
            print "Ger:",g,"an kyns sylabellen yw:",k,"an sylabelennow erell yw:",e,"an nessa sylabelenn yw:",n
        #print [(g, re.findall(dewson_sevel_re,g)) for g in geryow if re.findall(dewson_sevel_re,g) != []]

class Ger:
    # class for a word of Cornish text
    def __init__(self,ger):
        self.ger = ger # an ger kowal
        # dilea an dashow -
        # self.ger = self.ger.replace("-","")
        # dilea an . ; , ?
        # strip out punctuation characters
        self.ger = self.ger.replace(".","")
        self.ger = self.ger.replace(";","")
        self.ger = self.ger.replace(",","")
        self.ger = self.ger.replace("?","")
        self.ger = self.ger.replace("'","")
        self.ger = self.ger.replace(" ","")
        # print ger
        self.n_sls = 0 # niver sylabelennow
        self.sls = []  # rol a sylabelennow
        gergesys = self.ger # rann an ger yw gesys
        while gergesys != '':
            k = rannans.kynsa_syl(gergesys,rannans.kynsaRegexp)
            self.sls.append(copy.copy(k))
            if (len(k)>0) and (len(gergesys.split(k,1))>1):
                gergesys = gergesys.split(k,1)[1]
            else:
                gergesys = ''
            self.n_sls = self.n_sls + 1
    def diskwedh(self):
        # show output for each word
        print "An ger yw:",self.ger
        print "Niver a sylabelennow yw:",self.n_sls
        print "Hag yns i:"
        print self.sls
        for i in range(self.n_sls):
            print i+1, ":",self.sls[i]
            

if __name__ == '__main__':
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    # take the input from a file specified
    # by a command line argument
    parser.add_argument("inputfile", type=str,
                         help="Specify the input text file containing Cornish text.")
    parser.add_argument("--test",action="store_true",
                        help="Test mode. Run test code.")
    args = parser.parse_args()
    # Check that the input parameter has been specified.
    if args.inputfile == None:
        # Print an error message if not and exit.
        print "Error: No input image file provided."
        sys.exit()
    inputfile = args.inputfile
    inputtext = file(inputfile).read()
    rannans = RannaSyllabelenn(inputtext)
    # run test code if --test argument has been used
    if args.test:
        rannans.profya(rannans.geryow)
    for i in rannans.geryow:
        g = Ger(i)
        if g.ger != '':
            g.diskwedh()
            print('\n')
