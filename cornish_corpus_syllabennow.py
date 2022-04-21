# coding=utf-8
import read_kernewek_KK_texts
import syllabenn_ranna_kw as syl
import nltk
import codecs
import os 

corpus_root = "kernewek_corpus/kemmyn_prefstrip/"

kw_texts, names = read_kernewek_KK_texts.getKKtexts_stripped(
            outlang='kw', corpus_root = "kernewek_corpus/kemmyn_prefstrip/")
           
#for t in zip(kw_texts.fileids(),names):
#    print(t[1], t[0])

# use NLTK functions to select words
# so that each is a separate NLTK Text
kw_texts_words = [kw_texts.words(i) for i in kw_texts.fileids()]
kw_texts_Texts = [nltk.Text(i) for i in kw_texts_words]

for i,t in enumerate(zip(kw_texts_words, names)):
    print(t[1])
    infile = os.path.join(corpus_root, kw_texts.fileids()[i])
    f = codecs.open(infile,"r",encoding="utf-8",errors="replace")
    inputtext = f.read()
    inputtext = syl.preprocess2ASCII(inputtext)
    #inputtext = inputtext.encode('utf-8')
    rannans = syl.RannaSyllabenn(inputtext)
    
    counts = syl.CountAllSyls()    
    punctchars = ".,;:!?()-"
    for i in rannans.geryow:
            g = syl.Ger(i,rannans, counts, False, regexps=syl.kwKemmynRegExp,
                    FSSmode=False,
                    CYmode=False, gwarnya=False)
            # avoid printing 'words' that consist only of a
            # punctuation character
            #if g.graph != '' and g.graph not in punctchars:
                # print short form word:nsyls
                #g.diskwedhshort(gwarnya=False)

    
    totalsylcounts = syl.totalcountsOutput(counts)
    print(totalsylcounts)
