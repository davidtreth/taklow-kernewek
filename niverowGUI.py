from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Entrybar, CheckButtonBar
import niverow

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Niverow')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = CheckButtonBar(root, ['Usya Hanow','Hanow Benow'], side=tk.TOP, anchor=tk.NW)
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2)
    def allstates(): print(options.state(), ent.fetch(), ent2.fetch())

    def printniver():
        """ show the number in Cornish, with the noun if the checkbox
         is selected """
        allstates()
        try:
            niver = float(ent.fetch())
            print(niver)
        except ValueError:            
            output = "Res yw gorra niver y'n kyst\n avel bysies, rag ensample '42'"
            print(output)
            msg3.config(fg = 'orange', bg='black',font=('Arial', 18, 'bold'))
        if niver or niver==0:
            if options.state()[0] == 1 and ent2.fetch() != "":
                if ent3.fetch() != "":
                    npl = ent3.fetch()
                else: npl = "ow"
                if niver == int(abs(niver)):
                    output = niverow.numberkw_noun(niver,ent2.fetch(),options.state()[1],npl)
                else:
                    output = niverow.numberkw_float_noun(niver,ent2.fetch(),options.state()[1],npl)
            else:
                output = niverow.numberkw_float(niver)
            print(output)
            msg3.config(fg = 'dark red', bg = 'light yellow', font=('Arial', 18, 'bold'))
        msg3.config(text = output)

    def clearboxes():
        ent.clear()
        ent2.clear()
        ent3.clear()
        msg3.config(fg = 'dark red', bg='light yellow',font=('Arial', 18, 'bold'), text='')
        
        
    msg = tk.Label(root, text="Gorrewgh niver a-woles mar pleg")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar for number
    ent = Entrybar(root)
    ent.pack()
    
    msg2 = tk.Label(root, text="Gorrewgh hanow kernewek a-woles mar pleg")
    msg2.config(font=('Arial', 16, 'bold'))
    msg2.pack()
    # text entry bar for noun
    ent2 = Entrybar(root)
    ent2.pack()
    # irregular plural?
    msg4 = tk.Label(root, text="Gorrewgh hanow liesplek a-woles mar nag yw -ow")
    msg4.config(font=('Arial', 16, 'bold'))
    msg4.pack()
    # text entry bar for plural noun
    ent3 = Entrybar(root)
    ent3.pack()
    # output
    msg3 = tk.Label(root)
    msg3.config(fg = 'dark red', bg='light yellow',font=('Arial', 18, 'bold'), text='')
    msg3.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Diskwedh Niver', font=('Arial',14),
           command = printniver).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Klerhe', font=('Arial', 14),
           command = clearboxes).pack(side=tk.LEFT)
    root.mainloop()


