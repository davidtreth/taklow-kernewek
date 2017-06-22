#!/usr/bin/python3
# -*- coding: utf-8 -*-
# David Trethewey 06-05-2016 
# code is Open Source (GPL)
# Fenten Igor yw an kodenn ma (GPL)
from __future__ import print_function
import sys, argparse
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Gadael, Radiobar, ScrolledText, CheckButtonBar, wraplines
import textwrap

def allstates():
    print(options.state(), options2.state(),
          rhybudd.state(), ent.gettext())
    
def printsylranna():
    """ show the output in Welsh, according to the options
    in the radiobar is selected """
    allstates()
    inputtext = ent.gettext()
    print("Input: {i}".format(i=inputtext))
    output = ''
    msg3.text.config(fg = 'dark red', bg = 'light yellow',
                     font=('Helvetica', 16+fontsizeadj, 'bold'), state=tk.NORMAL)
    if inputtext:
        # standardise quote characters etc.
        inputtext = syl.preprocess2ASCII(inputtext)
        if options2.state() == 'Rhannu ymlaen':
            fwd = True
        else: fwd = False
        regexps=syl.cyRegExp
        if options.state() == 'Mode Hir':
            output = syl.detailSylsText(inputtext, fwd, regexps=regexps,
                                        FSSmode=False, CYmode=True, gwarnya=rhybudd.state()[0])
            # long mode doesn't normally need word wrapping, but just in case
            # someone enters Llan50goch in full
            output=wraplines(output)
            
            msg3.text.config(font=('Helvetica', 14+fontsizeadj, 'normal'),
                             width=66, height=12+heightadjust)
            
        elif options.state() == 'Mode Llinell':
            msg3.text.config(font=('Helvetica', 16+fontsizeadj, 'bold'),
                             width=60, height=11+heightadjust)
            lines = inputtext.split('\n')                
            for l in lines:                    
                output += syl.countSylsLine(l, fwd, regexps=regexps,
                                            FSSmode=False, CYmode=True, gwarnya=rhybudd.state()[0])+'\n\n'
            output = wraplines(output)

        else:
            msg3.text.config(font=('Helvetica', 16+fontsizeadj, 'bold'),
                             width=60, height=11+heightadjust)
            # use short mode by default if nothing is selected
            output = syl.detailSylsText(inputtext, fwd,
                                        short=True, regexps=regexps,
                                        FSSmode=False, CYmode=True,  gwarnya=rhybudd.state()[0])
            output = textwrap.fill(output, 60)
        print(output)
    msg3.settext(output)
    msg3.text.config(state=tk.DISABLED)

def clearboxes():
    ent.clear()
    msg3.text.config(fg = 'dark red', bg='light yellow',
                     font=('Helvetica', 16+fontsizeadj, 'bold'),state=tk.NORMAL)
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
        fontsizeadj = -1

    root = tk.Tk()
    root.title('Syllabenn Rhannu Cymraeg')
    mhead = tk.Label(root, text = "Dewisiadau")
    mhead.config(font=('Helvetica', 16+fontsizeadj, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = Radiobar(root, ['Mode Hir', 'Mode Byr', 'Mode Llinell'],
                       side=tk.TOP, anchor=tk.NW,default='Mode Byr')
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2, padx=10, pady=10)

    options2 = Radiobar(options, ['Rhannu ymlaen', 'Rhannu yn ôl'],
                        side=tk.TOP, anchor=tk.NW, default='Rhannu yn ôl')
    options2.pack(side=tk.LEFT, fill=tk.Y)
    options2.config(pady=10)

    
    rhybudd = CheckButtonBar(options2, ['Rhybuddio os nac ydy\'r gair wedi defnyddio yn cyfan'], side=tk.TOP, anchor=tk.NW)
    rhybudd.pack(side=tk.LEFT, fill=tk.Y)        
    
    msg = tk.Label(root, text="Rhowch testun Cymraeg ar lawr os gwelwch yn dda:")
    msg.config(font=('Helvetica', 16+fontsizeadj, 'bold'))
    msg.pack()
    
    # text entry bar for input
    ent = ScrolledText(root)
    ent.text.config(width=60,height=11+heightadjust)
    ent.pack(expand=0)
    
    # output
    msg3 = ScrolledText(root)
    msg3.text.config(fg = 'dark red', bg='light yellow', width=60, height=11+heightadjust,
                     font=('Helvetica', 16+fontsizeadj, 'bold'), state=tk.DISABLED)
    msg3.pack()
    # buttons
    Gadael(root).pack(side=tk.RIGHT)
    disk = tk.Button(root, text = 'Dangos Sillafau', font=('Helvetica',14+fontsizeadj),
                     command = printsylranna)
    tk.Button(root, text = 'Clirio', font=('Helvetica', 14+fontsizeadj),
           command = clearboxes).pack(side=tk.LEFT)
    tk.Button(root, text = 'Copïo i\'r Clipbwrdd', font=('Helvetica', 14+fontsizeadj),
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


