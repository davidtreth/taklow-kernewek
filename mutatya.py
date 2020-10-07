# coding=utf-8
# David Trethewey revised 09-08-2016
# This doesn't actually determine whether
# a word should mutate
#
# all it does is take a word and mutation state 
# from 1 to 6
# in function mutate(word, mutationstate)
# and return the mutated form
#
# 1 = no mutation
# 2 = soft mutation k-->g, p-->b etc.
# 3 = breathed mutation p->f k->h t->th
# 4 = hard mutation g->k d->t b->p
# 5 = mixed I
# 6 = mixed II after 'th
#
# or for Welsh in fuction mutate_cy(word, mutationstate)
# mutation state can be one of 1, 2, 7, 8
# where 7 = nasal mutation
#       8 = mixed mutation after neg. part. ni
#           either soft or breathed depending on
#           initial letter
#
# it will try to return it in the same case
# i.e. lower, UPPER, or Title
import sys, imp
imp.reload(sys)
if sys.version_info[0] < 3:
    sys.setdefaultencoding('utf-8')
    
def caseFormat(word,outputcase):
    # outputcase determines 
    # capitalisation of output
    if outputcase == 'lower':
        return word.lower()
    if outputcase == 'upper':
        return word.upper()
    if outputcase == 'title':
        return word.title()
    return word

def findOutputCase(word):
    outputcase = 'lower' # default
    if word.islower():
        outputcase = 'lower'
    if word.istitle():
        outputcase = 'title'
    if word.isupper():
        outputcase = 'upper'
    return outputcase
 

def mutate(word,mutationstate, trad=False):
    """ 
    take word as a str 
    and mutationstate as integer from 1-6
    use variable outputcase
    to return word in same capitalisation
    as it went in
    note that non-standard capITALization
    will be turned lower case
    variable trad set to True will expect and return
    traditional graphs as in SWF/T
    """

    outputcase = findOutputCase(word)
    word = word.lower()
    # default to no mutation if mutationstate isn't what is
    # expected (int from 1-6)
    if not(isinstance(mutationstate,int)):
        mutationstate = 1
    if (mutationstate < 1) or (mutationstate > 6):
        mutationstate = 1

    if mutationstate == 1:
        # unmutated
        return caseFormat(word,outputcase)

    if mutationstate == 2:
        # lentition
        newword = word
        # exception for Gorsedh -> An Orsedh
        if (word[0:7] == "gorsedh") or (word[0:7] == "gorseth"):
            newword = word[1:]
            return caseFormat(newword,outputcase)

        if (word[0:2] == "go")or(word[0:2] == "gu")or(word[0:3] == "gro")or(word[0:3] == "gru"):
            newword = "w" + word[1:]
            return caseFormat(newword,outputcase)

        if word[0] == "g":
            newword = word[1:]
        if (word[0] == "b")or(word[0] == "m"):
            newword = "v" + word[1:]
        if word[0] == "k":
            newword = "g" + word[1:]
        if trad and ((word[0] == "c" and word[0:2] != "ch")or(word[0:2] == "qw")):
            # if using traditional spelling recognise initial c
            newword = "g" + word[1:]
        if word[0:2] == "ch":
            newword = "j" + word[2:]
        if word[0] == "d":
            if word[0:4] == "dydh":
                newword = "j"+word[1:]
            else:
                newword = "dh" + word[1:]
        if word[0] == "p":
            newword = "b" + word[1:]
        if word[0] == "t":
            newword = "d" + word[1:]
        return caseFormat(newword,outputcase)

    if mutationstate == 3:
        # breathed mutation
        newword = word
        if word[0] == "k":
            if word[0:2] not in ['kl', 'kr']:
                newword = "h" + word[1:]
        if trad and word[0] == "c":
            if word[0:2] not in ['cl', 'cr']:
                newword = "h" + word[1:]
        if trad and word[0:2] == "qw":
            newword = "wh" + word[2:]
        if word[0] == "p":
            newword = "f" + word[1:]
        if word[0] == "t":
            newword = "th" + word[1:]
        return caseFormat(newword,outputcase)

    if mutationstate == 4:
        # hard mutation
        newword = word
        if word[0] == "b":
            newword = "p" + word[1:]
        if word[0] == "d":
            newword = "t" + word[1:]
        if word[0] == "g":
            if trad and word[1] not in 'einyw':
                newword = "c" + word[1:]
            elif trad and word[1] == "w":
                newword = "q" + word[1:]
            else:
                newword = "k" + word[1:]
        return caseFormat(newword,outputcase)

    if mutationstate == 5:
        # mixed mutation
        newword = word
        if word[0] == "b":
            newword = "f" + word[1:]
        if word[0] == "d":
            newword = "t" + word[1:]
        if word[0] == "m":
            newword = "f" + word[1:]
        if (word[0:2] == "go")or(word[0:2] == "gu")or(word[0:3] == "gro")or(word[0:3] == "gru"):
            if trad:
                newword = "wh" + word[1:]
            else:
                newword = "hw" + word[1:]
            return caseFormat(newword,outputcase)
        if word[0:2] == "gw" and trad:
            newword = "wh"+ word[2:]
        else:
            if word[0] == "g":
                if word[0:2] == "gl" or word[0:2] == "gr":
                    pass
                else:
                    newword = "h"+ word[1:]
        return caseFormat(newword,outputcase)

    if mutationstate == 6:
        # the mixed mutation after 'th infixed pronoun
        newword = word
        if word[0] == "b":
            newword = "v" + word[1:]
        if word[0] == "d":
            newword = "t" + word[1:]
        if word[0] == "m":
            newword = "v" + word[1:]        
        # exception for Gorsedh -> An Orsedh
        if (word[0:7] == "gorsedh") or (word[0:7] == "gorseth"):
            newword = word[1:]
            return caseFormat(newword,outputcase)
        if (word[0:2] == "go")or(word[0:2] == "gu")or(word[0:3] == "gro")or(word[0:3] == "gru"):
            newword = "w" + word[1:]
            return caseFormat(newword,outputcase)
        if word[0] == "g":
            if word[0:2] == "gl" or word[0:2] == "gr":
                pass
            else:
                newword = "h" + word[1:]
        if word[0:2] == "gw":
            newword = word[1:]
        return caseFormat(newword,outputcase)

def mutate_cy(word, mutationstate):
    """
    take Welsh word as a str
    and mutationstate as integer 1-3 or 7, 8
    use variable outputcase
    to return word in same capitalisation
    as it went in
    note that non-standard capITALization
    will be turned lower case
    1 = unmutated
    2 = soft mutation
    3 = aspirate mutation
    7 = nasal mutation
    8 = mixed mutation (after negative particle
    Ni - may by written or not, where 
    those letters that undergo aspirate mutation
    do so, and other letters undergo soft mutation)
    """
    outputcase = findOutputCase(word)
    word = word.lower()
    
    if not(isinstance(mutationstate, int)):
        mutationstate = 1
    if mutationstate not in [1, 2, 3, 7, 8]:
        mutationstate = 1

    if mutationstate == 1:
        # unmutated
        return caseFormat(word, outputcase)
    if mutationstate == 2:
        # lentition
        newword = word
        if word[0] == "g":
            newword = word[1:]
        if (word[0] == "b")or(word[0] == "m"):
            newword = "f" + word[1:]
        if word[0] == "c" and word[0:2] != "ch":
            newword = "g" + word[1:]
        if word[0] == "d" and word[0:2] != "dd":
            newword = "d" + word
        if word[0] == "p" and word[0:2] != "ph":
            newword = "b" + word[1:]
        if word[0] == "t" and word[0:2] != "th":
            newword = "d" + word[1:]
        if word[0:2] == "ll":
            newword = word[1:]
        if word[0:2] == "rh":
            newword = "r" + word[2:]
        return caseFormat(newword, outputcase)
    
    if mutationstate == 3:
        # breathed mutation
        newword = word
        if word[0] == "c" and word[0:2] != "ch":
            newword = "ch" + word[1:]
        if word[0] == "p" and word[0:2] != "ph":
            newword = "ph" + word[1:]
        if word[0] == "t" and word[0:2] != "th":
            newword = "th" + word[1:]
        return caseFormat(newword,outputcase)
        
    if mutationstate == 7:
        # nasal mutation
        newword = word
        if word[0] == "c" and word[0:2] != "ch":
            newword = "ngh" + word[1:]
        if word[0] == "p" and word[0:2] != "ph":
            newword = "mh" + word[1:]
        if word[0] == "t" and word[0:2] != "th":
            newword = "nh" + word[1:]
        if word[0:2] == "th":
            newword = "nh" + word[2:]
        if word[0] == "b":
            newword = "m" + word[1:]
        if word[0] == "d" and word[0:2] != "dd":
            newword = "n" + word[1:]
        if word[0] == "g":
            newword = "ng" + word[1:]
            
        return caseFormat(newword,outputcase)
    
    if mutationstate == 8:
        # mixed mutation
        if word[0] in "cpt":
            newword = mutate_cy(word, 3)
        else:
            newword = mutate_cy(word, 2)
        return caseFormat(newword, outputcase)
        
def rev_mutate(word, listmode = False, trad = False):
    """ takes a word and outputs all possible words that could mutate to it 

    By default it will output a dictionary indexed by number 1 to 6, if listmode
    is set to True, it will be a flat list with duplicates removed
    """
    outputcase = findOutputCase(word)
    word = word.lower()
    # we assume the word can be unmutated.
    # generally true, though initial dh- before mutation
    # is rare and limited mainly to compounds of preposition dhe
    unmutated = {1:[word], 2:[], 3:[], 4:[], 5:[], 6:[]}
    if (word[0:2] == "wo")or(word[0:2] == "wu")or(word[0:3] == "wro")or(word[0:3] == "wru"):
        # g->w
        unmutated[2].append("g"+word[1:])
    if (word[0] in "aeilnuwy" or word[0:2] in ["ra", "re", "ri", "ry"] or word[0:6] in ["orsedh", "orseth"])and not(word[0:2] == "wh" and trad):
        unmutated[2].append("g"+word)
    if (word[0] == "v"):
        unmutated[2].append("b" + word[1:])
        unmutated[2].append("m" + word[1:])
    if word[0] == "g":
        if trad and word[1] not in 'einyw':
            unmutated[2].append("c" + word[1:])
        elif trad and word[1] == "w":
            unmutated[2].append("q" + word[1:])
        else:
            unmutated[2].append("k" + word[1:])
    if word[0] == "j":
        if word[0:4] == "jydh":
            unmutated[2].append("d" + word[1:])
        else:
            unmutated[2].append("ch" + word[1:])
    if word[0:2] == "dh":
        unmutated[2].append("d" + word[2:])
    if word[0] == "b":
        unmutated[2].append("p" + word[1:])
    if word[0] == "d" and word[0:2] != "dh":
        unmutated[2].append("t" + word[1:])

    if word[0] == "h":
        if trad and word[1] not in 'einyw':
            unmutated[3].append("c" + word[1:])
        else:
            unmutated[3].append("k" + word[1:])
    if trad and word[0:2] == "wh":
        unmutated[3].append("qw" + word[2:])
    if word[0] == "f":
        unmutated[3].append("p" + word[1:])
    if word[0:2] == "th":
        unmutated[3].append("t" + word[2:])

    if word[0] == "p":
        unmutated[4].append("b" + word[1:])
    if word[0] == "t" and word[0:2] != "th":
        unmutated[4].append("d" + word[1:])
    if word[0] == "k":
        unmutated[4].append("g" + word[1:])
    if trad and word[0] == "c" and word[1] not in 'einyw':
        unmutated[4].append("g" + word[1:])
    if trad and word[0:2] == "qw":
        unmutated[4].append("g" + word[1:])

    if word[0] == "f":
        unmutated[5].append("b" + word[1:])
        unmutated[5].append("m" + word[1:])
    if word[0] == "t" and word[0:2] != "th":
        unmutated[5].append("d" + word[1:])
    if (word[0:3] == "hwo")or(word[0:3] == "hwu")or(word[0:4] == "hwro")or(word[0:4] == "hwru"):
        unmutated[5].append("g" + word[2:])
    if trad and (word[0:3] == "who")or(word[0:3] == "whu")or(word[0:4] == "whro")or(word[0:4] == "whru"):
        unmutated[5].append("g" + word[2:])
    if word[0] == "h":
        unmutated[5].append("g"+ word[1:])
    if trad and word[0:2] == "wh":
        unmutated[5].append("gw"+ word[2:])

    if word[0] == "v":
        unmutated[6].append("b" + word[1:])
        unmutated[6].append("m" + word[1:])        
    if word[0] == "t" and word[0:2] != "th":
        unmutated[6].append("d" + word[1:])
    # exception for Gorsedh -> An Orsedh
    if trad:
        if (word[0:6] in ["orsedh", "orseth"] or (word[0] == "w" and word[1] != "h")):
            unmutated[6].append("g" + word)
    else:
        if (word[0:6] in ["orsedh", "orseth"] or word[0] == "w"):
            unmutated[6].append("g" + word)
    if (word[0:2] == "wo")or(word[0:2] == "wu")or(word[0:3] == "wro")or(word[0:3] == "wru"):
        unmutated[6].append("g" + word[1:])
    if word[0] == "h" and word[1] != "w":
        unmutated[6].append("g" + word[1:])


    unmutatedcasef = {}
    for k in unmutated.keys():
        unmutatedcasef[k] = []
        for w in unmutated[k]:
            outw = caseFormat(w, outputcase)
            unmutatedcasef[k].append(outw)

    if listmode:
        unmutlist = []
        for v in unmutatedcasef.values():
            unmutlist.extend(v)
        unmutlist = list(set(unmutlist))
        unmutlist.sort()
        return unmutlist
    else:
        return unmutatedcasef
    
def format_rev_mutate(revmdict, kw=False, cy=False):
    """ return a formatted output of the reversed mutation dictionary 

    If kw is True, the explanation is in Cornish
    """
    if 7 in revmdict:
        cy = True
    if kw:
        mdesc = {1:"Furv didreylys: ",
                 2:"Treylyans medhel (studh 2) diworth: ",
                 3:"Treylyans hwythsonek (studh 3) diworth: ",
                 4:"Treylyans kales (studh 4) diworth: ",
                 5:"Treylyans kemmyskys (studh 5) diworth: ",
                 6:"Treylyans kemmyskys (wosa raghanow stegys a-ji 'th) diworth: "}
        output = "Y halsa bos an ger:\n\n"
    elif cy:
        mdesc = {1:"Ffurf heb treiglad: ",
                 2:"Treiglad meddal oddi wrth: ",
                 3:"Treiglad llais oddi wrth: ",
                 7:"Treiglad trwynol oddi wrth: "}
        output = "Gall bod y gair:\n\n"
    else:
        mdesc = {1:"Unmutated form: ",
                 2:"Soft mutation (2nd state) of: ",
                 3:"Breathed mutation (3rd state) of: ",
                 4:"Hard mutation (4th state) of: ",
                 5:"Mixed mutation (5th state) of: ",
                 6:"Mixed mutation (after infixed pronoun 'th) of: "}
        output = "The word could be:\n\n"
    # find length of longest explanation string
    # so that the output can be made to line up
    hirder = max(len(v) for k,v in mdesc.items() if len(revmdict[k])>0)
    hirder_r = max(len(" ".join(v)) for v in revmdict.values())
    for k in mdesc.keys():
        if len(revmdict[k]) > 0:
            output += mdesc[k]
            spasow = " "*(hirder-len(mdesc[k])+hirder_r-len(" ".join(revmdict[k])))
            output += spasow
            for r in revmdict[k]:
                output += r 
                output += " "
            output += "\n"
    return output

def rev_mutate_cy(word, listmode = False):
    """ Takes a word and outputs all possible words that could mutate to it
    By default it will output a dictionary indexed by numbers [1, 2, 3, 7],
    if listmode is set to True, it will be a flat list with duplicates
    removed
    """
    outputcase = findOutputCase(word)
    word = word.lower()

    # assume initial mh- nh- ngh- dd- only occur in mutated forms
    # unmutated initial ph- th- are rare but do exist
    unmutated = {1:[], 2:[], 3:[], 7:[]}
    if word[0:3] != "ngh" and word[0:2] not in ["dd", "mh", "nh", "ng"]:
        unmutated[1].append(word)
    # g->0
    if word[0] in "aâeêëiîïloöôruûwŵyŷ" and word[0:2] not in ["rh", "ll"]:
        unmutated[2].append("g"+word)
    if word[0] == "f" and word[0:2] != "ff":
        unmutated[2].append("b" + word[1:])
        unmutated[2].append("m" + word[1:])
    if word[0] == "g":
        unmutated[2].append("c" + word[1:])
    if word[0:2] == "dd":
        unmutated[2].append("d" + word[2:])
    if word[0] == "b":
        unmutated[2].append("p" + word[1:])
    if word[0] == "d" and word[0:2] != "dd":
        unmutated[2].append("t" + word[1:])
    if word[0] == "l" and word[0:2] != "ll":
        unmutated[2].append("ll" + word[1:])
    if word[0] == "r" and word[0:2] != "rh":
        unmutated[2].append("rh" + word[1:])
    
    if word[0:2] == "ch":
        unmutated[3].append("c"+word[2:])
    if word[0:2] == "ph":
        unmutated[3].append("p"+word[2:])
    if word[0:2] == "th":
        unmutated[3].append("t"+word[2:])
    
    if word[0:3] == "ngh":
        unmutated[7].append("c"+word[3:])
    if word[0:2] == "mh":
        unmutated[7].append("p"+word[2:])
    if word[0:2] == "ng" and word[0:3] != "ngh":
        unmutated[7].append("g"+word[2:])
    if word[0:2] == "nh":
        unmutated[7].append("t"+word[2:])
    if word[0] == "m" and word[0:2] != "mh":
        unmutated[7].append("b"+word[1:])
    if word[0] == "n" and word[0:2] not in ["ng", "nh"]:
        unmutated[7].append("d"+word[1:])
    
    unmutatedcasef = {}
    for k in unmutated.keys():
        unmutatedcasef[k] = []
        for w in unmutated[k]:
            outw = caseFormat(w, outputcase)
            unmutatedcasef[k].append(outw)

    if listmode:
        unmutlist = []
        for v in unmutatedcasef.values():
            unmutlist.extend(v)
        unmutlist = list(set(unmutlist))
        unmutlist.sort()
        return unmutlist
    else:
        return unmutatedcasef

def basicTests():
    """test code - doesn't do all cases"""
    
    kath = "kath"
    kath2 = "Kath"
    kath3 = "KATH"
    kath4 = "kaTH"
    gwari = "gwari"
    expl = {1:"No Mutation", 2:"Soft Mutation\nvarious causes e.g. fem. sing. nouns after article, A verbal particle", 3:"Breathed Mutation\ne.g. after 'ow' possessive pronoun = E. 'my'",4:"Hard Mutation\ne.g. after present participle 'ow'", 5:"Mixed Mutation\ne.g. after Y verbal particle", 6:"Mixed mutation after 'th (infixed pronoun 2p sing.)"}
    underline = "-"*30
    print(underline+"\n")
    for s in range(6):
        print(expl[s+1]+'\n')
        print("mutate('{w}',{m}) = {r}".format(w=kath,m=s+1, r=mutate(kath,s+1)))
        print("mutate('{w}',{m}) = {r}".format(w=kath2,m=s+1, r=mutate(kath2,s+1)))
        print("mutate('{w}',{m}) = {r}".format(w=kath3,m=s+1, r=mutate(kath3,s+1)))
        print("mutate('{w}',{m}) = {r}".format(w=kath4,m=s+1, r=mutate(kath4,s+1)))
        print("\nmutate('{w}',{m}) = {r}\n".format(w=gwari,m=s+1, r=mutate(gwari,s+1)))
        print(underline+"\n")
               
    print("note - doesn't preserve capitalisation of non-standard capiTALISed input")

def basicTests_cy():
    """test code - doesn't do all cases"""
    
    kath = "cath"
    kath2 = "Cath"
    kath3 = "CATH"
    kath4 = "caTH"
    gwari = "gwari"
    pen = "pen"
    tad = "tad"
    beic = "beic"
    draig = "draig"
    llan = "llan50goch"
    mor = "môr"
    rhwyfo = "rhwyfo"
    prynu = "prynais"
    gwerthu = "gwerthais"
    
    expl = {1:"No Mutation", 2:"Soft Mutation\nvarious causes e.g. fem. sing. nouns after article, dy 'you' sg. poss. pron.", 3:"Breathed Mutation\ne.g. after 'a' and",7:"Nasal mutation\ne.g. after fy 'my' or yn 'in'"}
    underline = "-"*30
    print(underline+"\n")
    for s in [1,2,3,7]:
        print(expl[s]+'\n')
        print("mutate('{w}',{m}) = {r}".format(w=kath,m=s, r=mutate_cy(kath,s)))
        print("mutate('{w}',{m}) = {r}".format(w=kath2,m=s, r=mutate_cy(kath2,s)))
        print("mutate('{w}',{m}) = {r}".format(w=kath3,m=s, r=mutate_cy(kath3,s)))
        print("mutate('{w}',{m}) = {r}".format(w=kath4,m=s, r=mutate_cy(kath4,s)))
        print("\nmutate('{w}',{m}) = {r}".format(w=gwari,m=s, r=mutate_cy(gwari,s)))
        print("\nmutate('{w}',{m}) = {r}".format(w=pen,m=s, r=mutate_cy(pen,s)))
        print("\nmutate('{w}',{m}) = {r}".format(w=tad,m=s, r=mutate_cy(tad,s)))
        print("\nmutate('{w}',{m}) = {r}".format(w=beic,m=s, r=mutate_cy(beic,s)))
        print("\nmutate('{w}',{m}) = {r}".format(w=draig,m=s, r=mutate_cy(draig,s)))
        print("\nmutate('{w}',{m}) = {r}".format(w=llan,m=s, r=mutate_cy(llan,s)))
        print("\nmutate('{w}',{m}) = {r}".format(w=mor,m=s, r=mutate_cy(mor,s)))
        print("\nmutate('{w}',{m}) = {r}\n".format(w=rhwyfo,m=s, r=mutate_cy(rhwyfo,s)))
        
        print(underline+"\n")
    print("Mixed mutation\nafter Ni negative particle, which is not always actually written/spoken but mutation remains.")
    print("mutate('{w}', {m}) = {r}\n".format(w=gwerthu, m=8, r = mutate_cy(gwerthu, 8)))
    print("mutate('{w}', {m}) = {r}\n".format(w=prynu, m=8, r = mutate_cy(prynu, 8)))
    
    print("note - doesn't preserve capitalisation of non-standard capiTALISed input")

    
def reverseTests():
    """ test reverse mutation """
    print("main form")
    print(rev_mutate("gath"))
    print(rev_mutate("hath"))
    print(rev_mutate("voes"))
    print(rev_mutate("fos"))
    print(rev_mutate("den"))
    print(rev_mutate("dhen"))
    print(rev_mutate("tas"))
    print(rev_mutate("thas"))
    print(rev_mutate("weli"))
    print(rev_mutate("kwari"))
    print(rev_mutate("hwari"))
    print(rev_mutate("whari"))
    print(rev_mutate("gweth"))
    print(rev_mutate("jydh"))
    print(rev_mutate("japel"))
    print(rev_mutate("kara"))
    print(rev_mutate("cara"))
    print("trad form")
    print(rev_mutate("gath", False, True))
    print(rev_mutate("hath", False, True))
    print(rev_mutate("voes", False, True))
    print(rev_mutate("fos", False, True))
    print(rev_mutate("den", False, True))
    print(rev_mutate("dhen", False, True))
    print(rev_mutate("tas", False, True))
    print(rev_mutate("thas", False, True))
    print(rev_mutate("weli", False, True))
    print(rev_mutate("kwari", False, True))
    print(rev_mutate("hwari", False, True))
    print(rev_mutate("whari", False, True))
    print(rev_mutate("gweth", False, True))
    print(rev_mutate("jydh", False, True)) 
    print(rev_mutate("japel", False, True))
    print(rev_mutate("kara", False, True))
    print(rev_mutate("cara", False, True))

def reverseTests_cy():
    p = rev_mutate_cy("bren")
    t = rev_mutate_cy("dad")
    g = rev_mutate_cy("gam")
    f = rev_mutate_cy("faich")
    dd = rev_mutate_cy("ddyn")
    g2 = rev_mutate_cy("air")
    ll = rev_mutate_cy("lais")
    rh = rev_mutate_cy("res")
    mh = rev_mutate_cy("mhren")
    nh = rev_mutate_cy("nhad")
    ngh= rev_mutate_cy("ngham")
    m = rev_mutate_cy("maich")
    n = rev_mutate_cy("nyn")
    ng = rev_mutate_cy("ngŵr")
    ph = rev_mutate_cy("phren")
    th = rev_mutate_cy("thad")
    ch = rev_mutate_cy("cham")
    print(format_rev_mutate(p))
    print(format_rev_mutate(t))
    print(format_rev_mutate(g))
    print(format_rev_mutate(f))
    print(format_rev_mutate(dd))
    print(format_rev_mutate(g2))
    print(format_rev_mutate(ll))
    print(format_rev_mutate(rh))
    print(format_rev_mutate(mh))
    print(format_rev_mutate(nh))
    print(format_rev_mutate(ngh))
    print(format_rev_mutate(m))
    print(format_rev_mutate(n))
    print(format_rev_mutate(ng))
    print(format_rev_mutate(ph))
    print(format_rev_mutate(th))
    print(format_rev_mutate(ch))


if __name__ == "__main__":
    basicTests()
    reverseTests()


    
