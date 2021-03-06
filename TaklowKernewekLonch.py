# coding=utf-8
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

def runLauncher(mytools, wtitle='TaklowKernewek GUI'):
    # put up a simple launcher bar for later use
    root = tk.Tk()
    root.title(wtitle)
    row1 = tk.Frame(root)
    row2 = tk.Frame(root)
    for (name, commandLine) in mytools[:5]:
        b = tk.Button(row1, text=name, fg='black', bg='beige', border=2,
                   command=PortableLauncher(name, commandLine))
        b.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    row1.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
    for (name, commandLine) in mytools[5:]:
        b = tk.Button(row2, text=name, fg='black', bg='beige', border=2,
                   command=PortableLauncher(name, commandLine))
        b.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    row2.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
                
    root.mainloop()

mytools = [
    ('Niverow', 'niverowGUI.py'),
    ('Apposyans Awgrym', 'apposyans_awgrymGUI.py'),
    ('Mutatya', 'mutatyaGUI.py'),
    ('Inflektya', 'inflektyaGUI.py'),
    ('Termyn ha Dydhyas', 'termynGUI.py'),
    ('Ranna Syllabennow', 'sylrannakwGUI.py'),
    ('Treuslytherenna KK->FSS', 'treuslytherennaGUI.py'),
    ('Kov Treylyans', 'kovtreylyansGUI.py'),
    ('Statistegow Korpus', 'corpus_wordfreqGUI.py')    
    ]
    # ('Tekst --> Kows (dre espeak)', 'kows_kernewek_GUI.py')
    # removed from main launchyer as user may not have espeak installed

mytools_netbook = [
    ('Niverow', 'niverowGUI.py'),
    ('Apposyans Awgrym', 'apposyans_awgrymGUI.py'),    
    ('Mutatya', 'mutatyaGUI.py'),
    ('Inflektya', 'inflektyaGUI.py --netbook'),
    ('Termyn ha Dydhyas', 'termynGUI.py'),
    ('Ranna Syllabennow', 'sylrannakwGUI.py --netbook'),
    ('Treuslytherenna KK->FSS', 'treuslytherennaGUI.py --netbook'),
    ('Kov Treylyans', 'kovtreylyansGUI.py --netbook'),
    ('Statistegow Korpus', 'corpus_wordfreqGUI.py --netbook'),
    ('Tekst --> Kows (dre espeak)', 'kows_kernewek_GUI.py')
    ]
    # ('Tekst --> Kows (dre espeak)', 'kows_kernewek_GUI.py')
    # removed from main launchyer as user may not have espeak installed
    
mytools_cymraeg = [('Niferau', 'niferaucyGUI.py'),
                   ('Treiglo', 'treigloGUI.py'),
                   ('Rhannu Sillafau', 'sylrannacyGUI.py')
    ]
mytools_cymraeg_netbook = [('Niferau', 'niferaucyGUI.py'),
                           ('Treiglo', 'treigloGUI.py'),
                           ('Rhannu Sillafau', 'sylrannacyGUI.py --netbook')
    ]
if __name__ == '__main__':
    prestart, toolbar = 1, 0
    if prestart:
        runImmediate(mytools)
    if toolbar:
        runLauncher(mytools)
        
    
    
