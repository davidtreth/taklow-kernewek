import random
import string
import keskows5_word
import keskows5_readwords
from keskows5_createword import get_input
import argparse

#questionwords = ["py", "piw"]
questionwords = ["piw"]
questionwords_e = ["who"]
question_bos = ["yw"]
question_bos_e = ["is"]
#question_bos = ["yw","eus"]
pronouns = ["my","ty","ev","hi","ni","hwi","i"]
pronouns_e = ["I","you","he","she","we","you","they"]
pronouns_suffixed = ["vy", "jy", "ev","hi","ni","hwi","i"]
pronouns_suffixed_e = ["I", "you", "he","she","we","you","they"]
pronouns_possessive = ["ow","dha","y","hy","agan","agas","aga"]
pronouns_possessive_e = ["my","your","his","her","our","your","their"]
relativepronouns = ["nep","hag",""]
relativepronouns_e = ["who","that","that"]
prepositions = ["yn","gans","heb","war","yn-dann"]
prepositions_e = ["in","with","without","on","under"]

article = ["an"]
article_e = ["the"]
specifiers = ["ma","na"]
specifiers_e = ["this","that"]
numerals = ["unn","dew","tri","peswar","pymp","hwegh","seyth","eth","naw","deg","unnek","dewdhek","trydhek","peswardhek","pympthek","hwetek","seytek","etek","nownsek","ugens"]
numerals_e = ["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty"]

# load in the vocabulary

food = keskows5_readwords.food
food_g = keskows5_readwords.food_g
food_v = keskows5_readwords.food_v
food_a = keskows5_readwords.food_a
food_n_e = keskows5_readwords.food_n_e
food_a_e = keskows5_readwords.food_a_e
food_v_e = keskows5_readwords.food_v_e


veg = keskows5_readwords.veg
veg_g = keskows5_readwords.veg_g
veg_v = keskows5_readwords.veg_v
veg_a = keskows5_readwords.veg_a
veg_n_e = keskows5_readwords.veg_n_e
veg_a_e = keskows5_readwords.veg_a_e
veg_v_e = keskows5_readwords.veg_v_e


meat = keskows5_readwords.meat
meat_g = keskows5_readwords.meat_g
meat_v = keskows5_readwords.meat_v
meat_a = keskows5_readwords.meat_a
meat_n_e = keskows5_readwords.meat_n_e
meat_a_e = keskows5_readwords.meat_a_e
meat_v_e = keskows5_readwords.meat_v_e


drink = keskows5_readwords.drink
drink_g = keskows5_readwords.drink_g
drink_v = keskows5_readwords.drink_v
drink_a = keskows5_readwords.drink_a
drink_n_e = keskows5_readwords.drink_n_e
drink_a_e = keskows5_readwords.drink_a_e
drink_v_e = keskows5_readwords.drink_v_e

buildings = keskows5_readwords.buildings
buildings_g = keskows5_readwords.buildings_g
buildings_v = keskows5_readwords.buildings_v
buildings_a = keskows5_readwords.buildings_a
buildings_n_e = keskows5_readwords.buildings_n_e
buildings_a_e = keskows5_readwords.buildings_a_e
buildings_v_e = keskows5_readwords.buildings_v_e

animals = keskows5_readwords.animals
animals_g = keskows5_readwords.animals_g
animals_v = keskows5_readwords.animals_v
animals_a = keskows5_readwords.animals_a
animals_n_e = keskows5_readwords.animals_n_e
animals_a_e = keskows5_readwords.animals_a_e
animals_v_e = keskows5_readwords.animals_v_e

people = keskows5_readwords.people
people_g = keskows5_readwords.people_g
people_v = keskows5_readwords.people_v
people_a = keskows5_readwords.people_a
people_n_e = keskows5_readwords.people_n_e
people_a_e = keskows5_readwords.people_a_e
people_v_e = keskows5_readwords.people_v_e

transport1 =keskows5_readwords.transport1 # lywya
transport1_g =keskows5_readwords.transport1_g 
transport1_v = keskows5_readwords.transport1_v
transport1_a = keskows5_readwords.transport1_a
transport1_n_e = keskows5_readwords.transport1_n_e
transport1_a_e = keskows5_readwords.transport1_a_e
transport1_v_e = keskows5_readwords.transport1_v_e

transport2 = keskows5_readwords.transport2#marghogeth
transport2_g = keskows5_readwords.transport2_g
transport2_v = keskows5_readwords.transport2_v
transport2_a = keskows5_readwords.transport2_a
transport2_n_e = keskows5_readwords.transport2_n_e
transport2_a_e = keskows5_readwords.transport2_a_e
transport2_v_e = keskows5_readwords.transport2_v_e

readable = keskows5_readwords.readable
readable_g = keskows5_readwords.readable_g
readable_v = keskows5_readwords.readable_v
readable_a = keskows5_readwords.readable_a
readable_n_e = keskows5_readwords.readable_n_e
readable_a_e = keskows5_readwords.readable_a_e
readable_v_e = keskows5_readwords.readable_v_e


verbs = [food_v,veg_v,meat_v,drink_v,buildings_v,animals_v,people_v,transport1_v,transport2_v,readable_v]
nouns = [food,veg,meat,drink,buildings,animals,people,transport1,transport2,readable]
adjectives = [food_a,veg_a,meat_a,drink_a,buildings_a,animals_a,people_a,transport1_a,transport2_a,readable_a]
genders = [food_g,veg_g,meat_g,drink_g,buildings_g,animals_g,people_g,transport1_g,transport2_g,readable_g]
nouns_e = [food_n_e,veg_n_e,meat_n_e,drink_n_e,buildings_n_e,animals_n_e,people_n_e,transport1_n_e,transport2_n_e,readable_n_e]
verbs_e = [food_v_e,veg_v_e,meat_v_e,drink_v_e,buildings_v_e,animals_v_e,people_v_e,transport1_v_e,transport2_v_e,readable_v_e]
adj_e = [food_a_e,veg_a_e,meat_a_e,drink_a_e,buildings_a_e,animals_a_e,people_a_e,transport1_a_e,transport2_a_e,readable_a_e]
aux = ["gul","mynnes","galloes"]
aux_e = ["do","want","can"]

negative = ["ny","na"]
negative_e = ["not","not"]
interrogative = ["a"]
interrogative_e = ["do"]

mutationstate = 1
topic = 0
animalsubject = 0

verbs_animalsubject = keskows5_readwords.verbs_animalsubject
verbs_animalsubject_e = keskows5_readwords.verbs_animalsubject_e

def chooseatrandom(list):
    a = int(random.random()*len(list))
    return list[a]
def chooseatrandom2(list):
    a = int(random.random()*len(list))
    return a

def inflect(verb,person,tense,suffix_pro):
    ''' Should really be rewritten to use the inflektya.py module '''
    if verb == "gul":
        if tense =="present":
            verbinfs = ["gwrav","gwredh","gwra","gwra","gwren","gwrewgh","gwrons"]
        if tense =="preterite":
            verbinfs = ["gwrug","gwrussys","gwrug","gwrug","gwrussyn","gwrussowgh","gwrussons"]
        if tense =="imperfect":
            verbinfs = ["gwren","gwres","gwre","gwre","gwren","gwrewgh","gwrens"]
        if suffix_pro == True:
            return verbinfs[person-1] + " "+pronouns_suffixed[person-1]
        if suffix_pro == False:
            return verbinfs[person-1]
    if (verb == "kara"):
        if (person == 2)or(person == 5)or(person == 6):
            verb = "kera"
    if (verb == "eva")and(tense=="present"):
        if (person ==3)or(person==4):
            verb = "yva"
    if (verb == "dybri"):
        if (person ==3)or(person==4):
            verb = "debera"
    if (verb == "galloes")and(tense=="present"):
        if person != 1:
            verb = "gylloes"
    if (verb == "galloes")and(tense=="preterite"):
        if ((person < 3)or(person>5))and(person!=7):
            verb = "gylloes"
    if (verb == "galloes")and(tense=="imperfect"):
        verb = "gylloes"
    if tense == "present":
        endings = ["av","ydh","","","yn","owgh","ons"]
    if tense == "preterite":
        endings = ["is","sys","as","as","syn","sowgh","sons"]
    if tense == "imperfect":
        endings = ["en","es","a","a","en","ewgh","ens"]
    if suffix_pro == True:
        if (verb[-1] in "aeiouy")and(verb[-2:]!="ya"):
            return verb[:-1] + endings[person-1]+" "+pronouns_suffixed[person-1]
        if verb[-3:]=="aya":
            return verb[:-1] + endings[person-1]+" "+pronouns_suffixed[person-1]
        if verb[-2:]=="ya":
            if ("y" in endings[person-1])or("i" in endings[person-1])or("s"in endings[person-1]):
                return verb[:-2] + endings[person-1]+" "+pronouns_suffixed[person-1]
            else:
                return verb[:-1] + endings[person-1]+" "+pronouns_suffixed[person-1]
        if (verb[-2] in "aeiouy")and(not(verb[-3] in "aeiouy")):
            return verb[:-2] + endings[person-1]+" "+pronouns_suffixed[person-1]
        if verb[-3] in "aeiouy":
            return verb[:-3] + endings[person-1]+" "+pronouns_suffixed[person-1]
    if suffix_pro ==False:
        if (verb[-1] in "aeiouy")and(verb[-2:]!="ya"):
            return verb[:-1] + endings[person-1]
        if verb[-3:]=="aya":
            return verb[:-1] + endings[person-1]
        if verb[-2:]=="ya":
            if ("y" in endings[person-1])or("i" in endings[person-1])or("s"in endings[person-1]):
                return verb[:-2] + endings[person-1]
            else:
                return verb[:-1] + endings[person-1]
        if (verb[-2] in "aeiouy")and(not(verb[-3] in "aeiouy")):
            return verb[:-2] + endings[person-1]
        if verb[-3] in "aeiouy":
            return verb[:-3] + endings[person-1]      


def inflect_e(verb,person,tense,suffix_pro):
        if verb == "make":
            if tense =="present":
                verbinfs = ["make","make","makes","makes","make","make","make"]
            if tense =="preterite":
                verbinfs = ["made","made","made","made","made","made","made"]
            if tense =="imperfect":
                verbinfs = ["used to make","used to make","used to make","used to make","used to make","used to make","used to make"]
            if suffix_pro == True:
                return pronouns_e[person-1] + " " + verbinfs[person-1] 
            return verbinfs[person-1]
	if verb == "can":
           if tense =="present":
                verbinfs = ["can","can","can","can","can","can","can"]
           if tense =="preterite":
                verbinfs = ["could","could","could","could","could","could","could"]
           if tense =="imperfect":
                verbinfs = ["used to be able to","used to be able to","used to be able to","used to be able to","used to be able to","used to be able to","used to be able to"]
           if suffix_pro == True:
                return pronouns_e[person-1] + " " + verbinfs[person-1] 
           return verbinfs[person-1]

	if verb == "do":
           if tense =="present":
                verbinfs = ["do","do","does","does","do","do","do"]
           if tense =="preterite":
                verbinfs = ["did","did","did","did","did","did","did"]
           if tense =="imperfect":
                verbinfs = ["used to do","used to do","used to do","used to do","used to do","used to do","used to do"]
           if suffix_pro == True:
                return pronouns_e[person-1] + " " + verbinfs[person-1] 
           return verbinfs[person-1] 

        if tense == "present":
            endings = ["","","s","s","","",""]
        if tense == "preterite":
            endings = ["ed","ed","ed","ed","ed","ed","ed"]
            if verb[-1] in "aeiou":
                endings = ["d","d","d","d","d","d","d"]
        if tense == "imperfect":
            endings = ["","","","","","",""]
        if verb == "want":
            if suffix_pro == True:
                if tense == "imperfect":
                   return pronouns_e[person-1]+" used to "+verb+endings[person-1]+ " to "
                return pronouns_e[person-1] + " " + verb + endings[person-1] + " to "
	   
            if suffix_pro == False:
               if tense == "imperfect":
                   return "used to "+verb+endings[person-1]+" to "
               return verb + endings[person-1] + " to "


        if verb == "see":
	   if tense == "preterite":
	      verb = "saw"
	      endings = ["","","","","","",""]

 	if verb == "buy":
	   if tense == "preterite":
	      verb = "bought"
	      endings = ["","","","","","",""]

 	if verb == "eat":
           if tense =="preterite":
                verb = "ate"
                endings = ["","","","","","",""]

  	if verb == "drink":
           if tense =="preterite":
                verb = "drank"
                endings = ["","","","","","",""]
  	if verb == "build":
           if tense =="preterite":
                verb = "built"
                endings = ["","","","","","",""]
  	if verb == "drive":
           if tense =="preterite":
                verb = "drove"
                endings = ["","","","","","",""]
        if verb == "write":
	   if tense == "preterite":
	      verb = "wrote"
	      endings = ["","","","","","",""]

        if suffix_pro == False:
            if tense == "imperfect":
                return "used to "+verb+endings[person-1] 
            return verb + endings[person-1]
        if suffix_pro == True: 
            if tense == "imperfect":
                return pronouns_e[person-1]+" used to "+verb+endings[person-1]
            return pronouns_e[person-1] + " " + verb + endings[person-1]

def mutate(word):
    ''' Should really be rewritten to use mutatya.py module '''
    global mutationstate
    if mutationstate ==1:
        return word
    if mutationstate ==2:
        newword = word
        if (word[0] == "b")or(word[0] == "m"):
            newword = "v"+word[1:]
        if word[0] == "k":
            newword = "g"+word[1:]
        if word[0:2] == "ch":
            newword = "j"+word[2:]
        if word[0] == "d":
            newword = "dh" + word[1:]
        if (word[0:2] == "go")or(word[0:2] == "gu")or(word[0:3] == "gro")or(word[0:3]=="gru"):
            newword = "w" + word[1:]
            return newword
        if word[0] == "g":
            newword = word[1:]
        if word[0] == "p":
            newword = "b"+word[1:]
        if word[0] == "t":
            newword = "d"+word[1:]
        return newword
    if mutationstate == 3:
        newword = word
        if word[0] == "k":
            newword = "h"+word[1:]
        if word[0] == "p":
            newword = "f"+word[1:]
        if word[0] == "t":
            newword = "th"+word[1:]
        return newword
    if mutationstate == 4:
        newword = word
        if word[0] == "b":
            newword = "p"+word[1:]
        if word[0] == "d":
            newword = "t"+word[1:]
        if word[0] == "g":
            newword = "k"+word[1:]
        return newword
    if mutationstate ==5:
        newword = word
        if word[0] == "b":
            newword = "f"+word[1:]
        if word[0] == "d":
            newword = "t"+word[1:]
        if word[0] == "m":
            newword = "f"+word[1:]
        if (word[0:2] == "go")or(word[0:2] == "gu")or(word[0:3] == "gro")or(word[0:3]=="gru"):
            newword = "hw" + word[1:]
            return newword
        if word[0] == "g":
            newword = "h"+word[1:]
        return newword

# again, comparative and superlative functions should 
# exist in a separate module

def make_comparative(adj):
    comp = ""
    if adj == "drog":
        comp = "gweth"
        return comp
    if adj == "da":
        comp = "gwell"
        return comp
    if adj == "byghan":
        comp = "le"
        return comp

    if (adj[-2:]=="th")or(adj[-2:]=="dh"):
        comp = adj[:-2]+"ttha"
        return comp

    if (adj[-1] == "v")and(adj[-2] in "aeiouy"):
        comp = adj[:-1]+"ffa"
        return comp
    if (adj[-1] == "g")and(adj[-2] in "aeiouy"):
        comp = adj[:-1]+"kka"
        return comp    
    if (not(adj[-1] in "aeiouy"))and(adj[-2] in "aeiouy"):
        comp = adj + adj[-1]+"a"
        return comp
    if (not(adj[-1] in "aeiouy"))and(not(adj[-2] in "aeiouy")):
        comp = adj +"a"
        return comp
    if comp == "": 
        print("adjective {a} fails to make comparative".format(a=adj)) 
        pause = get_input("pause")

def make_comparative_e(adj):
    comp = ""
    comp = adj + "er"
    if adj == "good":
       comp = "better"
    if adj == "bad":
       comp = "worse"
    return comp

def make_superlative(adj):
    if adj == "drog":
        supr = "an gwettha"
        return supr
    if adj == "da":
        supr = "an gwella"
        return supr
    if adj == "byghan":
        supr = "an lyha"
        return supr
    supr = "an "+make_comparative(adj)
    return supr

def make_superlative_e(adj):
    supr = "the " + adj + "est"
    if adj == "good":
        supr = "the best"	
    if adj == "bad":
        supr = "the worst"
    return supr

def gen_sentence(structure,js,topics,a_s,epls,persons):
    global topic
    global animalsubject
    global tense
    global mutationstate
    global eng_plural
    global person_3ps
    tenses = ["present","preterite","imperfect"]
    tense = tenses[int(random.random()*len(tenses))]
    sentence = ""
    sentence_e = ""			
    mutationstate = 1
    eng_plural = 0
    person_3ps = -1
    if (structure[:2]=="tn")or(structure[:2]=="Pn"):
        topiclist = [5,6]
        topic = topiclist[int(random.random()*len(topiclist))]
        if topic ==5:
            animalsubject = 1 
    firstelement = True
    # adjust Cornish sentence structure to produce better English
    # for the translation
    structure_e = structure[:]
    js_e = js[:]
    topics_e = topics[:]
    a_s_e = a_s[:]
    epls_e = epls[:]
    persons_e = persons[:]
    if ("na" in structure_e)and(structure_e[0] !="q")and(structure_e[0:3] != "INq"):
        s1,s2 = structure_e.split("na")
	structure_e = s1 + "an" + s2
        js_e = js[:len(s1)]+[js[len(s1)+1]]+[js[len(s1)]]+js[-1*len(s2):]
    	topics_e = topics[:len(s1)]+[topics[len(s1)+1]]+[topics[len(s1)]]+topics[-1*len(s2):]
    	a_s_e = a_s[:len(s1)]+[a_s[len(s1)+1]]+[a_s[len(s1)]]+a_s[-1*len(s2):]
    	epls_e = epls[:len(s1)]+[epls[len(s1)+1]]+[epls[len(s1)]]+epls[-1*len(s2):]
    	persons_e = persons[:len(s1)]+[persons[len(s1)+1]]+[persons[len(s1)]]+persons[-1*len(s2):]
    if ("nc" in structure_e)and(structure_e[0] !="q")and(structure_e[0:3] != "INq"):
        s1,s2 = structure_e.split("nc")
	structure_e = s1 + "cn" + s2
        js_e = js[:len(s1)]+[js[len(s1)+1]]+[js[len(s1)]]+js[-1*len(s2):]
    	topics_e = topics[:len(s1)]+[topics[len(s1)+1]]+[topics[len(s1)]]+topics[-1*len(s2):]
    	a_s_e = a_s[:len(s1)]+[a_s[len(s1)+1]]+[a_s[len(s1)]]+a_s[-1*len(s2):]
    	epls_e = epls[:len(s1)]+[epls[len(s1)+1]]+[epls[len(s1)]]+epls[-1*len(s2):]
    	persons_e = persons[:len(s1)]+[persons[len(s1)+1]]+[persons[len(s1)]]+persons[-1*len(s2):]
    if ("ns" in structure_e)and(structure_e[0] !="q")and(structure_e[0:3] != "INq"):
        s1,s2 = structure_e.split("ns")
	structure_e = s1 + "sn" + s2
        js_e = js[:len(s1)]+[js[len(s1)+1]]+[js[len(s1)]]+js[-1*len(s2):]
    	topics_e = topics[:len(s1)]+[topics[len(s1)+1]]+[topics[len(s1)]]+topics[-1*len(s2):]
    	a_s_e = a_s[:len(s1)]+[a_s[len(s1)+1]]+[a_s[len(s1)]]+a_s[-1*len(s2):]
    	epls_e = epls[:len(s1)]+[epls[len(s1)+1]]+[epls[len(s1)]]+epls[-1*len(s2):]
    	persons_e = persons[:len(s1)]+[persons[len(s1)+1]]+[persons[len(s1)]]+persons[-1*len(s2):]
    if ("tne" in structure_e):
        s1,s2 = structure_e.split("tne")
	structure_e = s1 + "enL" + s2        
        js_e = js[:len(s1)]+[js[len(s1)+2]]+[js[len(s1)+1]]+[0]+js[-1*len(s2):]
    	topics_e = topics[:len(s1)]+[topics[len(s1)+2]]+[topics[len(s1)+1]]+[0]+topics[-1*len(s2):]
    	a_s_e = a_s[:len(s1)]+[a_s[len(s1)+2]]+[a_s[len(s1)-1]]+[0]+a_s[-1*len(s2):]
    	epls_e = epls[:len(s1)]+[epls[len(s1)+2]]+[epls[len(s1)-1]]+[0]+epls[-1*len(s2):]
    	persons_e = persons[:len(s1)]+[persons[len(s1)+2]]+[persons[len(s1)-1]]+[0]+persons[-1*len(s2):]
#	print structure_e
#	print js,js_e
#	print topics,topics_e
#    print epls_e

    for s in range(len(structure)):
    	j = js[s]
	j_e = js_e[s]
	t = topics[s]
	t_e = topics_e[s]
	a = a_s[s]
	a_e = a_s_e[s]
	ep = epls[s]
	ep_e = epls_e[s]
	per = persons[s]
	per_e = persons_e[s]
        w,w_e = gen_elements(structure[s],structure_e[s],j,t,a,ep,per,j_e,t_e,a_e,ep_e,per_e)
        if firstelement == True:
            w = string.capitalize(w)
	    w_e = string.capitalize(w_e)
            if (structure[s] != "!")and(structure[s]!="@"):
                firstelement = False
        sentence = sentence + w + " "
        sentence_e = sentence_e + w_e + " "
    if structure[s] != "?":
          sentence =  sentence[:-1] + "."
          sentence_e =  sentence_e[:-1] + "."	
    else:
          sentence =  sentence[:-1]
          sentence_e =  sentence_e[:-1]
    # do some common contractions and changes
    # before a vowel
    # by string.replace()
    if " yn an" in sentence:
        sentence = string.replace(sentence," yn an"," y'n")
    if "vynnydh jy" in sentence:
        sentence = string.replace(sentence,"vynnydh jy","vynn'ta")
    while ("  " in sentence):
        sentence = string.replace(sentence,"  "," ")

    while ("  " in sentence_e):
            sentence_e = string.replace(sentence_e,"  "," ")
    if "ny yw" in sentence:
        sentence = string.replace(sentence,"ny yw","nyns yw")
    if "py a" in sentence:
        sentence = string.replace(sentence,"py a","pyth a")
	
    if "Do not is" in sentence_e:
        sentence_e = string.replace(sentence_e,"Do not is","Isn't")
    if sentence[-2:]==" ?":
        sentence = sentence[:-2]+"?"
    if sentence_e[-2:]==" ?":
        sentence_e = sentence_e[:-2]+"?"
    if sentence[0] == " ":
        sentence = sentence[1:]
    if sentence_e[0] == " ":
        sentence_e = sentence_e[1:]
    # return sentence + " - " + sentence_e
    return sentence , sentence_e


def gen_js(structure):
    global topic	
    global animalsubject
    global tense
    global mutationstate
    global eng_plural
    global person_3ps
    global person
    tenses = ["present","preterite","imperfect"]
    tense = tenses[int(random.random()*len(tenses))]
    sentence = ""
    sentence_e = ""			
    mutationstate = 1
    eng_plural = 0
    person_3ps = -1        
    person = 0
    js = []
    topics = []
    a_s = []
    epls = []
    pers = []
    for s in range(len(structure)):
        j,t,a,ep,per = gen_j(structure[s])
	js.append(j)
	topics.append(t)
	a_s.append(a)
	epls.append(ep)
	pers.append(per)
    return js,topics,a_s,epls,pers


def gen_j(element):
    global mutationstate
    global topic
    global animalsubject
    global tense
    global eng_plural
    global person_3ps
    global person
    if element == "L": #null element
       	j = 0
	return j,topic,animalsubject,eng_plural,person
    if element == "Q":
        j = chooseatrandom2(questionwords)
	person_3ps = 3
        return j,topic,animalsubject,eng_plural,person
    if element == "q":
        j = chooseatrandom2(question_bos)
        return j,topic,animalsubject,eng_plural,person
    if element == "p":
        j = chooseatrandom2(pronouns)
	person_3ps = j+1
        return j,topic,animalsubject,eng_plural,person
    if element == "P":
        j = chooseatrandom2(pronouns_possessive)
        return j,topic,animalsubject,eng_plural,person

    if element == "r":
        j = chooseatrandom2(prepositions)
        topic = int(random.random()*10)
        w = prepositions[j]
        if w =="yn":
            topiclist = [0,4,7,9] 
            topic = topiclist[int(random.random()*len(topiclist))]
        if w == "yn-dann":
            topiclist = [1,2,4,7,8,9]
            topic = topiclist[int(random.random()*len(topiclist))]
        if w == "war":
            topiclist = [0,1,2,4,7,8,9]
            topic = topiclist[int(random.random()*len(topiclist))]
        return j,topic,animalsubject,eng_plural,person
    if element == "a":
        j = chooseatrandom2(adjectives[topic])
        return j,topic,animalsubject,eng_plural,person

    if element == "c":
        j = chooseatrandom2(adjectives[topic])
        return j,topic,animalsubject,eng_plural,person
    if element == "s":
        j = chooseatrandom2(adjectives[topic])
        return j,topic,animalsubject,eng_plural,person
    if element == "n":
        j =  chooseatrandom2(nouns[topic])
	person_3ps = 3
        e = eng_plural
        eng_plural = 0
        return j,topic,animalsubject,e,person
    if element == "t":
        j = 0
        return j,topic,animalsubject,eng_plural,person
    if element == "e":
        j =  chooseatrandom2(specifiers)
        return j,topic,animalsubject,eng_plural,person
    if element == "v":
        if animalsubject ==0:
            j = chooseatrandom2(verbs[topic])
        else:
            verbs_to_use = []
            verbs_to_use_e = []
            for v in verbs[topic]:
                if v in verbs_animalsubject:
                    verbs_to_use.append(v)
            for v in verbs_e[topic]:
                if v in verbs_animalsubject_e:
                    verbs_to_use_e.append(v)
            j = chooseatrandom2(verbs_to_use)
        return j,topic,animalsubject,eng_plural,person

    if element == "x":
        j = chooseatrandom2(aux)
        return j,topic,animalsubject,eng_plural,person

    if element == "i":
        if animalsubject ==0:
            j = chooseatrandom2(verbs[topic])
        else:
            verbs_to_use = []
            verbs_to_use_e = []
            for v in verbs[topic]:
                if v in verbs_animalsubject:
                    verbs_to_use.append(v)
            for v in verbs_e[topic]:
                if v in verbs_animalsubject_e:
                    verbs_to_use_e.append(v)  
            j = chooseatrandom2(verbs_to_use)
        return j,topic,animalsubject,eng_plural,person

    if element == "N":
       	j = 0
        return j,topic,animalsubject,eng_plural,person

    if element == "-":
        j = 1
        return j,topic,animalsubject,eng_plural,person

    if element == "I":
        j = 0
        return j,topic,animalsubject,eng_plural,person

    if element == "V": #inflected verb
        person = int(random.random()*7)+1
        j = chooseatrandom2(verbs[topic])
        return j,topic,animalsubject,eng_plural,person

    if element == "X": #inflected auxillary
        person = int(random.random()*7)+1
        j = chooseatrandom2(aux)
        return j,topic,animalsubject,eng_plural,person 

    if element =="?":
       	j = 0
        return j,topic,animalsubject,eng_plural,person
    if element =="Y":
        j = 0
        topic = int(random.random()*10)
        return j,topic,animalsubject,eng_plural,person
    if element =="A":
        j = 0
        mutationstate = 2
        return j,topic,animalsubject,eng_plural,person
    if element == "R":
        if topic == 6:
            j = chooseatrandom2(relativepronouns)
        else:
	    j = 1
        return j,topic,animalsubject,eng_plural,person
    if element =="!":
        j = 0
        topic = int(random.random()*10)
        return j,topic,animalsubject,eng_plural,person
    if element =="@":
        j = 0
        topiclist = [5,6]
        topic = topiclist[int(random.random()*len(topiclist))]
        if topic ==5:
            animalsubject = 1 
        return j,topic,animalsubject,eng_plural,person
    if element =="#":
        j = chooseatrandom2(numerals)
	if j>0:
           eng_plural = 1
        if topic in [1,2,3]: #if we are talking about veg, meat or drink
	    eng_plural = 0
        return j,topic,animalsubject,eng_plural,person

def gen_elements(element,element_e,j,t,a,ep,per,j_e,t_e,a_e,ep_e,per_e):
    w = gen_element(element,j,t,a,ep,per,j,t,a,ep,per)[0]
    w_e = gen_element(element_e,j_e,t_e,a_e,ep_e,per_e,j_e,t_e,a_e,ep_e,per_e)[1]
    return w,w_e

def gen_element(element,j,t,a,ep,per,j_e,t_e,a_e,ep_e,per_e):
    global mutationstate
    global topic
    global animalsubject
    global tense
    global eng_plural
    global person_3ps
    if element == "L": #null element
       	w = ""
	w_e = ""
	return w,w_e

    if element == "Q":
        w = questionwords[j]
        w = mutate(w)
        w_e = questionwords_e[j_e]
        mutationstate = 1
	person_3ps = 3
        return w,w_e
    if element == "q":
        w = question_bos[j]
        w = mutate(w)
        w_e = question_bos_e[j]	
        mutationstate = 1
        return w,w_e
    if element == "p":
        w = pronouns[j]
        w = mutate(w)
        w_e = pronouns_e[j_e]
        mutationstate = 1
	person_3ps = j+1
        return w,w_e
    if element == "P":
        w = pronouns_possessive[j]
        w = mutate(w)
        if (w=="ow")or(w=="hy")or(w=="aga"):
            mutationstate=3
        if (w=="dha")or(w=="y"):
            mutationstate=2
        if (w=="agan")or(w=="agas"):
            mutationstate=1
        w_e = pronouns_possessive_e[j_e]
        return w,w_e

    if element == "r":
        w = prepositions[j]
        mutationstate = 1
        w = mutate(w)
        if w == "dhe":
            mutationstate = 2
        else:
            mutationstate = 1
        w_e = prepositions_e[j_e]
        return w,w_e
    if element == "a":
        w = adjectives[t][j]
        w = mutate(w)
        mutationstate = 1
        w_e = adj_e[t_e][j_e]
        return w,w_e

    if element == "c":
        w = adjectives[t][j]
        w = make_comparative(w)
        w = mutate(w)
        mutationstate = 1
        w_e = adj_e[t_e][j_e]
        w_e = make_comparative_e(w_e)
        return w,w_e
    if element == "s":
        w = adjectives[t][j]
        w = make_superlative(w)
        w = mutate(w)
        mutationstate = 1
        w_e = adj_e[t_e][j_e]
        w_e = make_superlative_e(w_e)
        return w,w_e
    if element == "n":
        w = nouns[t][j]
        w = mutate(w)
        mutationstate = 1
        if genders[t][j] == "f":
            mutationstate = 2
        w_e = nouns_e[t_e][j_e]
	if ep_e == 1:
	   if w_e[-1] == "y":
	      w_e = w_e [:-1] + "ie"
	   if w_e[-1] == "s":
	      w_e = w_e + "e"
	   w_e = w_e + "s"
	   if w_e[-4:-1] == "man":
	      w_e = w_e[:-3]+"en"
	person_3ps = 3
        return w,w_e
    if element == "t":
        w =  article[0]
        w = mutate(w)
        mutationstate = 1
        w_e = article_e[0]
        return w,w_e
    if element == "e":
        w = specifiers[j]
        w = mutate(w)
        mutationstate = 1
        w_e = specifiers_e[j_e]
        return w,w_e
    if element == "v":
        if a == 0:
            w = inflect(verbs[t][j],3,tense,False)
            w_e = inflect_e(verbs_e[t_e][j_e],person_3ps,tense,False)
        else:
            verbs_to_use = []
            verbs_to_use_e = []
            for v in verbs[t]:
                if v in verbs_animalsubject:
                    verbs_to_use.append(v)
            for v in verbs_e[t_e]:
                if v in verbs_animalsubject_e:
                    verbs_to_use_e.append(v)
            w = inflect(verbs_to_use[j],3,tense,False)
            w_e = inflect_e(verbs_to_use_e[j_e],person_3ps,tense,False)
        mutationstate = 2
        w = mutate(w)
        mutationstate = 1
        return w,w_e

    if element == "x":
        w = inflect(aux[j],3,tense,False)
        mutationstate = 2
        w = mutate(w)
        mutationstate = 1
        w_e = inflect_e(aux_e[j_e],person_3ps,tense,False)
        return w,w_e

    if element == "i":
        if a ==0:
            w =  verbs[t][j]
            w_e = verbs_e[t_e][j_e]
        else:
            verbs_to_use = []
            verbs_to_use_e = []
            for v in verbs[t]:
                if v in verbs_animalsubject:
                    verbs_to_use.append(v)
            for v in verbs_e[t_e]:
                if v in verbs_animalsubject_e:
                    verbs_to_use_e.append(v)  
            w = verbs_to_use[j]
            w_e = verbs_to_use_e[j_e]
        w = mutate(w)
        mutationstate = 1
        return w,w_e

    if element == "N":
        w =  negative[0]
        w = mutate(w)
        mutationstate = 2
        w_e = negative_e[0]
        return w,w_e

    if element == "-":
        w = negative[1]
        mutationstate = 2
        w_e = negative_e[1]
        return w,w_e

    if element == "I":
        w =  interrogative[0]
        w = mutate(w)
        mutationstate = 2
        w_e = interrogative_e[0]
        return w,w_e

    if element == "V": #inflected verb

        w = inflect(verbs[t][j],person,tense,True)
        w = mutate(w)
        mutationstate = 1
        w_e = inflect_e(verbs_e[t_e][j_e],per,tense,True)
        return w,w_e

    if element == "X": #inflected auxillary
        w = inflect(aux[j],person,tense,True)
        w = mutate(w)
        mutationstate = 1
        w_e = inflect_e(aux_e[j_e],per,tense,True)
        return w,w_e 

    if element =="?":
        return "?","?"
    if element =="Y":
        w = "y"
	w_e = ""
        mutationstate = 5
        return w,w_e
    if element =="A":
        w = "a"
	w_e = ""
        mutationstate = 2
        return w,w_e
    if element == "R":
        if t == 6:
            w = relativepronouns[j]
            w_e = relativepronouns_e[j_e]
        else:
	    w = relativepronouns[1]
            w_e = relativepronouns_e[1]
        if w != "":
            w = mutate(w)
            mutationstate = 1
        return w,w_e
    if element =="!":
        w = "" 
	w_e = ""
        return w,w_e
    if element =="@":
        w = ""
	w_e = ""
        return w,w_e
    if element =="#":
        w = numerals[j]
        w_e = numerals_e[j]
        if (j==0)or(j==1):      
            mutationstate = 2
        if j==2:
            mutationstate = 3
        if t in [1,2,3]: #if we are talking about veg, meat or drink
            w = ""
            w_e = ""
        return w,w_e
    

#sentence structure codes
#q-question word (bos)
#p pronoun
#r - preposition
#a - adjective
#c - comparative adjective
#s - superlative adjective
#n - noun
#t - article
#e - specifier
#v - verb (3ps singular)
#x - auxillary (3ps)
#i - infinitive
#Q - question word
#? - question mark
#I - interrogative particle
#N - negative particle ny
# # numeral
#V - inflected verb
#X - inflected auxillary verb
#A - a particle
#P - possessive pronoun
#r - preposition
#! - change topic (random)
#@ - change topic to animate topic (people or animals)
#- - negative particle na
#Y - Y particle

#sentence structures
# this is essentially a not very rigoursly defined 
# context-free grammar.
question_sentence_structures = ["QAvtn?","QAvtne?","qtna?","qtnc?","INqtna?","qtns?","IV#na?","INVns?","NXi#nc?","INXina?","IXins?","IV#nrtna?"]
statement_sentence_structures = ["pAv#n","pAvna","pAxi#n","pAxina","NV#n","pAvnrtn","pAvnrns","pAxinrn","pAxinrna","NVnrn","NXin","pAvPn","pAvPna","pAxiPn","pAxiPna","NVPn","pAvPnrtn","pAvPnrns","pAxinrPn","pAxinrPna","NVnrPn","NXiPn","@tn!Av#n","@tn!Axinc","rnYVtn","rnYV#n","P@n!Avna","P@n!Axins","Nv@tn!na","@tnRAV","@tn-V"]
sentence_structures = []
sentence_structures.extend(question_sentence_structures)
sentence_structures.extend(statement_sentence_structures)

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--english",action="store_true",
                    help="Give English translations for sentences.")
parser.add_argument("--onesent",action="store_true",
                    help="Return one sentence only. Default behaviour is to return list with the same number of elements as the list of sentence structures.")
parser.add_argument("--writetofile",action="store_true",
                    help="Write to file rather than command-line.")
args = parser.parse_args()

if args.writetofile:
    outputfilename_k = "lavar_k.txt"
    outputfilename_e = "lavar_e.txt"
    outputfile_k = file("lavar_k.txt","w")
    if args.english:
        outputfile_e = file("lavar_e.txt","w")

if args.onesent:
    topic = int(random.random()*10)    
    k = int((random.random()*len(sentence_structures)))
    js,topics,a_s,engpls,pers = gen_js(sentence_structures[k])
    outputsents = gen_sentence(sentence_structures[k],js,topics,a_s,engpls,pers) 
    outputsent_k = outputsents[0]
    if args.english:
        outputsent_e = outputsents[1]
        print("{kw} - {en}".format(kw=outputsent_k.ljust(40), en=outputsent_e.rjust(40)))
    else:
        print("{kw}".format(kw=outputsent_k))
    if args.writetofile:
        outputfile_k.write(outputsent_k+"\n") 
        if args.english:
            outputfile_e.write(outputsent_e+"\n")
else:
    numsents_q = len(question_sentence_structures)
    numsents_s = len(statement_sentence_structures)

    for i in range(numsents_q):
        topic = int(random.random()*10)    
        k = int((random.random()*len(question_sentence_structures)))
        js,topics,a_s,engpls,pers = gen_js(question_sentence_structures[k])
        #    print question_sentence_structures[j]
        outputsents = gen_sentence(question_sentence_structures[k],js,topics,a_s,engpls,pers) 
        outputsent_k = outputsents[0]
        if args.english:
            outputsent_e = outputsents[1]
            print("{kw} - {en}".format(kw=outputsent_k.ljust(40), en=outputsent_e.rjust(40)))
        else:
            print("{kw}".format(kw=outputsent_k))
        if args.writetofile:
            outputfile_k.write(outputsent_k+"\n")
            if args.english:
                outputfile_e.write(outputsent_e+"\n")
        
    for i in range(numsents_s):
        topic = int(random.random()*10)
        k = int((random.random()*len(statement_sentence_structures)))
        js ,topics,a_s,engpls,pers = gen_js(statement_sentence_structures[k])
        #    print statement_sentence_structures[j]
        outputsents = gen_sentence(statement_sentence_structures[k],js,topics,a_s,engpls,pers) 
        outputsent_k = outputsents[0]
        if args.english:
            outputsent_e = outputsents[1]
            print("{kw} - {en}".format(kw=outputsent_k.ljust(40), en=outputsent_e.rjust(40)))
        else:
            print("{kw}".format(kw=outputsent_k))
        if args.writetofile:
            outputfile_k.write(outputsent_k+"\n")
            if args.english:
                outputfile_e.write(outputsent_e+"\n")

if args.writetofile:
    outputfile_k.close()
    if args.english:
        outputfile_e.close()
