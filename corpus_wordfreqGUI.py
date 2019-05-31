# coding=utf-8
from __future__ import print_function
import sys, argparse
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya2, Entrybar, Radiobar, ScrolledText, wraplines
import matplotlib.pyplot as plt
import copy
import textwrap


try:
    import cornish_corpus
except ImportError:
    print("error importing cornish_corpus")

    
comparelist = []
defaultsamples = ['dhe', 'gans', 'war', 'dhymm', 'dhymmo', 'genev', 'warnav', 'rag', 'mes']
#["a","ha","an","dhe","yn","yw","ow","ev","rag","mes","esa","yth","y"]
class CorpusStats(tk.Frame):
    labelTexts = {'modechoice': {'en':['General Report',
                                       'Word Frequencies List',
                                       'Letter Frequencies List',
                                       'Letter Frequencies List\n(without digraphs)',
                                       'Length of words\n(cumulative frequency graph)',
                                       'Word Frequency Bar Chart',
                                       'Lexical Dispersion Plot',
                                       'Concordance'],
                                 'kw':['Derivas Ollgemmyn',
                                       'Rol Menowghderow Ger',
                                       'Rol Menowghderow Lytherenn',
                                       'Rol Menowghderow Lytherenn\n(heb dilytherennow)',
                                       'Hirder Geryow\n(tresenn menowghder kumulativ)',
                                       'Menowghder Ger (tresenn barr)',
                                       'Tresenn Keskar Ger',
                                       'Konkordans']},
                  'textchoice':{'en':['Life of Meryasek',
                                      'Charter Fragment',
                                      'Creation of the World',
                                      'Passion of our Lord',
                                      'Origo Mundi',
                                      'Passio Christ',
                                      'Resurrectio Domini',
                                      'Skeul an Yeth 1 examples',
                                      'Solemptnyta',
                                      'LoTR chapters',
                                      'Tregear Homilies',
                                      'All Texts'],
                                'kw':['Bewnans Meryasek',
                                      'Darn Chartour',
                                      'Gwreans an Bys',
                                      'Passhyon Agan Arloedh',
                                      'Origo Mundi',
                                      'Passio Christ',
                                      'Resurrectio Domini',
                                      'Ensamplow Skeul an Yeth 1',
                                      'Solemptnyta',
                                      'Chapters Arloedh an Bysowyer',
                                      'Pregothow Tregear',
                                      'Oll an Tekstow']},
                  'textchoicems':{'en':['Life of Ke',
                                      'Charter Fragment',
                                      'Creation of the World',
                                      'Passion of our Lord',
                                      'Origo Mundi',
                                      'Passio Christ',
                                      'Resurrectio Domini',
                                      'All Texts'],
                                'kw':['Bewnans Ke',
                                      'Darn Chartour',
                                      'Gwreans an Bys',
                                      'Passhyon Agan Arloedh',
                                      'Origo Mundi',
                                      'Passio Christ',
                                      'Resurrectio Domini',
                                      'Oll an Tekstow']},   
                  'mhead':{False:{'en': 'Text (Kemmyn)',
                                  'kw': 'Tekst (Kemmyn)'},
                           True:{'en': 'Text (Manuscript)',
                                 'kw': 'Tekst (Mammskrif)'}},
                  'mhead2':{'en': 'Options',
                            'kw': 'Dewis Gwrythyans'},
                  'msg': {'en': 'Enter the minimum number of letters\nfor word frequency list below:',
                          'kw': 'Keworrowgh isella niver a lytherennow\nrag rolyow menoghder ger a-woeles:'},
                  'msg2':{'en': 'Enter the number of words to report\nfrequency of below:\ndefault = 20',
                          'kw': 'Keworrowgh niver a eryow dhe dherivas\nan menowghder a-woeles:\ndefowt = 20'},
                  'msg3':{'en': 'Enter a word to compare frequencies of\nacross the texts:',
                          'kw': 'Keworrowgh ger dhe geheveli\nmenowghderow dres an tekstow:'},
                  'keworra':{'en': 'Add word to the list',
                             'kw': "Keworra ger dhe'n rol"},
                  'klerhe': {'en': 'Clear the list',
                             'kw': 'Klerhe an rol'},
                  'dalleth': {'en': 'Start',
                              'kw': 'Dalleth'},
                  'klerhefigs': {'en': 'Clear Figures',
                                 'kw': 'Klerhe Tresennow'},
                  'klyppbordh': {'en': 'Copy to Clipboard',
                                 'kw': "Kopi dhe'm Klyppbordh"},
                  'switchlang': {'en':'Kernewek',
                                 'kw': 'English'},
                  'switchms':{False:{'en':'Switch to manuscript',
                                     'kw':'Skwychya dhe Vammskrif'},
                              True:{'en':'Switch to Kemmyn',
                                    'kw':'Skwychya dhe Gemmyn'}},
                  'windowtitle': {'en': 'Cornish Corpus Statistics',
                                  'kw': 'Korpus Kernewek'},
                  'NLTKerr':{'en': 'Python Natural Language Processing Toolkit (NLTK) not available.\nDownload from www.nltk.org if not on the system.',
                             'kw': 'Nyns yw Python Natural Language Processing Toolkit (NLTK) kavadow.\nIskargewgh diworth www.nltk.org mar nyns yw war agas jynn-amontya.'}
    }

    def __init__(self, parent = None, netbook=False, english=False, mscript=False):
        tk.Frame.__init__(self, parent)
        if english:
            self.ifacelang = 'en'
        else:
            self.ifacelang = 'kw'
        self.mscript = mscript
        self.netbook = netbook
        if self.netbook:
            self.heightadjust = -8
            self.fontsizeadj = -4
            self.padadj = -5
            self.wline = 50
        else:
            self.heightadjust = 0
            self.fontsizeadj = 0
            self.padadj = 0
            self.wline = 60
        self.comparelist = []
        self.defaultsamples = ['dhe', 'gans', 'war', 'dhymm', 'dhymmo', 'genev', 'warnav', 'rag', 'mes']
        self.master.title(CorpusStats.labelTexts['windowtitle'][self.ifacelang])
        self.pack()
        self.make_widgets()
        
    def make_widgets(self):
        """ display GUI widgets """
        self.mhead = tk.Label(self, text = CorpusStats.labelTexts['mhead'][self.mscript][self.ifacelang])
        self.mhead.config(font=('Helvetica', 16+self.fontsizeadj, 'bold'))
        self.mhead.pack(side=tk.TOP, anchor=tk.NW)        
        c = self.checkNLTK()
        print("NLTK available = {c}".format(c=c))
        if c == 0:
            self.names = ["Bewnans Meryasek", "Charter Fragment", "Gwreans an Bys",
                          "Passhyon Agan Arloedh", "Origo Mundi",
                          "Passio Christ","Resurrectio Domini", "Skeul an Yeth 1", "Solemptnyta",
                          "LoTR chapters", "Tregear Homilies"]
        else:
            # import cornish_corpus
            # uneccesary as done already
            self.kk_texts, self.names = cornish_corpus.corpusKW(args.manuscript, outlang=self.ifacelang)
            self.kk_text_dict = {k:v for (k,v) in zip(self.names, self.kk_texts)}
        if self.mscript:
            textmenu = CorpusStats.labelTexts['textchoicems'][self.ifacelang]
            # make all texts option still 10 even though there are fewer texts in manuscript spelling
            optionnums = list(range(len(textmenu)-1))
            optionnums.append(10)
        else:
            textmenu = CorpusStats.labelTexts['textchoice'][self.ifacelang]
            optionnums = list(range(len(textmenu)))
            
        self.textchoice = Radiobar(self, textmenu, vals=optionnums, side = tk.TOP, anchor = tk.NW,
                                   default = 2, justify=tk.LEFT,
                                   font=('Helvetica', 13+self.fontsizeadj, 'normal'))
        self.textchoice.pack(side=tk.LEFT, fill=tk.Y)
        self.textchoice.config(relief=tk.RIDGE, bd=2)
        self.switchlang = tk.Button(self.textchoice, text=CorpusStats.labelTexts['switchlang'][self.ifacelang],
                                    font=('Helvetica', 14+self.fontsizeadj), command=self.changeifacelang)
        self.switchlang.pack(anchor=tk.SW, side=tk.LEFT, padx=10, pady=10)
        self.switchms = tk.Button(self.textchoice, text=CorpusStats.labelTexts['switchms'][self.mscript][self.ifacelang],
                                    font=('Helvetica', 14+self.fontsizeadj), command=self.switchms)
        self.switchms.pack(anchor=tk.SW, side=tk.LEFT, padx=10, pady=10)
        

        self.mhead2 = tk.Label(self, text=CorpusStats.labelTexts['mhead2'][self.ifacelang])
        self.mhead2.config(font=('Helvetica', 16+self.fontsizeadj*2, 'bold'))
        self.mhead2.pack(side=tk.TOP, anchor=tk.NW)
        mchoicetext = CorpusStats.labelTexts['modechoice'][self.ifacelang]
        mchoicevals = range(len(mchoicetext))
        self.modechoice = Radiobar(self, mchoicetext,
                                   vals = mchoicevals,
                                   side=tk.TOP, anchor=tk.NW, justify=tk.LEFT, default = 0,
                                   font = ('Helvetica',13+self.fontsizeadj, 'normal'))
        self.msg1 = tk.Label(self.modechoice, text=CorpusStats.labelTexts['msg'][self.ifacelang],
                             anchor=tk.W, justify=tk.LEFT, pady=10+self.padadj)
        self.msg1.config(font=('Helvetica', 12+self.fontsizeadj))
        self.msg1.pack(anchor=tk.W)
        self.ent = Entrybar(self.modechoice,
                            anchor=tk.NW)
        self.ent.pack(anchor=tk.W, padx=5)        
        self.msg2 = tk.Label(self.modechoice, text=CorpusStats.labelTexts['msg2'][self.ifacelang],
                             anchor=tk.W, justify=tk.LEFT, pady=10+self.padadj)
        self.msg2.config(font=('Helvetica', 12+self.fontsizeadj))
        self.msg2.pack(anchor=tk.W)
        self.ent2 = Entrybar(self.modechoice,
                             anchor=tk.NW)
        self.ent2.pack(anchor=tk.W, padx=5)        
        self.msg3 = tk.Label(self.modechoice, text=CorpusStats.labelTexts['msg3'][self.ifacelang],
                             anchor=tk.W, justify=tk.LEFT, pady=10+self.padadj)
        self.msg3.config(font=('Helvetica', 12+self.fontsizeadj))
        self.msg3.pack(anchor=tk.W, padx=5)        
        self.ent3 = Entrybar(self.modechoice,
                             anchor=tk.NW)
        self.ent3.pack(anchor=tk.W, padx=5)
        self.keworra = tk.Button(self.modechoice, text=CorpusStats.labelTexts['keworra'][self.ifacelang],
                                 font=('Helvetica', 14+self.fontsizeadj),
                                 command = self.addtocomparelist)
        self.klerhe = tk.Button(self.modechoice, text=CorpusStats.labelTexts['klerhe'][self.ifacelang],
                                font=('Helvetica', 14+self.fontsizeadj),
                                command = self.clearcomparelist)
        self.keworra.pack(anchor=tk.NW, side=tk.LEFT, pady=10)
        self.klerhe.pack(anchor=tk.NW, side=tk.LEFT, pady=10)
        self.modechoice.pack(side=tk.LEFT, fill=tk.Y)
        self.modechoice.config(relief=tk.RIDGE, bd=2)
        self.outbox = ScrolledText(self)
        self.outbox.text.config(bg = 'light yellow', fg = 'dark red', width=60, height=20+self.heightadjust,
                                font=('Courier', 14+self.fontsizeadj, 'bold'))
        self.outbox.pack()
        # buttons
        self.Kwitya = Kwitya2(self)
        self.Kwitya.pack(side=tk.RIGHT)
        self.dalleth = tk.Button(self, text = CorpusStats.labelTexts['dalleth'][self.ifacelang],
                                 font=('Helvetica',14),
                                 command = self.printoutput)
        self.klerhefigs = tk.Button(self, text = CorpusStats.labelTexts['klerhefigs'][self.ifacelang],
                                    font=('Helvetica',14+self.fontsizeadj),
                                    command = self.clearfigures)
        self.klyppbordh = tk.Button(self, text = CorpusStats.labelTexts['klyppbordh'][self.ifacelang],
                                    font=('Helvetica', 14+self.fontsizeadj),
                                    command = self.copyclipbd)
    
        if c == 0:
            self.dalleth['state']=tk.DISABLED
            self.outbox.settext(CorpusStats.labelTexts['NLTKerr'][self.ifacelang])
        self.klerhefigs.pack(side=tk.RIGHT)
        self.dalleth.pack(side=tk.RIGHT)
        self.klyppbordh.pack(side=tk.LEFT)              

    def checkNLTK(self):
        try:
            import nltk
        except ImportError:
            return 0
        return 1
    
    def addtocomparelist(self):
        newword = self.ent3.fetch()
        if "," in newword:
            newwordlist = newword.split(",")
            newwordlist = [w.strip() for w in newwordlist]
            newwordlist = [w.lower() for w in newwordlist if w.isalpha()]
            self.comparelist.extend(newwordlist)
        else:
            newword = newword.strip()
            newword = newword.lower()
            self.comparelist.append(newword)
        self.outbox.settext(self.comparelist)
        self.ent3.clear()
        
    def clearcomparelist(self):
        del self.comparelist[:]
        self.outbox.settext("")

    def getcomparelist(self):
        return self.comparelist

    def clearfigures(self):
        plt.close("all")
        self.focus_force()
    
    def allstates(self): print(self.textchoice.state(), self.modechoice.state(), self.ent.fetch(), self.ent2.fetch(), self.ent3.fetch())

    def getIntMinL(self, eboxtext, defaultval=1):
        """ get integer for minimum word length, or for number of frequencies to return. """
        try:
            minL = int(eboxtext)
        except ValueError:
            print("warning, input cannot be converted to integer. using value of {d}".format(d=defaultval))
            minL = defaultval
        return minL

    def changeifacelang(self):
        if self.ifacelang == 'kw':
            self.ifacelang = 'en'
        else:
            self.ifacelang = 'kw'
        self.switchlang.config(text=self.labelTexts['switchlang'][self.ifacelang])
        self.switchms.config(text=self.labelTexts['switchms'][self.mscript][self.ifacelang])
        self.master.title(self.labelTexts['windowtitle'][self.ifacelang])
        self.mhead.config(text=self.labelTexts['mhead'][self.mscript][self.ifacelang])
        if self.mscript:
            newpicks = self.labelTexts['textchoicems'][self.ifacelang]
        else:
            newpicks = self.labelTexts['textchoice'][self.ifacelang]
        for p,r in zip(newpicks, self.textchoice.rads):
            r.config(text=p)
            
        self.mhead2.config(text=self.labelTexts['mhead2'][self.ifacelang])
        newpicks = self.labelTexts['modechoice'][self.ifacelang]
        for p,r in zip(newpicks, self.modechoice.rads):
            r.config(text=p)        
        self.msg1.config(text=self.labelTexts['msg'][self.ifacelang])
        self.msg2.config(text=self.labelTexts['msg2'][self.ifacelang])
        self.msg3.config(text=self.labelTexts['msg3'][self.ifacelang])
        self.keworra.config(text=self.labelTexts['keworra'][self.ifacelang])
        self.klerhe.config(text=self.labelTexts['klerhe'][self.ifacelang])
        self.dalleth.config(text=self.labelTexts['dalleth'][self.ifacelang])
        self.klerhefigs.config(text=self.labelTexts['klerhefigs'][self.ifacelang])
        self.klyppbordh.config(text=self.labelTexts['klyppbordh'][self.ifacelang])
        # reload texts to get new names
        self.kk_texts, self.names = cornish_corpus.corpusKW(self.mscript, outlang=self.ifacelang)
        self.kk_text_dict = {k:v for (k,v) in zip(self.names, self.kk_texts)}
        # rerun self.printoutput to show results in new interface language
        self.printoutput()

    def switchms(self):
        self.mscript = not(self.mscript)
        self.mhead.config(text=self.labelTexts['mhead'][self.mscript][self.ifacelang])
        currstate = self.textchoice.state()
        self.textchoice.destroyrads()
        self.switchlang.pack_forget()
        self.switchms.pack_forget()
        #self.textchoice.pack_forget()
        # reload texts to get new names
        self.kk_texts, self.names = cornish_corpus.corpusKW(self.mscript, outlang=self.ifacelang)
        self.kk_text_dict = {k:v for (k,v) in zip(self.names, self.kk_texts)}
        if self.mscript:
            textmenu = CorpusStats.labelTexts['textchoicems'][self.ifacelang]
        else:
            textmenu = CorpusStats.labelTexts['textchoice'][self.ifacelang]
            
        # make all texts option still 11 even though there are fewer texts in manuscript spelling
        optionnums = list(range(len(textmenu)-1))
        optionnums.append(11)
        if currstate not in optionnums:
            currstate = 2
        self.textchoice.newrads(picks=textmenu, vals=optionnums,
                                default=currstate)
        self.switchms.config(text=self.labelTexts['switchms'][self.mscript][self.ifacelang])
        self.switchlang.pack(anchor=tk.SW, side=tk.LEFT, padx=10, pady=10)
        self.switchms.pack(anchor=tk.SW, side=tk.LEFT, padx=10, pady=10)
        # rerun self.printoutput to show results in manuscript / Kemmyn
        self.printoutput()        
        
    def printoutput(self):
        """ show the output """
        if self.modechoice.state() == 0:
            topN = self.getIntMinL(self.ent2.fetch(), 20)
            minL = self.getIntMinL(self.ent.fetch(), 4)
            if self.textchoice.state() == 11:
                outputtext = cornish_corpus.basicReportAll(self.kk_texts,
                                                           self.names, topN, minL,
                                                           pause=False,
                                                           outlang=self.ifacelang)
            else:
                outputtext = cornish_corpus.basicReport(
                    self.kk_text_dict[self.names[self.textchoice.state()]],
                    self.names[self.textchoice.state()],
                    topN, minL,
                    outlang=self.ifacelang)
            outputtext = wraplines(outputtext, self.wline)
            
            self.outbox.settext(outputtext)
        if self.modechoice.state() == 1:
            # rol menowghder ger
            topN = self.getIntMinL(self.ent2.fetch(), 20)
            minL = self.getIntMinL(self.ent.fetch())
            if self.textchoice.state() == 11:
                self.outbox.settext(cornish_corpus.MostFrequentWords(self.kk_texts, self.names,
                                                                     topN, minL,
                                                                     outlang=self.ifacelang))
            else:
                self.outbox.settext(cornish_corpus.MostFreqWords1Text(
                    self.kk_text_dict[self.names[self.textchoice.state()]], self.names[self.textchoice.state()],
                    topN, minL,
                    outlang=self.ifacelang))
        if self.modechoice.state() == 2:
            if self.textchoice.state() == 11:
                self.outbox.settext(cornish_corpus.MostFreqLetters(self.kk_texts, self.names, outlang=self.ifacelang))
            else:
                self.outbox.settext(cornish_corpus.MostFreqLetters1Text(
                    self.kk_text_dict[self.names[self.textchoice.state()]], self.names[self.textchoice.state()],
                    outlang=self.ifacelang))
        if self.modechoice.state() == 3:
            if self.textchoice.state() == 11:
                self.outbox.settext(cornish_corpus.MostFreqLetters(self.kk_texts, self.names, False, False,
                                                                   outlang=self.ifacelang))
            else:
                self.outbox.settext(cornish_corpus.MostFreqLetters1Text(
                    self.kk_text_dict[self.names[self.textchoice.state()]], self.names[self.textchoice.state()],
                    False, False, outlang=self.ifacelang))
               
        if self.modechoice.state() == 4:
            plt.figure()
            if self.textchoice.state() == 11:
                self.outbox.settext(cornish_corpus.nLettersFDist(self.kk_texts,self.names, outlang=self.ifacelang))
            else:
                self.outbox.settext(cornish_corpus.nLettersFDist(
                    [self.kk_text_dict[self.names[self.textchoice.state()]]],[self.names[self.textchoice.state()]],
                    outlang=self.ifacelang))
            plt.show()
        if self.modechoice.state() == 5:
            plt.figure()
            comparelist = self.getcomparelist()
            if len(comparelist) == 0:
                comparelist = self.defaultsamples           
            self.outbox.text.config(bg = 'light yellow', fg = 'dark red',
                                    font=('Courier', 12+self.fontsizeadj, 'normal'))
            if self.textchoice.state() == 11:
                outputtext = str(comparelist)+'\n\n'+cornish_corpus.compareSamples(
                    self.kk_texts, self.names, comparelist,
                    outlang=self.ifacelang)
            else:
                outputtext = str(comparelist)+'\n\n'+cornish_corpus.compareSamples(
                    [self.kk_text_dict[self.names[self.textchoice.state()]]],
                    [self.names[self.textchoice.state()]],
                    comparelist, outlang=self.ifacelang)
            outputtext = wraplines(outputtext, self.wline)
            self.outbox.settext(outputtext)        
            plt.show()
        if self.modechoice.state() == 6:
            comparelist = self.getcomparelist()
            if len(comparelist) == 0:
                comparelist = self.defaultsamples
            self.outbox.text.config(bg = 'light yellow', fg = 'dark red',
                                    font=('Courier', 12+self.fontsizeadj, 'normal'))
            if self.textchoice.state() == 11:
                outputtext = str(comparelist)+'\n\n'+cornish_corpus.compareSamplesLinear(
                    self.kk_texts, self.names, comparelist, outlang=self.ifacelang)
            else:
                outputtext = str(comparelist)+'\n\n'+cornish_corpus.compareSamplesLinear(
                    [self.kk_text_dict[self.names[self.textchoice.state()]]],
                    [self.names[self.textchoice.state()]],
                    comparelist, outlang=self.ifacelang)
            outputtext = wraplines(outputtext, self.wline)           
            self.outbox.settext(outputtext)
            plt.show()
        if self.modechoice.state() == 7:
            comparelist = self.getcomparelist()
            if len(comparelist) == 0:
                comparelist = ['dhe', 'gans']
            self.outbox.text.config(bg = 'light yellow', fg = 'dark red',
                                    font=('Courier', 12+self.fontsizeadj, 'normal'))
            if self.textchoice.state() == 11:
                outputtext = str(comparelist)+'\n\n'+cornish_corpus.concordances(
                    self.kk_texts, self.names, comparelist, 60, 25, outlang=self.ifacelang)
            else:
                outputtext = str(comparelist)+'\n\n'+cornish_corpus.concordances(
                    [self.kk_text_dict[self.names[self.textchoice.state()]]],
                    [self.names[self.textchoice.state()]],
                    comparelist, 60,25, outlang=self.ifacelang)
            outputtext = wraplines(outputtext, self.wline)
            self.outbox.settext(outputtext)                
    def copyclipbd(self):
        self.clipboard_clear()
        self.clipboard_append(self.outbox.gettext())
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--netbook", action="store_true",
                        help="Netbook mode - for smaller screens.")
    parser.add_argument("-m", "--manuscript", action="store_true",
                        help="Use manuscript spelling texts instead of Kemmyn.")
    parser.add_argument("-e", "--english", action="store_true",
                        help="Start with interface in English (default is Cornish).")    
    args = parser.parse_args()

    corpus = CorpusStats(netbook=args.netbook, english=args.english, mscript=args.manuscript)
    corpus.mainloop()    
