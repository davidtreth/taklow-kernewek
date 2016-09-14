# coding=utf-8
# David Trethewey
# updated 14-09-2016
import time
import niverow
import mutatya
import math

misyow = {1:"Genver",
          2:"Hwevrer",
          3:"Meurth",
          4:"Ebrel",
          5:"Me",
          6:"Metheven",
          7:"Gortheren",
          8:"Est",
          9:"Gwynngala",
          10:"Hedra",
          11:"Du",
          12:"Kevardhu"}

dydhyow = {0:"Dy' Lun",
           1:"Dy' Meurth",
           2:"Dy' Mergher",
           3:"Dy' Yow",
           4:"Dy' Gwener",
           5:"Dy' Sadorn",
           6:"Dy' Sul"}

def termyn_approx(hour, minute):
    hoursfrac = hour + minute/60.0
    hoursfrac *= 4.0
    hoursfrac = round(hoursfrac)
    hoursfrac /= 4.0
    # print(hoursfrac)
    hourint = math.floor(hoursfrac)
    if hoursfrac % 1 == 0:
        termyn = niverow.numberkw(hoursfrac) + " eur"
    if hoursfrac % 1 == 0.25:
        termyn = "kwarter wosa "+ niverow.numberkw(hourint)
    if hoursfrac % 1 == 0.5:
        termyn = "hanter wosa "+ niverow.numberkw(hourint)
    if hoursfrac % 1 == 0.75:
        termyn = "kwarter dhe "+ mutatya.mutate(niverow.numberkw(hourint+1),2)
    if hour < 12:
        termyn += " myttinweyth"
    elif hour < 18:
        termyn += " dohajydhweyth"
    else:
        termyn += " gorthugherweyth"
    return termyn

timenow = time.localtime()
date_kw = "{wday} {mday} mis-{mon}".format(wday=dydhyow[timenow.tm_wday], mday=niverow.numberkw_ord(timenow.tm_mday), mon=misyow[timenow.tm_mon])


print(date_kw)
print("{h:02}:{m:02}".format(h=timenow.tm_hour, m=timenow.tm_min))
print(termyn_approx(timenow.tm_hour % 12, timenow.tm_min))
