# coding=utf-8
from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Radiobar, Entrybar, CheckButtonBar
import mutatya
import textwrap

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Mutatya')
    mhead = tk.Label(root, text = "Studh Treylyans")
    mhead.config(font=('Helvetica', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)
    # various mutation states
    mstate = Radiobar(root, ['1 (heb treylyans)', '2 (medhel)', '3 (hwythys)', '4 (kales)', '5 (kemmyskys)', '6 (kemmyskys wosa \'th)', '7 (kildreylyans)'], side=tk.TOP, anchor=tk.NW,default='1 (heb treylyans)')
    mstate.pack(side=tk.LEFT, fill=tk.Y)
    mstate.config(relief=tk.RIDGE, bd=2)

    tradgraph = CheckButtonBar(mstate, ['Lytherennans\nhengovek (SWF/T)'], side=tk.TOP, justify = tk.LEFT, anchor=tk.NW)
    tradgraph.pack(side=tk.LEFT, fill=tk.Y)

    def allstates(): print(mstate.state(), tradgraph.state(), intmstate(), ent.fetch())
    def intmstate():
        """ extract integer mutation state to call mutatya.mutate() with
        if nothing has been clicked, assume no mutation (state 1) """
        try:
            return int(mstate.state()[0])
        except:
            return 1
        
    def copyclipbd():
        root.clipboard_clear()
        root.clipboard_append(msg2.cget("text"))

    def printmform():
        """ show the mutated form of whatever has been input in the
        entry bar """
        if intmstate() < 7:
            #print(mutatya.mutate(ent.fetch(),intmstate()))
            mutatys =  mutatya.mutate(ent.fetch(),intmstate(), tradgraph.state()[0])
            mutatys = textwrap.fill(mutatys, 60)
            print(mutatys)
            msg2.config(text = mutatys,
                        font=('Courier', 16, 'bold'))
        else:
            dimutatys = mutatya.format_rev_mutate(mutatya.rev_mutate(ent.fetch(), False, tradgraph.state()[0]), True)
            #print(mutatya.format_rev_mutate(mutatya.rev_mutate(ent.fetch(), False, tradgraph.state()[0]), True))
            mutatys = textwrap.fill(dimutatys, 60)
            print(dimutatys)
            msg2.config(text = dimutatys,
            font=('Courier', 14, 'bold'))
    
    msg = tk.Label(root, text="Gorrewgh ger kernewek a-woles mar pleg",
                   padx=5)
    msg.config(font=('Helvetica', 16, 'bold'))
    msg.pack()
    
    # text entry bar
    ent = Entrybar(root)
    ent.pack(padx=5, pady=5)

    msg2 = tk.Label(root)
    msg2.config(bg = 'light yellow', fg = 'dark red', font=('Courier', 16, 'bold'))
    msg2.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Mutatya', font=('Helvetica',14),
           command = printmform).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Kopi dhe\'n Klyppbordh', font=('Helvetica', 14),
              command = copyclipbd).pack(side=tk.LEFT)
    root.mainloop()


