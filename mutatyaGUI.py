from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *
from taklowGUI import Kwitya, Radiobar, Entrybar, CheckButtonBar
import mutatya

if __name__ == '__main__':
    root = Tk()
    root.title('Mutatya')
    mhead = Label(root, text = "Studh Treylyans")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=TOP, anchor=NW)
    # various mutation states
    mstate = Radiobar(root, ['1 (heb treylyans)', '2 (medhel)', '3 (kales)', '4 (hwythys)', '5 (kemmyskys)', '6 (kemmyskys wosa \'th)', '7 (kildreylyans)'], side=TOP, anchor=NW,default='1 (heb treylyans)')
    mstate.pack(side=LEFT, fill=Y)
    mstate.config(relief=RIDGE, bd=2)

    tradgraph = CheckButtonBar(root, ['Lytherennans hengovek'], side=TOP, anchor=NW)
    tradgraph.pack(side=LEFT, fill=Y)
    tradgraph.config(relief=RIDGE, bd=2)

    def allstates(): print(mstate.state(), tradgraph.state(), intmstate(), ent.fetch())
    def intmstate():
        """ extract integer mutation state to call mutatya.mutate() with
        if nothing has been clicked, assume no mutation (state 1) """
        try:
            return int(mstate.state()[0])
        except:
            return 1
    def printmform():
        """ show the mutated form of whatever has been input in the
        entry bar """
        if intmstate() < 7:
            print(mutatya.mutate(ent.fetch(),intmstate()))
            msg2.config(text = mutatya.mutate(ent.fetch(),intmstate(), tradgraph.state()[0]),
                        font=('Monospace', 18, 'bold'))
        else:
            print(mutatya.format_rev_mutate(mutatya.rev_mutate(ent.fetch(), False, tradgraph.state()[0]), True))
            msg2.config(text = mutatya.format_rev_mutate(mutatya.rev_mutate(ent.fetch(), False, tradgraph.state()[0]), True),
            font=('Monospace', 14, 'bold'))
    
    msg = Label(root, text="Gorrewgh ger kernewek a-woles mar pleg")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar
    ent = Entrybar(root)
    ent.pack()

    msg2 = Label(root)
    msg2.config(bg = 'light yellow', fg = 'dark red', font=('Monospace', 18, 'bold'))
    msg2.pack(expand=YES,fill=BOTH, anchor=CENTER)

    # buttons
    Kwitya(root).pack(side=RIGHT)
    Button(root, text = 'Mutatya', font=('Arial',14),
           command = printmform).pack(side=RIGHT)
    root.mainloop()


