# coding=utf-8
from __future__ import print_function
import sys, os
sys.path.append('..')
if sys.version_info[0] < 3:
    import Tkinter as tk
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import tkinter as tk
from taklowGUI import Kwitya, ScrolledText
import gorhemmyn_kw as gor
import kernewek_to_welshorthography as kw2cy
#import niverow_to_geryow
import textwrap


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Kewsel Kernewek gans espeak')

    def allstates(): print(ent.gettext())

    def kewsel(kwtext, replacefigs=False):
        """ speaks cornish text by Cymricising the spelling
        and feeding to espeak at the command line """
        # first replace numerals by words in Cornish
        # not enabled pending resolving import niverow issue
        if replacefigs:
            kwtext = niverow_to_geryow.niverow2kwtext(kwtext)
            
        tekst_cy = kw2cy.towelsh([kwtext])
        print(tekst_cy)
        espeakcmd = 'espeak -vcy \"{t}\"'.format(t=tekst_cy)
        os.system(espeakcmd)
        
    def printentbar():
        """ show whatever has been input in the
        entry bar, and speak it """
        print(ent.gettext())
        outtext = textwrap.fill(ent.gettext(), 60)
        msg2.config(text = outtext)
        root.update_idletasks()
        kewsel(ent.gettext())
        
    def gorhemmyn():
        """ choose a greeting appropriate to the time of day
        using time on the system clock, and speak it """
        g = gor.Gorhemmyn()
        msg2.config(text = g.gorhemmyn)
        root.update_idletasks()
        # could use method inside gorhemmyn_kw instead
        # g.kewsel()
        kewsel(g.gorhemmyn)

    def clearboxes():
        """ clear input and output boxes """
        msg2.config(text = '')
        ent.clear()
        
    
    msg = tk.Label(root, text="Gorrewgh geryow kernewek a-woles mar pleg")
    msg.config(font=('Helvetica', 16, 'bold'))
    msg.pack()
    
    # text entry bar
    ent = ScrolledText(root)
    ent.text.config(width=40,height=11)
    ent.pack(expand=tk.YES, fill=tk.BOTH)

    # output display
    msg2 = tk.Label(root)
    msg2.config(bg = 'light yellow', fg = 'dark red', font=('Helvetica', 18, 'bold'))
    msg2.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Kewsel', font=('Helvetica',14),           
           command = printentbar).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Gorhemmyn', font=('Helvetica',14),
           command = gorhemmyn).pack(side=tk.LEFT)
    
    tk.Button(root, text = 'Klerhe', font=('Helvetica',14),           
           command = clearboxes).pack(side=tk.LEFT)
    
    root.mainloop()


