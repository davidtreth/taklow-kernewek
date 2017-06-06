# coding=utf-8
import nltk
from nltk.corpus import PlaintextCorpusReader

def getKKtexts(filepattern=r".*kk.*\.txt",corpus_root = "kernewek_corpus/", outlang='kw'):
    textNames = {'en':["Life of Meryasek", "Charter Fragment", "Creation of the World",
                       "Passion of our Lord", "Origo Mundi", "Passio Christ",
                       "Resurrectio Domini", "Solemptnyta", "LoTR chapters",
                       "Tregear Homilies"],
                 'kw':["Bewnans Meryasek", "Darn Chartour", "Gwreans an Bys",
                       "Passhyon Agan Arloedh", "Origo Mundi", "Passio Christ",
                       "Resurrectio Domini", "Solemptnyta", "Chapters Arloedh an Bysowyer",
                       "Pregothow Tregear"]
                 }
    # select the Kernewek Kemmyn texts with a regular expression
    kk_texts = PlaintextCorpusReader(corpus_root,filepattern,encoding="latin-1")
    # print names of files to the console
    # to make sure we're selecting the right files
    print(kk_texts.fileids(),"\n")
    # names are hardcoded atm    
    #kknames = ["Bewnans Meryasek","Charter Fragment", "Gwreans an Bys","Passhyon Agan Arloedh", "Origo Mundi","Passio Christ","Resurrectio Domini","Solemptnyta","LoTR chapters","Tregear Homilies"]
    kknames = textNames[outlang]
    return kk_texts, kknames

def getMStexts(filepattern=r".*ms.txt", corpus_root="kernewek_corpus/", outlang='kw'):
    textNames = {'en':["Life of Kea", "Charter Fragment", "Creation of the World",
                       "Passion of our Lord", "Origo Mundi", "Passio Christ",
                       "Resurrectio Domini"],
                 'kw':["Bewnans Ke", "Darn Chartour", "Gwreans an Bys",
                       "Passhyon Agan Arloedh", "Origo Mundi", "Passio Christ",
                       "Resurrectio Domini"]
                 }
    # select the manuscript spelling texts with a regular expression
    ms_texts = PlaintextCorpusReader(corpus_root,filepattern,encoding="latin-1")
    # print names of files to the console
    # to make sure we're selecting the right files
    print(ms_texts.fileids(),"\n")
    # names are hardcoded atm    
    #msnames = ["Bewnans Ke","Charter Fragment", "Gwreans an Bys","Passhyon Agan Arloedh", "Origo Mundi","Passio Christ","Resurrectio Domini"]
    msnames = textNames[outlang]
    return ms_texts, msnames
