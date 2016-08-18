# -*- coding: utf-8 -*-
# A basic 'translation memory' software
# which is set up with the example sentences at the
# ends of chapters of Skeul An Yeth 1 by Wella Brown
import nltk
from nltk.corpus import stopwords
import csv, os
from operator import itemgetter
import sys, imp
imp.reload(sys)
sys.setdefaultencoding('utf-8')


def getCorpusSents(sentencefile):
    """ expects a text file which is a comma separated variable file
    with headers including 'SentenceNumber' with an index number
    that should be unique in the corpus, 'Kernewek' with the text
    in Cornish, and 'English' with the same text in English. 
    It can be more than one sentence. 
    Return a tuple of two dictionaries containing the sentences
    in Cornish, and in English """
    with open(sentencefile) as csvinfile:
        reader = csv.DictReader(csvinfile)
        kw_sents = {}
        en_sents = {}
        for row in reader:
            kw_sents[int(row['SentenceNumber'])] = row['Kernewek']
            en_sents[int(row['SentenceNumber'])] = row['English']
    return kw_sents, en_sents

def getCorpusSentBigrams(sentencefile, trigrams = False, casesensit = True, cornish=False, maxstopwords=99):
    """ expects a text file which is a comma separated variable file
    with headers including 'SentenceNumber' with an index number
    that should be unique in the corpus, 'Kernewek' with the text
    in Cornish, and 'English' with the same text in English. 
    It can be more than one sentence. 
    
    find all of the bigrams, or trigrams within
    each entry in the corpus 
    Returns a list that contains a series of tuples, (n, b)
    where n is the sentence number, and b is the n-gram itself
    expressed as a a tuple 
    
    By default is case-sensitive, if not will return everything converted to lower case
    
    By default will return the bigrams/trigrams of the English versions 
    of each entry, unless the keyword variable cornish is True """
    with open(sentencefile) as csvinfile:
        reader = csv.DictReader(csvinfile)
        #print(reader.fieldnames)
        sents_bigrams = []
        sents_trigrams = []
        kw_sents = {}
        en_sents = {}
        for row in reader:
            # convert each entry into a list of words
            kw = nltk.word_tokenize(row['Kernewek'])
            en = nltk.word_tokenize(row['English'])
            if not(casesensit):
                kw = [w.lower() for w in kw]
                en = [w.lower() for w in en]
            if cornish:
                words = kw
            else:
                words = en
            # by default finds bigrams
            # if trigrams is True find trigrams instead
            if trigrams:
                for t in nltk.trigrams(words):
                    if cornish:
                        nstop = 0
                    else:
                        nstop=sum([w in stopwords.words('english') for w in t])
                    if nstop <= maxstopwords:
                        sents_trigrams.append((row['SentenceNumber'], t))
                # kwtri = list(nltk.trigrams(kw))
                # entri = list(nltk.trigrams(en))
            else:
                for b in nltk.bigrams(words):
                    if cornish:
                        nstop = 0
                    else:
                        nstop=sum([w in stopwords.words('english') for w in b])
                    if nstop <= maxstopwords:
                        sents_bigrams.append((row['SentenceNumber'], b))
                # kwbi = list(nltk.bigrams(kw))
                # enbi = list(nltk.bigrams(en))
            #print(kw, en)
            #print(kwbi, enbi)
        if trigrams:
            return sents_trigrams
        else:
            return sents_bigrams


def getInSentWords(casesensit=True):
    """ get a sentence in from the command line """
    inputSen = raw_input("Enter an English sentence\n")
    insentwords = nltk.word_tokenize(inputSen)
    if not(casesensit):
        insentwords = [w.lower() for w in insentwords]
    return insentwords


def getTrigrams(wordlist):
    """ get the trigrams, as a list of a list of words """
    inStrigrams = nltk.trigrams(wordlist)
    listinpSt = list(inStrigrams)
    return listinpSt

def getBigrams(wordlist):
    """ get the bigrams, as a list of a list of words """
    inSbigrams = nltk.bigrams(wordlist)
    listinpSb = list(inSbigrams)
    return listinpSb

def findCommonNgrams(corpussents, inputSNgrams):
    """ find the common n-grams between the corpus, and 
    a given sentence 

    return a list of the sentence numbers, and the common N grams"""
    sentNs = [s[0] for s in corpussents if s[1] in inputSNgrams]
    commonNgrams = nltk.defaultdict(list)
    for s in corpussents:
        if s[1] in inputSNgrams:
            commonNgrams[int(s[0])].append(s[1])
    commonNgrams = {k:commonNgrams[k] for k in commonNgrams if len(commonNgrams[k])>0}
    sentNs = sorted(set([int(n) for n in sentNs]))
    return sentNs, commonNgrams

def unpacklisttuples(tuplelist):
    punctchars = "!:,.?\"\'"
    if len(tuplelist) == 1:
        output = "("
        for i,w in enumerate(tuplelist[0]):
            if i > 0 and w not in punctchars:
                output += " "
            output += w
        output += ")"
    else:
        output = ""
        for t in tuplelist:
            output += "("
            for i,w in enumerate(t):
                if i > 0 and w not in punctchars:
                    output += " "
                output += w
            output += "), "
        output = output[:-2]
    return output
            
            
            
            

def outputSent(insentwords):
    """ display the output for a list of words insentwords """
    # display the trigrams from the input sentence
    print("\ntrigrams for input sentence are:")
    listinpSt = getTrigrams(insentwords)
    print(listinpSt)
    # display the bigrams from the input sentence
    print("\nbigrams for input sentence are:")
    listinpSb = getBigrams(insentwords)
    print(listinpSb)
    # find common bigrams and trigrams
    sentNs, bigrs =  findCommonNgrams(skeulyethbi_all, listinpSb)
    sentNsT, trigrs =  findCommonNgrams(skeulyethtri_all, listinpSt)
    
    sentNs_1stop, bigrs_1stop =  findCommonNgrams(skeulyethbi_1stop, listinpSb)
    sentNsT_2stop, trigrs_2stop =  findCommonNgrams(skeulyethtri_2stop, listinpSt)
    # remove sentence numbers from the list of bigrams
    # if they also appear in the trigrams
    sentNs = [s for s in sentNs if s not in sentNsT]
    sentNs_1stop = [s for s in sentNs_1stop if s not in sentNsT_2stop]
    # remove sentence numbers from the list of all bigrams and trigrams
    # if they also appear in the list of non-stopword bigrams and trigrams
    sentNsT = [s for s in sentNsT if s not in sentNsT_2stop]
    sentNs = [s for s in sentNs if s not in sentNs_1stop]
        
    # create list of tuples of index number and Ngrams
    # for N grams containing at least 1 non stopword
    # i.e. maximum 1 stopword in bigrams, 2 in trigrams.
    sentNs_big_1stop = [(n, bigrs[n]) for n in sentNs_1stop]
    sentNs_tri_2stop = [(n, trigrs[n]) for n in sentNsT_2stop]
    # sort the lists by the first element of the Ngram
    sentNs_big_1stop = sorted(sentNs_big_1stop, key=itemgetter(1))
    sentNs_tri_2stop = sorted(sentNs_tri_2stop, key=itemgetter(1))
    sentNs_big_1stop = sorted(sentNs_big_1stop, key=lambda nlist:len(nlist[1]), reverse=True)
    sentNs_tri_2stop = sorted(sentNs_tri_2stop, key=lambda nlist:len(nlist[1]), reverse=True)
    # make a list of the sentence numbers with the same sorting
    sentNs_1stop = [i[0] for i in sentNs_big_1stop]
    sentNsT_2stop = [i[0] for i in sentNs_tri_2stop]

    # create list of tuples of index number and Ngrams
    # for N grams containing all stopwords
    sentNs_big = [(n, bigrs[n]) for n in sentNs]
    sentNs_tri = [(n, trigrs[n]) for n in sentNsT]
    # sort the lists by the first element of the Ngram
    sentNs_big = sorted(sentNs_big, key=itemgetter(1))
    sentNs_tri = sorted(sentNs_tri, key=itemgetter(1))
    sentNs_big = sorted(sentNs_big, key=lambda nlist:len(nlist[1]), reverse=True)
    sentNs_tri = sorted(sentNs_tri, key=lambda nlist:len(nlist[1]), reverse=True)   
 
    # make a list of the sentence numbers with the same sorting
    sentNs = [i[0] for i in sentNs_big]
    sentNsT = [i[0] for i in sentNs_tri]

    # print the common trigrams, and bigrams
    # and the sentences where they occur    
    print("\nListing N grams with a minimum of 1 non-stopword each:")
    print("Common trigrams:\n")
    for n in sentNsT_2stop:    
        print("{kw}  --  {en} {t}".format(kw=kw_sents[n].ljust(60), en=en_sents[n].ljust(60), t = unpacklisttuples(trigrs[n])))
    print("\nCommon bigrams:\n")
    for n in sentNs_1stop:    
        print("{kw}  --  {en} {b}".format(kw=kw_sents[n].ljust(60), en=en_sents[n].ljust(60), b = unpacklisttuples(bigrs[n])))
    print("\nOther N grams containing only stopwords:")
    print("Common trigrams:\n")
    for n in sentNsT:    
        print("{kw}  --  {en} {t}".format(kw=kw_sents[n].ljust(60), en=en_sents[n].ljust(60), t = unpacklisttuples(trigrs[n])))
    print("\nCommon bigrams:\n")
    for n in sentNs:    
        print("{kw}  --  {en} {b}".format(kw=kw_sents[n].ljust(60), en=en_sents[n].ljust(60), b = unpacklisttuples(bigrs[n])))

    
    
if __name__ == "__main__":
    # by default use the example sentences at
    # the end of each chapter from
    # Skeul an Yeth 1 by Wella Brown
    skeulanyeth = "skeulanyeth.csv"
    skeulanyeth = os.path.join("kernewek_corpus",skeulanyeth)
    # get the Cornish and English sentences
    # as a dictionary indexed by a number
    kw_sents, en_sents = getCorpusSents(skeulanyeth)
    # get corpus bigrams and trigrams as a list of nested tuples
    casesensit = False
    skeulyethbi_1stop = getCorpusSentBigrams(skeulanyeth, casesensit = casesensit, maxstopwords=1)
    skeulyethtri_2stop = getCorpusSentBigrams(skeulanyeth, trigrams=True, casesensit = casesensit, maxstopwords=2)
    skeulyethbi_all = getCorpusSentBigrams(skeulanyeth, casesensit = casesensit)
    skeulyethtri_all = getCorpusSentBigrams(skeulanyeth, trigrams=True, casesensit = casesensit)
    while True:
        # get a sentence from the command-line
        insentwords = getInSentWords(casesensit)
        # display output for it
        outputSent(insentwords)
        print("\n")
