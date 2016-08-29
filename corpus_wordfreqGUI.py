from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Entrybar, Radiobar, ScrolledText
import matplotlib.pyplot as plt
import copy

comparelist = []
defaultsamples = ["a","ha","an","dhe","yn","yw","ow","ev","rag","mes","esa","yth","y"]

def checkNLTK():
    try:
        import nltk
    except ImportError:
        return 0
    return 1
    
def addtocomparelist():
    newword = ent3.fetch()
    if "," in newword:
        newwordlist = newword.split(",")
        newwordlist = [w.strip() for w in newwordlist]
        newwordlist = [w.lower() for w in newwordlist if w.isalpha()]
        comparelist.extend(newwordlist)
    else:
        newword = newword.strip()
        newword = newword.lower()
        comparelist.append(newword)
        outbox.settext(comparelist)
    ent3.clear()
        
def clearcomparelist():
    del comparelist[:]
    outbox.settext("")

def getcomparelist():
    return comparelist

def clearfigures():
    plt.close("all")
    
def allstates(): print(textchoice.state(), modechoice.state(), ent.fetch(), ent2.fetch(), ent3.fetch())

def getIntMinL(eboxtext, defaultval=1):
    """ get integer for minimum word length, or for number of frequencies to return. """
    try:
        minL = int(eboxtext)
    except ValueError:
        print("warning, input cannot be converted to integer. using value of {d}".format(d=defaultval))
        minL = defaultval
    return minL
    
def printoutput():
    """ show the output """
    if modechoice.state() == 'Derivas Ollgemmyn':
        topN = getIntMinL(ent2.fetch(), 20)
        minL = getIntMinL(ent.fetch(), 4)
        if textchoice.state() == 'Oll an Tekstow':
            outbox.settext(cornish_corpus.basicReportAll(kk_texts,
                                                         names, topN, minL,
                                                         pause=False))
        else:
            outbox.settext(cornish_corpus.basicReport(
                kk_text_dict[textchoice.state()], textchoice.state(),
                topN, minL))                       
    if modechoice.state() == 'Rol Menoghderow Ger':
        topN = getIntMinL(ent2.fetch(), 20)
        minL = getIntMinL(ent.fetch())
        if textchoice.state() == 'Oll an Tekstow':
            outbox.settext(cornish_corpus.MostFrequentWords(kk_texts, names,
                                                            topN, minL))
        else:
            outbox.settext(cornish_corpus.MostFreqWords1Text(
                kk_text_dict[textchoice.state()], textchoice.state(),
                topN, minL))
    if modechoice.state() == 'Hirder Geryow\n(tresenn menowghder kumulativ)':
        plt.figure()
        if textchoice.state() == 'Oll an Tekstow':
            outbox.settext(cornish_corpus.nLettersFDist(kk_texts,names))
        else:
            outbox.settext(cornish_corpus.nLettersFDist(
                [kk_text_dict[textchoice.state()]],[textchoice.state()]))
        plt.show()
    if modechoice.state() == 'Menowghder Ger\n(tresenn barr)':
        plt.figure()
        comparelist = getcomparelist()
        if len(comparelist) == 0:
            comparelist = defaultsamples           
        outbox.text.config(bg = 'light yellow', fg = 'dark red',
                               font=('Courier', 12, 'normal'))
        if textchoice.state() == 'Oll an Tekstow': 
            outbox.settext(str(comparelist)+'\n\n'+cornish_corpus.compareSamples(
            kk_texts, names, comparelist))
        else:
            outbox.settext(str(comparelist)+'\n\n'+cornish_corpus.compareSamples(
            [kk_text_dict[textchoice.state()]],[textchoice.state()], comparelist))        
        plt.show()     
                
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Corpus Kernewek')

    mhead = tk.Label(root, text = "Tekst")
    mhead.config(font=('Helvetica', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)
    # check NLTK is available
    c = checkNLTK()
    print("NLTK available = {c}".format(c=c))
    if c == 0:
        names = ["Bewnans Meryasek","Gwreans an Bys","Origo Mundi",
        "Passio Christ","Resurrectio Domini","Solemptnyta","LoTR chapter",
        "Tregear Homilies"]
    else:
        import cornish_corpus
        kk_texts, names = cornish_corpus.corpusKK()
        kk_text_dict = {k:v for (k,v) in zip(names, kk_texts)}
    # choose text
    textmenu = copy.copy(names)
    textmenu.append("Oll an Tekstow")
    textchoice = Radiobar(root, textmenu, side=tk.TOP, anchor=tk.NW,
                          default='Bewnans Meryasek', justify=tk.LEFT)
    textchoice.pack(side=tk.LEFT, fill=tk.Y)
    textchoice.config(relief=tk.RIDGE, bd=2)
    mhead2 = tk.Label(root, text="Dewis Gwrythyans")
    mhead2.config(font=('Helvetica', 16, 'bold'))
    mhead2.pack(side=tk.TOP, anchor=tk.NW)
    
    modechoice = Radiobar(root, ['Derivas Ollgemmyn', 'Rol Menoghderow Ger',
                                 'Hirder Geryow\n(tresenn menowghder kumulativ)',
                                 'Menowghder Ger\n(tresenn barr)'],
                          side=tk.TOP, anchor=tk.NW, justify = tk.LEFT, default = 'Derivas Ollgemmyn')
    msg = tk.Label(modechoice, text="Keworrowgh isella niver a lytherennow\nrag rolyow menoghder ger a-woeles:",
                   anchor=tk.W, justify=tk.LEFT, pady=10)
    msg.config(font=('Helvetica', 12))
    msg.pack(anchor=tk.W)
    ent = Entrybar(modechoice,
                   anchor=tk.NW)
    ent.pack(anchor=tk.W)
    msg2 = tk.Label(modechoice, text="Keworrowgh niver a eryow dhe dherivas\nan menowghder a-woeles:\ndefowt = 20",
                    anchor=tk.W, justify=tk.LEFT, pady=10)
    msg2.config(font=('Helvetica', 12))
    msg2.pack(anchor=tk.W)
    ent2 = Entrybar(modechoice,
                    anchor=tk.NW)
    ent2.pack(anchor=tk.W)
    msg3 = tk.Label(modechoice, text="Keworrowgh ger dhe geheveli\nmenowghderow dres an tekstow:",
                    anchor=tk.W, justify=tk.LEFT, pady=10)
    msg3.config(font=('Helvetica', 12))
    msg3.pack(anchor=tk.W)
    ent3 = Entrybar(modechoice,
                    anchor=tk.NW)
    ent3.pack(anchor=tk.W)        
    keworra = tk.Button(modechoice, text="Keworra ger dhe'n rol", font=('Helvetica', 14),
              command = addtocomparelist)
    klerhe = tk.Button(modechoice, text='Klerhe an rol', font=('Helvetica', 14),
              command = clearcomparelist)
    keworra.pack(anchor=tk.NW, pady=10)
    klerhe.pack(anchor=tk.NW, pady=10)        
    modechoice.pack(side=tk.LEFT, fill=tk.Y)
    modechoice.config(relief=tk.RIDGE, bd=2)
    outbox = ScrolledText(root)
    outbox.text.config(bg = 'light yellow', fg = 'dark red', width=60, height=20,
                    font=('Courier', 14, 'bold'))

    outbox.pack()
    c=checkNLTK()
    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    dalleth = tk.Button(root, text = 'Dalleth', font=('Helvetica',14),
                        command = printoutput)
    klerhefigs = tk.Button(root, text = 'Klerhe Tresennow', font=('Helvetica',14),
                           command = clearfigures)
    
    if c == 0:
        dalleth['state']=tk.DISABLED
        outbox.settext("Python Natural Language Processing Toolkit (NLTK) not available.\nDownload from www.nltk.org if not on the system.")
    klerhefigs.pack(side=tk.RIGHT)
    dalleth.pack(side=tk.RIGHT)   



    root.mainloop()


