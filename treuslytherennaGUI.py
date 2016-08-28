from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Radiobar, ScrolledText
from sylrannakwGUI import checkNLTK
def allstates(): print(options.state(), options2.state(), ent.gettext())

def printtreus():
    """ show the output in Cornish, according to the options
     in the radiobar is selected """
    allstates()
    inputtext = ent.gettext()
    print("Input: {i}".format(i=inputtext))
    output = ''
    msg3.text.config(fg = 'dark red', bg = 'light yellow',
                     font=('Arial', 16, 'bold'), state=tk.NORMAL)
    if inputtext:
        if options2.state() == 'Rannans war-rag':
            fwd = True
        else: fwd = False
            
        if options.state() == 'Mode Hir':
            output = tr.text_KK2FSS(inputtext,fwd,longform=True)
            msg3.text.config(font=('Arial', 14, 'normal'),
                             width=66, height=12)
        elif options.state() == 'Mode Linenn' or options.state() == 'Mode Berr':
            msg3.text.config(font=('Arial', 16, 'bold'),
                             width=60, height=11)
            lines = inputtext.split('\n')
            for l in lines:
                if options.state() == 'Mode Linenn':
                    output += tr.line_KK2FSS(l,fwd) + '\n\n'
                else:
                    output += tr.line_KK2FSS(l,fwd,longform=False) + '\n'
        print(output)

    msg3.settext(output)
    msg3.text.config(state=tk.DISABLED)
    
def clearboxes():
    ent.clear()
    msg3.text.config(fg = 'dark red', bg='light yellow',
                     font=('Arial', 16, 'bold'), state=tk.NORMAL)
    msg3.clear()
    msg3.text.config(state=tk.DISABLED)
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Treuslytherenna Kernewek Kemmyn --> Furv Skrifys Savonek')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = Radiobar(root, ['Mode Hir', 'Mode Berr', 'Mode Linenn'], side=tk.TOP, anchor=tk.NW,default='Mode Linenn')
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2, padx=10, pady=10)

    options2 = Radiobar(options, ['Rannans war-rag', 'Rannans war-dhelergh'], side=tk.TOP, anchor=tk.NW, default='Rannans war-rag')
    options2.pack(side=tk.LEFT, fill=tk.Y)
    options2.config(pady=10)
    

        
        
    msg = tk.Label(root, text="Gorrewgh tekst Kernewek Kemmyn a-woeles mar pleg:")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar for input
    ent = ScrolledText(root)
    ent.text.config(width=60, height = 11)
    ent.pack(expand=0)
    
    # output
    msg3 = ScrolledText(root)
    msg3.text.config(fg = 'dark red', bg='light yellow', width = 60, height = 11,
                     font=('Arial', 16, 'bold'), state=tk.DISABLED)
    msg3.pack()
        
    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    treus = tk.Button(root, text = 'Treuslytherenna KK --> FSS', font=('Arial',14),
           command = printtreus)
    tk.Button(root, text = 'Klerhe', font=('Arial', 14),
           command = clearboxes).pack(side=tk.LEFT)
    # check NLTK is available
    c = checkNLTK()
    print("NLTK available = {c}".format(c=c))           
    if c[0] == 1:
        import treuslytherenna as tr
    else:
        treus['state'] = tk.DISABLED
        msg3.text.config(state=tk.NORMAL)
        msg3.settext(c[1])
        
    treus.pack(side=tk.RIGHT)       
    root.mainloop()


