from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import argparse
from taklowGUI import Kwitya, Radiobar, ScrolledText


def checkNLTK():
    try:
        import nltk
    except ImportError:
        errtext = "Python Natural Language Processing Toolkit (NLTK) not available.\nDownload from www.nltk.org if not on the system."
        return 0, errtext
    retvalue = 1
    errtext = ""
    try:
        t = nltk.word_tokenize("test text")
    except AttributeError:
        errtext += "nltk.word_tokenize() not available.\nUse nltk.download() in the Python shell to download Punkt Tokenizer Models.\n"
        retvalue = 0
    try:
        from nltk.corpus import stopwords
    except ImportError:
        errtext += "NLTK stopwords corpus not available.\nUse nltk.download() in the Python shell to download NLTK stopwords corpus."
        retvalue = 0
    if retvalue == 1:
        errtext = "success"
    return retvalue, errtext
    
def allstates(): print(options.state(), ent.gettext())

def printkovtreylyans():
    """ show the output in Cornish, according to the options
     in the radiobar is selected """
    allstates()
    inputtext = ent.gettext()
    print("Input: {i}".format(i=inputtext))
    output = ''
    msg3.text.config(fg = 'dark red', bg = 'light yellow', font=('Courier', 14, 'normal'), state=tk.NORMAL)
    if inputtext:
        if options.state() == 'All trigrams and bigrams':
            output = kovtreylyans.kovtreyl(inputtext, skeulanyeth1, False, allNgrams=True, linelength=outputwidth-2)
            msg3.text.config(font=('Courier', 12, 'normal'))
        else:
            # show only N grams containing non stopwords
            output = kovtreylyans.kovtreyl(inputtext, skeulanyeth1, False, allNgrams=False, linelength=outputwidth-2)
        # print(output)

    msg3.settext(output)
    msg3.text.config(state=tk.DISABLED)
def clearboxes():
    ent.clear()
    msg3.text.config(fg = 'dark red', bg='light yellow',font=('Courier', 12, 'normal'),state=tk.NORMAL)
    msg3.clear()
    msg3.text.config(state=tk.DISABLED)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--netbook", action="store_true",
                        help="Netbook mode - for smaller screens.")
    args = parser.parse_args()
    if args.netbook:
        outputwidth=60
    else:
        outputwidth=80
    root = tk.Tk()
    root.title('Kovtreylyans Kernewek')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Helvetica', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = Radiobar(root, ['All trigrams and bigrams', 'Only N grams with a non-stopword'], side=tk.TOP, anchor=tk.NW,default='Only N grams with a non-stopword')
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2, padx=5, pady=5)


    
    msg = tk.Label(root, text="Write an English sentence in the box below please:")
    msg.config(font=('Helvetica', 16, 'bold'))
    msg.pack(pady=10)
    
    # text entry bar for input
    ent = ScrolledText(root)
    ent.text.config(width=outputwidth,height=7)
    ent.pack(expand=0)
    
    # output
    msg3 = ScrolledText(root)

    msg3.text.config(fg = 'dark red', bg='light yellow', width=outputwidth,
                     height=11,font=('Courier', 14, 'bold'), state=tk.DISABLED)
    msg3.pack()
    
    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    disk = tk.Button(root, text = 'Diskwedh Treylyansow', font=('Helvetica',14),
              command = printkovtreylyans)
    tk.Button(root, text = 'Klerhe', font=('Helvetica', 14),
           command = clearboxes).pack(side=tk.LEFT)

    # check NLTK is available
    c = checkNLTK()
    print("NLTK available = {c}".format(c=c))
    if c[0] == 1:
        import kovtreylyans
        skeulanyeth1 = kovtreylyans.readCorpusSkeulYeth()
    else:
        msg3.text.config(state=tk.NORMAL)
        msg3.settext(c[1])
        disk['state'] = tk.DISABLED
        
    disk.pack(side=tk.RIGHT)    

    root.mainloop()


