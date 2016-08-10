from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Radiobar, Entrybar, CheckButtonBar
import mutatya

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Treiglo')
    mhead = tk.Label(root, text = "Ystad Treiglo")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)
    # various mutation states
    mstate = Radiobar(root, ['1 (heb treiglo)', '2 (treiglad meddal)', '3 (treiglad llais)', '7 (treiglad trwynol)', '8 (cymysgu wedi "ni")', '9 (gwrthdroi treiglad)'], side=tk.TOP, anchor=tk.NW,default='1 (heb treiglo)')
    mstate.pack(side=tk.LEFT, fill=tk.Y)
    mstate.config(relief=tk.RIDGE, bd=2)

    def allstates(): print(mstate.state(), tradgraph.state(), intmstate(), ent.fetch())
    def intmstate():
        """ extract integer mutation state to call mutatya.mutate_cy() with
        if nothing has been clicked, assume no mutation (state 1) """
        try:
            return int(mstate.state()[0])
        except:
            return 1
    def printmform():
        """ show the mutated form of whatever has been input in the
        entry bar """
        if intmstate() < 9:
            print(mutatya.mutate_cy(ent.fetch(),intmstate()))
            msg2.config(text = mutatya.mutate_cy(ent.fetch(),intmstate()),
                        font=('Monospace', 18, 'bold'))
        else:
            print(mutatya.format_rev_mutate(mutatya.rev_mutate_cy(ent.fetch(), False), cy=True))
            msg2.config(text = mutatya.format_rev_mutate(mutatya.rev_mutate_cy(ent.fetch(), False), cy=True),
            font=('Monospace', 14, 'bold'))
    
    msg = tk.Label(root, text="Rhowch gair Cymraeg islaw os gwelwch yn dda")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar
    ent = Entrybar(root)
    ent.pack()

    msg2 = tk.Label(root)
    msg2.config(bg = 'light yellow', fg = 'dark red', font=('Monospace', 18, 'bold'))
    msg2.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Treiglo', font=('Arial',14),
           command = printmform).pack(side=tk.RIGHT)
    root.mainloop()


