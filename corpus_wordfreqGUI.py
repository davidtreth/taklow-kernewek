from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Entrybar, Radiobar, ScrolledText
import cornish_corpus
import matplotlib
import pylab

comparelist = []
defaultsamples = ["a","ha","an","dhe","yn","yw","ow","ev","rag","mes","esa","yth","y"]

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
    comparelist = []
    outbox.settext("")

def getcomparelist():
    return comparelist

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
        outbox.settext(cornish_corpus.basicReport(kk_text_dict[textchoice.state()], textchoice.state(), topN, minL))                       
    if modechoice.state() == 'Rol Menoghderow Ger':
        topN = getIntMinL(ent2.fetch(), 20)
        minL = getIntMinL(ent.fetch())
        outbox.settext(cornish_corpus.MostFreqWords1Text(kk_text_dict[textchoice.state()], textchoice.state(), topN, minL))
    if modechoice.state() == 'Hirder Geryow\n(tresenn menowghder kumulativ)':
        cornish_corpus.nLettersFDist(kk_texts,names)
        pylab.show()
    if modechoice.state() == 'Menowghder Ger\n(tresenn barr)':
        comparelist = getcomparelist()
        if len(comparelist) == 0:
            comparelist = defaultsamples
        outbox.text.config(bg = 'light yellow', fg = 'dark red',
                               font=('Monospace', 12, 'normal'))
        outbox.settext(str(comparelist)+'\n\n'+cornish_corpus.compareSamples(kk_texts, names, comparelist))
        pylab.show()     
                
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Corpus Kernewek')
    mhead = tk.Label(root, text = "Tekst")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)
    kk_texts, names = cornish_corpus.corpusKK()
    kk_text_dict = {k:v for (k,v) in zip(names, kk_texts)}
    # choose text
    textchoice = Radiobar(root, names, side=tk.TOP, anchor=tk.NW,default='Bewnans Meryasek', justify=tk.LEFT)
    textchoice.pack(side=tk.LEFT, fill=tk.Y)
    textchoice.config(relief=tk.RIDGE, bd=2)
    modechoice = Radiobar(root, ['Derivas Ollgemmyn', 'Rol Menoghderow Ger',
                                 'Hirder Geryow\n(tresenn menowghder kumulativ)',
                                 'Menowghder Ger\n(tresenn barr)'],
                          side=tk.TOP, anchor=tk.NW, justify = tk.LEFT, default = 'Derivas Ollgemmyn')
    msg = tk.Label(modechoice, text="Keworrowgh isella niver a lytherennow rag rolyow menoghder ger a-woeles:",
                   anchor=tk.W, justify=tk.LEFT, pady=10)
    msg.config(font=('Arial', 12))
    msg.pack()
    ent = Entrybar(modechoice,
                   anchor=tk.NW)
    ent.pack(fill=tk.X)
    msg2 = tk.Label(modechoice, text="Keworrowgh niver a eryow dhe dherivas an menowghder a-woeles:",
                    anchor=tk.W, justify=tk.LEFT, pady=10)
    msg2.config(font=('Arial', 12))
    msg2.pack()
    ent2 = Entrybar(modechoice,
                    anchor=tk.NW)
    ent2.pack(fill=tk.X)
    msg3 = tk.Label(modechoice, text="Keworrowgh ger dhe geheveli menowghderow dres an tekstow:",
                    anchor=tk.W, justify=tk.LEFT, pady=10)
    msg3.config(font=('Arial', 12))
    msg3.pack()
    ent3 = Entrybar(modechoice,
                    anchor=tk.NW)
    ent3.pack(fill=tk.X)        
    keworra = tk.Button(modechoice, text='Keworra dhe rol', font=('Arial', 14),
              command = addtocomparelist)
    klerhe = tk.Button(modechoice, text='Klerhe rol', font=('Arial', 14),
              command = clearcomparelist)
    keworra.pack(anchor=tk.NW)
    klerhe.pack(anchor=tk.NW)        
    modechoice.pack(side=tk.LEFT, fill=tk.Y)
    modechoice.config(relief=tk.RIDGE, bd=2)
        
    outbox = ScrolledText(root)
    outbox.text.config(bg = 'light yellow', fg = 'dark red', width=60, height=30,
                    font=('Monospace', 14, 'bold'))
    outbox.pack()
    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Dalleth', font=('Arial',14),
              command = printoutput).pack(side=tk.RIGHT)
    root.mainloop()


