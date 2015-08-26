# gorhemmyn_kw.py
# David Trethewey
# 11-07-2015 
# skrifys rag #speakcornish week 2015
import time
import os
import kernewek_to_welshorthography
class Gorhemmyn:
    # py termynyow a wra chanjya 
    # furv an gorhemmynadow
    bora = 3
    myttin = 7
    dydh = 11
    dohajydh = 14
    gorthugher = 18
    nos = 23
    def __init__(self):
        t = time.localtime()
        our = t.tm_hour
        self.gorhemmyn = "Dydh da" # default
        if our >= Gorhemmyn.nos or our < Gorhemmyn.bora:
            self.gorhemmyn = "Nos da"
        if our >= Gorhemmyn.bora and our < Gorhemmyn.myttin:
            self.gorhemmyn = "Bora da"
        if our >= Gorhemmyn.myttin and our < Gorhemmyn.dydh:
            self.gorhemmyn = "Myttin da"
        if our >= Gorhemmyn.dydh and our < Gorhemmyn.dohajydh:
            self.gorhemmyn = "Dydh da"
        if our >= Gorhemmyn.dohajydh and our < Gorhemmyn.gorthugher:
            self.gorhemmyn = "Dohajydh da"
        if our >= Gorhemmyn.gorthugher and our < Gorhemmyn.nos:
            self.gorhemmyn = "Gorthugher da"

    def pryntya(self):
        print(self.gorhemmyn)

    def kewsel(self):
        tekst_cy = kernewek_to_welshorthography.towelsh(self.gorhemmyn)
        #print(tekst_cy)
        espeakcmd = 'espeak -vcy \"{t}\"'.format(t=tekst_cy)
        #print(espeakcmd)
        os.system(espeakcmd)
        
if __name__ == "__main__":
    g = Gorhemmyn()
    g.pryntya()
    g.kewsel()
