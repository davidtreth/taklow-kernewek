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
                 font=('Arial', 13, 'normal')):
        Frame.__init__(self, parent)
        self.var = StringVar()
        for pick in picks:
            rad = Radiobutton(self, text=pick, value = pick, variable=self.var)
            rad.config(font=font)
            rad.pack(side=side, anchor=anchor, expand=YES)
    def state(self):
        return self.var.get()

class Entrybar(Frame):
    """ text entry bar """
    def __init__(self, parent=None, side=TOP, anchor=N,
                 font=('Arial', 13, 'normal')):
        Frame.__init__(self,parent)
        self.var = StringVar()
        ent = Entry(self)
        ent.config(textvariable = self.var, font=font)
        ent.pack(side=side,anchor=anchor, fill=X)
        
    def fetch(self):
        return self.var.get()
                         
if __name__ == '__main__':
    root = Tk()
    Kwitya(root).pack(side=RIGHT)
    root.mainloop()
    
