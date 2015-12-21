import nltk
from nltk.corpus import PlaintextCorpusReader

def getKKtexts(filepattern=r".*kk.*\.txt",corpus_root = "kernewek_corpus/"):
    # select the Kernewek Kemmyn texts with a regular expression
    kk_texts = PlaintextCorpusReader(corpus_root,filepattern)
    # print names of files to the console
    # to make sure we're selecting the right files
    print kk_texts.fileids(),"\n"
    # names are hardcoded atm    
    kknames = ["Bewnans Meryasek","Gwreans an Bys","Origo Mundi","Passio Christ","Resurrectio Domini","Solemptnyta","LoTR chapter","Tregear Homilies"]
    return kk_texts, kknames
