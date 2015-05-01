#!/usr/bin/python
# -*- coding: utf-8 -*-
# David Trethewey 01-05-2015 
# code is Open Source (GPL)
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
    """
    RannaSyllabelenn is a class containing methods for syllable segmentation
    """
    
    # syllabelRegExp should match syllable anywhere in a word
    # a syllable could be CV, CVC, VC, V	
    syllabelRegExp = r'''(?x)
    ((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kw|Kw|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gg?h|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|hw?|Hw?|pr|pl?|Pr|Pl?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bkdjlmnrtwyBKDJLMNRTVWY]) # consonant
    (ay|aw|eu|ey|ew|iw|oe|oy|ow|ou|uw|yw|[aeoiuy])
(lgh|bl|br|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nt|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])? # vowel (optional)
    )| # or
    ((ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY]) # vowel
    (lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nt|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])?) # consonant (optional)
    '''

    # diwethRegExp matches a syllable at the end of the word
    diwetRegexp =  r'''(?x)
    ((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kw|Kw|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gg?h|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|hw?|Hw?|pr|pl?|Pr|Pl?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bkdjlmnrtwyBKDJLMNRTVWY])? #consonant or c. cluster
    (ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY]) # vowel
    (lgh|bl|br|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nt|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])? # optionally a second consonant or cluster ie CVC?
    )$
    '''
    #| # or
    #((ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])#vowel
    #(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nt|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])?)$ # C. same as before but only match at end of string
    
    # kynsaRegexp matches syllable at beginning of a word
    # 1st syllable could be CV, CVC, VC, V
    kynsaRegexp =  r'''(?x)
    (^((bl|br|Bl|Br|kl|Kl|kr|Kr|kn|Kn|kw|Kw|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|hw?|Hw?|pr|pl?|Pr|Pl?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|wr|Wr|wl|Wl|[bkdjlmnrtwyBKDJLMNRTVWY]) # C. matching only at start of string 
    (ay|aw|eu|ey|ew|iw|oe|oy|ow|ou|uw|yw|[aeoiuy]) # Vowel
    (lgh|bb?|kk?|ch|dh|dd?|ff?|vv?|gg?h?|ll?|mm?|nd|ns|nt|nn?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])? # optional C.
    ))| # or
    (^((ay|aw|eu|ew|ey|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY]))(lgh|bb?|kk?|ch|dh|dd?|ff?|vv?|gg?h?|ll?|mm?|nd|ns|nt|nn?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])? # VC?
)|(\-)(.*?)'''	
    # rising dipthongs
    dewson_sevel_re = r'ya|ye|yo|yu|wa|we|wi|wo|wy'
    # falling dipthongs
    dewson_kodha_re = r'ay|oe|oy|ey|aw|ew|iw|ow|uw|yw'
    # word ending in vowels
    pennvog_re = r'^(.*?)(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ou|Ow|Uw|Yw|[aeoiuyAEIOUY])$'
    # word ending in consonants
    lostkess_re = r'^(.*?)(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nt|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])$'
    # consonant-vowel sequence at the end
    lostKB_re =  r'(.*?)(bl|br|Bl|Br|bb?|kl|Kl|kr|Kr|kn|Kn|kw|Kw|kk?|ch|Ch|Dhr?|dhr?|dl|dr|Dl|Dr|dd?|fl|Fl|fr?|Fr?|vl|Vl|vr|Vr|vv?|Vv?|gwr?|gwl?|gl|gr|gg?h|gn?|Gwr?|Gwl?|Gl|Gr|Gn?|ll?|mm?|nd|ns|nt|nn?|hw?|Hw?|pr|pl?|Pr|Pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|shr?|Shr?|str?|Str?|skr?|Skr?|sbr|Sbr|sp?l?|Sp?l?|tth|Tth|thr?|Thr?|tr|Tr|tl|Tl|tt?|wr|Wr|wl|Wl|[jwyBKDLJMNRTVWY])(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])$'
    # vowel-consonant sequnce at the end
    lostBK_re = r'(.*?)(ay|aw|ey|eu|ew|iw|oe|oy|ow|ou|uw|yw|Ay|Aw|Ey|Eu|Ew|Iw|Oe|Oy|Ow|Ou|Uw|Yw|[aeoiuyAEIOUY])(lgh|bl|bb?|kl|kr|kn|kw|kk?|ch|dhr?|dl|dr|dd?|fl|fr?|ff?|vl|vv?|gg?h|gw|gl|gn?|ll?|mm?|nd|ns|nt|nn?|pr|pl?|pp?|rgh?|rdh?|rth?|rv|rn|rr?|sh|st|sk|sp|ss?|tt?h|tt?|[jw])$'

    def __init__(self, inputtext):
        """
        initialize RannaSyllabelenn object
        """
        # print(inputtext)
        self.geryow = nltk.word_tokenize(inputtext)
        # print(geryow)
	
    def ranna_syl(self,ger,regexp,fwd=True,bwd=False):
        """ divide a word into a list of its syllables
        and return this
        """
        syl_list = []
        if fwd:
            while ger:
            # print(ger)
                k = self.kynsa_syl(ger,regexp)
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
            while ger:
                # print(ger)
                d = self.diwettha_syl(ger,regexp)
                # print(d)
                # add the syllable to the list
                if d != '':
                    syl_list.insert(0,d)
                if d != '' and len(ger.split(d,1))>1:
                # if there is more of the word before the
                # last syllable
                # remove the last syllable
                    ger = ger.split(d,1)[0]
                else: 
                    ger = ''
        # this is currently returning
        # a list of plain text
        # not Sylabellen objects
        return syl_list

    def diwettha_syl(self,ger, regexp):
        """ find last syllable of a word
        """
        diwettha_syl = ''
        # take off a trailing hyphen 
        if ger[-1] == '-':
            ger = ger[:-1]
        dsyl = re.findall(regexp,ger) 
        # print(dsyl)
        if not(dsyl == []):
            diwettha_syl=dsyl[0][1]+dsyl[0][2]+dsyl[0][3]
        # this is currently returning
        # plain text
        # not Sylabellen objects
        return diwettha_syl

    def kynsa_syl(self, ger, regexp):
        """ find 1st syllable of word
        """
        kynsa_syl = ''
        # print(ger)
        # take off an initial hyphen from the syllable
        if ger != '' and ger[0] == '-':
            ger = ger[1:]
        # print(ger)
        ksyl = re.findall(regexp,ger)
        # print("An kynsa sylabellen yw: {ksyl}".format(ksyl=ksyl))
        if not(ksyl == []):
            kynsa_syl = ksyl[0][1]+ksyl[0][5]
        return kynsa_syl

    def diwettha_lytherenn(self,ger):
        """ return last letter of a word
        """
        d_l = ''
        if ger[-1].isalpha():
            d_l = ger[-1]
        return d_l

    def profya(self, geryow):
        """ test code
        """
        # removya an dashow -
        # geryow = [g.replace("-","") for g in geryow]

        # Kavos an diwettha bogalenn yn ger mars eus bogalenn orth penn an ger 
        # i.e. match regular expression for vowel at the end of the word for a list of words
        pennvog =  [re.findall(RannaSyllabelenn.pennvog_re,g) for g in geryow if (not(re.findall(RannaSyllabelenn.pennvog_re,g)) ==[])]
        # Kavos an diwettha kessonenn yn ger mars eus kessonenn orth penn an ger
        # i.e. match regular expression for consonant at the end of the word for a list of words
        lostkess = [re.findall(RannaSyllabelenn.lostkess_re,g) for g in geryow if (not(re.findall(RannaSyllabelenn.lostkess_re,g))==[])]
        # Kavos an diwettha kessonenn ha bogalenn mars eus -KB orth penn an ger
        # i.e. match regular expression for consonant+vowel at end of the word
        lostKB = [re.findall(RannaSyllabelenn.lostKB_re,g) for g in geryow if not(re.findall(RannaSyllabelenn.lostKB_re,g)==[])]
        # print(pennvog)
        # print(lostkess)
        tuples = [d[0] for d in lostKB]
        stem = [t[0] for t in tuples]
        dsyl = [t[1]+t[2] for t in tuples]
        # print(lostkessvog)
        # print(zip(stem,dsyl))
        # Kavos an diwettha bogalenn ha kessonenn mars eus -BK orth penn an ger
        # i.e. match regular expression for vowel+consonant at end of the word
        lostBK = [re.findall(RannaSyllabelenn.lostBK_re,g) for g in geryow if not(re.findall(RannaSyllabelenn.lostBK_re,g)==[])]
        tuples = [d[0] for d in lostBK]
        stem = [t[0] for t in tuples]
        dsyl = [t[1]+t[2] for t in tuples]
        # print(lostvogkess)
        # print(zip(stem,dsyl))

        # create list of last syllables and first syllables of list of words 'geryow'
        dsls = [self.diwettha_syl(g,RannaSyllabelenn.diwetRegexp) for g in geryow if self.diwettha_syl(g,RannaSyllabelenn.diwetRegexp) != '']
        # print(dsls)
        ksls = [self.kynsa_syl(g,RannaSyllabelenn.kynsaRegexp) for g in geryow if self.kynsa_syl(g,RannaSyllabelenn.kynsaRegexp) != ''] 
        # print(ksls)
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
            if self.kynsa_syl(g,RannaSyllabelenn.kynsaRegexp) != '':
                nessasls.append(self.kynsa_syl(g,RannaSyllabelenn.kynsaRegexp))
            else:
                nessasls.append('')

        # print(slserell)
        # print(nessasls)
        geryowk = [g for g in geryow if self.kynsa_syl(g,RannaSyllabelenn.kynsaRegexp) != ''] 
        # print(zip(ksls,geryowk))
        #for k,n,e,g in zip(ksls,nessasls,slserell,geryowk):
            # print("Ger: {g}, an kynsa sylabellen yw: {k}, an sylabelennow erell yw: {e}, an nessa sylabelenn yw: {n}".format(g=g,k=k,e=e,n=n))

        # print([(g, re.findall(dewson_sevel_re,g)) for g in geryow if re.findall(dewson_sevel_re,g) != []])

class Ger:
    """
    # class for a word of Cornish text
    """
    def __init__(self,ger):
        """ initialize Ger object
        """
        self.graph = ger # an ger kowal
        # dilea an dashow -
        # self.grapheme = self.grapheme.replace("-","")
        # dilea an . ; , ?
        # strip out punctuation characters
        self.graph = self.graph.replace(".","")
        self.graph = self.graph.replace(";","")
        self.graph = self.graph.replace(",","")
        self.graph = self.graph.replace("?","")
        self.graph = self.graph.replace("'","")
        self.graph = self.graph.replace(" ","")
        # print(ger)
        self.n_sls = 0 # niver sylabelennow
        self.sls = []  # rol a sylabelennow yn furv tekst
        self.slsObjs = [] # rol a taklennow sylabelennow
        # go backwards from end 
        # sls = rannans.ranna_syl(self.graph,RannaSyllabelenn.diwetRegexp,fwd=False,bwd=True)
        # go forwards
        sls = rannans.ranna_syl(self.graph,RannaSyllabelenn.kynsaRegexp,fwd=True,bwd=False)
        # print(sls)
        self.sls = sls
        self.n_sls = len(sls)
        # gergesys = self.graph # rann an ger yw gesys
        # while gergesys != '':
            # k = rannans.kynsa_syl(gergesys,rannans.kynsaRegexp)
            # self.sls.append(copy.copy(k))
            # if (len(k)>0) and (len(gergesys.split(k,1))>1):
            #     gergesys = gergesys.split(k,1)[1]
            # else:
            #     gergesys = ''
            # self.n_sls = self.n_sls + 1
        for s in self.sls:
            self.slsObjs.append(Syllabelenn(s))
        if len(self.slsObjs) == 1:
            self.slsObjs[0].stressed = True
            self.slsObjs[0].monosyl = True
        elif len(self.slsObjs) > 1:
            # TODO - test for exceptions
            # penultimate stress
            self.slsObjs[-2].stressed = True

    def diskwedh(self):
        # show output for each word
        print("An ger yw: {g}".format(g=self.graph))
        print("Niver a sylabelennow yw: {n}".format(n=self.n_sls))
        print("Hag yns i:\n{sls}".format(sls=self.sls))
        for i in range(self.n_sls):
            gr = self.slsObjs[i].grapheme
            if self.slsObjs[i].stressed:
                gr = gr.upper()
            print("S{n}: {g}".format(n=i+1,g=gr))
            
class Syllabelenn:           
    """
    Class for syllable
    """
    def __init__(self,graph):
        """
        Initialize Syllabelenn object
        """
        self.grapheme = graph
        self.stressed = False
        self.monosyl = False
        self.structure = ''
        syl = re.findall(RannaSyllabelenn.syllabelRegExp,graph)
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

    def lengthSylParts(self):
        pass
        # TO DO
        # determine length of each part of syllable
        # check structure
        # find out whether consonants are doubled
        # if a monosyllble...
        # if stressed etc
        # make array for length of each syllable part 
        # 1 = short, 2 = halflong, 3 = long
        # also give total syllable length

if __name__ == '__main__':
    """
    If invoked at command-line
    """
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
        print("Error: No input file provided.")
        sys.exit()
    inputfile = args.inputfile
    inputtext = file(inputfile).read()
    rannans = RannaSyllabelenn(inputtext)
    # run test code if --test argument has been used
    if args.test:
        rannans.profya(rannans.geryow)
    for i in rannans.geryow:
        g = Ger(i)
        if g.graph != '':
            g.diskwedh()
            print('\n')
