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

    return chekkGorthyp(gorthyp, keworrans, interMode)
    
def marnas(n=20, interMode=True):
    x1 = random.choice(np.arange(n) + 1)
    x2 = random.choice(np.arange(n) + 1)
    marnasyans = x1 - x2
    gorthyp = govynn("Pyth yw {a} marnas {b}?\n".format(a=niverow.numberkw(x1),
                                                        b=niverow.numberkw(x2)))
    return chekkGorthyp(gorthyp, marnasyans, interMode)
    

def govynn1(niverewn=0, poyntys=0, mode="keworramarnas", interMode=True):
    starttime = time.time()
    if mode=="keworramarnas":
        g = random.choice([keworra, marnas])
    elif mode == "marnas":
        g = marnas
    else:
        g = keworra
    if g(interMode=interMode):
        t = time.time() - starttime
        poyntys += max([10-t, 0]) + 1
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

    for i in range(20):
        gorth, niverewn, poyntys, tekst = govynn1(niverewn, poyntys, "keworramarnas")
        print(tekst)

    print("Dha niver a boyntys yw {n:.1f}".format(n=poyntys))
