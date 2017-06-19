#!/usr/bin/python
# -*- coding: utf-8 -*-
# David Trethewey 
# code is Open Source (GPL)
# Fenten Igor yw an kodenn ma (GPL)

# import nltk
from itertools import permutations
from syllabenn_ranna_kw import kwKemmynRegExp as kwRE
import re

def pubPermutyans(instr, minL=4, maxL=9):
    assert maxL > minL
    allP = []
    for i in range(minL, maxL+1):
        print("i = {}".format(i))
        P_i = [''.join(p) for p in permutations(instr, i)]
        #print(P_i)
        allP.extend(P_i)
    return allP
        
        

def pubPermutyansNawbedrek(nawbedrek = "nawbedrek"):
    assert len(nawbedrek) == 9
    #lytherennow = nltk.FreqDist(nawbedrek)
    # start by all permutations of the 9 letters
    gerva = pubPermutyans(nawbedrek)
    # the letter in the middle that must be used
    reslyther = nawbedrek[4]
    # filter the list of permutations by fact of containing necessary letter
    print("pub permutyans kevys, hidla gans edhomm reslyther")
    pubNaw4 = set(g for g in gerva if reslyther in g)
    return pubNaw4


def dybriGer(reKynsa, ger, verbose=False):
    """ consume the word by the word-initial regexp """
    if verbose:
        print("ger arbrovel {g}".format(g=ger))
    while ger:
        syl = re.findall(reKynsa, ger)
        if verbose:
            print(syl)
        try:
            # if indexing fails, then there is not a valid syllable
            # to consume the string as a potential Cornish word
            ger = ger.replace(syl[0][0], "")
        except IndexError:
            if verbose:
                print("False")
            return False
    # if string is fully consumed return True
    if verbose:
        print("True")
    return True
    

if __name__ == "__main__":
    q = "0"
    while not(q.isalpha() and len(q) == 9):
        q = raw_input("ynworra 9 lyther mar pleg:\n")
        #print(pubPermutyansNawbedrek(q))
        p = pubPermutyansNawbedrek(q)
        geryowposs = [g for g in p if dybriGer(kwRE.kynsaRegExp, g, verbose=False)]
        # sort alphabetically then by length
        geryowposs.sort()
        geryowposs.sort(key=len)

        print(geryowposs)

        print("ynworrans o {q}, niver a eryow 4-9 lyther yw {n}, niver a eryow gans 9 lyther yw {nn}".format(
            q=q, n=len(geryowposs), nn=len([g for g in geryowposs if len(g)==9])))
