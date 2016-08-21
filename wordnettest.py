# -*- coding: utf-8 -*-
# some test code using WordNet synsets
from __future__ import print_function
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import sys, imp
from operator import itemgetter
import kovtreylyans

imp.reload(sys)
if sys.version_info[0] < 3:
    sys.setdefaultencoding('utf-8')

def getsynonyms(word):
    print("word: {w}".format(w=word))
    synsets = wn.synsets(word)
    if int(nltk.__version__[0]) < 3:
        definitions = [s.definition for s in synsets]
    else:
        definitions = [s.definition() for s in synsets]        
    for d in zip(synsets, definitions):
        print("{s}: {df}".format(s=d[0], df=d[1]))
    hypernyms = []
    synonyms = []
    for syn in synsets:
        hyp = syn.hypernyms()
        hyp = [h for h in hyp if h not in hypernyms]
        hypernyms.extend(hyp)
    print("\nHypernyms")
    #print(hypernyms)
    
    if int(nltk.__version__[0]) < 3:
        definitions = [s.definition for s in hypernyms]
    else:
        definitions = [s.definition() for s in hypernyms]        
    for d in zip(hypernyms, definitions):
        print("{h}: {df}".format(h=d[0], df=d[1]))
    print("\nHyponyms of all hypernyms")
    for h in hypernyms:
        hypo = h.hyponyms()
        if int(nltk.__version__[0]) < 3:
            synonyms.extend([lemma.name for synset in hypo for lemma in synset.lemmas])
        else:
            synonyms.extend([lemma.name() for synset in hypo for lemma in synset.lemmas()])
    synonyms = sorted(set(synonyms))
    print(", ".join([s.replace("_"," ") for s in synonyms]))
    return synonyms


skeulanyeth1 = kovtreylyans.readCorpusSkeulYeth()
while True:
    if sys.version_info[0] < 3:
        text = raw_input("Enter some text please.\n")
    else:
        text = input("Enter some text please.\n")
    words = nltk.word_tokenize(text)
    subst_sents = []
    for w in words:
        if w not in stopwords.words('english'):
            syns = getsynonyms(w)
            for s in syns:
                subst = text.replace(w,s)
                subst = subst.replace("_", " ")
                # print(subst)
                subst_sents.append(subst)
                
        print("\n")

    subst_sents = set(subst_sents)


    commonbigrams = nltk.defaultdict(list)
    commontrigrams = nltk.defaultdict(list)
    for sent in subst_sents:
        print(sent)
        sentwords = nltk.word_tokenize(sent)
        sentwords = [w.lower() for w in sentwords]
        listinpSt = kovtreylyans.getTrigrams(sentwords)
        listinpSb = kovtreylyans.getBigrams(sentwords)
        #print(listinpSt)
        #print(listinpSb)
        sentNs_1stop, bigrs_1stop =  kovtreylyans.findCommonNgrams(skeulanyeth1.bi_1stop,
                                                                   listinpSb)
        sentNsT_2stop, trigrs_2stop =  kovtreylyans.findCommonNgrams(skeulanyeth1.tri_2stop,
                                                                     listinpSt)

        
        #print(bigrs_1stop)
        for b in bigrs_1stop:
            for bi in bigrs_1stop[b]:
                commonbigrams[b].append(bi)
            commonbigrams[b] = list(set(commonbigrams[b]))
                    
        #print(trigrs_2stop)
        for t in trigrs_2stop:
            for tri in trigrs_2stop[t]:
                commontrigrams[t].append(tri)
            commontrigrams[t] = list(set(commontrigrams[t]))

    order1 = sorted(commonbigrams, key=commonbigrams.get)
    commonbigrams = [(n, commonbigrams[n]) for n in order1]
    commonbigrams = sorted(commonbigrams, key=lambda nlist:len(nlist[1]), reverse=True)
    
    order1 = sorted(commontrigrams, key=commontrigrams.get)
    commontrigrams = [(n, commontrigrams[n]) for n in order1]
    commontrigrams = sorted(commontrigrams, key=lambda nlist:len(nlist[1]), reverse=True)
    
   
    # print(commonbigrams)
    print("\n")
    for t in commontrigrams:
        print(kovtreylyans.formatSentences(skeulanyeth1.kw_sents[t[0]], skeulanyeth1.en_sents[t[0]],
                                           kovtreylyans.unpacklisttuples(t[1])))
        #print("{kw}  --  {en} : {ng}".format(kw=skeulanyeth1.kw_sents[t], en=skeulanyeth1.en_sents[t], ng=commontrigrams[t]))
              
    for b in commonbigrams:
        print(kovtreylyans.formatSentences(skeulanyeth1.kw_sents[b[0]], skeulanyeth1.en_sents[b[0]],
                                           kovtreylyans.unpacklisttuples(b[1])))
        #print("{kw}  --  {en} : {ng}".format(kw=skeulanyeth1.kw_sents[b], en=skeulanyeth1.en_sents[b], ng=commonbigrams[b]))
        
    #print(commonbigrams)
    #print(commontrigrams)
    
        #kovtreylyans.kovtreyl(sent, skeulanyeth1, False, False)
    
