# coding=utf-8
from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Entrybar, Radiobar
import niverow
# import apposyans_awgrym as aw
# currently functions are implemented internally rather
# than importing text mode ones
import time, random
import math

class AppAwgrym(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.master.title("Apposyans Awgrym")
        self.pack()
        # initialise parameters
        self.niverewn = 0
        self.nivergwrys = 0
        self.poyntys = 0
        self.Ngovynn = 20
        self.gorthypkewar = 0
        self.make_widgets()
        self.dalleth()

    def make_widgets(self):
        """ display the GUI widgets """
        self.mhead = tk.Label(self, text = "Dewisyow")
        self.mhead.config(font=('Helvetica', 16, 'bold'), padx=5, pady=5)
        self.mhead.pack(side=tk.TOP, anchor=tk.NW)
        # choose difficulty level        
        self.options2 = Radiobar(self, ['Es', 'Kres', 'Kales', 'Pur Gales'],
                                vals = [1, 2, 3, 4],
                                side=tk.TOP,
                                justify=tk.LEFT, anchor=tk.NW,
                                default=1)
        self.options2.pack(side=tk.LEFT, fill=tk.Y)
        self.options2.config(relief=tk.RIDGE, bd=2, padx=5)


        # choose whether to have addition, subtraction or either at random
        self.options = Radiobar(self.options2,
                                ['Keworra po marnas', 'Keworra', 'Marnas'],
                                side=tk.TOP,
                                justify=tk.LEFT, anchor=tk.NW,
                                default='Keworra po marnas')
        self.options.pack(side=tk.LEFT, fill=tk.Y)
        #self.options.config(relief=tk.RIDGE, bd=2, padx=0)
        self.options.config(padx=0, pady=10)

        self.kalettermsg = tk.Label(self.options,
                                    text="Gwask 'Dalleth'\nwosa chanjya\n"
                                    "an nivel kaletter\nrag dastalleth\n"
                                    "an apposyans.")
        self.kalettermsg.config(font=('Helvetica', 11), padx=5, pady=5)
        self.kalettermsg.pack(side=tk.TOP, fill=tk.Y)
        
        
        self.msg = tk.Label(self, text="Govynn:")
        self.msg.config(font=('Helvetica', 16, 'bold'), padx=10, pady=10)
        self.msg.pack(anchor=tk.W)
    
        # question
        self.govynn = tk.Label(self)
        self.govynn.pack(anchor=tk.W)
        self.govynn.config(fg = 'black', bg='light yellow',
                           font=('Helvetica', 18, 'bold'), text='',
                           padx=10, pady=10)
        self.govynn.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)
    
        self.msg2 = tk.Label(self, text="Gorrewgh gorthyp yn bysies "
                             "a-woles mar pleg:")
        self.msg2.config(font=('Helvetica', 16, 'bold'),
                         padx=10, pady=10)
        self.msg2.pack(anchor=tk.W)
        # text entry bar for answer
        self.gorthyp = Entrybar(self)
        self.gorthyp.config(padx=10, pady=5)
        self.gorthyp.pack(anchor=tk.W)
        self.gorthyp.focus()
        # bind both Enter and the numeric keypad Enter
        self.master.bind('<Return>', lambda event: self.rigorthyp())
        self.master.bind('<KP_Enter>', lambda event: self.rigorthyp())

        # output
        self.msg3 = tk.Label(self)
        self.msg3.config(fg = 'dark red', bg='light yellow',
                         font=('Helvetica', 18, 'bold'),
                         text='', padx=10, pady=10)
        self.msg3.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER)

        # buttons
        Kwitya(self).pack(side=tk.RIGHT)
        tk.Button(self, text = 'Profya Gorthyp', font=('Helvetica',14),
                  command = self.rigorthyp).pack(side=tk.RIGHT)
        tk.Button(self, text = 'Dalleth', font=('Helvetica', 14),
                  command = self.dalleth).pack(side=tk.LEFT)
        
    def chooseMaxN(self):
        """ based on difficulty choose maximum size of numbers """
        # easy allowed only numbers up to 10
        # and supresses negative answers to subtractions
        # medium up to 20, and hard up to 40
        maxNdict = {1: 10, 2: 20, 3:40, 4:100}
        return maxNdict[self.options2.state()]
        
    def choosemode(self):        
        """ set question mode depending on radio button
        either addition, subtraction or either randomly """
        if self.options.state() == "Keworra po marnas":
            self.qumode = "keworramarnas"
        else:
            self.qumode = self.options.state().lower()
        
    def allstates(self): print(self.options.state(), self.gorthyp.fetch())
    
    def diskwedhgovynn(self, tekst):
        """ display the question """
        self.govynn.config(fg = 'black', bg = 'light yellow',
                      font=('Helvetica', 18, 'bold'), text=tekst)
    
    def chekkGorthyp(self, g, kewar):
        """ check answer against the correct one,
            returning a bool and a message """
        try:
            g = int(g)
            if g == kewar:
                return True, "Ty a ros {}\nEwn os".format(g)
            else:
                return False, "Ty a ros {}\nKamm os".format(g)
        except:
            return False, "Nag yw {} niver".format(g)

    def keworra(self):
        """ ask an addition question """
        n = self.chooseMaxN()
        # random numbers in question
        x1 = math.ceil(random.random() * n)
        x2 = math.ceil(random.random() * n)
        # calculate answer
        keworrans = x1 + x2
        # store sum and answer as text and figures
        self.gorthyptekst = "{a} + {b} = {c}".format(a=niverow.numberkw(x1),
                                              b=niverow.numberkw(x2),
                                              c=niverow.numberkw(keworrans))
        self.gorthypbys = "{a} + {b} = {c}".format(a=x1, b=x2, c=keworrans)
        if self.options2.state() < 4:
            gov = "Pyth yw {a} ha {b}?".format(a=niverow.numberkw(x1),
                                               b=niverow.numberkw(x2))
        else:
            gov = "Pyth yw {a} + {b}?".format(a=niverow.numberkw(x1),
                                               b=niverow.numberkw(x2))
            
        gov = gov.replace("ha u","hag u")
        gov = gov.replace("ha e","hag e")
        gov = gov.replace("ha o","hag o")
        # display the question        
        self.diskwedhgovynn(gov)
        return keworrans


    
    def marnas(self):
        """ ask a subtraction question """
        n = self.chooseMaxN()
        # random numbers in question
        x1 = math.ceil(random.random() * n)
        x2 = math.ceil(random.random() * n)
        while self.options2.state() == 1 and x2 > x1:
            # choose again if difficulty is easy
            # and result is negative
            x1 = math.ceil(random.random() * n)
            x2 = math.ceil(random.random() * n)
        # calculate answer
        marnasyans = x1 - x2
        # store sum and answer as text and figures
        self.gorthyptekst = "{a} - {b} = {c}".format(a=niverow.numberkw(x1),
                                        b=niverow.numberkw(x2),
                                        c=niverow.numberkw_float(marnasyans))
        self.gorthypbys = "{a} - {b} = {c}".format(a=x1, b=x2, c=marnasyans)
        # display the question
        if self.options2.state() < 4:
            gov = "Pyth yw {a} marnas {b}?".format(a=niverow.numberkw(x1),
                                                   b=niverow.numberkw(x2))
        else:
            gov = "Pyth yw {a} - {b}?".format(a=niverow.numberkw(x1),
                                                   b=niverow.numberkw(x2))
        
        self.diskwedhgovynn(gov)
        return marnasyans
    
    def govynn1(self):
        """ ask a question, choosing addition or subtraction """
        self.starttime = time.time()
        self.choosemode()
        if self.qumode=="keworramarnas":
            g = random.choice([self.keworra, self.marnas])
        elif self.qumode == "marnas":
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
            self.govynn.config(text='', padx=10, pady=10)
        except ValueError:            
            output = "Res yw gorra niver y'n kyst\n avel bysies,"
            " rag ensample '42'"
            print(output)
            self.msg3.config(fg = 'orange', bg='black',
                             font=('Helvetica', 18, 'bold'), text=output)
            niver = -99
        self.gorthyp.clear()
        if niver or niver==0:
            kewarder = self.chekkGorthyp(niver, self.gorthypkewar)        
            
            if kewarder[0]:
                # if answer was correct
                t = time.time() - self.starttime
                # increment total points by at least 1 point
                # and up to an extra 1 point for speed
                self.poyntys += max([(10.0-t)/10.0, 0]) + 1
                self.niverewn += 1
                tekst = ("{gt}\n{k}\n{t:.1f}s, {e}/{g},"
                " sommenn poyntys = {p:.2f}").format(gt=self.gorthyptekst,
                                                     k=kewarder[1], t=t,
                                                     p=self.poyntys,
                                                     e=self.niverewn,
                                                     g=self.nivergwrys)
                fcolour='dark green'
            else:
                # if the answer was wrong
                tekst = ("{gt}  {b}\n{k}\n{e}/{g},"
                " sommenn poyntys = {p:.2f}").format(k=kewarder[1],
                                                     gt=self.gorthyptekst,
                                                     b=self.gorthypbys,
                                                     p=self.poyntys,
                                                     e=self.niverewn,
                                                     g=self.nivergwrys)                
                fcolour='dark red'
            if niver != -99:
                # if a numeric input was given
                # i.e. don't go to next question if
                # a non-numeric answer was given
                print(tekst)
                self.msg3.config(fg = fcolour, bg = 'light yellow',
                                 font=('Helvetica', 18, 'bold'), text=tekst)
                if self.nivergwrys < self.Ngovynn:
                    # ask next question
                    self.gorthypkewar = self.govynn1()
                else:
                    # if required number of questions have been asked                
                    self.gorfenna()
                    
    def bonuspoyntys(self, bonus=5):
        """ points bonus for getting all correct """
        self.poyntys = self.poyntys + bonus
                     
        
    def gorfenna(self):
        """ give report of user's number correct, and score """
        if self.niverewn == self.Ngovynn:
            self.bonuspoyntys()
            bonusmsg  = ("\nKeslowena!\nTy a worthybis pub govynn yn ewn.\n"
            "Bonus a bymp poynt yw genes!\n")
        elif self.niverewn == 0:
            bonusmsg = ("\nTruan!\nTy a worthybis pub govynn yn kamm!\n"
            "Martesen kath a gerdhas a-dro dha vysowek!\n")
        else:
            bonusmsg = ""
        endmsg = ("Ty a wrug {e} kewar a {N}. {b}"
        "Dha skor yw {n:.2f} a boyntys").format(e = self.niverewn,
                                                N = self.Ngovynn,
                                                b = bonusmsg,
                                                n = self.poyntys)
        self.msg3.config(fg = 'blue', bg = 'light yellow',
                         font=('Helvetica', 18, 'bold'), text=endmsg)
        
    def dalleth(self):
        """ clear answer box, and reset parameters """
        self.gorthyp.clear()
        self.msg3.config(fg = 'dark red', bg='light yellow',
                         font=('Helvetica', 18, 'bold'), text='')
        self.niverewn = 0
        self.nivergwrys = 0
        self.poyntys = 0
        self.Ngovynn = 20        
        self.gorthypkewar = self.govynn1()
        
        
if __name__ == '__main__':
    kwiz = AppAwgrym()
    kwiz.mainloop()    



