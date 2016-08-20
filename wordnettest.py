# -*- coding: utf-8 -*-
# some test code using WordNet synsets
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import sys, imp
import kovtreylyans
imp.reload(sys)
if sys.version_info[0] < 3:
    sys.setdefaultencoding('utf-8')


def getsynonyms(word):
    print("word: {w}".format(w=word))
    synsets = wn.synsets(word)
    definitions = [s.definition() for s in synsets]
    for d in zip(synsets, definitions):
        print(d)
    hypernyms = []
    synonyms = []
    for syn in synsets:
        hyp = syn.hypernyms()
        hypernyms.extend(hyp)
    print("\nHypernyms")
    print(hypernyms)
    definitions = [s.definition() for s in hypernyms]
    for d in zip(hypernyms, definitions):
        print(d)
    print("\nHyponyms of all hypernyms")
    for h in hypernyms:
        hypo = h.hyponyms()
        synonyms.extend([lemma.name() for synset in hypo for lemma in synset.lemmas()])
    print(synonyms)
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
        sentNs_1stop, bigrs_1stop =  kovtreylyans.findCommonNgrams(skeulanyeth1.bi_1stop, listinpSb)
        sentNsT_2stop, trigrs_2stop =  kovtreylyans.findCommonNgrams(skeulanyeth1.tri_2stop, listinpSt)

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

    for t in commontrigrams:
        print("{kw}  --  {en} : {ng}".format(kw=skeulanyeth1.kw_sents[t], en=skeulanyeth1.en_sents[t], ng=commontrigrams[t]))
              
    for b in commonbigrams:
        print("{kw}  --  {en} : {ng}".format(kw=skeulanyeth1.kw_sents[b], en=skeulanyeth1.en_sents[b], ng=commonbigrams[b]))
        
    #print(commonbigrams)
    #print(commontrigrams)
    
        #kovtreylyans.kovtreyl(sent, skeulanyeth1, False, False)
    
