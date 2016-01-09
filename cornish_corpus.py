# -*- coding: utf-8 -*-
# David Trethewey 13-04-2015
#
# A little on using Python NLTK 
# to do so corpus analysis and descriptive stats etc.
# on Cornish texts
#
# this is all rather unreadable and not too easily reusable
# todo: rewrite this to make it more modular
# and usable e.g by making it possible to change
# inputs etc. other than by directly editing source code
# 
# 21-12-2015 - edits to start to make this more modular
#
import nltk
# import the matplotlib library to make the output graphs
import matplotlib
import pylab

def basicReport(text):
    print("Text: ",text.name)
    print("\n")
    print("Collocations: {c}\n".format(c=text.collocations()))
    # frequency distribution
    fdist_len = nltk.FreqDist([len(w) for w in text])
    # print fdist_len.keys()
    # this should already be alphabetic
    text_alpha = [w for w in text if w.isalpha()]
    print("number of words = {nw}\n".format(nw=len(text_alpha)))
    print("number of different words = {ndw}\n".format(ndw = len(set([w.lower() for w in text_alpha]))))
    # frequency distribution (alphabetic)
    fdist_len2 = nltk.FreqDist([len(w) for w in text_alpha])
    print("Lengths of words in descending order of frequency {lw}\n".format(lw = [(length,freq) for length,freq in fdist_len2.items()]))
    # frequency distribution (alphabetic, lowercase)
    fdist_alpha = nltk.FreqDist([w.lower() for w in text_alpha])
    vocab = fdist_alpha.keys()
    print("Top 50 words: {w50}\n".format(w50=vocab[:50]))
    # frequency distribution (alphabetic, lowercase, more than 4 letters)
    fdist_alpha_fourormore = nltk.FreqDist([w.lower() for w in text_alpha if len(w)>=4]) 
    vocab4 = fdist_alpha_fourormore.keys()
    print("Top 50 words of 4 or more letters: {w50_4}\n".format(w50_4=vocab4[:50]))

def listPercentsN(text,cfd,dictlist):
    print "\nText: ",text.name,"\n"
    fdist = cfd[text.name]
    # dictionary indexed by length of word
    lenwordsdict = {}
    for s in fdist:
        print s," letters : ",str(100*(float(fdist[s])/len(text)))[:5],"% "
        lenwordsdict[s] = 100*(float(fdist[s])/len(text))
    dictlist.append(lenwordsdict)
    print "\n"
    #cfd.tabulate(cumulative=True)

        
def nLettersFDist(kk_texts_Texts,names):
    # conditional frequency distribution
    # based on length of words
    cfd = nltk.ConditionalFreqDist(
        (text.name,len(word))
        for text in kk_texts_Texts
        for word in text if word.isalpha())
    dictlist = []
    nameslist = [n for n in names]
    #print nameslist
    for t in kk_texts_Texts:
        listPercentsN(t,cfd,dictlist)
    #print dictlist
    for d in range(len(dictlist)):
        keyslist = [0]+[i[0] for i in dictlist[d].items()]
        valueslist = [0]+[i[1] for i in dictlist[d].items()]
        valueslist_cumulative = [sum(valueslist[0:i+1]) for i in keyslist]
        print keyslist
        #pylab.plot(keyslist,valueslist,label = nameslist[d],linewidth=2)
        if d == 7:
            st = "--"
        else:
            st = "-"
        print "d=",d
        pylab.plot(keyslist,valueslist_cumulative,label = nameslist[d],linewidth=2,linestyle=st)
    pylab.title("Cumulative % frequency of lengths of words in various Cornish texts.")
    pylab.legend()
    pylab.xlabel("Word length")
    pylab.ylabel("Cumulative % frequency")
    
def compareSamples(kk_texts_Texts,names):
    # the words to compare abundance of across the texts
    samples = sorted(["a","ha","an","dhe","yn","yw","ow","ev","rag","mes","esa","yth","y"])
    # conditional frequency distribution
    # based on alphabetic words 
    cfd2 = nltk.ConditionalFreqDist(
        (text.name,word.lower())
        for text in kk_texts_Texts
        for word in text if word.isalpha())

    for t in kk_texts_Texts:
        print "\nText: ",t.name,"\n"
        fdist = cfd2[t.name]
        for s in fdist.keys()[:20]:
            print s," : ",str(100*(float(fdist[s])/len(t)))[:5],"% "
        print "\n"
    #cfd2.tabulate(cumulative=True)
    #cfd.plot(cumulative=True)

    pylab.figure()
    colors = "rgbcmkyw"
    freqs_lists = []
    for t in kk_texts_Texts:
        f = cfd2[t.name]
        freqs_list = [100.0*float(f[s])/len(t) for s in samples]
        print freqs_list
        freqs_lists.append(freqs_list)
    
    ind = pylab.arange(len(samples))
    nameslist = [n for n in names]
    width = 1.0/(len(nameslist)+1)

    bar_groups = []
    for s in range(len(nameslist)):
        bars = pylab.bar(ind+s*width,freqs_lists[s],width=width,color = colors[s % len(colors)])
        bar_groups.append(bars)
    # add some vertical lines for readability
    for s in range(len(samples)):
        pylab.axvline(x=((s+1)*width*(len(nameslist)+1)-0.5*width), ymin=0, ymax = 100, linewidth=0.5, color='b', linestyle='-')
        pylab.title("% frequency of various words in Cornish texts")
        pylab.ylabel("% frequency")
        pylab.legend([b[0] for b in bar_groups],nameslist)
        pylab.xticks(ind+(len(nameslist)/2.0)*width,samples)
        pylab.tight_layout()
            
def corpusKK():
    # do imports for traditional (and some revived) texts in Kemmyn
    import read_kernewek_KK_texts
    kk_texts, names = read_kernewek_KK_texts.getKKtexts()
    # use NLTK functions to select words
    kk_texts_words = [kk_texts.words(i) for i in kk_texts.fileids()]
    # select those words that are alphabetic
    kk_texts_words_alpha = [[w for w in t if w.isalpha()] for t in kk_texts_words]
    # make a NLTK text from the alphabetic words in each of the texts
    # then put into a list of nltk.Text 
    #kk_texts_Texts = [nltk.Text(i) for i in kk_texts_words]
    kk_texts_Texts = [nltk.Text(i) for i in kk_texts_words_alpha]
    # print kk_texts_words_alpha[0][:10]
    # cycle through the texts
    # do basic report
    for i in kk_texts_Texts:
        basicReport(i)

    nLettersFDist(kk_texts_Texts,names)
    compareSamples(kk_texts_Texts,names)
    


if __name__ == '__main__':     
    corpusKK()
    pylab.show()
