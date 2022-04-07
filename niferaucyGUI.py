# coding=utf-8
from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Gadael, Entrybar, CheckButtonBar
import niverow
import textwrap

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Niferau')
    mhead = tk.Label(root, text = "Dewisiadau")
    mhead.config(font=('Open Sans', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = CheckButtonBar(root, ['Defniddio Enw','Enw Benywol'],
                             side=tk.TOP,
                             justify=tk.LEFT, anchor=tk.NW)
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2, padx=5)

    scl = tk.Scale(root, label="Uchaf Tradd", from_=200, to=10,
                   tickinterval=190, resolution=5)
    scl.pack(side=tk.LEFT, anchor=tk.SW, fill=tk.Y, padx=5, pady=5)
    scl.set(20)
    
    def allstates(): print(options.state(), ent.fetch(), ent2.fetch(), scl.get())
    nifercy = niverow.NiferCymraeg()

    def printniver():
        """ show the number in Welsh, with the noun if the checkbox
         is selected """
        allstates()
        nifercy.setMaxTrad(scl.get())
        try:
            niver = float(ent.fetch())
            print(niver)
        except ValueError:            
            output = "Mae rhaid rhowch nifer yn y bocs\n mewn ffigurau, fel esiampl '42'"
            print(output)
            output = textwrap.fill(output, 40)
            msg3.config(fg = 'orange', bg='black',font=('Open Sans', 18, 'bold'), text=output)
            return None

        if niver or niver==0:
            if options.state()[0] == 1 and ent2.fetch() != "":
                if ent3.fetch() != "":
                    npl = ent3.fetch()
                else: npl = "au"
                if niver == int(abs(niver)):
                    output = nifercy.numbercy_noun(niver,ent2.fetch(),options.state()[1],npl)
                else:
                    output = nifercy.numbercy_float_noun(niver,ent2.fetch(),options.state()[1],npl)
            else:
                output = nifercy.numbercy_float(niver)
            output = textwrap.fill(output, 40)
            print(output)
            
            msg3.config(fg = 'dark red', bg = 'light yellow', font=('Open Sans', 18, 'bold'), text=output)
        #msg3.config(text = output)

    def clearboxes():
        ent.clear()
        ent2.clear()
        ent3.clear()
        msg3.config(fg = 'dark red', bg='light yellow',font=('Open Sans', 18, 'bold'), text='')
        
    def copyclipbd():
        root.clipboard_clear()
        root.clipboard_append(msg3.cget("text"))
        
    msg = tk.Label(root, text="Rhowch nifer islaw os gwelwch yn dda")
    msg.config(font=('Open Sans', 16, 'bold'))
    msg.pack(anchor=tk.W, padx=5, pady=2)
    
    # text entry bar for number
    ent = Entrybar(root)
    ent.pack(anchor=tk.W)
    
    msg2 = tk.Label(root, text="Rhowch enw Cymraeg islaw os gwelwch yn dda")
    msg2.config(font=('Open Sans', 16, 'bold'))
    msg2.pack(anchor=tk.W, padx=5, pady=2)
    # text entry bar for noun
    ent2 = Entrybar(root)
    ent2.pack(anchor=tk.W)
    # irregular plural?
    msg4 = tk.Label(root, text="Rhowch enw Cymraeg lluosog islaw os nac ydy -au")
    msg4.config(font=('Open Sans', 16, 'bold'))
    msg4.pack(anchor=tk.W, padx=5, pady=2)
    # text entry bar for plural noun
    ent3 = Entrybar(root)
    ent3.pack(anchor=tk.W)
    # output
    msg3 = tk.Label(root)
    msg3.config(fg = 'dark red', bg='light yellow',font=('Open Sans', 18, 'bold'), text='')
    msg3.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

    # buttons
    Gadael(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Dangos Nifer', font=('Open Sans',14),
           command = printniver).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Clirio', font=('Open Sans', 14),
           command = clearboxes).pack(side=tk.LEFT)
    tk.Button(root, text = 'Copïo i\'r Clipbwrdd', font=('Open Sans', 14),
              command = copyclipbd).pack(side=tk.LEFT)
    root.mainloop()


