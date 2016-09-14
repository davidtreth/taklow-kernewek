# coding=utf-8
# David Trethewey
# updated 14-09-2016
import time
import niverow
import mutatya
import math
import argparse

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
        termyn = get_hour(hourint, 0)
    if hoursfrac % 1 == 0.25:
        termyn = "kwarter wosa "+ get_hour(hourint, 0)
    if hoursfrac % 1 == 0.5:
        termyn = "hanter wosa "+ get_hour(hourint, 0)
    if hoursfrac % 1 == 0.75:
        termyn = "kwarter dhe "+ mutatya.mutate(get_hour((hourint+1)%24,0),2)
    return termyn

def get_hour(hour, minute):
    if hour == 0:
        h = "hanternos"
    elif hour == 12:
        h = "hanterdydh"
    else:
        hour12 = hour % 12
        if hour < 12:
            ampm = " myttinweyth"
        elif hour < 18:
            ampm = " dohajydhweyth"
        else:
            ampm = " gorthugherweyth"
        if minute in [0,15,30,45]:
            h = niverow.numberkw(hour12) + " eur" + ampm
        else:
            h = niverow.numberkw(hour12) + ampm
    return h

def termyn_exact(hour, minute):
    if minute == 0:
        termyn = get_hour(hour)
    elif minute == 15:
        termyn = "kwarter wosa " + get_hour(hour, minute)
    elif minute == 30:
        termyn = "hanter wosa "+ get_hour(hour, minute)
    elif minute == 45:
        termyn = "kwarter dhe "+ mutatya.mutate(get_hour((hour+1) % 24, minute),2)
    else:
        if minute < 30:
            termyn = niverow.numberkw_noun(minute, "mynysenn") + " wosa " + get_hour(hour, minute)
        else:
            termyn = niverow.numberkw_noun(60-minute, "mynysenn") + " dhe " + mutatya.mutate(get_hour((hour+1) % 24, minute),2)
    return termyn
    
    
timenow = time.localtime()
date_kw = "{wday} {mday} mis-{mon}".format(wday=dydhyow[timenow.tm_wday], mday=niverow.numberkw_ord(timenow.tm_mday), mon=misyow[timenow.tm_mon])

if __name__ == '__main__':
    """
    If invoked at the command-line
    """
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    # take the input from a file specified
    # by a command line argument
    parser.add_argument("-d", "--dydh", action="store_true",
                        help="Skrif dydhyas yn Kernewek\nOutput date in Cornish")
    parser.add_argument("-b", "--blydhen", action="store_true",
                        help="Skrif blydhen y'n dydhyas\nInclude year in the date")
    parser.add_argument("-n", "--nes", action="store_true",
                        help="Skrif eur nesogas\nOutput approximate time")
    parser.add_argument("-k", "--kewar", action="store_true",
                        help="Skrif eur kewar dhe'n mynysenn\nOutput time exact to the minute")
    args = parser.parse_args()
    timenow = time.localtime()

    if args.dydh:
        if args.blydhen:
            date_kw = "{wday} {mday} mis-{mon} {yr}".format(
                wday = dydhyow[timenow.tm_wday],
                mday = niverow.numberkw_ord(timenow.tm_mday),
                mon = misyow[timenow.tm_mon],
                yr = niverow.numberkw(timenow.tm_year))
        else:
            date_kw = "{wday} {mday} mis-{mon}".format(
                wday = dydhyow[timenow.tm_wday],
                mday = niverow.numberkw_ord(timenow.tm_mday),
                mon = misyow[timenow.tm_mon])
        print(date_kw)
    if args.nes or args.kewar:
        print("{h:02}:{m:02}".format(h=timenow.tm_hour, m=timenow.tm_min))
        if args.nes:
            print(termyn_approx(timenow.tm_hour, timenow.tm_min))
        if args.kewar:
            print(termyn_exact(timenow.tm_hour, timenow.tm_min))
