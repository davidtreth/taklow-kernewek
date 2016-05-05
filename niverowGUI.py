from Tkinter import *
from taklowGUI import Kwitya, Entrybar, CheckButtonBar
import niverow

if __name__ == '__main__':
    root = Tk()
    root.title('Niverow')
    mhead = Label(root, text = "Dewisyow")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=TOP, anchor=NW)

    options = CheckButtonBar(root, ['Usya Hanow','Hanow Benow'], side=TOP, anchor=NW)
    options.pack(side=LEFT, fill=Y)
    options.config(relief=RIDGE, bd=2)
    def allstates(): print options.state(), ent.fetch(), ent2.fetch()

    def printniver():
        """ show the number in Cornish, with the noun if the checkbox
         is selected """
        allstates()
        if ent.fetch().isdigit():
            if options.state()[0] == 1 and ent2.fetch() != "":
                output = niverow.numberkw_noun(int(ent.fetch()),ent2.fetch(),options.state()[1])
            else:
                output = niverow.numberkw(int(ent.fetch()))
            print(output)
            msg3.config(fg = 'dark red', bg = 'light yellow', font=('Arial', 18, 'bold'))
        else:
            output = "Res yw gorra niver y'n kyst\n avel bysies, rag ensample '42'"
            msg3.config(fg = 'orange', bg='black',font=('Arial', 18, 'bold'))
        msg3.config(text = output)

    msg = Label(root, text="Gorrewgh niver a-woles mar pleg")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar for number
    ent = Entrybar(root)
    ent.pack()
    
    msg2 = Label(root, text="Gorrewgh hanow kernewek a-woles mar pleg")
    msg2.config(font=('Arial', 16, 'bold'))
    msg2.pack()
    # text entry bar for noun
    ent2 = Entrybar(root)
    ent2.pack()

    # output
    msg3 = Label(root)
    msg3.config(fg = 'dark red', bg='light yellow',font=('Arial', 18, 'bold'), text='')
    msg3.pack(expand=YES,fill=BOTH, anchor=CENTER)

    # buttons
    Kwitya(root).pack(side=RIGHT)
    Button(root, text = 'Diskwedh Niver', font=('Arial',14),
           command = printniver).pack(side=RIGHT)
    root.mainloop()


