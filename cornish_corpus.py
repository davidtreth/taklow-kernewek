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
# 26-08-2016 - further edits to make more modular
# and introduce some interactivity
#
from __future__ import print_function
import nltk
# import the matplotlib library to make the output graphs
import matplotlib
import pylab
import sys

def basicReport(text, textname, topN=50, minL=4):
    """ print out at the command line a report of a text 

    Given an NLTK text, output the number of words, number
    of different words, and some word frequency information.

    @param text: An NLTK text
    @param topN: A number detailing how many of the most frequent words
    should be listed.
    @type topN: C{int}
    @param minL: A number detailing the minimum number of letters in the second
    list of words and their frequencies.
    @type minL: C{int}
    """
    print(("Text: {n}".format(n=textname)))
    print("\n")
    print("Collocations: {c}\n".format(c=text.collocations()))
    text_alpha = [w for w in text if w.isalpha()]
    print(("number of words = {nw}\n".format(nw=len(text_alpha))))
    print(("number of different words = {ndw}\n".format(ndw = len(set([w.lower() for w in text_alpha])))))
    # frequency distribution (alphabetic)
    fdist_len = nltk.FreqDist([len(w) for w in text_alpha])
    print(("Lengths of words in descending order of frequency {lw}\n".format(
        lw = [(length,freq) for length,freq in fdist_len.items()])))
    # frequency distribution (alphabetic, lowercase)
    fdist_alpha = nltk.FreqDist([w.lower() for w in text_alpha])
    # convert the items of the frequency distribution into a list of tuples
    vocabkeyvaltup = [(k,v) for (k,v) in fdist_alpha.items()]
    # sort by decreasing frequency
    vocab = sorted(vocabkeyvaltup, key=lambda keyvaltup: keyvaltup[1], reverse=True)
    # make of list of the words themselves
    vocab = [v[0] for v in vocab]
    print(("Top {tN} words: {wN}\n".format(tN = topN, wN=[w.encode("ascii") for w in vocab[:topN]])))
    # frequency distribution (alphabetic, lowercase, more than minL letters)
    fdist_alpha_minL_ormore = nltk.FreqDist([w.lower() for w in text_alpha if len(w)>=minL])
    vocabkeyvaltup = [(k,v) for (k,v) in fdist_alpha_minL_ormore.items()]
    vocab4 = sorted(vocabkeyvaltup, key=lambda keyvaltup: keyvaltup[1], reverse=True)
    vocab4 = [v[0] for v in vocab4]
    print(("Top {tN} words of {m} or more letters: {wN_m}\n".format(tN = topN,
                                                                     m=minL,
                                                                     wN_m=[w.encode("ascii") for w in vocab4[:topN]])))

def listPercentsN(text,cfd,dictlist, textname):
    """
    add a dictionary lenwordsdict that describes the frequencies of words by length
    to the list dictlist

    @param text: an NLTK text
    @param cfd: an NLTK conditional frequency distribution for the text
    @param dictlist: A list containing dictionaries, where each one contains the
    frequencies of words of different lengths.
    @type dictlist: C{list}
    """
    print("\nText: {n}\n".format(n=textname))
    fdist = cfd[text.name]
    # dictionary indexed by length of word
    lenwordsdict = {}
    for s in fdist:
        print(s," letters : ",str(100*(float(fdist[s])/len(text)))[:5],"% ")
        lenwordsdict[s] = 100*(float(fdist[s])/len(text))
    dictlist.append(lenwordsdict)
    print("\n")
    #cfd.tabulate(cumulative=True)

    
def nLettersFDist(kk_texts_Texts,names):
    """ create conditional frequency distributions
    based on length of words for a set of NLTK texts,
    and draw a graph.

    @param kk_texts_Texts: a list of NLTK texts
    @param names: the names of the texts
    @type kk_texts_Texts: C{list}
    @type names: C{list}
    """
    cfd = nltk.ConditionalFreqDist(
            (text.name,len(word))
            for text in kk_texts_Texts
            for word in text if word.isalpha())
    # a list containing dictionaries indexed by length of word
    # which contain percentage frequencies of words of that length
    dictlist = []
    #print nameslist
    for t in zip(kk_texts_Texts, names):
        listPercentsN(t[0],cfd,dictlist, t[1])
    #print dictlist
    for d in range(len(dictlist)):
        keyslist = [0]+[i[0] for i in dictlist[d].items()]
        valueslist = [0]+[i[1] for i in dictlist[d].items()]
        valueslist_cumulative = [sum(valueslist[0:i+1]) for i in keyslist]
        #print(keyslist)
        #pylab.plot(keyslist,valueslist,label = nameslist[d],linewidth=2)
        if d == 7:
            st = "--"
        else:
            st = "-"
        #print("d=",d)
        pylab.plot(keyslist,valueslist_cumulative,label = nameslist[d],linewidth=2,linestyle=st)
    pylab.title("Cumulative % frequency of lengths of words in various Cornish texts.")
    pylab.legend()
    pylab.xlabel("Word length")
    pylab.ylabel("Cumulative % frequency")

def getCFD(kk_texts_Texts, casesensit=False):
    """
    get conditional frequency distribution of all the texts

    @param kk_texts_Text: a list of NLTK Texts
    @type kk_texts_Text: C{list}
    @param casesensit: whether to be case sensitive
    @type casesensit: C{bool}
    """
    # based on alphabetic words
    if casesensit:
        cfd = nltk.ConditionalFreqDist(
            (text.name,word)
            for text in kk_texts_Texts
            for word in text if word.isalpha())
    else:
        cfd = nltk.ConditionalFreqDist(
            (text.name,word.lower())
            for text in kk_texts_Texts
            for word in text if word.isalpha())
    return cfd

def MostFrequentWords(kk_texts_Texts, textnames, N=20, casesensit=False):
    """
    print out list of the most frequent words in each text

    @param kk_texts_Texts: List of NLTK Texts.
    @type kk_texts_Texts: C{list}
    @param N: how many words to list. Default is 20.
    @type N: C{int}
    @param casesensit: whether to be case sensitive.
    @type casesensit: C{bool}
    """
    cfd = getCFD(kk_texts_Texts, casesensit)
    for t in zip(kk_texts_Texts, textnames):
        print("\nText: {n}\n".format(n=t[1]))
        fdist = cfd[t[0].name]
        keyvaltup = [(k,v) for (k,v) in fdist.items()]
        keyvaltupsort = sorted(keyvaltup, key=lambda keyvaltup: keyvaltup[1], reverse=True)
        print("{n} most frequent words are:".format(n=N))
        for kv in keyvaltupsort[:N]:
            print(kv[0]," : ",str(100*(float(kv[1])/len(t[0])))[:5],"% ")
        print("\n")
    #cfd.tabulate(cumulative=True)
    #cfd.plot(cumulative=True)

def compareSamples(kk_texts_Texts,names, samples, casesensit=False):
    """
    Produce a bar plot comparing the frequency of words in a list samples
    across the different texts.

    @param kk_texts_Texts: A list of NLTK Texts.
    @type kk_texts_Texts: C{list}
    @param names: A list of the text names.
    @type names: C{list}
    @param samples: A list of sample words to compare.
    @type samples: C{list}
    @param casesensit: Whether to be case sensitive.
    @type casesensit: C{bool}
    """
    cfd = getCFD(kk_texts_Texts, casesensit)
    colors = "rgbcmkyw"
    freqs_lists = []
    for t in kk_texts_Texts:
        f = cfd[t.name]
        if casesensit:
            freqs_list = [100.0*float(f[s])/len(t) for s in samples]
        else:
            freqs_list = [100.0*float(f[s.lower()])/len(t) for s in samples]
        print("Text {t}, frequencies {f}.".format(t=t.name, f=freqs_list))
        freqs_lists.append(freqs_list)

    # produce one group of bars for each text
    ind = pylab.arange(len(samples))
    width = 1.0/(len(names)+1)
    bar_groups = []
    for s in range(len(names)):
        bars = pylab.bar(ind+s*width,freqs_lists[s],width=width,color = colors[s % len(colors)])
        bar_groups.append(bars)
    # add some vertical lines for readability
    for s in range(len(samples)):
        pylab.axvline(x=((s+1)*width*(len(names)+1)-0.5*width), ymin=0, ymax = 100,
                      linewidth=0.5, color='b', linestyle='-')
        
    pylab.title("% frequency of various words in Cornish texts")
    pylab.ylabel("% frequency")
    pylab.legend([b[0] for b in bar_groups],names)
    pylab.xticks(ind+(len(names)/2.0)*width,samples)
    pylab.tight_layout()
            
def corpusKK():
    """
    do imports for traditional (and some revived) texts in Kemmyn
    """
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
    return kk_texts_Texts, names


def basicReportAll(kk_texts_Texts, textnames, topN=50, minL=4, pause=True):
    """
    cycle through the texts and output a basic report for each

    @param kk_texts_Texts: a list of NLTK Texts.
    @type kk_texts_Texts: C{list}
    @param textnames: a list of the names of the texts.
    @type textnams: C{list}
    @param topN: how many of the most frequent words to list.
    @type topN: C{int}
    @param minL: minimum number of letters for the second list
    of most frequent words omitting short words.
    @type minL: C{int}
    @param pause: whether to pause between each text.
    @type pause: C{bool}
    """
    for i in zip(kk_texts_Texts, textnames):
        basicReport(i[0], i[1], topN, minL)
        if pause:
            if sys.version_info[0] < 3:
                w = raw_input("Press Enter to continue...\n")
            else:
                w = input("Press Enter to continue...\n")
            if w.lower() == "skip" or w.lower() == "lamma":
                pause = False

def freqCompareInterAct(casesensit=False, interactive=True):
    """ 
    Request words from the command line input and
    run compareSamples() to compare their frequencies.
    
    @param casesensit: whether to be case sensitive
    @type casesensit: C{bool}
    @param interactive: whether to use interactive mode. If False, use a
    default list of samples.
    @type interactive: C{bool}
    """
    defaultsamples = ["a","ha","an","dhe","yn","yw","ow","ev","rag","mes","esa","yth","y"]
    print("Please enter a words to compare frequency across the texts.\nEnter the word 'default' to use the default wordlist.\nPress Enter without any text to stop building the wordlist and draw the graph:")
    # the words to compare abundance of across the texts
    
    if not(interactive):
        samples = defaultsamples
    else:
        samples = []
        while interactive:
            if sys.version_info[0] < 3:
                w = raw_input("Enter word:\n")
            else:
                w = input("Enter word:\n")
            if len(w) > 0:
                if w.lower() == "default":
                    # if the word 'default' is entered
                    # use the default sample word list
                    samples = defaultsamples
                    interactive = False
                else:
                    # otherwise append the sample to the list
                    samples.append(w)
            else:
                # if w has length zero
                # stop building the samples list
                interactive = False
    if not(casesensit):
        samples = [s.lower() for s in samples]
    samples = sorted(set(samples))    
    compareSamples(kk_texts_Texts,names, samples)

if __name__ == '__main__':     
    kk_texts_Texts, names = corpusKK()
    basicReportAll(kk_texts_Texts, names)
    if sys.version_info[0] < 3:
        w = raw_input("Plot cumulative frequency plot for lengths of words (y/n)?\n")
    else:
        w = input("Plot cumulative frequency plot for lengths of words (y/n)?\n")
    if w.isalpha():
        if w[0].lower=="y":
            nLettersFDist(kk_texts_Texts,names)
            pylab.figure()
    freqCompareInterAct()    
    pylab.show()
