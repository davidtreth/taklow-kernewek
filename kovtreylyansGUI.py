from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Radiobar, ScrolledText
import kovtreylyans

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Kovtreylyans Kernewek')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = Radiobar(root, ['All trigrams and bigrams', 'Only N grams with a non-stopword'], side=tk.TOP, anchor=tk.NW,default='Only N grams with a non-stopword')
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2)

    skeulanyeth1 = kovtreylyans.readCorpusSkeulYeth()
    
    def allstates(): print(options.state(), ent.gettext())

    def printkovtreylyans():
        """ show the output in Cornish, according to the options
         in the radiobar is selected """
        allstates()
        inputtext = ent.gettext()
        print("Input: {i}".format(i=inputtext))
        output = ''
        msg3.text.config(fg = 'dark red', bg = 'light yellow', font=('Arial', 14, 'normal'), state=tk.NORMAL)
        if inputtext:
            if options.state() == 'All trigrams and bigrams':
                output = kovtreylyans.kovtreyl(inputtext, skeulanyeth1, False, allNgrams=True)
                msg3.text.config(font=('Arial', 12, 'normal'))
            else:
                # show only N grams containing non stopwords
                output = kovtreylyans.kovtreyl(inputtext, skeulanyeth1, False, allNgrams=False)
            # print(output)

        msg3.settext(output)
        msg3.text.config(state=tk.DISABLED)
    def clearboxes():
        ent.clear()
        msg3.text.config(fg = 'dark red', bg='light yellow',font=('Arial', 12, 'normal'),state=tk.NORMAL)
        msg3.clear()
        msg3.text.config(state=tk.DISABLED)
        
        
    msg = tk.Label(root, text="Write an English sentence in the box below please:")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar for input
    ent = ScrolledText(root)
    ent.text.config(width=40,height=7)
    ent.pack(expand=0)
    
    # output
    msg3 = ScrolledText(root)
    msg3.text.config(fg = 'dark red', bg='light yellow', width=40, height=11,font=('Arial', 14, 'bold'), state=tk.DISABLED)
    msg3.pack()

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Diskwedh Treylyansow', font=('Arial',14),
              command = printkovtreylyans).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Klerhe', font=('Arial', 14),
           command = clearboxes).pack(side=tk.LEFT)
    root.mainloop()


