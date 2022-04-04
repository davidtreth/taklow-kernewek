# coding=utf-8
from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Gadael, Radiobar, Entrybar, CheckButtonBar
import mutatya
import textwrap

def allstates(): print(mstate.state(), ent.fetch())
def intmstate():
    """ extract integer mutation state to call mutatya.mutate_cy() with
    if nothing has been clicked, assume no mutation (state 1) 
    Not actually needed in this script since vals is set in Radiobar """
    try:
        return int(mstate.state()[0])
    except:
        return 1
        
def printmform():
    """ show the mutated form of whatever has been input in the
    entry bar """
    if mstate.state() < 9:
        weditreiglo = mutatya.mutate_cy(ent.fetch(),mstate.state())
        weditreiglo = textwrap.fill(weditreiglo, 60)
        #print(mutatya.mutate_cy(ent.fetch(),mstate.state()))
        print(weditreiglo)
        msg2.config(text = weditreiglo,
                    font=('Courier', 18, 'bold'))
    else:
        hebtreiglo = mutatya.format_rev_mutate(mutatya.rev_mutate_cy(ent.fetch(), False), cy=True)
        hebtreiglo = textwrap.fill(hebtreiglo, 60)
        print(hebtreiglo)
        
        msg2.config(text = hebtreiglo, font=('Courier', 14, 'bold'))

def copyclipbd():
    """ copy the contents of the output window to the clipboard """
    root.clipboard_clear()
    root.clipboard_append(msg2.cget("text"))

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Treiglo')
    mhead = tk.Label(root, text = "Ystad Treiglo")
    mhead.config(font=('Helvetica', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)
    # various mutation states
    mstate = Radiobar(root, ['Heb treiglo', 'Treiglad meddal', 'Treiglad llais', 'Treiglad trwynol', 'Cymysgu wedi "ni"', 'Gwrthdroi treiglad'],
                      [1,2,3,7,8,9], side=tk.TOP, anchor=tk.NW,default=1)
    mstate.pack(side=tk.LEFT, fill=tk.Y)
    mstate.config(relief=tk.RIDGE, bd=2)
    
    msg = tk.Label(root, text="Rhowch gair Cymraeg islaw os gwelwch yn dda")
    msg.config(font=('Helvetica', 16, 'bold'))
    msg.pack()
    
    # text entry bar
    ent = Entrybar(root)
    ent.pack()

    msg2 = tk.Label(root)
    msg2.config(bg = 'light yellow', fg = 'dark red', font=('Courier', 18, 'bold'))
    msg2.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

    # buttons
    Gadael(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Treiglo', font=('Helvetica',14),
           command = printmform).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Copïo i\'r Clipfwrdd', font=('Helvetica', 14),
              command = copyclipbd).pack(side=tk.LEFT)
    root.mainloop()


