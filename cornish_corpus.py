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
import matplotlib.pyplot as plt
import numpy as np
import string
import sys, argparse
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    
import imp
imp.reload(sys)
if sys.version_info[0] < 3:
    sys.setdefaultencoding('utf-8')


def countchars(text_alpha, chdigraph=True, const_digraphs = True,
               vowel_digraphs = True):
    """ 
    @param text_alpha: list of alphabetic words
    @type text_alpha: C{list}
    """
    # currently filters out non-ascii chars    
    text_alpha = [w.lower() for w in text_alpha]


    if chdigraph:
        text_alpha = [w.replace("cch", u"ć") for w in text_alpha]
        text_alpha = [w.replace("ch", u"č") for w in text_alpha]
    if const_digraphs:
        text_alpha = [w.replace("ggh", u"ǵ") for w in text_alpha]
        text_alpha = [w.replace("gh", u"ǧ") for w in text_alpha]
        
        text_alpha = [w.replace("dh", u"ð") for w in text_alpha]
        
        text_alpha = [w.replace("tth", u"ꝥ") for w in text_alpha]
        text_alpha = [w.replace("th", u"Þ") for w in text_alpha]

        text_alpha = [w.replace("ssh", u"ś") for w in text_alpha]
        text_alpha = [w.replace("sh", u"š") for w in text_alpha]

        text_alpha = [w.replace("hw", u"ħ") for w in text_alpha]

    if vowel_digraphs:
        text_alpha = [w.replace("oe", u"ǒ") for w in text_alpha]
        text_alpha = [w.replace("ou", u"ú") for w in text_alpha]
        text_alpha = [w.replace("eu", u"ě") for w in text_alpha]

    textst = "".join(text_alpha)
    
    chardict = nltk.defaultdict(int)
    for c in textst:
        if chdigraph:
            c = c.replace(u"ć", "cch")
            c = c.replace(u"č", "ch")
        if const_digraphs:
            c = c.replace(u"ǵ", "ggh")
            c = c.replace(u"ǧ", "gh")
            c = c.replace(u"ð", "dh")
            c = c.replace(u"ꝥ", "tth")
            c = c.replace(u"Þ", "th")

            c = c.replace(u"ś", "ssh")
            c = c.replace(u"š", "sh")
            c = c.replace(u"ħ", "hw") 
        if vowel_digraphs:
            c = c.replace(u"ǒ", "oe")
            c = c.replace(u"ú", "ou")
            c = c.replace(u"ě", "eu")
        
        chardict[c] += 1
    return chardict


def basicReport(text, textname, topN=50, minL=4, printcmdline=True, outlang='kw'):
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
    outTexts = {'texttitle': {'en': 'Text', 'kw': 'Tekst'},
                'nwords': {'en':'number of alphabetic words',
                           'kw':'niver geryow lytherennek'},
                'ndiffwords': {'en':'number of different alphabetic words',
                               'kw':'niver geryow lytherennek dihaval'},
                'nchars': {'en':'total number of characters in alphabetic words',
                           'kw': 'sommenn niver lytherennow yn geryow lytherennek'},
                'meanlenword': {'en':'mean word length',
                                'kw':'hirder ger mayn'},
                'freqwordshead': {'en':'Lengths of words in descending order of frequency',
                                  'kw':'Hirder geryow yn aray diyskynna menowghder'},
                'top': {'en':'Top ',
                        'kw':''},
                'words': {'en':'words',
                          'kw':'geryow moyha kemmyn'},
                'wordsof':{'en':'words of',
                           'kw':'geryow moyha kemmyn gans'},
                'letters': {'en':'or more letters',
                            'kw':'lytherennow dhe\'n lyha'}
                }
    outputtext = ""
    outputtext += "{t}: {n}\n\n".format(t=outTexts['texttitle'][outlang], n=textname)
    # note - doesn't return True for accented characters
    text_alpha = [w for w in text if w.isalpha()]
    outputtext += "{t} = {nw}\n".format(t=outTexts['nwords'][outlang], nw=len(text_alpha))
    outputtext += "{t} = {ndw}\n\n".format(t=outTexts['ndiffwords'][outlang],
                                           ndw = len(set([w.lower() for w in text_alpha])))
    
    outputtext += "{t} = {c}\n".format(t=outTexts['nchars'][outlang],
                                       c=sum(len(w) for w in text_alpha))
    outputtext += "{t} = {m:.02f}\n\n".format(t=outTexts['meanlenword'][outlang],
                                              m=np.mean([len(w) for w in text_alpha]))
    # frequency distribution (alphabetic)
    fdist_len = nltk.FreqDist([len(w) for w in text_alpha])
    outputtext += "{t}\n{lw}\n\n".format(t=outTexts['freqwordshead'][outlang],
                                         lw = [(length,freq) for length,freq in fdist_len.items()])
    # frequency distribution (alphabetic, lowercase)
    fdist_alpha = nltk.FreqDist([w.lower() for w in text_alpha])
    # convert the items of the frequency distribution into a list of tuples
    vocabkeyvaltup = [(k,v) for (k,v) in fdist_alpha.items()]
    # sort by decreasing frequency
    vocab = sorted(vocabkeyvaltup, key=lambda keyvaltup: keyvaltup[1], reverse=True)
    # make of list of the words themselves
    vocab = [v[0] for v in vocab]
    if sys.version_info[0] < 3:
        wN=[w.encode("ascii") for w in vocab[:topN]]
    else:
        wN=vocab[:topN]
    outputtext += "{t1}{tN} {t2}:\n{wN}\n\n".format(t1=outTexts['top'][outlang],
                                                    t2=outTexts['words'][outlang],
                                                    tN = topN, wN=wN)
    # frequency distribution (alphabetic, lowercase, more than minL letters)
    fdist_alpha_minL_ormore = nltk.FreqDist([w.lower() for w in text_alpha if len(w)>=minL])
    vocabkeyvaltup = [(k,v) for (k,v) in fdist_alpha_minL_ormore.items()]
    vocab4 = sorted(vocabkeyvaltup, key=lambda keyvaltup: keyvaltup[1], reverse=True)
    vocab4 = [v[0] for v in vocab4]
    if sys.version_info[0] < 3:
        wN_m=[w.encode("ascii") for w in vocab4[:topN]]
    else:
        wN_m=vocab4[:topN]
    outputtext += "{t1}{tN} {t2} {m} {t3}:\n{wN_m}\n\n".format(t1=outTexts['top'][outlang],
                                                               t2=outTexts['wordsof'][outlang],
                                                               t3=outTexts['letters'][outlang],
                                                               tN = topN,
                                                               m=minL,
                                                               wN_m=wN_m)
    if printcmdline:
        print(outputtext)
    return outputtext

def listPercentsN(text,cfd,dictlist, textname, outlang='kw'):
    """
    add a dictionary lenwordsdict that describes the frequencies of words by length
    to the list dictlist

    @param text: an NLTK text
    @param cfd: an NLTK conditional frequency distribution for the text
    @param dictlist: A list containing dictionaries, where each one contains the
    frequencies of words of different lengths.
    @type dictlist: C{list}
    """
    outTexts = {
        'text': {'en':'Text',
                 'kw':'Tekst'},
        'letters': {'en':'letters',
                    'kw':'lytherenn'}
        }

    print("\n{t}: {n}\n".format(t=outTexts['text'][outlang],
                                n=textname))
    fdist = cfd[text.name]
    # dictionary indexed by length of word
    lenwordsdict = {}
    for s in fdist:
        print(s," {t} : ".format(t=outTexts['letters'][outlang]),str(100*(float(fdist[s])/len(text)))[:5],"% ")
        lenwordsdict[s] = 100*(float(fdist[s])/len(text))
    dictlist.append(lenwordsdict)
    print("\n")
    #cfd.tabulate(cumulative=True)

def formatCFDnLetters(cfdlist, outlang='kw'):
    """
    return formatted text output
    for list of cumulative frequency by
    length of words for each texts

    @param cfdlist: a list of tuples
    each of which has the first item the
    text name, and the second a list of tuples
    consisting of an integer expressing length
    of word, and a float of the cumulative percentage
    """
    outTexts = {
        'letters': {'en':'letters',
                    'kw':'lytherenn'}
        }
    outputtext = ""
    for t in cfdlist:
        outputtext += t[0] + "\n"
        for tup in t[1]:
            outputtext += "{n} {t}: {cumul:.2f}%\n".format(n=tup[0],
                                                           t=outTexts['letters'][outlang],
                                                           cumul=float(tup[1]))
        outputtext += "\n"
    return outputtext
            
        
        
        
def nLettersFDist(kk_texts_Texts,names, outlang='kw'):
    """ create conditional frequency distributions
    based on length of words for a set of NLTK texts,
    and draw a graph.

    @param kk_texts_Texts: a list of NLTK texts
    @param names: the names of the texts
    @type kk_texts_Texts: C{list}
    @type names: C{list}
    """
    outTexts = {
        'plottitle': {'en':'Cumulative % frequency of lengths of words in various Cornish texts.',
                      'kw':'% Menowghder Kumulativ hirder geryow yn tekstow Kernewek divers.'},
        'plottitle2': {'en':'Cumulative % frequency of lengths of words in',
                       'kw':'% Menowghder Kumulativ hirder geryow yn'},
        'xlab':{'en':'Word length',
                'kw':'Hirder Ger'},
        'ylab':{'en':'Cumulative % frequency',
                'kw':'Menowghder % kumulativ'}
        }
    cfd = nltk.ConditionalFreqDist(
            (text.name,len(word))
            for text in kk_texts_Texts
            for word in text if word.isalpha())
    # a list containing dictionaries indexed by length of word
    # which contain percentage frequencies of words of that length
    dictlist = []
    output = []
    #print nameslist
    for t in zip(kk_texts_Texts, names):
        listPercentsN(t[0],cfd,dictlist, t[1], outlang=outlang)
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
        plt.plot(keyslist,valueslist_cumulative,label = names[d],linewidth=2,linestyle=st)
        output.append(zip(keyslist, valueslist_cumulative))
    if len(names) > 1:
        plt.title(outTexts['plottitle'][outlang])
        plt.legend()
    else:
        plt.title("{t} {n}.".format(t=outTexts['plottitle2'][outlang],
                                    n=names[0]))
    plt.xlabel(outTexts['xlab'][outlang])
    plt.ylabel(outTexts['ylab'][outlang])
    plt.tight_layout()
    return formatCFDnLetters(zip(names,output), outlang=outlang)

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

def MostFrequentWords(kk_texts_Texts, textnames, N=20, minL = 1, casesensit=False, outlang='kw'):
    """
    return a list of the most frequent words in each text

    @param kk_texts_Texts: List of NLTK Texts.
    @type kk_texts_Texts: C{list}
    @param N: how many words to list. Default is 20.
    @type N: C{int}
    @param casesensit: whether to be case sensitive.
    @type casesensit: C{bool}
    """
    outTexts = {
        'text':{'en':'Text',
                'kw':'Tekst'},
        'the':{'en':'The',
               'kw':'An'},
        'mostfreq':{'en':'most frequent words',
                    'kw':'geryow moyha kemmyn'},
        'atleast':{'en':'with at least',
                   'kw':'gans dhe\'n lyha'},
        'are':{'en':'are',
               'kw':'yw'},
        'letters':{'en':'letters are',
                   'kw':'lytherenn yw'}
        }
    outputtext = ""
    cfd = getCFD(kk_texts_Texts, casesensit)
    for t in zip(kk_texts_Texts, textnames):
        outputtext += "{x}: {n}\n".format(x=outTexts['text'][outlang], n=t[1])
        fdist = cfd[t[0].name]
        keyvaltup = [(k,v) for (k,v) in fdist.items()]
        keyvaltupsort = sorted(keyvaltup, key=lambda keyvaltup: keyvaltup[1], reverse=True)

        if minL > 1:
            keyvaltupsort = [(k,v) for (k,v) in keyvaltupsort if len(k) >= minL]
            outputtext += "{t0} {n} {t1} {t2} {m} {t3}:\n\n".format(t0=outTexts['the'][outlang],
                                                                    t1=outTexts['mostfreq'][outlang],
                                                                    t2=outTexts['atleast'][outlang],
                                                                    t3=outTexts['letters'][outlang],
                                                                    n=N, m=minL)
        else:
            outputtext += "{t0} {n} {t1} {t2}:\n\n".format(t0=outTexts['the'][outlang],
                                                           t1=outTexts['mostfreq'][outlang],
                                                           t2=outTexts['are'][outlang],
                                                           n=N)
        if len(keyvaltupsort) > 0:
            maxL = max(len(kv[0]) for kv in keyvaltupsort[:N])        
            maxF = keyvaltupsort[0][1]
        else:
            maxL = N
            maxF = 0
        for kv in keyvaltupsort[:N]:
            outputtext += "{word:<{m}} : {pcfreq:.3%} :   N = {freq:>{lg}}\n".format(word=kv[0],
                                                                                     m=maxL+2,
                                                                                     pcfreq=float(kv[1])/len(t[0]),
                                                                                     freq=kv[1],
                                                                                     lg=int(np.log10(maxF))+1)
            #print(kv[0]," : ",str(100*(float(kv[1])/len(t[0])))[:5],"% ")
        outputtext += "\n"
    #cfd.tabulate(cumulative=True)
    #cfd.plot(cumulative=True)
    return outputtext


    
def MostFreqWords1Text(Text, name, N=20, casesensit=False, outlang='kw'):
    """
    find most frequent words for a single text
    
    @param Text: A NLTK text
    @param name: The name of the next
    @type name: C{string}
    @param N: how many words to list. Default is 20.
    @type N: C{int}
    @param casesensit: whether to be case sensitive.
    @type casesensit: C{bool}
    """
    return MostFrequentWords([Text], [name], N, casesensit, outlang=outlang)


def MostFreqLetters(kk_texts_Texts, textnames,
                    condigraph=True, voweldigraph=True,
                    chdigraph=True, outlang='kw'):
    """
    return a list of the most frequent letters in each text
    
    @param kk_texts_Texts: List of NLTK Texts.
    @type kk_texts_Texts: C{list}
    @type condigraph: C{bool}
    @type voweldigraph: C{bool}
    """
    outTexts= {'lettersdesc':{'en':'Letters in descending order of frequency',
                              'kw':'Lytherennow yn aray diyskynna menowghder'},
               'text':{'en':'Text',
                       'kw':'Tekst'}
               }
    outputtext = ""
    for t in zip(kk_texts_Texts, textnames):
        outputtext += "{x}: {n}\n".format(x = outTexts['text'][outlang], n=t[1])
        textalpha = [w for w in t[0] if w.isalpha()]
        lentextstr = len("".join(textalpha))
        chardict = countchars(textalpha, chdigraph, condigraph, voweldigraph)
        kvtup = [(k,v) for (k,v) in chardict.items()]
        kvtupsort = sorted(kvtup, key = lambda kvtup: kvtup[1], reverse=True)
        outputtext += "{t}:\n\n".format(t=outTexts['lettersdesc'][outlang])
        maxF = kvtupsort[0][1]
        for kv in kvtupsort:
            outputtext += "{char:3}:{pcfreq:^8.2%}: N = {freq:>{lg}}\n".format(char=kv[0],
                                                                               pcfreq=float(kv[1])/lentextstr,
                                                                               freq=kv[1],
                                                                               lg=int(np.log10(maxF))+1)
        outputtext += "\n"
    return outputtext


def MostFreqLetters1Text(Text, name,
                         condigraph=True, voweldigraph=True, chdigraph=True, outlang='kw'):
    """
    return a list of the most frequent letters in each text
    
    @param Text: A NLTK text
    @param name: The name of the next
    @type name: C{string}
    @type condigraph: C{bool}
    @type voweldigraph: C{bool}
    """
    return MostFreqLetters([Text], [name], condigraph, voweldigraph, chdigraph, outlang=outlang)

def compareSamples(kk_texts_Texts,names, samples, casesensit=False, outlang='kw'):
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
    outTexts = {
        'text':{'en':'Text',
                'kw':'Tekst'},
        'freq':{'en':'frequencies',
                'kw':'menowghderow'},
        'plottitle':{'en':'% frequency of various words in Cornish texts',
                     'kw':'% menowghder nebes geryow yn tekstow Kernewek'},
        'plottitle2':{'en':'% frequency of various words in',
                      'kw':'% menowghder nebes geryow yn'},
        'ylab':{'en':'% frequency',
                'kw':'% menowghder'}
        }
    outputtext = ""
    cfd = getCFD(kk_texts_Texts, casesensit)
    colors = "rgbcmky"
    freqs_lists = []
    for t,n in zip(kk_texts_Texts, names):
        f = cfd[t.name]
        if casesensit:
            freqs_list = [100.0*float(f[s])/len(t) for s in samples]
        else:
            freqs_list = [100.0*float(f[s.lower()])/len(t) for s in samples]
            
        freqs_list_print = [round(fr, 4) for fr in freqs_list]
        outputtext += "{l1} {t}, {l2} {f}.\n\n".format(l1=outTexts['text'][outlang],
                                                       t=n, l2=outTexts['freq'][outlang],
                                                       f=freqs_list_print)
        freqs_lists.append(freqs_list)

    # produce one group of bars for each text
    ind = np.arange(len(samples))
    width = 1.0/(len(names)+1)
    bar_groups = []
    for s in range(len(names)):
        bars = plt.bar(ind+s*width,freqs_lists[s],width=width,color = colors[s % len(colors)])
        bar_groups.append(bars)

    if len(names) > 1:   
        # add some vertical lines for readability
        for s in range(len(samples)):
            plt.axvline(x=((s+1)*width*(len(names)+1)-0.5*width),
                          ymin=0, ymax = 100, linewidth=0.5, color='b', linestyle='-')
        plt.title(outTexts['plottitle'][outlang])
        plt.legend([b[0] for b in bar_groups],names)
    else:
        plt.title("{l} {n}".format(l=outTexts['plottitle2'][outlang],
                                   n=names[0]))
        
    plt.ylabel(outTexts['ylab'][outlang])
    plt.xticks(ind+(len(names)/2.0)*width,samples)
    plt.axis(xmin=-0.5*width, xmax = len(samples)*width*(len(names)+1)-0.5*width)
    plt.tight_layout()
    print(outputtext)
    return outputtext

def compareSamplesLinear(kk_texts_Texts,names, samples, casesensit=False, outlang='kw'):
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
    outTexts = {
        'text':{'en':'Text',
                'kw':'Tekst'},
        'length':{'en':'length',
                  'kw':'hirder'},
        'words':{'en':'words',
                 'kw':'geryow'},
        'sample':{'en':'Sample word',
                  'kw':'Ger sampel'},
        'occur':{'en':'Number of occurances',
                 'kw':'Niver hwarvedhyansow'},
        'index':{'en': 'Indexes',
                 'kw': 'Menegennow'},
        'pcindex':{'en': 'Percent Indexes',
                   'kw': 'Menegennow Kansrann'},
        'xlab':{'en':'Percent location in text',
                'kw':'Savla kansrann y\'n tekst'}
    }

    outputtext = ""
    cfd = getCFD(kk_texts_Texts, casesensit)
    colors = "rgbcmk"
    ycoord = 0.1
    yticks = []
    if len(kk_texts_Texts) == 1:
        plt.figure()
        plt.title(names[0])
        axes = plt.gca()
        nwords = len(kk_texts_Texts[0])
        outputtext += "{a}: {t}, {b}: {l} {c}\n".format(a=outTexts['text'][outlang],
                                                        t=names[0],
                                                        b=outTexts['length'][outlang],
                                                        l=nwords,
                                                        c=outTexts['words'][outlang])
        for i,s in enumerate(samples):
            indexes = []
            pcindexes = []        
            for j,w in enumerate(kk_texts_Texts[0]):
                if not(casesensit):
                    w = w.lower()
                if s == w:
                    indexes.append(j)
                    pcindexes.append(round(100.0*j/nwords,1))
            print(s, zip(indexes, pcindexes))
            outputtext += "{a}: {s}. {b}: {n}\n{c}:{i}\n{d}: {p}\n".format(
                a = outTexts['sample'][outlang],
                n=len(indexes), s=s,
                b = outTexts['occur'][outlang],
                c = outTexts['index'][outlang],
                d = outTexts['pcindex'][outlang],
                i=indexes, p=pcindexes)
            col = colors[i % len(colors)]
            plt.plot(pcindexes, np.zeros(len(pcindexes)) + ycoord, "{c}s".format(c=col))
            yticks.append(ycoord)
            ycoord += 0.1
        axes.set_xlim([0,100])
        axes.set_ylim([0,0.1*len(samples)+0.1])
        axes.set_yticklabels(samples)
        axes.set_xlabel(outTexts['xlab'][outlang])
        axes.set_yticks(yticks)

            
    else:
        for s in samples:
            plt.figure()
            axes = plt.gca()
            plt.title(s)
            ycoord = 0.1
            outputtext += "{a}: {s}\n".format(a=outTexts['sample'][outlang],
                                              s=s)
            for j,(t,n) in enumerate(zip(kk_texts_Texts, names)):
                indexes = []
                pcindexes = []
                nwords = len(t)
                print(n)
                for i,w in enumerate(t):
                    if not(casesensit):
                        w = w.lower()
                    if s == w:
                        indexes.append(i)
                        pcindexes.append(round(100.0*i/nwords,1))
                print(s, zip(indexes,pcindexes))
                outputtext += "{a} {t}:\n{b}: {n}. {c}:{i}\n{d}: {p}\n".format(
                    a = outTexts['text'][outlang],
                    b = outTexts['occur'][outlang],
                    c = outTexts['index'][outlang],
                    d = outTexts['pcindex'][outlang],
                    t=n, n=len(indexes), i=indexes, p=pcindexes)
                col = colors[i % len(colors)]
                plt.plot(pcindexes, np.zeros(len(pcindexes))+ycoord,"{c}s".format(c=col))
                yticks.append(ycoord)            
                ycoord += 0.1
            outputtext += "\n"
            axes.set_xlim([0,100])
            axes.set_ylim([0,0.1*len(kk_texts_Texts)+0.1])            
            axes.set_yticklabels(names)
            axes.set_xlabel(outTexts['xlab'][outlang])
            axes.set_yticks(yticks)
        
    return outputtext
def corpusKW(manuscript=False, outlang='kw'):
    """
    do imports for traditional (and some revived) texts in Kemmyn
    """
    import read_kernewek_KK_texts
    if manuscript:
        kw_texts, names = read_kernewek_KK_texts.getMStexts(outlang=outlang)
    else:
        kw_texts, names = read_kernewek_KK_texts.getKKtexts(outlang=outlang)
    # use NLTK functions to select words
    kw_texts_words = [kw_texts.words(i) for i in kw_texts.fileids()]
    # select those words that are alphabetic
    kw_texts_words_alpha = [[w for w in t if w.isalpha()] for t in kw_texts_words]
    # make a NLTK text from the alphabetic words in each of the texts
    # then put into a list of nltk.Text 
    #kk_texts_Texts = [nltk.Text(i) for i in kk_texts_words]
    kw_texts_Texts = [nltk.Text(i) for i in kw_texts_words_alpha]
    # print kk_texts_words_alpha[0][:10]
    return kw_texts_Texts, names


def basicReportAll(kk_texts_Texts, textnames, topN=50, minL=4, pause=True, outlang='kw'):
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
    outTexts = {'input':{'en':'Press Enter to continue...\n',
                         'kw':'Gwask Enter dhe besya...\n'}
                }
    outputtext = ""
    for i in zip(kk_texts_Texts, textnames):
        outputtext += basicReport(i[0], i[1], topN, minL, outlang=outlang)
        if pause:
            if sys.version_info[0] < 3:
                w = raw_input(outTexts['input'][outlang])
            else:
                w = input(outTexts['input'][outlang])
            if w.lower() == "skip" or w.lower() == "lamma":
                pause = False
    return outputtext

def concordances(kk_texts_Texts, textnames, samples, width=59, lines=25, outlang='kw'):
    """ get the output for the .concordance() method of each nltk Text 
    
    @param kk_texts_Texts: a list of NLTK Texts.
    @type kk_texts_Texts: C{list}
    @param textnames: a list of the names of the texts.
    @type textnams: C{list}
    @param samples: A list of sample words to compare.
    @type samples: C{list}
    @param width: width to pass to the Text.concordances() method
    @type width: C{int}        
    @param lines: number of lines of concordance output to give
    @type lines: C{int}            
    """
    outTexts = {
        'concord':{'en':'Concordances\n',
                   'kw':'Konkordansow\n'},
        'sample':{'en':'Sample word',
                  'kw':'Ger sampel'},
        'text':{'en':'Text',
                'kw':'Tekst'},
        'context':{'en':'Words appearing in similar contexts to',
                   'kw':'Geryow a diskwa yn kettestennow haval dhe'}
        }
    buff = StringIO()
    temp = sys.stdout
    sys.stdout = buff
    #outputtext = ""
    print(outTexts['concord'][outlang])
    #outputtext += "Concordances\n"
    for s in samples:
        print("{a} {s}\n".format(a=outTexts['sample'][outlang],
                                 s=s))
        #outputtext += "Sample word {s}\n".format(s=s)
        for t,n in zip(kk_texts_Texts,textnames):
            print("{a}: {t}\n".format(a=outTexts['text'][outlang],
                                      t=n))
            #outputtext += "Text: {t}\n".format(t=n)
            t.concordance(s, width, lines)
            print("\n{a} {s}:".format(a=outTexts['context'][outlang],
                                      s=s))
            #outputtext += "Word appearing in similar contexts to {s}:\n".format(s=s)
            t.similar(s)
            print("\n")
    sys.stdout = temp

    outtext = buff.getvalue()
    # replace English text in NLTK concordance output if outlang is kw
    kwreplaces = [['Displaying', 'Ow tiskwedhes'], ['matches', 'hwarvedhyans'],
                  ['No', 'Nag eus'], [' of ', ' a ']]
    if outlang == 'kw':
        for r in kwreplaces:
            outtext = outtext.replace(r[0], r[1])        
    return outtext

def findallRegex(kk_texts_Texts, textnames, regexes=["<.*><a><vynn>", "<.*><a><wra>", "<y><fynn.*>","<y><hwr.*>"], outlang='kw'):
    outTexts = {
        'regexsearch':{'en':'Regular Expression findall\n',
                   'kw':'findall Ekspresyans Reyth\n'},
        'regex':{'en':'Regex',
                  'kw':'Regex'},
        'text':{'en':'Text',
                'kw':'Tekst'},
        'noccur':{'en': 'N occurances',
                'kw':'N hwarvedhyansow'}
        }
    buff = StringIO()
    temp = sys.stdout
    sys.stdout = buff
    
    print(outTexts['regexsearch'][outlang])
    for r in regexes:
        print("{a} {r}\n".format(a=outTexts['regex'][outlang],
                                 r=r))
        #outputtext += "Sample word {s}\n".format(s=s)
        for t,n in zip(kk_texts_Texts,textnames):
            print("{a}: {t}\n".format(a=outTexts['text'][outlang],
                                      t=n))
            #outputtext += "Text: {t}\n".format(t=n)
            prevbuff = buff.getvalue()
            t.findall(r) 
            regexpoutput = buff.getvalue()
            regexpoutput = regexpoutput.replace(prevbuff, "")
            print(regexpoutput)
            if regexpoutput:           
                noccur = len(regexpoutput.split("; "))
            else:
                noccur = 0
            print("{a} {r}: {n}\n".format(a=outTexts['noccur'][outlang], n=noccur, r=r))
            
            print("\n")
    sys.stdout = temp
    outtext = buff.getvalue()
    return outtext

def generateText(kk_texts_Texts, textnames):
    """ not used at present because it doesn't work
    on NLTK version 3 """
    buff = StringIO()
    temp = sys.stdout
    sys.stdout = buff
    #outputtext = ""
    print("Generated text\n")
    #outputtext += "Generated text\n"
    
    for t,n in zip(kk_texts_Texts,textnames):
        print("Text: {t}\n".format(t=n))
        #outputtext += "Text: {t}\n".format(t=n)
        t.generate()
        print("\n")
    sys.stdout = temp
    return buff.getvalue()
        
def freqCompareInterAct(casesensit=False, interactive=True, outlang='kw'):
    """ 
    Request words from the command line input and
    run compareSamples() to compare their frequencies.
    
    @param casesensit: whether to be case sensitive
    @type casesensit: C{bool}
    @param interactive: whether to use interactive mode. If False, use a
    default list of samples.
    @type interactive: C{bool}
    """
    outTexts = {
        'intro':{'en':"Please enter a word to compare frequency across the texts.\nEnter the word 'default' to use the default wordlist.\nPress Enter without any text to stop building the wordlist and draw the graph:",
                 'kw':"Gorr ger mar pleg dhe gesheveli menowgher dres an tekstow.\nGorr an ger 'default' dhe usya an rol ger defowt.\nGorr Enter heb tekst dhe hedhi drehevel an rol ger ha delinya an tresenn:"},
        'input':{'en':'Enter word:\n',
                 'kw':'Gorr ger:\n'},
        'barchart':{'en':'Plot bar chart word frequency plot (y/n)?\n',
                    'kw':'Delinya tresenn menowghder ger barr (y/n)?\n'},        
        'lexdesp':{'en':'Plot lexical dispersion plot (y/n)?\n',
                   'kw':'Delinya tresenn keskar ger (y/n)?\n'},
        'concord':{'en':'Output concordances (y/n)?\n',
                   'kw':'Diskwedhes konkordansow (y/n)?\n'}        
        }
    defaultsamples = ["a","ha","an","dhe","yn","yw","ow","ev","rag","mes","esa","yth","y"]
    print(outTexts['intro'][outlang])
    # the words to compare abundance of across the texts
    
    if not(interactive):
        samples = defaultsamples
    else:
        samples = []
        while interactive:
            if sys.version_info[0] < 3:
                w = raw_input(outTexts['input'][outlang])
            else:
                w = input(outTexts['input'][outlang])
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
        if len(samples) == 0:
            samples = defaultsamples
    if not(casesensit):
        samples = [s.lower() for s in samples]
    samples = sorted(set(samples))    

    if sys.version_info[0] < 3:
        w = raw_input(outTexts['barchart'][outlang])
        w2 = raw_input(outTexts['lexdesp'][outlang])
        w3 = raw_input(outTexts['concord'][outlang])
    else:
        w = input(outTexts['barchart'][outlang])
        w2 = input(outTexts['lexdesp'][outlang])
        w3 = input(outTexts['concord'][outlang])        

    if w.isalpha() and w[0].lower()=="y":
        compareSamples(kk_texts_Texts,names, samples)
    if w2.isalpha() and w2[0].lower()=="y":
        compareSamplesLinear(kk_texts_Texts,names, samples)
    if w3.isalpha() and w3[0].lower()=="y":
        print(concordances(kk_texts_Texts,names, samples))

if __name__ == '__main__':
    outTexts = {'cumfreq':{'en':'Plot cumulative frequency plot for lengths of words (y/n)?\n',
                           'kw':'Delinya tresenn menowghder kumulativ hirder geryow (y/n)?\n'}
                }
                
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manuscript", action="store_true",
help="Use manuscript spelling texts instead of Kemmyn.")
    parser.add_argument("-e", "--english", action="store_true",
help="Output explanatory text in English (default is Cornish).")
    args = parser.parse_args()
    if args.english:
        outlang = 'en'
    else:
        outlang = 'kw'    
    kk_texts_Texts, names = corpusKW(args.manuscript, outlang=outlang)
    basicReportAll(kk_texts_Texts, names, outlang=outlang)
    if sys.version_info[0] < 3:
        w = raw_input(outTexts['cumfreq'][outlang])
    else:
        w = input(outTexts['cumfreq'][outlang])
    if w.isalpha():
        if w[0].lower()=="y":
            nLettersFDist(kk_texts_Texts,names, outlang=outlang)
            plt.figure()
    freqCompareInterAct(outlang=outlang)    
    plt.show()
