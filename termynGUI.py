# coding=utf-8
from __future__ import print_function
import sys
import time
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, CheckButtonBar, wraplines
import termyn, niverow
import espeaktexttospeech.gorhemmyn_kw as gorhemmyn
import textwrap

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Termyn ha Dydhyas')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Helvetica', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = CheckButtonBar(root, ['Dydhyas','Diskwedh Blydhen',
                                    'Termyn Niverow',
                                    'Termyn Nesogas', 'Termyn Kewar',
                                    'Gorhemmyn'],
                             side=tk.TOP,
                             justify=tk.LEFT, anchor=tk.NW)
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2)

    def allstates(): print(options.state())

    def printtermyn():
        """ show the time or date in Cornish according to the preferences
         in the checkboxes """
        allstates()
        dydh, blydh, niver, nes, kewar, gor = options.state()
        output = ""
        timenow = time.localtime()
        if dydh:
            if blydh:
                output += termyn.dydhyas(timenow, blydhen=True)
            else:
                output += termyn.dydhyas(timenow, blydhen=False)
            output += "\n"
        else:
            if blydh:
                output += niverow.numberkw(timenow.tm_year) + "\n"
        if niver:
            output += "{h:02d}:{m:02d}\n".format(h=timenow.tm_hour, m=timenow.tm_min)
        if nes:
            output += termyn.termyn_approx(timenow.tm_hour, timenow.tm_min) + "\n"
        if kewar:
            output += termyn.termyn_exact(timenow.tm_hour, timenow.tm_min) + "\n"
        if gor:
            g = gorhemmyn.Gorhemmyn()
            output += g.gorhemmyn
            try:
                # wrap in try in case espeak doesn't exist
                g.kewsel()
            except:
                pass

        wrapoutput = wraplines(output, 50)
        print(wrapoutput)
        msg3.config(fg = 'dark red', bg = 'light yellow', font=('Helvetica', 18, 'bold'), text=wrapoutput)
        #msg3.config(text = output)

    def clearboxes():
         msg3.config(fg = 'dark red', bg='light yellow',font=('Helvetica', 18, 'bold'), text='')
        
    def copyclipbd():
        root.clipboard_clear()
        root.clipboard_append(msg3.cget("text"))
        
    # output
    msg3 = tk.Label(root)
    msg3.config(fg = 'dark red', bg='light yellow',font=('Helvetica', 18, 'bold'), text='')
    msg3.pack(expand=tk.YES,fill=tk.BOTH, anchor=tk.CENTER, padx=5, pady=5,
              ipadx=10, ipady=10)

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Diskwedh', font=('Helvetica',14),
              command = printtermyn).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Klerhe', font=('Helvetica', 14),
           command = clearboxes).pack(side=tk.LEFT)
    tk.Button(root, text = 'Kopi dhe\'n Klyppbordh', font=('Helvetica', 14),
              command = copyclipbd).pack(side=tk.LEFT)
    root.mainloop()


