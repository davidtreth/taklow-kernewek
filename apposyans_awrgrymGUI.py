# coding=utf-8
from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Entrybar, Radiobar
import niverow
import apposyans_awrgrym as aw
import time, random
import numpy as np

class AppAwrgrym(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.master.title("Apposyans Awrgrym")
        self.pack()
        self.niverewn = 0
        self.nivergwrys = 0
        self.poyntys = 0
        self.Ngovynn = 20
        self.gorthypkewar = 0
        self.make_widgets()
        self.dalleth()

    def make_widgets(self):
        self.mhead = tk.Label(self, text = "Dewisyow")
        self.mhead.config(font=('Helvetica', 16, 'bold'))
        self.mhead.pack(side=tk.TOP, anchor=tk.NW)    
        self.options = Radiobar(self, ['Keworra po marnas', 'Keworra', 'Marnas'],
                                side=tk.TOP,
                                justify=tk.LEFT, anchor=tk.NW,
                                default='Keworra po marnas')
        self.options.pack(side=tk.LEFT, fill=tk.Y)
        self.options.config(relief=tk.RIDGE, bd=2)
        
        self.msg = tk.Label(self, text="Govynn:")
        self.msg.config(font=('Helvetica', 16, 'bold'))
        self.msg.pack(anchor=tk.W)
    
        # question
        self.govynn = tk.Label(self)
        self.govynn.pack(anchor=tk.W)
        self.govynn.config(fg = 'black', bg='light yellow',font=('Helvetica', 18, 'bold'), text='')
        self.govynn.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)
    
        self.msg2 = tk.Label(self, text="Gorrewgh gorthyp yn bysies a-woles mar pleg")
        self.msg2.config(font=('Helvetica', 16, 'bold'))
        self.msg2.pack(anchor=tk.W)
        # text entry bar for answer
        self.gorthyp = Entrybar(self)
        self.gorthyp.pack(anchor=tk.W)
        self.gorthyp.focus()
        self.master.bind('<Return>', lambda event: self.rigorthyp())

        # output
        self.msg3 = tk.Label(self)
        self.msg3.config(fg = 'dark red', bg='light yellow',font=('Helvetica', 18, 'bold'), text='')
        self.msg3.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

        # buttons
        Kwitya(self).pack(side=tk.RIGHT)
        tk.Button(self, text = 'Profya Gorthyp', font=('Helvetica',14),
                  command = self.rigorthyp).pack(side=tk.RIGHT)
        tk.Button(self, text = 'Dalleth', font=('Helvetica', 14),
                  command = self.dalleth).pack(side=tk.LEFT)
        

        
    def allstates(self): print(self.options.state(), self.gorthyp.fetch())
    
    def diskwedhgovynn(self, tekst):
        self.govynn.config(fg = 'black', bg = 'light yellow',
                      font=('Helvetica', 18, 'bold'), text=tekst)
    
    def chekkGorthyp(self, g, kewar):
        try:
            g = int(g)
            if g == kewar:
                return True, "Ewn os"
            else:
                return False, "Kamm os"
        except:
            return False, "Nag yw {a} niver".format(a=g)

    def keworra(self):
        n = 20
        x1 = random.choice(np.arange(n) + 1)
        x2 = random.choice(np.arange(n) + 1)
        keworrans = x1 + x2
        gov = "Pyth yw {a} ha {b}?\n".format(a=niverow.numberkw(x1),
                                             b=niverow.numberkw(x2))
        gov = gov.replace("ha u","hag u")
        gov = gov.replace("ha e","hag e")
        gov = gov.replace("ha o","hag o")        
        self.diskwedhgovynn(gov)
        return keworrans


    
    def marnas(self):
        n = 20
        x1 = random.choice(np.arange(n) + 1)
        x2 = random.choice(np.arange(n) + 1)
        marnasyans = x1 - x2
        self.diskwedhgovynn("Pyth yw {a} marnas {b}?\n".format(a=niverow.numberkw(x1),
                                                          b=niverow.numberkw(x2)))
        return marnasyans
    
    def govynn1(self, mode="keworramarnas"):
        self.starttime = time.time()
        if mode=="keworramarnas":
            g = random.choice([self.keworra, self.marnas])
        elif mode == "marnas":
            g = self.marnas
        else:
            g = self.keworra
        return g()
        
    def rigorthyp(self):
        """ submit answer """
        self.allstates()
        if self.nivergwrys >= self.Ngovynn:
            return None
        try:
            niver = float(self.gorthyp.fetch())
            print(niver)
            self.nivergwrys += 1
        except ValueError:            
            output = "Res yw gorra niver y'n kyst\n avel bysies, rag ensample '42'"
            print(output)
            self.msg3.config(fg = 'orange', bg='black',font=('Helvetica', 18, 'bold'), text=output)
            niver = -99
        self.gorthyp.clear()
        if niver or niver==0:
            kewarder = self.chekkGorthyp(niver, self.gorthypkewar)        
            
            if kewarder[0]:
                t = time.time() - self.starttime
                self.poyntys += max([10-t, 0]) + 1
                self.niverewn += 1
                tekst = "{k}\n{t:.1f}s, {e}/{g}, sommenn poyntys={p:.1f}".format(k=kewarder[1],
                                                                                   t=t,
                                                                                   p=self.poyntys,
                                                                                   e=self.niverewn,
                                                                                   g=self.nivergwrys)

                fcolour='dark green'
            else:
                tekst = "{k}\n{e}/{g}, sommenn poyntys={p:.1f}".format(k=kewarder[1],
                                                                         p=self.poyntys,
                                                                         e=self.niverewn,
                                                                         g=self.nivergwrys)                
                fcolour='dark red'
            if niver != -99:
                print(tekst)
                self.msg3.config(fg = fcolour, bg = 'light yellow', font=('Helvetica', 18, 'bold'), text=tekst)
                if self.nivergwrys < self.Ngovynn:
                    # ask next question
                    self.gorthypkewar = self.govynn1()
                else:
                    self.gorfenna()

    def gorfenna(self):
        endmsg = "Ty a wrug {e} kewar a {N}. Dha skor yw {n:.1f} boyntys".format(e = self.niverewn,
                                                                                 N = self.Ngovynn,
                                                                                 n = self.poyntys)
        self.msg3.config(fg = 'blue', bg = 'light yellow', font=('Helvetica', 18, 'bold'), text=endmsg)
        
    def dalleth(self):
        self.gorthyp.clear()
        self.msg3.config(fg = 'dark red', bg='light yellow',font=('Helvetica', 18, 'bold'), text='')
        self.niverewn = 0
        self.nivergwrys = 0
        self.poyntys = 0
        self.Ngovynn = 20        
        self.gorthypkewar = self.govynn1()
        
        
if __name__ == '__main__':
    kwiz = AppAwrgrym()
    kwiz.mainloop()    



