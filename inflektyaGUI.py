import Tkinter as tk
from taklowGUI import Kwitya, Radiobar, ScrolledText, Entrybar
import inflektya

tensesDict2 = {"A-lemmyn":"a-lemmyn",
              "Tremenys":"tremenys",
              "Anperfydh":"anperfydh",
              "Gorperfydh":"gorperfydh",
              "Islavarek A-lemmyn":"islavarek_a-lemmyn",
              "Islavarek Anperfydh":"islavarek_anperfydh",
              "Gorhemmyn":"gorhemmyn",
              "ppl":"ppl",
              "Devedhek":"devedhek",
              "Anperfydh Usadow":"anperfydh_usadow",
              "A-lemmyn Hir Indef":"a-lemmyn_hir_indef",
              "Anperfydh Hir":"anperfydh_hir",
              "A-lemmyn Hir Def":"a-lemmyn_hir_def",
              "A-lemmyn Hir Aff":"a-lemmyn_hir_aff",
              "Perfydh":"perfydh"}

personDict = {'My':1, 'Ty':2, 'Ev':3, 'Hi':4, 'Ni':5,
              'Hwi':6, 'I':7, 'Anpersonek':0, 'Pub Person':-1}
personDictR = {v:k for k,v in personDict.items()}
suffixDict = {'Heb raghenwyn a syw':0, 'Raghenwyn a syw':1,
              'Raghenwyn a syw gans poeslev':2}

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Inflektya Verbow Kernewek')
    mhead = tk.Label(root, text = "Dewisyow")
    mhead.config(font=('Arial', 16, 'bold'))
    mhead.pack(side=tk.TOP, anchor=tk.NW)
    
    rhead = tk.Label(root, text = "Amser")
    rhead.config(font=('Arial', 12, 'bold'))
    rhead.pack(side=tk.TOP, anchor=tk.NW)
    options = Radiobar(root, ['A-lemmyn', 'Tremenys', 'Anperfydh', 'Gorperfydh',
                              'Islavarek A-lemmyn', 'Islavarek Anperfydh',
                              'Gorhemmyn', 'ppl', 'Devedhek',
                              'Anperfydh Usadow', 'A-lemmyn Hir Indef',
                              'Anperfydh Hir', 'A-lemmyn Hir Def',
                              'A-lemmyn Hir Aff', 'Perfydh'],
                       side=tk.TOP, anchor=tk.NW,default='A-lemmyn')
    options.pack(side=tk.LEFT, fill=tk.Y)
    options.config(relief=tk.RIDGE, bd=2)

    rhead2 = tk.Label(root, text = "Person")
    rhead2.config(font=('Arial', 12, 'bold'))
    rhead2.pack(side=tk.TOP, anchor=tk.NW)
    options2 = Radiobar(root, ['My', 'Ty', 'Ev', 'Hi', 'Ni',
                               'Hwi', 'I', 'Anpersonek', 'Pub Person'],
                        side=tk.TOP, anchor=tk.NW, default='My')
    options2.pack(side=tk.LEFT, fill=tk.Y)
    options2.config(relief=tk.RIDGE, bd=2)

    rhead3 = tk.Label(root, text = "Raghenwyn a syw")
    rhead3.config(font=('Arial', 12, 'bold'))
    rhead3.pack(side=tk.TOP, anchor=tk.NW)
    options3 = Radiobar(root, ['Heb raghenwyn a syw', 'Raghenwyn a syw',
                               'Raghenwyn a syw gans poeslev'], side=tk.TOP,
                        anchor=tk.NW, default = 'Heb raghenwyn a syw')
    options3.pack(side=tk.LEFT, fill=tk.Y)
    options3.config(relief=tk.RIDGE, bd=2)
    
    def allstates(): 
        print options.state(), options2.state(), options3.state(), ent.fetch()

    def printinflektya():
        """ show the output in Cornish, according to the options
         in the radiobar is selected """
        allstates()
        inputtext = ent.fetch()
        inputtext = inputtext.lower()
        print("Input: {i}".format(i=inputtext))
        output = ''
        msg3.text.config(fg = 'dark red', bg = 'light yellow', font=('Monospace', 16, 'bold'), state=tk.NORMAL)
        if inputtext:
            if options2.state() == 'Pub Person':
                if options.state() == 'ppl':
                    output = inflektya.inflektya(inputtext, 1, tensesDict2[options.state()], suffixDict[options3.state()])[0]
                else:
                    # print all persons
                    output = ''
                    validoutputs = 0
                    for p in range(8):
                        outperson, valid = inflektya.inflektya(inputtext, p, tensesDict2[options.state()],suffixDict[options3.state()])
                        validoutputs += valid
                        output += '{pers}{s}:{s2}{outp}'.format(pers = personDictR[p], s=" "*(15-len(personDictR[p])), outp = outperson, s2 = " "*(20-len(outperson)))
                        if p < 7:
                            output += '\n'
                    if validoutputs == 0:
                        output = "Nyns yw amser '{t}' ewn rag verb '{v}'".format(t=options.state(), v=inputtext)
            else:
                output = inflektya.inflektya(inputtext,
                                             personDict[options2.state()],
                                             tensesDict2[options.state()],
                                             suffixDict[options3.state()])[0]
                if output == 'NULL':
                    output = "Nyns yw amser '{t}', person '{p}' ewn rag verb '{v}'".format(t=options.state(), p=options2.state(), v=inputtext)
                # msg3.text.config(font=('Arial', 14, 'normal'))
            if not(inputtext.isalpha()):
                output = "Gwarnyans, nyns yw an ynworrans alpfabetek.\n\n"+output
            print(output)

        msg3.settext(output)
        msg3.text.config(state=tk.DISABLED)
    def clearboxes():
        ent.clear()
        msg3.text.config(fg = 'dark red', bg='light yellow',font=('Monospace', 16, 'bold'),state=tk.NORMAL)
        msg3.clear()
        msg3.text.config(state=tk.DISABLED)
        
        
    msg = tk.Label(root, text="Gorrewgh verb kernewek a-woeles mar pleg:")
    msg.config(font=('Arial', 16, 'bold'))
    msg.pack()
    
    # text entry bar for input
    ent = Entrybar(root)
    ent.pack()
    
    # output
    msg3 = ScrolledText(root)
    msg3.text.config(fg = 'dark red', bg='light yellow', width=40, height=11,font=('Monospace', 16, 'bold'), state=tk.DISABLED)
    msg3.pack()

    # buttons
    Kwitya(root).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Inflektya Verb', font=('Arial',14),
              command = printinflektya).pack(side=tk.RIGHT)
    tk.Button(root, text = 'Klerhe', font=('Arial', 14),
           command = clearboxes).pack(side=tk.LEFT)
    root.mainloop()


