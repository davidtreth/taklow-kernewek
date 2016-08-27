# based on PyGadgets.py from Programming Python 3rd edition examples
from __future__ import print_function
import sys, time
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from launchmodes import PortableLauncher    # reuse program start class

def runImmediate(mytools):
    # launch programs immediately
    print('Yma ow talleth Python/Tk GUI rag taklowkernewek') # msgs to temp stdout screen
    for (name, commandLine) in mytools:
        PortableLauncher(name, commandLine)()           # call now to start now
    print('Unn pols mar pleg...')                       # \b means a backspace
    if sys.platform[:3] == 'win':
        # on Windows keep stdio console window up for 5 seconds
        for i in range(5): time.sleep(1); print(('\b' + '.'*10), end = ' ')

def runLauncher(mytools):
    # put up a simple launcher bar for later use
    root = tk.Tk()
    root.title('TaklowKernewek GUI')
    for (name, commandLine) in mytools:
        b = tk.Button(root, text=name, fg='black', bg='beige', border=2,
                   command=PortableLauncher(name, commandLine))
        b.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    root.mainloop()

mytools = [
    ('Niverow', 'niverowGUI.py'),
    ('Mutatya', 'mutatyaGUI.py'),
    ('Inflektya', 'inflektyaGUI.py'),
    ('Ranna Syllabennow', 'sylrannakwGUI.py'),
    ('Treuslytherenna KK->FSS', 'treuslytherennaGUI.py'),
    ('Kov Treylyans', 'kovtreylyansGUI.py'),
    ('Statistegow Korpus\n(linenn arghadow)', 'cornish_corpus.py'),
    ('Menowghder Ger', 'corpus_wordfreqGUI.py'),
    ('Tekst --> Kows (dre espeak)', 'espeak-text-to-speech/kows_kernewek_GUI.py')
    ]

if __name__ == '__main__':
    prestart, toolbar = 1, 0
    if prestart:
        runImmediate(mytools)
    if toolbar:
        runLauncher(mytools)
        
    
    
