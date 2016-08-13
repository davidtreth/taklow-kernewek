from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from taklowGUI import Kwitya, Radiobar, ScrolledText
import syllabenn_ranna_kw as syl

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Syllabenn Ranna Kernewek')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)

    options = Radiobar(root, ['Mode Hir', 'Mode Berr', 'Mode Linenn'], side=tk.TOP, anchor=tk.NW,default='Mode Berr')
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2)

    options2 = Radiobar(root, ['Rannans war-rag', 'Rannans war-dhelergh'], side=tk.TOP, anchor=tk.NW, default='Rannans war-dhelergh')
    options2.pack(side=tk.LEFT, fill=tk.Y)
    options2.config(relief=tk.RIDGE, bd=2)
    
    def allstates(): print(options.state(), options2.state(), ent.gettext())

    def printsylranna():
        """ show the output in Cornish, according to the options
         in the radiobar is selected """
        allstates()
        inputtext = ent.gettext()
        print("Input: {i}".format(i=inputtext))
        output = ''
        msg3.text.config(fg = 'dark red', bg = 'light yellow', font=('Arial', 16, 'bold'), state=tk.NORMAL)
        if inputtext:
            if options2.state() == 'Rannans war-rag':
                fwd = True
            else: fwd = False
                
            if options.state() == 'Mode Hir':
                output = syl.detailSylsText(inputtext,fwd)
                msg3.text.config(font=('Arial', 14, 'normal'))
            elif options.state() == 'Mode Linenn':
                lines = inputtext.split('\n')                
                for l in lines:                    
                    output += syl.countSylsLine(l,fwd)+'\n\n'
                output = output[:-1]
            else:
                # use short mode by default if nothing is selected
                output = syl.detailSylsText(inputtext,fwd,short=True)
            print(output)

        msg3.settext(output)
        msg3.text.config(state=tk.DISABLED)
    def clearboxes():
        ent.clear()
        msg3.text.config(fg = 'dark red', bg='light yellow',font=('Arial', 16, 'bold'),state=tk.NORMAL)
        msg3.clear()
        msg3.text.config(state=tk.DISABLED)
        
        
    msg = tk.Label(root, text="Gorrewgh tekst kernewek a-woeles mar pleg:")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar for input
    ent = ScrolledText(root)
    ent.text.config(width=40,height=11)
    ent.pack(expand=0)
    
    # output
    msg3 = ScrolledText(root)
    msg3.text.config(fg = 'dark red', bg='light yellow', width=40, height=11,font=('Arial', 16, 'bold'), state=tk.DISABLED)
    msg3.pack()

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Diskwedh Syllabennow', font=('Arial',14),
           command = printsylranna).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Klerhe', font=('Arial', 14),
           command = clearboxes).pack(side=tk.LEFT)
    root.mainloop()


