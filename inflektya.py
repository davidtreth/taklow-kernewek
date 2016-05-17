# David Trethewey
# vershyon 14-05-2016
"""
An module ma a wra inflektya verbow Kernewek
This module inflects Cornish verbs
"""
import re
import datainflektya as dtinf

def make_tense_dict(list_tenses, past_pl="NULL"):
    """
    y telledh bos list_tenses rol taklennow RannowVerbAnreyth
    list_tenses should be a list of RannowVerbAnreyth objects (parts of irregular verbs)
    assembles these into a dictionary of dictionaries and returns it
    """
    outdict = {}
    for t in list_tenses:
        outdict[t.amser] = t.rannow_dict
    if past_pl != "NULL":
        outdict["ppl"] = past_pl
    return outdict

def lastvowel(verbstr):
    """ return the last vowel of a string """
    if verbstr[-1] in vowels:
        finalvowel = verbstr[-1]
        pos = len(verbstr)-1
        return finalvowel, pos
    else:
        return lastvowel(verbstr[:-1])

def lastconsonant(verbstr):
    """ kavoes an diwettha kessonenn
    returns last consonant cluster for hardening/doubling in subjunctive """
    consonants = re.split(r'[aeiouy]', verbstr)
    lastcon = consonants[-1]
    if lastcon == '':
        lastcon = consonants[-2]
    # lenlastconstclust = len(lastcon)
    # pos = len(verbstr)-lenlastconstclust
    # return lastcon, pos, lenlastconstclust
    return lastcon

def inflektya_reyth(verb, stem, person, tense, suffix_pro):
    """ inflect a regular verb
    verb is the verbal noun
    stem is the stem
    person is an integer 0-7
    tense is here an integer 0-7
    suffix_pro is a flag to determine whether there are
    no suffixed pronouns, standard ones, or emphatic ones """
    if tense < 8:
        # should always be an integer 0-7
        # check whether should use the endings with i/y vowel
        # verbow a worfenn gans -el, -es, -he, -i
        # ha verbow in rol verbs_i_3sp
        # a'n jeves 3s. tremenys gans -is yn le -as
        
        if (verb[-2:] in dtinf.endings_ivowel or verb[-1:] in dtinf.endings_ivowel) and (
                (not verb in dtinf.verbs_klywes)and(not verb in dtinf.verbs_ankevi)):
            endings = dtinf.endings_alltenses_i.tense_endings(tensesDict[tense])
        elif tense == 1 and verb in dtinf.verbs_i_3sp:
            endings = dtinf.endings_alltenses_i.tense_endings(tensesDict[tense])
        elif tense == 2 and verb in dtinf.verbs_i_imp:
            endings = dtinf.endings_alltenses_i.tense_endings(tensesDict[tense])
        else:
            endings = dtinf.endings_alltenses.tense_endings(tensesDict[tense])
    if tense < 7:
        # for all tenses except past participle
        ending = endings.person_ending(person)
    if tense == 7: # if past participle
        ending = endings
    # in verbs such as benniga change g-->k in 3ps and 2p imp.
    if ending == "":
        if stem[-1] == "g":
            stem = stem[:-1] + "k"
        if stem[-2:] == "gy":
            stem = stem[:-2] + "ky"
    # verbow a worfenn gans -he:
    # verbs ending in -he:
    if verb[-2:] == "he":
        if tense == 0 and ((person == 3)or(person == 4)):
            # 3s a-lemmyn a'th eus a wosa an ben
            # 3s. pres has a not just stem alone
            ending = "a"
        if ending != "":
            if ending[0] == "s":
                # mars eus -s- gorra a kyns an -s-
                # where there is an -s- an a is added before the s
                ending = "a"+ending
        if (tense == 4)or(tense == 5):
            # -ah- yn islavarek
            # subjunctive has extra -ah-
            ending = "ah"+ending
        if tense == 7:
            # yma -es dhe'n ben yn ppl
            # past participle adds -es to the stem.
            ending = "es"
    origending = ending #before addition of suffixed pronoun
    if (suffix_pro == 1)and(person > 0)and(tense != 7):
        # if there should be suffixed pronouns, and it isn't impersonal or ppl
        ending = ending + " " + dtinf.suffixed_pros[person]
    if (suffix_pro == 2)and(person > 0)and(tense != 7):
        # if there should be emphatic suffixed pronouns, and not impersonal or ppl
        ending = ending + " " + dtinf.suffixed_pros_emph[person]
    # verbow a worfenn gans -ya
    # verbs ending in -ya
    if stem[-1] == "y":
        # -y- yw gwithys heb y arall, i po s yn penn po nag eus penn
        # -y- retained except where another y, i or s occurs in the ending
        # or where there is no suffix (3s pres, 2s imperative)
        # yn verb amaya, an y yw gwithys pupprys
        # in amaya, the y is always retained
        if verb not in dtinf.verbs_amaya:
            if origending == "":
                stem = stem[:-1]
            else:
                if (origending[0] == "y") or (origending[0] == "i") or (
                        origending[0] == "s"):
                    stem = stem[:-1]
    # verbow gans maneruster bogalenn
    # verbs with vowel affectation

    # type TAVA:
    # yma a diwettha bogalenn an ben
    # a is last vowel of stem
    # tardra --> terdrys
    if verb in dtinf.verbs_tava:
        # a-->e mar bogalenn y'n penn  -i-, -y-, po -owgh
        # a-->e when vowel of ending is -i-, -y-, or -owgh
        # hag yn 2pl gorhemmyn kyns -ewgh
        # also in 2pl imperative before -ewgh
        if origending != "":
            if (("i" in origending or "y" in origending) or ("owgh" in origending)) or (
                    ("ewgh" in origending)and(person == 6)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if stem[-1] == 'y':
                    laststemvowel, pos = lastvowel(stem[:-1])
                if laststemvowel == "a":
                    if (tense == 4)or(tense == 5):
                        # chanjys dhe -y- yn islavarek
                        # in subjunctive further affected to -y-
                        stem = stem[:pos] + "y" + stem[pos+1:]
                    else:
                        stem = stem[:pos] + "e" + stem[pos+1:]

    if verb in dtinf.verbs_amma:
        # AMMA, RANNA - a-->y
        if origending != "":
            if (("i" in origending or "y" in origending) or ("owgh" in origending)) or (
                    ("ewgh" in origending)and(person == 2)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if stem[-1] == 'y':
                    laststemvowel, pos = lastvowel(stem[:-1])
                if laststemvowel == "a":
                    stem = stem[:pos] + "y" + stem[pos+1:]
                if laststemvowel == "e":
                    # verbs such as eva
                    stem = stem[:pos] + "y" + stem[pos+1:]

    if verb in dtinf.verbs_pregowtha:
        # pregowtha ow-->ew
        if origending != "":
            if (("i" in origending or "y" in origending) or ("owgh" in origending)) or (
                    ("ewgh" in origending)and(person == 2)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if stem[-1] == 'y':
                    laststemvowel, pos = lastvowel(stem[:-1])
                if laststemvowel == "o":
                    stem = stem[:pos] + "e" + stem[pos+1:]

    if verb in dtinf.verbs_dannvon:
        # dannvon, daskorr o-->e
        if origending != "":
            if ("i" in origending or "y" in origending) or ("owgh" in origending) or (
                    ("ewgh" in origending)and(person == 2)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if stem[-1] == 'y':
                    laststemvowel, pos = lastvowel(stem[:-1])
                if laststemvowel == "o":
                    stem = stem[:pos] + "e" + stem[pos+1:]

    if verb in dtinf.verbs_fyllel:
        # FYLLEL y-->a
        if ((tense == 0)and(person == 1))or((tense == 1)and(person == 7))or(((tense == 3)or(tense == 5))and(person > 0))or((tense == 4)and((person ==3)or(person == 4))):
            laststemvowel, pos = lastvowel(stem)
            if laststemvowel == "y":
                stem = stem[:pos] + "a" + stem[pos+1:]
            
    # type IGERI
    # gwitha bogalenn ben derowel -a- po -o- yn amserowa syw:
    # retain original stem vowel -a- or -o- in following tenses:
    # pres/future 1s
    # preterite 3s and 3p
    # pluperfect all persons
    # subjuctive pres 3s. and 3p.
    # subjunctive imp. all persons
    # imperative 2s.
    if verb in dtinf.verbs_igeri_o:
        if ((tense == 0)and(person == 1))or(((tense == 1)or(tense == 4))and(
                (person == 3)or(person == 4)or(person == 7)))or(tense == 3)or(
                    tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if stem[-1] == 'y':
                    laststemvowel, pos = lastvowel(stem[:-1])
            if laststemvowel == "e":
                stem = stem[:pos] + "o" + stem[pos+1:]
        if verb in dtinf.verbs_dedhwi:
            if (tense == 0)and((person == 3)or(person == 4)):
                stem = "dedhow"
    if verb in dtinf.verbs_igeri_a:
        if ((tense == 0)and(person == 1))or(((tense == 1)or(tense == 4))and(
                (person == 3)or(person == 4)or(person == 7)))or(tense == 3)or(
                    tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if stem[-1] == 'y':
                    laststemvowel, pos = lastvowel(stem[:-1])
            if laststemvowel == "e":
                stem = stem[:pos] + "a" + stem[pos+1:]

    #type ERGHI
    # maneruster bogalenn kepar hag igeri hag ynwedh chanj bogalenn dhe'n 3s tremenys
    # same kind of vowel affectation as igeri with addition of 3s. preterite,
    # ending in -is also has a vowel change
    # retains original stem vowel in
    # pres/future 1s
    # preterite 3p only
    # pluperfect all persons
    # subjunctive pres./fut. 3s. and 3p.
    # subjunctive imp. all persons
    # imperative 2s'
    if verb in dtinf.verbs_erghi_a:
        # with most of these verbs, it is the 'e' in the verb noun
        # except diank and maybe others
        laststemvowel, pos = lastvowel(stem)
        if laststemvowel == "a":
            stem = stem[::-1].replace("a","e",1)[::-1]
        if ((tense == 0)and(person == 1))or((tense == 1)and(person == 7))or(
                tense == 3)or((tense == 4)and((person == 3)or(person == 4)or(
                    person == 7)))or(tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if stem[-1] == 'y':
                laststemvowel, pos = lastvowel(stem[:-1])
            if laststemvowel == "e":
                stem = stem[:pos] + "a" + stem[pos+1:]
        if verb in dtinf.verbs_gweskel:
            # gweskel has 3s. pres/fut gwysk, past participle gwyskys, loses k in some parts of verb
            if ((tense == 0)and((person == 3)or(person == 4)))or(tense == 7):
                stem = "gwysk"
    if verb in dtinf.verbs_erghi_o:
        if ((tense == 0)and(person == 1))or((tense == 1)and(person == 7))or(
                tense == 3)or((tense == 4)and((person == 3)or(person == 4)or(
                    person == 7)))or(tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if stem[-1] == 'y':
                laststemvowel, pos = lastvowel(stem[:-1])
            if laststemvowel == "e":
                stem = stem[:pos] + "o" + stem[pos+1:]
        if verb in dtinf.verbs_dinewi and tense == 0 and ((person == 3)or(person == 4)):
            # dinewi has 3s. pres/fut dinwa
            stem = "dinwa"

    if (verb in dtinf.three_s_presfut_y) and tense == 0 and ((person == 3)or(person == 4)):
        # group of verbs narrow vowel in 3s. pres/fut (sect 192 of Wella Brown 3rd ed.)
        laststemvowel, pos = lastvowel(stem)
        if stem[-1] == 'y':
            laststemvowel, pos = lastvowel(stem[:-1])
        if laststemvowel == "o":
            stem = stem[:pos] + "e" + stem[pos+1:]
        else:
            stem = stem[:pos] + "y" + stem[pos+1:]
    # godhevel has alternative verbal noun godhav
    # not implemented

    # GELWEL type conjugated as erghi
    # stem ends in -l, -n, or -r followed by -w-
    # original stem vowel is -a-
    # -o- placed before -w- in 3s. pres/fut
    # galwsons/gawlsons 3p. pret., pluperfect
    if verb in dtinf.verbs_gelwel:
        if ((tense == 0)and(person == 1))or((tense == 1)and(person == 7))or(
                tense == 3)or((tense == 4)and((person == 3)or(person == 4)or(
                    person == 7)))or(tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if stem[-1] == 'y':
                laststemvowel, pos = lastvowel(stem[:-1])
            if laststemvowel == "e":
                stem = stem[:pos] + "a" + stem[pos+1:]
        if (tense == 0)and((person == 3)or(person == 4)):
            stem = stem[:-2] + "ow"
        #optional
        if ((tense == 1)and(person == 7))or(tense == 3):
            stem = stem[:-2] + stem[-1] + stem[-2]

    # HWITHRA type
    # stem ends in two consonant sounds, the second of which is -l-, -m-, -n-, or -r-
    # delivra changes -vr- to -rv- 3s. pres/fut, 2s. imperative, + where ending starts with an s
    # NOT IMPLEMENTED
    # in subjunctives consonant before lrmn undergoes hardening of doubling
        # print(verb,stem, tense)
        # print(verb in verbs_hwithra)
    if verb in dtinf.verbs_hwithra:
        # print(stem)
        if ((tense == 0)and((person == 3)or(person == 4)))or((tense == 6)and(person == 2)):
            # in 3s. pres/future and 2s. imperative
            # a vowel is introduced usually -e-
            # sometimes -o- or -y-
            if verb in dtinf.verbs_resna:
                vowel = "o"
            else:
                if verb in dtinf.verbs_fekla:
                    vowel = "y"
                else:
                    vowel = "e"
            if stem[-2:] == "sh":
                stem = stem[:-2]+vowel+stem[-2:]
            else:
                if verb in dtinf.verbs_delivra:
                    stem = stem[:-2]+stem[-1]+stem[-2]
                else:
                    stem = stem[:-1]+vowel+stem[-1]
            
        if origending != "":
            if origending[0] == "s": 
                # when verbal ending starts with an -s-
                # the final consonant of the stem may drop out and be shortened
                # and an apostrophe introduced
                if stem[-2:] == "sh":
                    stem1 = stem[:-2]
                    stem2 = stem[-2:]
                else:
                    stem1 = stem[:-1]
                    stem2 = stem[-1:]
                    
                if verb not in dtinf.verbs_ankombra:
                    stem = stem1+"'"
                elif verb in dtinf.verbs_delivra:
                    stem = stem[:-2]+stem[-1]+stem[-2]
                elif verb in dtinf.verbs_fekla:
                    stem = stem1+ "y" +stem2
                else:
                    stem = stem1+ "e" +stem2

    # GWYSTLA type
    # final consonant is -l-, -m-, -n- or -r- preceded by two adjacent consonants.
    if verb in dtinf.verbs_gwystla:
        vowel = "e"
        if ((tense == 0)and((person == 3)or(person == 4)))or((tense == 6)and(person == 2)):
            # in 3s. pres/fut and 2s. imperative, an -e- is put before the final consonant
            stem = stem[:-1]+vowel+stem[-1]
        if origending != "":
            if origending[0] == "s":
                # when verbal ending starts with an -s-
                # -e- is put before the final consonant of the stem
                # and verb remains uncontracted
                stem = stem[:-1] + vowel + stem[-1]
        if (tense == 4)or(tense == 5):
            # subjunctive changes with following endings:
            # -ndl- > -ntl-; -ldr- > -ltr-; -rdr- > -rtr
            if stem[-3:] == "ndl":
                stem = stem[:-3] + "ntl"
            if stem[-3:] == "ldr":
                stem = stem[:-3] + "ltr"
            if stem[-3:] == "rdr":
                stem = stem[:-3] + "rtr"

    # LESTA
    # where stem ends in -s- followed by another consonant, this second consonant may be omitted
    # can be shown in writing by replacement with apostrophe
    if verb in dtinf.verbs_lesta:
        if origending != "":
            if origending[0] == "s":
                stem = stem[:-1]+"'"

    # diskwedhes, drehevel, gortos, hwilas. stem change in 3rd person present and 2p sing imperative
    if (verb in dtinf.verbs_stemdict_diskwedhes.keys())and(((tense == 0)and(
            (person == 3)or(person == 4))or(tense == 6 and person == 2))):
        stem = dtinf.verbs_stemdict_diskwedhes[verb]

    # DYBRI
    # vowel affectation in stem
    # y --> e e.g. in dybri
    # in pres pers 1,3,4,6,7
    # pres subj pers 3,4
    # imp subj all pers
    # imperative pers 2
    if verb in dtinf.verbs_dybri:
        if ((tense == 0) and (person in [1, 3, 4, 6, 7])) or ((tense == 4) and (
                person in [0, 3, 4, 7])) or (tense == 5) or ((tense == 6) and (person == 2)):
            stem = stem.replace("y", "e", 1)

    # return the result
    inflectedverb = stem+ending
    return inflectedverb, 1

def inflektya_validate_person(person):
    """ check person is an integer from 0 to 7 """
    # expect an integer from 0 to 7
    try:
        person = int(person)
        if person not in range(8):
            return False
        else:
            return True
    except ValueError:
        return False

def inflektya_validate_tense(verb, person, tense):
    """ check tense is one of the strings in the 
    tenses dictionary """
    if tense not in tensesDict.values():
        # validate tense parameter
        return False
    if ((person == 0)or(person == 1))and(tense == "gorhemmyn"):
        # impersonal and 1s don't exist in imperative
        # nyns eus anpersonek ha'n 1s y'n gorhemmyn
        # print "invalid tense/person combination"
        return False
    if tense == "devedhek" and verb not in dtinf.verbs_devedhek:
        # only a few verbs have a simple future tense
        # if not return invalid
        return False
    if tense == "anperfydh_usadow" and verb not in dtinf.verbs_anperfydh_usadow:
        # only a few verbs have a separate habitual imperfect
        # if not return invalid
        return False
    if tense in ["a-lemmyn_hir_indef", "anperfydh_hir", "a-lemmyn_hir_def",
                 "a-lemmyn_hir_aff"] and verb != "bos":
        # the long forms which are particular to bos
        return False
    if tense == "perfydh" and verb not in dtinf.verbs_perfydh:
        return False
    return True

def inflektya(verb, person, tense, suffix_pro=0):
    """ person: 0=imp,1=1s,2=2s,3=3sm,4=3sf,5=1p,6=2p,7=3p
     tense: 0=present, 1=preterite, 2=imperfect, 3=pluperfect, 4=subjpres, 5=subjimp
    6=imperative,7=past_participle,8=future,9=habitual imperfect
    0=longform_present_indef,11=longform_imperfect,12=longform_present_defni
    3=longform_present_aff,14=perfect
    expect string for the tense """
    
    # alternate spellings of the same verb, e.g. doen/degi
    if verb in dtinf.verbs_alternatesp.keys():
        verb = dtinf.verbs_alternatesp[verb]
    
    tenses_code_dict = {v:k for k, v in tensesDict.items()}

    # yma amser devedhek, anperfydh usadow ha perfydh dhe nebes verbow
    # certain verbs have simple future, habitual imperfect, perfect
    # nebes verbow yw defowtek
    # certain verbs are incomplete/defective

    # suffix_pro: flag to say whether to include suffixed pronoun
    if suffix_pro not in [0, 1, 2]:
        # if it is anything other than 0,1,2
        # set to 0 i.e. no suffixed pronoun
        suffix_pro = 0
    invalidinput = "NULL"
    # successflag = 1 if successful, 0 if error
    if not inflektya_validate_person(person):
        return invalidinput, 0
    else:
        person = int(person)

    if not inflektya_validate_tense(verb, person, tense):
        # if the tense is invalid for the verb, return a NULL
        return invalidinput, 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    if verb[-1] in vowels:
        stem = verb[:-1]
    if verb[-1] not in vowels:
        stem = verb
    if (verb[-2:] == "el")or(verb[-2:] == "es")or(verb[-2:] == "as")or(verb[-2:] == "os"):
        stem = verb[:-2]
    if verb[-3:] == "oes":
        stem = verb[:-3]
                
    if verb in dtinf.verbs_stemnoun:
        stem = verb
    if ("islavarek" in tense)and(verb not in dtinf.verbs_gwystla)and(verb[-2:] != "ia"):
        # kesson a wra dewblek po kaleshe y'n islavarek
        # double/harden consonants in subjunctive
        # but not generally in verbs_gwystla
        # and not in verbs ending -ia
        lastconststem = lastconsonant(stem)
        # print(lastconststem)
        if lastconststem in dtinf.stem_changes.keys():
            # do a string replace, but first reverse the stem, and the
            # arguments for replace, so that it is only done once
            # for the last time lastconststem occurs in stem
            stem = stem[::-1].replace(lastconststem[::-1],
                                      dtinf.stem_changes[lastconststem][::-1], 1)[::-1]
    regular = verb not in dtinf.irregverbs_all.keys()
    if regular:
        return inflektya_reyth(verb, stem, person, tenses_code_dict[tense], suffix_pro)

    if not regular:
        if tense == "ppl":
            inflectedverb = dtinf.irregverbs_all[verb].getppl()
        else:
            inflectedverb = dtinf.irregverbs_all[verb].get_inf_verb(tense, person)
            if (suffix_pro == 1)and(person > 0):
                inflectedverb += " " + dtinf.suffixed_pros[person]
            if (suffix_pro == 2)and(person > 0):
                inflectedverb += " " + dtinf.suffixed_pros_emph[person]
        return inflectedverb, 1


def inflektya_prepos(prepos, person, suffix_pro=0):
    """
    inflektya prepos rag person
    suffix_pro a wra determya mars eus raghenwyn a syw
    0 = nag eus, 1 = raghanow a syw, 2 = raghanow emphatek a syw
    inflect prepos for person
    suffix_pro determines whether a suffixed pronoun follows
    0 = none, 1 = normal suff.pro., 2 = emphatic suff. pro.
    """
    invalidinput = 'NULL'
    if not inflektya_validate_person(person):
        return invalidinput, 0
    else:
        person = int(person)

    if dtinf.prep_stems_all.has_key(prepos) and dtinf.prep_endings_all.has_key(prepos):
        inflectedprep = dtinf.prep_stems_all[prepos][person] + dtinf.prep_endings_all[prepos][person]
    else:
        print("Rager {prepos} yw anaswonnys.\n\
Preposition {prepos} is unknown".format(prepos=prepos))
        return invalidinput, 0
    ending = ""
    if (prepos == "dhe")and(suffix_pro > 0)and((person == 1)or(person == 2)):
        ending += "o"
    if (suffix_pro == 1)and(person > 0):
        ending += " " + dtinf.suffixed_pros[person]
    if (suffix_pro == 2)and(person > 0):
        ending += " " + dtinf.suffixed_pros_emph[person]
    inflectedprep = inflectedprep + ending
    return inflectedprep, 1

def rol_personys_amserow(verb):
    """
    pryntya rol a personys ha'n amserow rag verb
    print a list of persons for each tense of verb
    """
    print("Verb {verb}:".format(verb=verb.upper()))
    # print imperfect before preterite
    # to match order in "Cornish Verbs"
    tensesorder = [0, 2, 1, 3, 4, 5, 6, 7]
    if verb not in dtinf.irregverbs_all.keys():
        tlist = [tensesDict[t] for t in tensesorder]
        t_en_list = [tensesDictEN[t] for t in tensesorder]
    else:
        tlist = dtinf.irregverbs_all[verb].tenses_list
        t_en_list = dtinf.irregverbs_all[verb].tenses_en_list

    for t, t_en in zip(tlist, t_en_list):
        print("\nAmser: {amser} {tenseEN}".format(amser=t.capitalize().ljust(20),
                                                  tenseEN=t_en.capitalize().rjust(20)))
        if t == "ppl":
            print("{person}: {inflVerb}".format(person="PPL".ljust(14),
                                                inflVerb=inflektya(verb, 1, t, 1)[0]).rjust(12))
        else:
            # print impersonal at the end instead so it matches "Cornish Verbs" book
            persons = range(1, 8)
            persons.append(0)
            for p in persons:
                print("{person}: {inflVerb}".format(person=personDict[p].ljust(14),
                                                    inflVerb=inflektya(verb, p, t, 1)[0]).rjust(12))
    print("\n")

def rol_personys_prepos(prepos):
    """
    pryntya rol a personys rag prepos
    print a list of persons for a preposition
    """
    print("Preposition {p}:".format(p=prepos.upper()))
    for p in range(7):
        if inflektya_prepos(prepos, p+1, 1)[1] == 0:
            # if prepos is not known as a preposition
            break
        print("{person}: {inflPrep}".format(person=personDict[p+1].ljust(14),
                                            inflPrep=inflektya_prepos(prepos, p+1, 1)[0].rjust(12)))
    print("\n")

def rol_personys_amser_interact():
    """ Interactively get a verb from keyboard input and repeat until 'q' is entered """
    verb = raw_input("Ro an verb dhe inflektya mar pleg. Ro 'q' dhe kwittya. \n\
Enter the verb to inflect please. Enter 'q' to quit.\n\n")
    if verb.lower() != 'q':
        rol_personys_amserow(verb)
        return 0
    else:
        return 1
def rol_personys_prepos_interact():
    """ Interactively get a preposition from keyboard input and repeat until 'q' is entered """
    prepos = raw_input("Ro an rager dhe inflektya mar pleg. Ro 'q' dhe kwittya. \n\
Enter the preposition to inflect please. Enter 'q' to quit.\n\n")
    if prepos.lower() != 'q':
        rol_personys_prepos(prepos)
        return 0
    else:
        return 1

def run_testcode():
    """ when started from the command-line, print out a few verbs and prepositions
    and then ask for them interactively """
    rol_personys_amserow("prena")
    rol_personys_amserow("bos")
    rol_personys_amserow("y'm beus")
    rol_personys_amserow("godhvos")
    rol_personys_amserow("mos")
    rol_personys_amserow("dos")
    rol_personys_amserow("ri")
    rol_personys_amserow("doen")
    rol_personys_amserow("gul")
    rol_personys_amserow("mynnes")
    rol_personys_amserow("galloes")
    rol_personys_prepos("dhe")
    rol_personys_prepos("gans")
    rol_personys_prepos("dres")
    q = 0
    while q == 0:
        q = rol_personys_amser_interact()
    q = 0
    while q == 0:
        q = rol_personys_prepos_interact()

# person: 0=imp,1=1s,2=2s,3=3sm,4=3sf,5=1p,6=2p,7=3p

personDict = {0:'anpersonek',
              1:'1s',
              2:'2s',
              3:'3sm',
              4:'3sf',
              5:'1pl',
              6:'2pl',
              7:'3pl'}

# tense: 0=present, 1=preterite, 2=imperfect, 3=pluperfect, 4=subjpres, 5=subjimp
# 6=imperative,7=past_participle,8=future,9=habitual imperfect
# 10=longform_present_indef,11=longform_imperfect,12=longform_present_defni
# 13=longform_present_aff,14=perfect
tensesDict = {0:"a-lemmyn",
              1:"tremenys",
              2:"anperfydh",
              3:"gorperfydh",
              4:"islavarek_a-lemmyn",
              5:"islavarek_anperfydh",
              6:"gorhemmyn",
              7:"ppl",
              8:"devedhek",
              9:"anperfydh_usadow",
              10:"a-lemmyn_hir_indef",
              11:"anperfydh_hir",
              12:"a-lemmyn_hir_def",
              13:"a-lemmyn_hir_aff",
              14:"perfydh"}
tensesDictEN = {0:"present",
                1:"preterite",
                2:"imperfect",
                3:"pluperfect",
                4:"present subjunctive",
                5:"imperfect subjunctive",
                6:"imperative",
                7:"past participle",
                8:"simple future",
                9:"habitual imperfect",
                10:"present (long form, indefinite)",
                11:"imperfect (long form)",
                12:"present (long form, definite)",
                13:"present (long form, affirmative)",
                14:"perfect"}
vowels = ["a", "e", "i", "o", "u", "y"]

if __name__ == '__main__':
    run_testcode()
