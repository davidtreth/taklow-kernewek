# base module for GUI
from Tkinter import *
from tkMessageBox import askokcancel

class Kwitya(Frame):
    """ define quit button """
    def __init__(self, parent = None,font=('Arial',14)):
        Frame.__init__(self,parent)
        self.pack()
        widget = Button(self, text='Kwitya', font=font,command=self.kwitya)
        widget.pack(side=LEFT)
    def kwitya(self):
        ans = askokcancel('Verifya kwityans', "Kwitya yn hwir?")
        if ans: Frame.quit(self)

class Radiobar(Frame):
    """ radio buttons to select one from a list """
    def __init__(self,parent=None, picks=[], side=LEFT, anchor=W,
                 font=('Arial', 13, 'normal'), default = False):
        Frame.__init__(self, parent)
        self.var = StringVar()
        if default in picks:
            self.var.set(default)
        for pick in picks:
            rad = Radiobutton(self, text=pick, value = pick, variable=self.var)
            rad.config(font=font)
            rad.pack(side=side, anchor=anchor, expand=N)
    def state(self):
        return self.var.get()

class CheckButtonBar(Frame):
    """ a row of check boxes """
    def __init__(self,parent=None, labels = [], side=LEFT,anchor=W,
                 font=('Arial', 14, 'normal')):
        Frame.__init__(self,parent)
        self.states = []
        for l in labels:
            var = IntVar()
            chk = Checkbutton(self,text=l,variable=var)
            chk.pack(side=TOP)
            chk.config(font=font)
            self.states.append(var)
    def state(self):
        return [v.get() for v in self.states]
        

class Entrybar(Frame):
    """ text entry bar """
    def __init__(self, parent=None, side=TOP, anchor=N,
                 font=('Arial', 13, 'normal')):
        Frame.__init__(self,parent)
        self.var = StringVar()
        self.ent = Entry(self)
        self.ent.config(textvariable = self.var, font=font)
        self.ent.pack(side=side,anchor=anchor, fill=X)
        
    def fetch(self):
        return self.var.get()
    def clear(self):
        self.ent.delete(0,END)
                         
if __name__ == '__main__':
    root = Tk()
    Kwitya(root).pack(side=RIGHT)
    root.mainloop()
    
