from Tkinter import *
from taklowGUI import Kwitya, Entrybar, CheckButtonBar, Radiobar
import syllabenn_ranna_kw as syl

if __name__ == '__main__':
    root = Tk()
    root.title('Syllabenn Ranna Kernewek')
    mhead = Label(root, text = "Dewisyow")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=TOP, anchor=NW)

    options = Radiobar(root, ['Mode Hir', 'Mode Berr', 'Mode Linenn'], side=TOP, anchor=NW,default='Mode Berr')
    options.pack(side=LEFT, fill=Y)
    options.config(relief=RIDGE, bd=2)

    options2 = Radiobar(root, ['Rannans war-rag', 'Rannans war-dhelergh'], side=TOP, anchor=NW, default='Rannans war-dhelergh')
    options2.pack(side=LEFT, fill=Y)
    options2.config(relief=RIDGE, bd=2)
    
    def allstates(): print options.state(), options2.state(), ent.fetch()

    def printsylranna():
        """ show the output in Cornish, according to the options
         in the radiobar is selected """
        allstates()
        inputtext = ent.fetch()
        print("Input: {i}".format(i=inputtext))
        output = ''
        msg3.config(fg = 'dark red', bg = 'light yellow', font=('Arial', 18, 'bold'))
        if inputtext:
            if options2.state() == 'Rannans war-rag':
                fwd = True
            else: fwd = False
                
            if options.state() == 'Mode Hir':
                output = syl.detailSylsText(inputtext,fwd)
                msg3.config(font=('Arial', 14, 'normal'))
            elif options.state() == 'Mode Linenn':
                output = syl.countSylsLine(inputtext,fwd)
            else:
                # use short mode by default if nothing is selected
                output = syl.detailSylsText(inputtext,fwd,short=True)
            print(output)

        msg3.config(text = output)

    def clearboxes():
        ent.clear()
        msg3.config(fg = 'dark red', bg='light yellow',font=('Arial', 18, 'bold'), text='')
        
        
    msg = Label(root, text="Gorrewgh tekst kernewek a-woeles mar pleg:")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar for input
    ent = Entrybar(root)
    ent.pack()
    
    # output
    msg3 = Label(root)
    msg3.config(fg = 'dark red', bg='light yellow',font=('Arial', 18, 'bold'), text='')
    msg3.pack(expand=YES,fill=BOTH, anchor=CENTER)

    # buttons
    Kwitya(root).pack(side=RIGHT)
    Button(root, text = 'Diskwedh Syllabennow', font=('Arial',14),
           command = printsylranna).pack(side=RIGHT)
    Button(root, text = 'Klerhe', font=('Arial', 14),
           command = clearboxes).pack(side=LEFT)
    root.mainloop()


