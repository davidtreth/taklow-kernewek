# coding=utf-8
import inflektya
import treuslytherenna as tr
import datainflektya_swf as dtinf_swf
import sys
import re

# import the data with special case and irregular verbs converted to SWF
inflektya.set_swfmode()

def inflektya_swf(verb, person, tense, suffix_pro=0):
    """ call inflektya.inflektya and transliterate its output into SWF """
    inflv, success = inflektya.inflektya(verb, person, tense, suffix_pro)
    if inflv != "NULL" and success == 1:
        # print(inflv)
        if verb in dtinf_swf.irregverbs_all:
            return inflv, 1
        else:
            if suffix_pro > 0 and person > 0 and tense != "ppl":
                suffix = " "+inflv.split(" ")[-1]
                inflv = inflv.split(" ")[-2]
            else:
                suffix = ""
            if tense == "tremenys" or tense == "gorperfydh":
                # single consonant replaces <ll>, <mm>, <nn> before j, s
                # in preterite and pluperfect/conditional
                inflv = inflv[::-1]
                inflv = re.sub(r'([aeoy])([js])ll',r'\1\2l', inflv, 1)             
                inflv = re.sub(r'([aeoy])([js])mm',r'\1\2m', inflv, 1)             
                inflv = re.sub(r'([aeoy])([js])nn',r'\1\2n', inflv, 1)             
                inflv = inflv[::-1]
            return tr.wordstr_KK2FSS(inflv, True, False)+suffix, 1        
    else:
        return "NULL", 0

def rol_personys_amserow(verb):
    """
    pryntya rol a personys ha'n amserow rag verb
    print a list of persons for each tense of verb
    """
    print("Verb {verb}:".format(verb=verb.upper()))
    # print imperfect before preterite
    # to match order in "Cornish Verbs"
    tensesorder = [0, 2, 1, 3, 4, 5, 6, 7]
    if verb not in dtinf_swf.irregverbs_all:
        tlist = [inflektya.tensesDict[t] for t in tensesorder]
        t_en_list = [inflektya.tensesDictEN[t] for t in tensesorder]
    else:
        tlist = dtinf_swf.irregverbs_all[verb].tenses_list
        t_en_list = dtinf_swf.irregverbs_all[verb].tenses_en_list

    for t, t_en in zip(tlist, t_en_list):
        print(("\nAmser: {amser} {tenseEN}".format(amser=t.capitalize().ljust(20),
                                                  tenseEN=t_en.capitalize().rjust(20))))
        if t == "ppl":
            print(("{person}: {inflVerb}".format(person="PPL".ljust(14),
                                                inflVerb=inflektya_swf(verb, 1, t, 1)[0]).rjust(12)))
        else:
            # print impersonal at the end instead so it matches "Cornish Verbs" book
            persons =list(range(1, 8))
            persons.append(0)
            for p in persons:
                print(("{person}: {inflVerb}".format(person=inflektya.personDict[p].ljust(14),
                                                    inflVerb=inflektya_swf(verb, p, t, 1)[0]).rjust(12)))
    print("\n")
    
def rol_pub_person_amser(verb):
    """
    daskorr avel rol Python a stringys pub person hag amser rag verb
    return as a Python list of strings all persons and tenses of a verb
    """
    allverbparts = []
    # print imperfect before preterite
    # to match order in "Cornish Verbs"
    tensesorder = [0, 2, 1, 3, 4, 5, 6, 7]
    if verb not in dtinf_swf.irregverbs_all:
        tlist = [inflektya.tensesDict[t] for t in tensesorder]
    else:
        tlist = dtinf_swf.irregverbs_all[verb].tenses_list
    for t in tlist:
        persons = list(range(1,8))
        persons.append(0)
        for p in persons:
            verbpart, success = inflektya_swf(verb, p, t, 0)
            if success == 1:
                # for non-existent persons the return will be ("NULL", 0)
                allverbparts.append(verbpart)
    return allverbparts

def rol_personys_amser_interact():
    """ Interactively get a verb from keyboard input and repeat until 'q' is entered """
    if sys.version_info[0] < 3:
        verb = raw_input("Ro an verb dhe inflektya mar pleg. Ro 'q' dhe kwittya. \n\
        Enter the verb to inflect please. Enter 'q' to quit.\n\n")
    else:
        verb = input("Ro an verb dhe inflektya mar pleg. Ro 'q' dhe kwittya. \n\
        Enter the verb to inflect please. Enter 'q' to quit.\n\n")
    if verb.lower() != 'q':
        rol_personys_amserow(verb)
        return 0
    else:
        return 1
    
def run_testcode():
    """ when started from the command-line,
    ask for input interactively """
    q = 0
    while q == 0:
        q = rol_personys_amser_interact()    

if __name__ == '__main__':
    run_testcode()
