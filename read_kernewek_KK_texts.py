import nltk
from nltk.corpus import PlaintextCorpusReader

def getKKtexts(filepattern=r".*kk.*\.txt",corpus_root = "kernewek_corpus/"):
    # select the Kernewek Kemmyn texts with a regular expression
    kk_texts = PlaintextCorpusReader(corpus_root,filepattern,encoding="latin-1")
    # print names of files to the console
    # to make sure we're selecting the right files
    print(kk_texts.fileids(),"\n")
    # names are hardcoded atm    
    kknames = ["Bewnans Meryasek","Charter Fragment", "Gwreans an Bys","Passhyon Agan Arloedh", "Origo Mundi","Passio Christ","Resurrectio Domini","Solemptnyta","LoTR chapters","Tregear Homilies"]
    return kk_texts, kknames

def getMStexts(filepattern=r".*ms.txt", corpus_root="kernewek_corpus/"):
    # select the manuscript spelling texts with a regular expression
    ms_texts = PlaintextCorpusReader(corpus_root,filepattern,encoding="latin-1")
    # print names of files to the console
    # to make sure we're selecting the right files
    print(ms_texts.fileids(),"\n")
    # names are hardcoded atm    
    msnames = ["Bewnans Ke","Charter Fragment", "Gwreans an Bys","Passhyon Agan Arloedh", "Origo Mundi","Passio Christ","Resurrectio Domini"]
    return ms_texts, msnames
