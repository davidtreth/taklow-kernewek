# David Trethewey revised 26-08-2015
# This doesn't actually determine whether
# a word should mutate
#
# all it does is take a word and mutation state 
# from 1 to 6
# and return the mutated form
#
# 1 = no mutation
# 2 = soft mutation k-->g, p-->b etc.
# 3 = breathed mutation p->f k->h t->th
# 4 = hard mutation g->k d->t b->p
# 5 = mixed I
# 6 = mixed II after 'th
#
# it will try to return it in the same case
# i.e. lower, UPPER, or Title

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

def mutate(word,mutationstate):
    # take word as a str 
    # and mutationstate as integer from 1-6
    # use variable outputcase
    # to return word in same capitalisation
    # as it went in
    # note that non-standard capITALization
    # will be turned lower case
    outputcase = 'lower' # default
    if word.islower():
        outputcase = 'lower'
    if word.istitle():
        word = word.lower()
        outputcase = 'title'
    if word.isupper():
        word = word.lower()
        outputcase = 'upper'

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
        if word[0:2] == "ch":
            newword = "j" + word[2:]
        if word[0] == "d":
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
            newword = "hw" + word[1:]
            return caseFormat(newword,outputcase)
        if word[0] == "g":
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
            newword = "h" + word[1:]
        if (word[0:2] == "gw"):
            newword = word[1:]
        return caseFormat(newword,outputcase)

def basicTests():
    """test code - doesn't do all cases"""
    
    kath = "kath"
    kath2 = "Kath"
    kath3 = "KATH"
    kath4 = "kaTH"
    gwari = "gwari"
    expl = {1:"No Mutation", 2:"Soft Mutation\nvarious causes e.g. fem. sing. nuns after article, A verbal particle", 3:"Breathed Mutation\ne.g. after 'ow' possessive pronoun = E. 'my'",4:"Hard Mutation\ne.g. after present participle 'ow'", 5:"Mixed Mutation\ne.g. after Y verbal particle", 6:"Mixed mutation after 'th (infixed pronoun 2p sing.)"}
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

    
if __name__ == "__main__":
    basicTests()


    
