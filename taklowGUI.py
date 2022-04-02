# coding=utf-8
# base module for GUI
import sys
import textwrap
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkMessageBox as messagebox
else:
    import tkinter as tk
    from tkinter import messagebox

def wraplines(outtext, width=60):
    """ word wrap one line at a time, to preserve original newlines """
    outtext = outtext.split("\n")
    outtext = [textwrap.fill(l, width) for l in outtext]
    outtext = "\n".join(outtext)
    return outtext

class Kwitya(tk.Frame):
    """ define quit button """
    def __init__(self, parent = None,font=('Helvetica',14)):
        tk.Frame.__init__(self,parent)
        self.pack()
        widget = tk.Button(self, text='Kwitya', font=font,command=self.kwitya)
        widget.pack(side=tk.LEFT)
    def kwitya(self):
        ans = messagebox.askokcancel('Verifya kwityans', "Kwitya yn hwir?")
        if ans: tk.Frame.quit(self)

class Kwitya2(tk.Frame):
    """ define quit button """
    def __init__(self, parent = None,font=('Helvetica',14)):
        tk.Frame.__init__(self,parent)
        self.pack()
        widget = tk.Button(self, text='Kwitya', font=font,command=self.kwitya)
        widget.pack(side=tk.LEFT)
    def kwitya(self):
        ans = messagebox.askokcancel('Verifya kwityans', "Kwitya yn hwir?")
        if ans: sys.exit()

class Gadael(tk.Frame):
    """ quit button in Welsh """
    def __init__(self, parent = None,font=('Helvetica',14)):
        tk.Frame.__init__(self,parent)
        self.pack()
        widget = tk.Button(self, text='Gadael', font=font,command=self.gadael)
        widget.pack(side=tk.LEFT)
    def gadael(self):
        ans = messagebox.askokcancel('Byddwch siwr am gadael?', "Gadael yn gwir?")
        if ans: tk.Frame.quit(self)
        
class Radiobar(tk.Frame):
    """ radio buttons to select one from a list """
    def __init__(self,parent=None, picks=[], vals = [], side=tk.LEFT, justify=tk.CENTER,
                 anchor=tk.W, font=('Helvetica', 13, 'normal'), default = False):
        tk.Frame.__init__(self, parent)
        if len(vals) == 0:
            # if vals is an empty list
            # use strings in picks
            # for values
            self.var = tk.StringVar()
            if default in picks:
                self.var.set(default)
            vals = picks
        else:
            # otherwise assume vals is
            # a list of ints
            self.var=tk.IntVar()
            if default in vals:
                self.var.set(default)
        self.rads = []            
        for pick, v in zip(picks, vals):
            rad = tk.Radiobutton(self, text=pick, value = v, justify=justify,
                                 variable=self.var)
            rad.config(font=font)
            rad.pack(side=side, anchor=anchor, expand=tk.N)
            self.rads.append(rad)
    def state(self):
        return self.var.get()
    
    def destroyrads(self):
        for rad in self.rads:
            rad.destroy()
            
    def newrads(self, picks=[], vals=[], side=tk.TOP, justify=tk.CENTER,
                anchor=tk.W, font=('Helvetica', 13, 'normal'), default=False):
        if len(vals) == 0:
            # if vals is an empty list
            # use strings in picks
            # for values
            self.var = tk.StringVar()
            if default in picks:
                self.var.set(default)
            vals = picks
        else:
            # otherwise assume vals is
            # a list of ints
            self.var=tk.IntVar()
            if default in vals:
                self.var.set(default)
        self.rads = []
        for pick, v in zip(picks, vals):
            rad = tk.Radiobutton(self, text=pick, value = v, justify=justify,
                                 variable=self.var)
            rad.config(font=font)
            rad.pack(side=side, anchor=anchor, expand=tk.N)
            self.rads.append(rad)
        

        

class CheckButtonBar(tk.Frame):
    """ a row of check boxes """
    def __init__(self,parent=None, labels = [], side=tk.LEFT,
                 justify=tk.CENTER, anchor=tk.W,
                 font=('Helvetica', 14, 'normal')):
        tk.Frame.__init__(self,parent)
        self.states = []
        for r, l in enumerate(labels):
            var = tk.IntVar()
            chk = tk.Checkbutton(self,text=l, font=font,
                                 justify=justify,
                                 variable=var).grid(row=r, sticky=tk.W)
            self.states.append(var)
            
    def state(self):
        return [v.get() for v in self.states]
        

class Entrybar(tk.Frame):
    """ text entry bar """
    def __init__(self, parent=None, side=tk.TOP, anchor=tk.N,
                 font=('Helvetica', 13, 'normal')):
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
                 font=('Helvetica', 14, 'normal')):
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
    
