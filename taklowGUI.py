# base module for GUI
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkMessageBox as messagebox
else:
    import tkinter as tk
    from tkinter import messagebox


class Kwitya(tk.Frame):
    """ define quit button """
    def __init__(self, parent = None,font=('Arial',14)):
        tk.Frame.__init__(self,parent)
        self.pack()
        widget = tk.Button(self, text='Kwitya', font=font,command=self.kwitya)
        widget.pack(side=tk.LEFT)
    def kwitya(self):
        ans = messagebox.askokcancel('Verifya kwityans', "Kwitya yn hwir?")
        if ans: tk.Frame.quit(self)

class Radiobar(tk.Frame):
    """ radio buttons to select one from a list """
    def __init__(self,parent=None, picks=[], side=tk.LEFT, anchor=tk.W,
                 font=('Arial', 13, 'normal'), default = False):
        tk.Frame.__init__(self, parent)
        self.var = tk.StringVar()
        if default in picks:
            self.var.set(default)
        for pick in picks:
            rad = tk.Radiobutton(self, text=pick, value = pick, variable=self.var)
            rad.config(font=font)
            rad.pack(side=side, anchor=anchor, expand=tk.N)
    def state(self):
        return self.var.get()

class CheckButtonBar(tk.Frame):
    """ a row of check boxes """
    def __init__(self,parent=None, labels = [], side=tk.LEFT,anchor=tk.W,
                 font=('Arial', 14, 'normal')):
        tk.Frame.__init__(self,parent)
        self.states = []
        for l in labels:
            var = tk.IntVar()
            chk = tk.Checkbutton(self,text=l,variable=var)
            chk.pack(side=tk.TOP)
            chk.config(font=font)
            self.states.append(var)
    def state(self):
        return [v.get() for v in self.states]
        

class Entrybar(tk.Frame):
    """ text entry bar """
    def __init__(self, parent=None, side=tk.TOP, anchor=tk.N,
                 font=('Arial', 13, 'normal')):
        tk.Frame.__init__(self,parent)
        self.var = tk.StringVar()
        self.ent = tk.Entry(self)
        self.ent.config(textvariable = self.var, font=font)
        self.ent.pack(side=side,anchor=anchor, fill=tk.X)
        
    def fetch(self):
        return self.var.get()
    def clear(self):
        self.ent.delete(0,tk.END)

class ScrolledText(tk.Frame):
    """ text box with scroll """
    def __init__(self,parent=None, text='', file=None,
                 font=('Arial', 14, 'normal')):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.makewidgets(font)
        self.settext(text, file)
    def makewidgets(self, font):
        sbar = tk.Scrollbar(self)
        text = tk.Text(self, relief=tk.SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set, font=font)
        sbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.text = text
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', text)
        self.text.mark_set(tk.INSERT, '1.0')
        self.text.focus()
    def gettext(self):
        return self.text.get('1.0', tk.END+'-1c')
    def clear(self):
        self.text.delete('1.0', tk.END)
                         
if __name__ == '__main__':
    root = tk.Tk()
    Kwitya(root).pack(side=tk.RIGHT)
    root.mainloop()
    
