# coding=utf-8
from __future__ import print_function
import sys, argparse
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Radiobar, ScrolledText, CheckButtonBar, wraplines
import textwrap

def allstates():
    print(options.state(), options2.state(),
          kkfss.state(), gwarnya.state(), ent.gettext())


def printsylranna():
    """ show the output in Cornish, according to the options
    in the radiobar is selected """
    allstates()
    inputtext = ent.gettext()
    print("Input: {i}".format(i=inputtext))
    output = ''
    msg3.text.config(fg = 'dark red', bg = 'light yellow',
                     font=('Open Sans', 16, 'bold'), state=tk.NORMAL)
    if inputtext:
        # standardise quote characters etc.
        inputtext = syl.preprocess2ASCII(inputtext)
        if options2.state() == 'Rannans war-rag':
            fwd = True
        else: fwd = False
        
        if kkfss.state() == 'Kernewek FSS':
            regexps=syl.kwFSSRegExp
            FSS = True
        else:
            regexps=syl.kwKemmynRegExp
            FSS = False
                
        if options.state() == 'Mode Hir':
            output = syl.detailSylsText(inputtext, fwd, regexps=regexps,
                                        FSSmode=FSS, gwarnya=gwarnya.state()[0])
            # only needed in cases of very long words
            output = wraplines(output)
            msg3.text.config(font=('Open Sans', 14, 'normal'),
                             width=66, height=12+heightadjust)
            
        elif options.state() == 'Mode Linenn':
            msg3.text.config(font=('Open Sans', 16, 'bold'),
                             width=60, height=11+heightadjust)
            lines = inputtext.split('\n')                
            for l in lines:                    
                output += syl.countSylsLine(l, fwd, regexps=regexps,
                                            FSSmode=FSS, gwarnya=gwarnya.state()[0])+'\n\n'
            output = wraplines(output)
        else:
            msg3.text.config(font=('Open Sans', 16, 'bold'),
                             width=60, height=11+heightadjust)
            # use short mode by default if nothing is selected
            output = syl.detailSylsText(inputtext, fwd,
                                        short=True, regexps=regexps,
                                        FSSmode=FSS, gwarnya=gwarnya.state()[0])
            output = textwrap.fill(output, 60)
        print(output)
    msg3.settext(output)
    msg3.text.config(state=tk.DISABLED)

def clearboxes():
    ent.clear()
    msg3.text.config(fg = 'dark red', bg='light yellow',
                     font=('Open Sans', 16+fontsizeadj, 'bold'),
                     state=tk.NORMAL)
    msg3.clear()
    msg3.text.config(state=tk.DISABLED)
    
def copyclipbd():
    root.clipboard_clear()
    root.clipboard_append(msg3.gettext())
        
def checkNLTK():
    try:
        import nltk
    except ImportError:        
        errtext = "Python Natural Language Processing Toolkit (NLTK) not available.\nDownload from www.nltk.org if not on the system."
        return 0, errtext
    try:
        t = nltk.word_tokenize("test text")
    except AttributeError:
        errtext = "nltk.word_tokenize() not available.\nUse nltk.download() in the Python shell to download Punkt Tokenizer Models."
        return 0, errtext
    return 1, "success"
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--netbook", action="store_true",
                        help="Netbook mode - for smaller screens.")
    args = parser.parse_args()
    if args.netbook:
        heightadjust = -4
        fontsizeadj = -1
    else:
        heightadjust = 0
        fontsizeadj = 0

    root = tk.Tk()
    root.title('Syllabenn Ranna Kernewek')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Open Sans', 16+fontsizeadj, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = Radiobar(root, ['Mode Hir', 'Mode Berr', 'Mode Linenn'],
                       side=tk.TOP, anchor=tk.NW,default='Mode Berr')
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2, padx=10, pady=10)

    options2 = Radiobar(options, ['Rannans war-rag', 'Rannans war-dhelergh'],
                        side=tk.TOP, anchor=tk.NW, default='Rannans war-dhelergh')
    options2.pack(side=tk.LEFT, fill=tk.Y)
    options2.config(pady=10)
    
    kkfss = Radiobar(options2, ['Kernewek Kemmyn', 'Kernewek FSS'],
                        side=tk.TOP, anchor=tk.NW, default='Kernewek Kemmyn')
    kkfss.pack(side=tk.LEFT, fill=tk.Y)
    kkfss.config(pady=10)
    
    gwarnya = CheckButtonBar(kkfss, ['Gwarnya mar nag yw ger argerdhys yn tien'], side=tk.TOP, anchor=tk.NW)
    gwarnya.pack(side=tk.LEFT, fill=tk.Y)        
        
    msg = tk.Label(root, text="Gorrewgh tekst kernewek a-woeles mar pleg:")
    msg.config(font=('Open Sans', 16+fontsizeadj, 'bold'))
    msg.pack()
    
    # text entry bar for input
    ent = ScrolledText(root)
    ent.text.config(width=60,height=11+heightadjust)
    ent.pack(expand=0)
    
    # output
    msg3 = ScrolledText(root)
    msg3.text.config(fg = 'dark red', bg='light yellow', width=60, height=11+heightadjust,
                     font=('Open Sans', 16+fontsizeadj, 'bold'), state=tk.DISABLED)
    msg3.pack()
    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    disk = tk.Button(root, text = 'Diskwedh Syllabennow', font=('Open Sans',14+fontsizeadj),
                     command = printsylranna)
    tk.Button(root, text = 'Klerhe', font=('Open Sans', 14+fontsizeadj),
           command = clearboxes).pack(side=tk.LEFT)
    tk.Button(root, text = 'Kopi dhe\'n Klyppbordh', font=('Open Sans', 14+fontsizeadj),
              command = copyclipbd).pack(side=tk.LEFT)
    # check NLTK is available
    c = checkNLTK()
    print("NLTK available = {c}".format(c=c))
    if c[0] == 1:    
        import syllabenn_ranna_kw as syl
    else:
        msg3.text.config(state=tk.NORMAL)
        msg3.settext(c[1])
        disk['state'] = tk.DISABLED
    disk.pack(side=tk.RIGHT)  

    root.mainloop()


