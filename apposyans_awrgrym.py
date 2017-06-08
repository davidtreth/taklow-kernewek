# coding=utf-8
#
# this isn't currently 08-06-17 being used by the
# apposyans_awrgrywGUI module, which implements
# the addition and subtraction functions etc. within itself

import niverow
import random
import sys
import time
import numpy as np

def govynn(tekst):
    if sys.version_info[0] < 3:
        gorthyp = raw_input(tekst)
    else:
        gorthyp = input(tekst)
    return gorthyp
def chekkGorthyp(g, kewar, interMode=True):
    try:
        g = int(g)
        if g == kewar:
            if interMode:
                print("Ewn os")            
                return True
            else:
                return True, "Ewn os"
        else:
            if interMode:
                print("Kamm os")
                return False
            else:
                return False, "Kamm os"
    except:
        if interMode:
            print("Nag yw {a} niver".format(a=g))
            return False
        else:
            return False, "Nag yw {a} niver".format(a=g)

def keworra(n = 20, interMode=True):
    x1 = random.choice(np.arange(n) + 1)
    x2 = random.choice(np.arange(n) + 1)
    keworrans = x1 + x2
    gov = "Pyth yw {a} ha {b}?\n".format(a=niverow.numberkw(x1),
                                         b=niverow.numberkw(x2))
    gov = gov.replace("ha u","hag u")
    gov = gov.replace("ha e","hag e")
    gov = gov.replace("ha o","hag o")
    gorthyp = govynn(gov)

    sommenntekst = "{a} + {b} = {c}".format(a=x1, b=x2, c=keworrans)
    print(sommenntekst)
    
    return chekkGorthyp(gorthyp, keworrans, interMode)
    
def marnas(n=20, interMode=True):
    x1 = random.choice(np.arange(n) + 1)
    x2 = random.choice(np.arange(n) + 1)
    marnasyans = x1 - x2
    gorthyp = govynn("Pyth yw {a} marnas {b}?\n".format(a=niverow.numberkw(x1),
                                                        b=niverow.numberkw(x2)))
    
    sommenntekst = "{a} - {b} = {c}".format(a=x1, b=x2, c=marnasyans)
    print(sommenntekst)
    return chekkGorthyp(gorthyp, marnasyans, interMode)

def liesriva(n=12, interMode=True):
    x1 = random.choice(np.arange(n) + 1)
    x2 = random.choice(np.arange(n) + 1)
    liesrivans = x1 * x2
    gorthyp = govynn("Pyth yw {a} lieshys gans {b}?\n".format(a=niverow.numberkw(x1),
                                                              b=niverow.numberkw(x2)))
    
    sommenntekst = "{a} * {b} = {c}".format(a=x1, b=x2, c=liesrivans)
    print(sommenntekst)
    return chekkGorthyp(gorthyp, liesrivans, interMode)

def disranna(n=12, interMode=True):
    x1 = random.choice(np.arange(n) + 1)
    x2 = random.choice(np.arange(n) + 1)
    liesrivans = x1 * x2
    gorthyp = govynn("Pyth yw {a} disrynnys gans {b}?\n".format(a=niverow.numberkw(liesrivans),
                                                                b=niverow.numberkw(x2)))
    sommenntekst = "{a} / {b} = {c}".format(a=liesrivans, b=x2, c=x1)
    print(sommenntekst)
    
    return chekkGorthyp(gorthyp, x1, interMode)
    
    
def govynn1(niverewn=0, poyntys=0, mode="oll", interMode=True):
    starttime = time.time()
    if mode=="oll":
        g = random.choice([keworra, marnas, liesriva, disranna])
    elif mode=="keworramarnas":
        g = random.choice([keworra, marnas])
    elif mode == "marnas":
        g = marnas
    else:
        g = keworra
    if g(interMode=interMode):
        t = time.time() - starttime
        poyntys += max([(10-t)/10.0, 0]) + 1
        niverewn += 1
        tekst = "{t:.1f}s, {e}/{g}, sommenn poyntys={p:.1f}\n".format(t=t,
                                                                      p=poyntys,
                                                                      e=niverewn,
                                                                      g=i+1)
        return True, niverewn, poyntys, tekst
    else:
        tekst = "{e}/{g}, sommenn poyntys={p:.1f}\n".format(p=poyntys,
                                                            e=niverewn,
                                                            g=i+1)
        return False, niverewn, poyntys, tekst

if __name__ == "__main__":
    poyntys = 0
    niverewn = 0
    ngovynn = 20
    for i in range(ngovynn):
        gorth, niverewn, poyntys, tekst = govynn1(niverewn, poyntys, "oll")
        print(tekst)

    if niverewn == ngovynn:
        print("Keslowena! Ty a worthybis pub govynn yn ewn! Bonus a bymp poynt yw genes!")
        poyntys += 5
    if niverewn == 0:
        print("Truan! Ty a worthybis pub govynn yn kamm!\nMartesen kath a gerdhas a-dro dha vysowek!\n")
    print("Dha niver a boyntys yw {n:.1f}".format(n=poyntys))
