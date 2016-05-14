# David Trethewey
# vershyon 14-05-2016
"""
An module ma a wra inflektya verbow Kernewek
This module inflects Cornish verbs
"""
import re

class LostowPersonek(object):
    """
    taklenn a wra gwitha lostow personek dhe unn amser verb
    an object to hold the personal endings for a verb tense
    """
    def __init__(self, rol_lostow, amser):
        self.lostow = rol_lostow
        self.lostow_dict = {}
        for i, lost in enumerate(rol_lostow):
            self.lostow_dict[i] = lost
        self.amser = amser
        
    def person_ending(self, personnum):
        """ return the personal ending for a single person defined by personnum """
        return self.lostow_dict[personnum]


class LostowPersonekOllAmser(object):
    """
    klass dhe wul taklennow a wra gwitha lostow personek an verbow yn pub amser
    a class to create objects to hold personal endings of all tenses in a verb
    """
    def __init__(self, lostowDict):
        """
        lostowDict a wra gwitha an lostow yn gerlyver
        gans yndeks an amser
        rag ensample lostowDict["a-lemmyn"] = lostow_alemmyn
        ha lostow_alemmyn yw taklenn LostowPersonek

        lostowDict holds the endings in a dictionary
        indexed by the tense
        e.g. lostowDict["a-lemmyn"] = lostow_alemmyn
        where lostow_alemmyn is a LostowPersonek object
        """
        self.lostow_dict = lostowDict

    def tense_endings(self, tense):
        """
        kavoes gerlyver lostow rag unn amser
        return dictionary of endings for a tense
        """
        return self.lostow_dict[tense]

class RannowVerbAnreyth(object):
    """
    verb anreyth inflektys - unn amser
    inflected irregular verb of one tense
    """
    # English translations of the tense names
    amserowEN = {"a-lemmyn":"present",
                 "tremenys":"preterite",
                 "anperfydh":"imperfect",
                 "gorperfydh":"pluperfect",
                 "islavarek_a-lemmyn":"present subjunctive",
                 "islavarek_anperfydh":"imperfect subjunctive",
                 "gorhemmyn":"imperative",
                 "ppl":"past participle",
                 "devedhek":"simple future",
                 "anperfydh_usadow":"habitual imperfect",
                 "a-lemmyn_hir_indef":"present (long form, indefinite)",
                 "anperfydh_hir":"imperfect (long form)",
                 "a-lemmyn_hir_def":"present (long form, definite)",
                 "a-lemmyn_hir_aff":"present (long form, affirmative)",
                 "perfydh":"perfect"}

    def __init__(self, verbnoun, anpersonek, my, ty, ev, hi, ni, hwi, i, amser):
        """ verbnoun: dictionary form, verbal noun / infinitive
        following arguments are the inflected forms:
        anpersonek: impersonal
        my: 1p sing
        ty: 2p sing
        ev, hi: 3p sing masc + fem
        ni: 1p plural
        hwi: 2p plural
        i: 3p plural
        amser: the tense
        """
        self.verbnoun = verbnoun
        # store the inflected forms in a list, and in a dictionary
        self.rannow = [anpersonek, my, ty, ev, hi, ni, hwi, i]
        self.rannow_dict = {0:anpersonek, 1:my, 2:ty, 3:ev, 4:hi, 5:ni, 6:hwi, 7:i}
        # store the tense name and its English translation
        self.amser = amser
        self.amser_en = RannowVerbAnreyth.amserowEN[amser]

class RannowVerbAnreythOllAmser(object):
    """
    kyst rag rannow verb anreyth
    container for parts of irregular verb
    """
    def __init__(self, verbnoun):
        """
        mar nag yw an verb defektiv, y fydh ganso
        amserow 0-7 ha martesen moy
        nebes verbow ny'th eus PPL
        gerlyver amserow yn dict_tenses
        pub alhwedh yn dict_tenses yw amser
        value yw taklenn RannowVerbAnreyth

        if not defective, it will have tenses 0-7 and maybe more
         a few verbs don't have past participle
         dictionary of tenses in dict_tenses
         each key in dict_tenses is tense
         value is RannowVerbAnreyth object
        """
        self.verbnoun = verbnoun
        self.tenses_list = []
        self.tenses_en_list = []
        self.dict_tenses = {}

    def add_tense(self, tense):
        """
        y telledh bos tense taklenn RannowVerbAnreyth
        tense should be RannowVerbAnreyth object
        """
        self.tenses_list.append(tense.amser)
        self.tenses_en_list.append(tense.amser_en)
        # a dictionary of dictionaries
        self.dict_tenses[tense.amser] = tense.rannow_dict

    def addppl(self, ppl):
        """
        keworra ppl dhe self.dict_tenses
        add past participle to self.dict_tenses
        """
        self.dict_tenses["ppl"] = ppl

    def add_tense_list(self, tense_list, ppl="NULL"):
        """
        keworra rol a amserow orth self.dict_tenses
        add a list of tenses to self.dict_tenses
        """
        for tn in tense_list:
            self.add_tense(tn)
        if ppl != "NULL":
            self.addppl(ppl)

    def getppl(self):
        """ daskavoes an ppl
        return the past participle """
        return self.dict_tenses["ppl"]

    def get_inf_verb(self, tense, person):
        """
        kavoes verb inflektys gans an amser ha'n person
        return the inflected verb for the tense and person
        """
        if self.dict_tenses.has_key(tense):
            return self.dict_tenses[tense][person]
        else:
            print("Nyns eus amser {t} dhe verb {v}.\n\
Verb {v} doesn't have tense {t}".format(v=self.verbnoun, t=tense))
            return "NULL"

# lostow verbow reyth
# regular verb endings
endings_present = LostowPersonek(["ir", "av", "ydh", "", "", "yn", "owgh",
                                  "ons"], "a-lemmyn")
endings_preterite = LostowPersonek(["as", "is", "sys", "as", "as", "syn",
                                    "sowgh", "sons"], "tremenys")
# lostow rag verbow gans i
# endings for verbs that use the i vowel
endings_preterite_i = LostowPersonek(["is", "is", "sys", "is", "is", "syn",
                                      "sowgh", "sons"], "tremenys")
endings_imperfect = LostowPersonek(["ys", "en", "es", "a", "a", "en",
                                    "ewgh", "ens"], "anperfydh")
endings_imperfect_i = LostowPersonek(["ys", "yn", "ys", "i", "i", "yn",
                                      "ewgh", "ens"], "anperfydh")
endings_pluperfect = LostowPersonek(["sys", "sen", "ses", "sa", "sa", "sen",
                                     "sewgh", "sens"], "gorperfydh")
endings_subj_pres = LostowPersonek(["er", "iv", "i", "o", "o", "yn", "owgh",
                                    "ons"], "islavarek_a-lemmyn")
endings_subj_imp = LostowPersonek(["ys", "en", "es", "a", "a", "en", "ewgh",
                                   "ens"], "islavarek_anperfydh")
endings_imperative = LostowPersonek(["", "", "", "es", "es", "yn", "ewgh",
                                     "ens"], "gorhemmyn")

# notenn - nyns eus 1s ha anpersonek dhe'n amser gorhemmyn
# note - 1s and impersonal do not exist for imperative
ending_pastparticiple = "ys"
suffixed_pros = {1:"vy", 2:"jy", 3:"ev", 4:"hi", 5:"ni", 6:"hwi", 7:"i"}
suffixed_pros_emph = {1:"evy", 2:"tejy", 3:"eev", 4:"hyhi", 5:"nyni",
                      6:"hwyhwi", 7:"ynsi"}

endings_alltenses = LostowPersonekOllAmser({endings_present.amser: endings_present,
                                            endings_preterite.amser: endings_preterite,
                                            endings_imperfect.amser: endings_imperfect,
                                            endings_pluperfect.amser: endings_pluperfect,
                                            endings_subj_pres.amser: endings_subj_pres,
                                            endings_subj_imp.amser: endings_subj_imp,
                                            endings_imperative.amser: endings_imperative,
                                            "ppl": ending_pastparticiple})
# lostow rag verbow gans i
# endings for verbs that use the i vowel
endings_alltenses_i = LostowPersonekOllAmser({endings_present.amser:endings_present.lostow_dict,
                                              endings_preterite_i.amser:endings_preterite_i.lostow_dict,
                                              endings_imperfect_i.amser:endings_imperfect_i.lostow_dict,
                                              endings_pluperfect.amser:endings_pluperfect.lostow_dict,
                                              endings_subj_pres.amser:endings_subj_pres.lostow_dict,
                                              endings_subj_imp.amser:endings_subj_imp.lostow_dict,
                                              endings_imperative.amser:endings_imperative.lostow_dict,
                                              "ppl":ending_pastparticiple})

# verbow ha'n ben an keth ha'n hanow verbek
# verbs with stem same as verbal noun
verbs_stemnoun = ["arvedh", "arveth", "astell", "aswonn", "daffar", "dalleth",
                  "dannvon", "daskorr", "dendil", "dervynn", "dewis", "diank",
                  "diberth", "difenn", "difres", "dolos", "dyerbynn", "godhav",
                  "godros", "gorhemmynn", "gormel", "gromyal", "gwari",
                  "gweres", "hepkorr", "hembronk", "hunros", "kanmel",
                  "kemmynn", "kuntell", "kynnik", "meythrin", "omdhal",
                  "omguntell", "omwen", "pe", "powes", "pregowth", "sommys",
                  "tynkyal", "yes"]

# verbow gans bogalenn i yn 3s tremenys
# verbs with i vowel in 3s preterite
verbs_i_3sp = ["aswonn", "attylli", "brewi", "dagrewi", "dedhewi", "dehweles",
               "demmedhi", "derivas", "diank", "dinewi", "dineythi",
               "diskrysi", "distrui", "domhwel", "dybri", "dynnerghi",
               "erghi", "godhav", "gorhemmynn", "gorthybi", "hedhi", "heveli",
               "kemmynna", "kentrewi", "kreuni", "krysi", "mollethi",
               "ombrederi", "omhweles", "prederi", "pysi", "synsi", "tevi",
               "tybi", "yeuni"]
# ha'n verbow gans -el
# plus all verbs in -el (not yet implemented)

# verbow gans bogalenn i yn anperfydh
# verbs with i vowel in imperfect
verbs_i_imp = ["amma", "aswonn", "dalleth", "dannvon", "dervynn", "dewis",
               "diberth", "difenn", "doen", "dyllo", "folhwerthin",
               "galloes", "godhav", "gonis", "govynn", "hembronk",
               "hwerthin", "lavasos", "minhwerthin", "omladh"]

#plus all verbs in -el, -es (except klywes and mynnes), -he and -i
verbs_tava = ["tava", "tardra", "kachya", "kampya", "shakya", "talkya"]
verbs_igeri_o = ["ankevi", "dasseni", "dasserghi", "dedhwi", "goderri",
                 "kelli", "kelmi", "keski", "kregi", "lenki", "leski",
                 "megi", "pedri", "perthi", "previ", "renki", "seni",
                 "serri", "telli", "terri", "treghi"]
verbs_igeri_a = ["dalleth", "diberth", "hwerthin", "minhwerthin", "peski"]
verbs_erghi_o = ["dagrewi", "dedhewi", "dinewi", "kentrewi", "kewsel",
                 "kynyewel", "mollethi"]
verbs_erghi_a = ["densel", "diank", "drehevel", "dynnerghi", "fyllel",
                 "godhevel", "gweskel", "heveli", "lemmel", "leverel",
                 "sevel", "terlemmel", "tewel", "tyli", "attyli"]
three_s_presfut_y = ["eva", "galloes", "gedya", "gweskel", "kavoes",
                     "kelli", "pobas", "tevi"]
verbs_lesta = ["bostya", "diwiska", "dyski", "gweskel", "gwiska", "kestya",
               "koska", "leski", "mostya", "ostya", "peski", "raska",
               "restya", "rostya", "tergoska", "trestya"]
verbs_gwystla = ["dampnya", "entra", "gustla", "gwandra", "handla", "hwystra",
                 "kentra", "moldra", "restra", "sklandra", "sompna",
                 "tardra", "tempra", "terlentri"]
verbs_hwithra = ["hwithra", "dybri", "fagla", "gwedhra", "hwedhla", "hwyrni",
                 "ladra", "lymna", "medra", "meythrin", "pedri", "pobla",
                 "ravna", "sotla", "sugna", "trobla", "resna", "sokra",
                 "fekla", "takla"]
verbs_gelwel = ["gelwel", "henwel", "lenwel", "merwel", "selwel"]
verbs_irregular = ["bos", "y'm beus", "darvos", "dos", "godhvos", "hwarvos",
                   "klywes", "omglywes", "mos", "piw", "tyli", "attyli",
                   "doen", "omdhoen", "dri", "dyllo", "gul", "ri", "ti",
                   "bryjyon"]

# vowel affectation y--> e in stem in some persons e.g. deber
verbs_dybri = ["dybri"]
# chanjyow ben kalesheans po dewblekheans
# hardening or doubling in ending of the stem
stem_changes = {"b":"pp", "bl":"ppl", "br":"ppr", "ch":"cch", "d":"tt",
                "dh":"tth", "dhl":"tthl", "dhr":"tthr", "dhw":"tthw",
                "dr":"ttr", "f":"ff", "g":"kk", "gh":"ggh", "gl":"kkl",
                "gn":"kkn", "he":"hah", "j":"cch", "k":"kk", "kl":"kkl",
                "kn":"kkn", "kr":"kkr", "l":"ll", "ld":"lt", "ldr":"ltr",
                "lv":"lf", "m":"mm", "mbl":"mpl", "mbr":"mpr", "n":"nn",
                "nd":"nt", "ndl":"ntl", "ndr":"ntr", "ng":"nk", "ngr":"nkr",
                "nj":"nch", "p":"pp", "r":"rr", "rd":"rt", "rdr":"rtr",
                "rdh":"rth", "rg":"rk", "rj":"rch", "rv":"rf", "s":"ss",
                "sh":"ssh", "sl":"ssl", "sn":"ssn", "sw":"ssw", "t":"tt",
                "th":"tth", "thl":"tthl", "thr":"tthr", "tl":"ttl", "v":"ff",
                "vn":"ffn", "vr":"ffr"}
vowels = ["a", "e", "i", "o", "u"]

# Verbow Anreyth
# Irregular verbs
# BOS
#need extra parameter to decide short/long
#say long = 0 or long = 1
#and another to distinguish usi/yma/eus and ymons/esons
#definite = 1 or definite = 0 to distinguish yma/usi from yma/eus
#affirmative = 1/0 to use yma/ymons in affirmative and usi/eus or esons in neg/interrog
# at present the above are implemented as separate tenses

# use short form as a default to avoid key error in dictionary
bos_shortpres = RannowVerbAnreyth("bos", "or", "ov", "os", "yw", "yw",
                                  "on", "owgh", "yns", "a-lemmyn")
bos_preterite = RannowVerbAnreyth("bos", "beus", "beuv", "beus", "beu", "beu",
                                  "beun", "bewgh", "bons", "tremenys")
bos_shortimperfect = RannowVerbAnreyth("bos", "os", "en", "es", "o", "o",
                                       "en", "ewgh", "ens", "anperfydh")
bos_pluperfect = RannowVerbAnreyth("bos", "bies", "bien", "bies", "bia", "bia",
                                   "bien", "biewgh", "biens", "gorperfydh")
bos_pressubj = RannowVerbAnreyth("bos", "ber", "biv", "bi", "bo", "bo",
                                 "byn", "bowgh", "bons", "islavarek_a-lemmyn")
bos_impfsubj = RannowVerbAnreyth("bos", "bes", "ben", "bes", "be", "be",
                                 "ben", "bewgh", "bens", "islavarek_anperfydh")
bos_imperative = RannowVerbAnreyth("bos", "NULL", "NULL", "bydh", "bedhes",
                                   "bedhes", "bedhen", "bedhewgh", "bedhens",
                                   "gorhemmyn")
bos_pastparticiple = "bedhys" # used only in compounds
bos_future = RannowVerbAnreyth("bos", "bydher", "bydhav", "bydhydh", "bydh",
                               "bydh", "bydhyn", "bydhowgh", "bydhons",
                               "devedhek")
bos_habitimperfect = RannowVerbAnreyth("bos", "bedhes", "bedhen", "bedhes",
                                       "bedha", "bedha", "bedhen", "bedhewgh",
                                       "bedhens", "anperfydh_usadow")
bos_longpres_indef = RannowVerbAnreyth("bos", "eder", "esov", "esos", "eus",
                                       "eus", "eson", "esowgh", "esons",
                                       "a-lemmyn_hir_indef")
bos_longpres_defni = RannowVerbAnreyth("bos", "eder", "esov", "esos", "usi",
                                       "usi", "eson", "esowgh", "esons",
                                       "a-lemmyn_hir_def")
bos_longpres_aff = RannowVerbAnreyth("bos", "eder", "esov", "esos", "yma",
                                     "yma", "eson", "esowgh", "ymons",
                                     "a-lemmyn_hir_aff")
bos_longimpf = RannowVerbAnreyth("bos", "eses", "esen", "eses", "esa", "esa",
                                 "esen", "esewgh", "esens", "anperfydh_hir")
bos_tenses = [bos_shortpres, bos_preterite, bos_shortimperfect, bos_pluperfect,
              bos_pressubj, bos_impfsubj, bos_imperative, bos_future,
              bos_habitimperfect, bos_longpres_indef, bos_longimpf,
              bos_longpres_defni, bos_longpres_aff]
bos_inflected = RannowVerbAnreythOllAmser("bos")
bos_inflected.add_tense_list(bos_tenses, bos_pastparticiple)


# Y'M BEUS
# y'th eus devedhek sempel hag anperfydh usadow
# has simple future and habitual imperfect
ymbeus_pres = RannowVerbAnreyth("y'm beus", "NULL", "y'm beus", "y'th eus",
                                "y'n jeves", "y's teves", "y'gan beus",
                                "y'gas beus", "y's teves", "a-lemmyn")
ymbeus_preterite = RannowVerbAnreyth("y'm beus", "NULL", "y'm beu", "y'feu",
                                     "y'n jeva", "y's teva", "y'gan beu",
                                     "y'gas beu", "y's teva", "tremenys")
ymbeus_imperfect = RannowVerbAnreyth("y'm beus", "NULL", "y'm bo", "y'th o",
                                     "y'n jevo", "y's tevo", "y'gan bo",
                                     "y'gas bo", "y's tevo", "anperfydh")
ymbeus_pluperfect = RannowVerbAnreyth("y'm beus", "NULL", "y'm bo", "y'th o",
                                      "y'n jevo", "y's tevo", "y'gan bo",
                                      "y'gas bo", "y's tevo", "gorperfydh")
ymbeus_pressubj = RannowVerbAnreyth("y'm beus", "NULL", "y'm bo", "y'fo",
                                    "y'n jeffo", "y's teffo", "y'gan bo",
                                    "y'gas bo", "y's teffo",
                                    "islavarek_a-lemmyn")
ymbeus_impfsubj = RannowVerbAnreyth("y'm beus", "NULL", "y'm be", "y'fe",
                                    "y'n jeffa", "y's teffa", "y'gan be",
                                    "y'gas be", "y's teffa",
                                    "islavarek_anperfydh")
ymbeus_future = RannowVerbAnreyth("y'm beus", "NULL", "y'm bydh", "y'fydh",
                                  "y'n jevydh", "y's tevydh", "y'gan bydh",
                                  "y'gas bydh", "y's tevydh", "devedhek")
ymbeus_habitimperfect = RannowVerbAnreyth("y'm beus", "NULL", "y'm bedha",
                                          "y'fedha", "y'n jevedha",
                                          "y's tevedha", "y'gan bedha",
                                          "y'gas bedha", "y's tevedha",
                                          "anperfydh_usadow")
ymbeus_tenses = [ymbeus_pres, ymbeus_preterite, ymbeus_imperfect,
                 ymbeus_pluperfect, ymbeus_pressubj, ymbeus_impfsubj,
                 ymbeus_future, ymbeus_habitimperfect]
# nag eus gorhemmyn
# no imperative
ymbeus_inflected = RannowVerbAnreythOllAmser("y'm beus")
ymbeus_inflected.add_tense_list(ymbeus_tenses)

# PIW
# y'th eus devedhek sempel hag anperfydh usadow
# has simple future and habitual imperfect
piw_pres = RannowVerbAnreyth("piw", "piwor", "piwov", "piwos", "piw", "piw",
                             "piwon", "piwowgh", "piwyns", "a-lemmyn")
piw_preterite = RannowVerbAnreyth("piw", "piwor", "piwev", "piwes", "piwva",
                                  "piwva", "piwven", "piwvewgh", "piwvons",
                                  "tremenys")
piw_imperfect = RannowVerbAnreyth("piw", "piwer", "piwen", "piwes", "piwo",
                                  "piwo", "piwen", "piwewgh", "piwens",
                                  "anperfydh")
piw_pluperfect = RannowVerbAnreyth("piw", "piwor", "piwvien", "piwvies",
                                   "piwvia", "piwvia", "piwvien", "piwviewgh",
                                   "piwviens", "gorperfydh")
piw_pressubj = RannowVerbAnreyth("piw", "piwver", "piwviv", "piwvi", "piwvo",
                                 "piwvo", "piwvyn", "piwvowgh", "piwvons",
                                 "islavarek_a-lemmyn")
piw_impfsubj = RannowVerbAnreyth("piw", "piwves", "piwven", "piwves", "piwva",
                                 "piwva", "piwven", "piwvewgh", "piwvens",
                                 "islavarek_anperfydh")
piw_future = RannowVerbAnreyth("piw", "piwor", "piwvydhav", "piwvydhydh",
                               "piwvydh", "piwvydh", "piwvydhyn",
                               "piwvydhowgh", "piwvydhons", "devedhek")
piw_habitimperfect = RannowVerbAnreyth("piw", "piwvedhes", "piwvedhen",
                                       "piwvedhes", "piwvedha", "piwvedha",
                                       "piwvedhen", "piwvedhewgh",
                                       "piwvedhens", "anperfydh_usadow")
piw_tenses = [piw_pres, piw_preterite, piw_imperfect, piw_pluperfect,
              piw_pressubj, piw_impfsubj, piw_future, piw_habitimperfect]
# nag eus gorhemmyn
# no imperative
piw_inflected = RannowVerbAnreythOllAmser("piw")
piw_inflected.add_tense_list(piw_tenses)

# GODHVOS
# a'th eus devedhek sempel mes nag anperfydh usadow
# has simple future but not habitual imperfect
godhvos_pres = RannowVerbAnreyth("godhvos", "godhor", "gonn", "godhes",
                                 "goer", "goer", "godhon", "godhowgh",
                                 "godhons", "a-lemmyn")
#2s pres/fut may contract to gosta

godhvos_preterite = RannowVerbAnreyth("godhvos", "godhves", "godhvev",
                                      "godhves", "godhva", "godhva", "godhven",
                                      "godhvewgh", "godhvons", "tremenys")

godhvos_imperfect = RannowVerbAnreyth("godhvos", "godhyes", "godhyen",
                                      "godhyes", "godhya", "godhya", "godhyen",
                                      "godhyewgh", "godhyens", "anperfydh")

godhvos_pluperfect = RannowVerbAnreyth("godhvos", "godhvies", "godhvien",
                                       "godhvies", "godhvia", "godhvia",
                                       "godhvien", "godhviewgh", "godhviens",
                                       "gorperfydh")

godhvos_pressubj = RannowVerbAnreyth("godhvos", "godher", "godhviv", "godhvi",
                                     "godhvo", "godhvo", "godhvyn", "godhvowgh",
                                     "godhvons", "islavarek_a-lemmyn")

godhvos_impfsubj = RannowVerbAnreyth("godhvos", "godhves", "godhven", "godhves",
                                     "godhve", "godhve", "godhven", "godhvewgh",
                                     "godhvens", "islavarek_anperfydh")

godhvos_imperative = RannowVerbAnreyth("godhvos", "NULL", "NULL", "godhvydh",
                                       "godhvydhes", "godhvydhes", "godhvydhyn",
                                       "godhvydhewgh", "godhvydhens",
                                       "gorhemmyn")

godhvos_pastparticiple = "godhvedhys"

godhvos_future = RannowVerbAnreyth("godhvos", "godhvydher", "godhvydhav",
                                   "godhvydhydh", "godhvydh", "godhvydh",
                                   "godhvydhyn", "godhvydhowgh", "godhvydhons",
                                   "devedhek")

godhvos_tenses = [godhvos_pres, godhvos_preterite, godhvos_imperfect,
                  godhvos_pluperfect, godhvos_pressubj, godhvos_impfsubj,
                  godhvos_imperative, godhvos_future]
godhvos_inflected = RannowVerbAnreythOllAmser("godhvos")
godhvos_inflected.add_tense_list(godhvos_tenses, godhvos_pastparticiple)

# TYLI
# a'th eus devedhek sempel mes nag anperfydh usadow
# has simple future but not habitual imperfect
tyli_pres = RannowVerbAnreyth("tyli", "tylir", "talav", "tylydh", "tal", "tal",
                              "tylyn", "tylowgh", "talons", "a-lemmyn")
tyli_preterite = RannowVerbAnreyth("tyli", "tylys", "tylis", "tylsys", "tylis",
                                   "tylis", "tylsyn", "tylsowgh", "talsons",
                                   "tremenys")
tyli_imperfect = RannowVerbAnreyth("tyli", "teles", "telen", "teles", "tela",
                                   "tela", "telen", "telewgh", "telens",
                                   "anperfydh")
tyli_pluperfect = RannowVerbAnreyth("tyli", "talvies", "talvien", "talvies",
                                    "talvia", "talvia", "talvien", "talviewgh",
                                    "talviens", "gorperfydh")
tyli_pressubj = RannowVerbAnreyth("tyli", "taller", "tylliv", "tylli", "tallo",
                                  "tallo", "tyllyn", "tyllowgh", "tallons",
                                  "islavarek_a-lemmyn")
tyli_impfsubj = RannowVerbAnreyth("tyli", "tallfes", "tallfen", "tallfes",
                                  "tallfa", "tallfa", "tallfen", "tallfewgh",
                                  "tallfens", "islavarek_anperfydh")
tyli_imperative = RannowVerbAnreyth("tyli", "NULL", "NULL", "tal", "teles",
                                    "teles", "telen", "telewgh", "telens",
                                    "gorhemmyn")

tyli_pastparticiple = "tylys"
tyli_future = RannowVerbAnreyth("tyli", "talvydher", "talvydhav", "talvydhydh",
                                "talvydh", "talvydh", "talvydhyn",
                                "talvydhowgh", "talvydhons", "devedhek")

tyli_tenses = [tyli_pres, tyli_preterite, tyli_imperfect, tyli_pluperfect,
               tyli_pressubj, tyli_impfsubj, tyli_imperative, tyli_future]
tyli_inflected = RannowVerbAnreythOllAmser("tyli")
tyli_inflected.add_tense_list(tyli_tenses, tyli_pastparticiple)

# ATTYLI
# kepar ha TYLI
# conjugated as TYLI
attyli_pres = RannowVerbAnreyth("attyli", "attylir", "attalav", "attylydh",
                                "attal", "attal", "attylyn", "attylowgh",
                                "attalons", "a-lemmyn")
attyli_preterite = RannowVerbAnreyth("attyli", "attylys", "attylis",
                                     "attylsys", "attylis", "attylis",
                                     "attylsyn", "attylsowgh", "attalsons",
                                     "tremenys")
attyli_imperfect = RannowVerbAnreyth("attyli", "atteles", "attelen", "atteles",
                                     "attela", "attela", "attelen", "attelewgh",
                                     "attelens", "anperfydh")
attyli_pluperfect = RannowVerbAnreyth("attyli", "attalvies", "attalvien",
                                      "attalvies", "attalvia", "attalvia",
                                      "attalvien", "attalviewgh", "attalviens",
                                      "gorperfydh")
attyli_pressubj = RannowVerbAnreyth("attyli", "attaller", "attylliv", "attylli",
                                    "attallo", "attallo", "attyllyn",
                                    "attyllowgh", "attallons",
                                    "islavarek_a-lemmyn")
attyli_impfsubj = RannowVerbAnreyth("attyli", "attallfes", "attallfen",
                                    "attallfes", "attallfa", "attallfa",
                                    "attallfen", "attallfewgh", "attallfens",
                                    "islavarek_anperfydh")
attyli_imperative = RannowVerbAnreyth("attyli", "NULL", "NULL", "attal",
                                      "atteles", "atteles", "attelen",
                                      "attelewgh", "attelens", "gorhemmyn")

attyli_pastparticiple = "attylys"
attyli_future = RannowVerbAnreyth("attyli", "attalvydher", "attalvydhav",
                                  "attalvydhydh", "attalvydh", "attalvydh",
                                  "attalvydhyn", "attalvydhowgh",
                                  "attalvydhons", "devedhek")

attyli_tenses = [attyli_pres, attyli_preterite, attyli_imperfect,
                 attyli_pluperfect, attyli_pressubj, attyli_impfsubj,
                 attyli_imperative, attyli_future]
attyli_inflected = RannowVerbAnreythOllAmser("attyli")
attyli_inflected.add_tense_list(attyli_tenses, attyli_pastparticiple)

# HWARVOS
# 3s yn unnsel
# only found in 3s
hwarvos_pres = RannowVerbAnreyth("hwarvos", "NULL", "NULL", "NULL", "hwer",
                                 "hwer", "NULL", "NULL", "NULL", "a-lemmyn")
hwarvos_preterite = RannowVerbAnreyth("hwarvos", "NULL", "NULL", "NULL",
                                      "hwarva", "hwarva", "NULL", "NULL",
                                      "NULL", "tremenys")
hwarvos_imperfect = RannowVerbAnreyth("hwarvos", "NULL", "NULL", "NULL",
                                      "NULL", "NULL", "NULL", "NULL", "NULL",
                                      "anperfydh")
hwarvos_pluperfect = RannowVerbAnreyth("hwarvos", "NULL", "NULL", "NULL",
                                       "hwarvia", "hwarvia", "NULL", "NULL",
                                       "NULL", "gorperfydh")
hwarvos_pressubj = RannowVerbAnreyth("hwarvos", "NULL", "NULL", "NULL",
                                     "hwarvo", "hwarvo", "NULL", "NULL",
                                     "NULL", "islavarek_a-lemmyn")
hwarvos_impfsubj = RannowVerbAnreyth("hwarvos", "NULL", "NULL", "NULL",
                                     "hwarva", "hwarva", "NULL", "NULL",
                                     "NULL", "islavarek_anperfydh")
hwarvos_pastparticiple = "hwarvedhys"
hwarvos_future = RannowVerbAnreyth("hwarvos", "NULL", "NULL", "NULL",
                                   "hwyrvydh", "hwyrvydh", "NULL", "NULL",
                                   "NULL", "devedhek")
hwarvos_tenses = [hwarvos_pres, hwarvos_preterite, hwarvos_pluperfect,
                  hwarvos_pressubj, hwarvos_impfsubj, hwarvos_future]
hwarvos_inflected = RannowVerbAnreythOllAmser("hwarvos")
hwarvos_inflected.add_tense_list(hwarvos_tenses, hwarvos_pastparticiple)

# DARVOS
# only 3s pret and past participle
# 3s tremenys ha ppl yn unnsel
darvos_preterite = RannowVerbAnreyth("darvos", "NULL", "NULL", "NULL", "darva",
                                     "darva", "NULL", "NULL", "NULL",
                                     "tremenys")
darvos_pastparticiple = "darvedhys"
darvos_tenses = [darvos_preterite]
darvos_inflected = RannowVerbAnreythOllAmser("darvos")
darvos_inflected.add_tense_list(darvos_tenses, darvos_pastparticiple)

# KLYWES
# no simple future or habitual imperfect

klywes_pres = RannowVerbAnreyth("klywes", "klywir", "klywav", "klywydh",
                                "klyw", "klyw", "klywyn", "klywowgh",
                                "klywons", "a-lemmyn")
klywes_preterite = RannowVerbAnreyth("klywes", "klywas", "klywis", "klywsys",
                                     "klywas", "klywas", "klywsyn",
                                     "klywsowgh", "klywsons", "tremenys")
klywes_imperfect = RannowVerbAnreyth("klywes", "klywes", "klywen", "klywes",
                                     "klywo", "klywo", "klywen", "klywewgh",
                                     "klywens", "anperfydh")
klywes_pluperfect = RannowVerbAnreyth("klywes", "klywsys", "klywsen", "klywses",
                                      "klywsa", "klywsa", "klywsen",
                                      "klywsewgh", "klywsens", "gorperfydh")
klywes_pressubj = RannowVerbAnreyth("klywes", "klywver", "klywviv", "klywvi",
                                    "klywvo", "klywvo", "klywvyn", "klywvowgh",
                                    "klywvons", "islavarek_a-lemmyn")
klywes_impfsubj = RannowVerbAnreyth("klywes", "klywves", "klywven", "klywves",
                                    "klywva", "klywva", "klywven", "klywvewgh",
                                    "klywvens", "islavarek_anperfydh")
klywes_imperative = RannowVerbAnreyth("klywes", "NULL", "NULL", "klyw",
                                      "klywes", "klywes", "klywyn", "klywewgh",
                                      "klywens", "gorhemmyn")
klywes_pastparticiple = "klywys"
klywes_tenses = [klywes_pres, klywes_preterite, klywes_imperfect,
                 klywes_pluperfect, klywes_pressubj, klywes_impfsubj,
                 klywes_imperative]
klywes_inflected = RannowVerbAnreythOllAmser("klywes")
klywes_inflected.add_tense_list(klywes_tenses, klywes_pastparticiple)

#OMGLYWES similarly conjugated
omglywes_pres = RannowVerbAnreyth("omglywes", "omglywir", "omglywav",
                                  "omglywydh", "omglyw", "omglyw", "omglywyn",
                                  "omglywowgh", "omglywons", "a-lemmyn")
omglywes_preterite = RannowVerbAnreyth("omglywes", "omglywas", "omglywis",
                                       "omglywsys", "omglywas", "omglywas",
                                       "omglywsyn", "omglywsowgh",
                                       "omglywsons", "tremenys")
omglywes_imperfect = RannowVerbAnreyth("omglywes", "omglywes", "omglywen",
                                       "omglywes", "omglywo", "omglywo",
                                       "omglywen", "omglywewgh", "omglywens",
                                       "anperfydh")
omglywes_pluperfect = RannowVerbAnreyth("omglywes", "omglywsys", "omglywsen",
                                        "omglywses", "omglywsa", "omglywsa",
                                        "omglywsen", "omglywsewgh",
                                        "omglywsens", "gorperfydh")
omglywes_pressubj = RannowVerbAnreyth("omglywes", "omglywver", "omglywviv",
                                      "omglywvi", "omglywvo", "omglywvo",
                                      "omglywvyn", "omglywvowgh", "omglywvons",
                                      "islavarek_a-lemmyn")
omglywes_impfsubj = RannowVerbAnreyth("omglywes", "omglywves", "omglywven",
                                      "omglywves", "omglywva", "omglywva",
                                      "omglywven", "omglywvewgh", "omglywvens",
                                      "islavarek_anperfydh")
omglywes_imperative = RannowVerbAnreyth("omglywes", "NULL", "NULL", "omglyw",
                                        "omglywes", "omglywes", "omglywyn",
                                        "omglywewgh", "omglywens", "gorhemmyn")
omglywes_pastparticiple = "omglywys"
omglywes_tenses = [omglywes_pres, omglywes_preterite, omglywes_imperfect,
                   omglywes_pluperfect, omglywes_pressubj, omglywes_impfsubj,
                   omglywes_imperative]
omglywes_inflected = RannowVerbAnreythOllAmser("omglywes")
omglywes_inflected.add_tense_list(omglywes_tenses, omglywes_pastparticiple)


# MOS/MONES
# a'th eus amser perfydh
# special perfect tense
mos_pres = RannowVerbAnreyth("mos", "er", "av", "edh", "a", "a", "en", "ewgh",
                             "ons", "a-lemmyn")
mos_preterite = RannowVerbAnreyth("mos", "es", "yth", "ythys", "eth", "eth",
                                  "ethen", "ethewgh", "ethons", "tremenys")
mos_imperfect = RannowVerbAnreyth("mos", "es", "en", "es", "e", "e", "en",
                                  "ewgh", "ens", "anperfydh")
mos_pluperfect = RannowVerbAnreyth("mos", "NULL", "gylsen", "gylses", "galsa",
                                   "galsa", "gylsen", "gylsewgh", "gylsens",
                                   "gorperfydh")
mos_perfect = RannowVerbAnreyth("mos", "NULL", "galsov", "galsos", "gallas",
                                "gallas", "galson", "galsowgh", "galsons",
                                "perfydh")
mos_pressubj = RannowVerbAnreyth("mos", "eller", "ylliv", "ylli", "ello",
                                 "ello", "yllyn", "yllowgh", "ellons",
                                 "islavarek_a-lemmyn")
mos_impfsubj = RannowVerbAnreyth("mos", "elles", "ellen", "elles", "ella",
                                 "ella", "ellen", "ellewgh", "ellens",
                                 "islavarek_anperfydh")
mos_imperative = RannowVerbAnreyth("mos", "NULL", "NULL", "ke", "es", "es",
                                   "deun", "kewgh", "ens", "gorhemmyn")
mos_pastparticiple = "gyllys"
mos_tenses = [mos_pres, mos_preterite, mos_imperfect, mos_pluperfect,
              mos_pressubj, mos_impfsubj, mos_imperative, mos_perfect]
mos_inflected = RannowVerbAnreythOllAmser("mos")
mones_inflected = RannowVerbAnreythOllAmser("mones")
mos_inflected.add_tense_list(mos_tenses, mos_pastparticiple)
mones_inflected.add_tense_list(mos_tenses, mos_pastparticiple)


# DOS/DONES
# a'th eus amser perfydh
# special perfect tense
dos_pres = RannowVerbAnreyth("dos", "deer", "dov", "deudh", "deu", "deu",
                             "deun", "dewgh", "dons", "a-lemmyn")
dos_preterite = RannowVerbAnreyth("dos", "deuthes", "deuth", "deuthys",
                                  "deuth", "deuth", "deuthen", "deuthewgh",
                                  "deuthons", "tremenys")
dos_imperfect = RannowVerbAnreyth("dos", "des", "den", "des", "do", "do",
                                  "den", "dewgh", "dens", "anperfydh")
dos_pluperfect = RannowVerbAnreyth("dos", "dothyes", "dothyen", "dothyes",
                                   "dothya", "dothya", "dothyen", "dothyewgh",
                                   "dothyens", "gorperfydh")
dos_perfect = RannowVerbAnreyth("dos", "deuves", "deuvev", "deuves", "deuva",
                                "deuva", "deuven", "deuvewgh", "deuvons",
                                "perfydh")
dos_pressubj = RannowVerbAnreyth("dos", "deffer", "dyffiv", "dyffi", "deffo",
                                 "deffo", "dyffyn", "dyffowgh", "deffons",
                                 "islavarek_a-lemmyn")
dos_impfsubj = RannowVerbAnreyth("dos", "deffes", "deffen", "deffes", "deffa",
                                 "deffa", "deffen", "deffewgh", "deffens",
                                 "islavarek_anperfydh")
dos_imperative = RannowVerbAnreyth("dos", "NULL", "NULL", "deus", "des",
                                   "des", "deun", "dewgh", "dens", "gorhemmyn")
dos_pastparticiple = "devedhys"
dos_tenses = [dos_pres, dos_preterite, dos_imperfect, dos_pluperfect,
              dos_pressubj, dos_impfsubj, dos_imperative, dos_perfect]
dos_inflected = RannowVerbAnreythOllAmser("dos")
dones_inflected = RannowVerbAnreythOllAmser("dones")
dos_inflected.add_tense_list(dos_tenses, dos_pastparticiple)
dones_inflected.add_tense_list(dos_tenses, dos_pastparticiple)

#DOEN
doen_pres = RannowVerbAnreyth("doen", "degir", "degav", "degedh", "deg", "deg",
                              "degon", "degowgh", "degons", "a-lemmyn")
doen_preterite = RannowVerbAnreyth("doen", "dug", "dug", "duges", "dug", "dug",
                                   "dugon", "dugowgh", "dugons", "tremenys")
doen_imperfect = RannowVerbAnreyth("doen", "degys", "degyn", "degys", "degi",
                                   "degi", "degyn", "degewgh", "degens",
                                   "anperfydh")
doen_pluperfect = RannowVerbAnreyth("doen", "degsys", "degsen", "degses",
                                    "degsa", "degsa", "degsen", "degsewgh",
                                    "degsens", "gorperfydh")
doen_pressubj = RannowVerbAnreyth("doen", "dokker", "dykkiv", "dykki", "dokko",
                                  "dokko", "dykkyn", "dykkowgh", "dokkons",
                                  "islavarek_a-lemmyn")
doen_impfsubj = RannowVerbAnreyth("doen", "dekkys", "dekken", "dekkes",
                                  "dekka", "dekka", "dekken", "dekkewgh",
                                  "dekkens", "islavarek_anperfydh")
doen_imperative = RannowVerbAnreyth("doen", "NULL", "NULL", "dog", "deges",
                                    "deges", "degyn", "degewgh", "degens",
                                    "gorhemmyn")
doen_pastparticiple = "degys"
doen_tenses = [doen_pres, doen_preterite, doen_imperfect, doen_pluperfect,
               doen_pressubj, doen_impfsubj, doen_imperative]
doen_inflected = RannowVerbAnreythOllAmser("doen")
doen_inflected.add_tense_list(doen_tenses, doen_pastparticiple)

# OMDHOEN
# kepar ha doen
# conjugated as for doen
omdhoen_pres = RannowVerbAnreyth("omdhoen", "omdhegir", "omdhegav", "omdhegedh",
                                 "omdheg", "omdheg", "omdhegon", "omdhegowgh",
                                 "omdhegons", "a-lemmyn")
omdhoen_preterite = RannowVerbAnreyth("omdhoen", "omdhug", "omdhug", "omdhuges",
                                      "omdhug", "omdhug", "omdhugon",
                                      "omdhugowgh", "omdhugons", "tremenys")
omdhoen_imperfect = RannowVerbAnreyth("omdhoen", "omdhegys", "omdhegyn",
                                      "omdhegys", "omdhegi", "omdhegi",
                                      "omdhegyn", "omdhegewgh", "omdhegens",
                                      "anperfydh")
omdhoen_pluperfect = RannowVerbAnreyth("omdhoen", "omdhegsys", "omdhegsen",
                                       "omdhegses", "omdhegsa", "omdhegsa",
                                       "omdhegsen", "omdhegsewgh", "omdhegsens",
                                       "gorperfydh")
omdhoen_pressubj = RannowVerbAnreyth("omdhoen", "omdhokker", "omdhykkiv",
                                     "omdhykki", "omdhokko", "omdhokko",
                                     "omdhykkyn", "omdhykkowgh", "omdhokkons",
                                     "islavarek_a-lemmyn")
omdhoen_impfsubj = RannowVerbAnreyth("omdhoen", "omdhekkys", "omdhekken",
                                     "omdhekkes", "omdhekka", "omdhekka",
                                     "omdhekken", "omdhekkewgh", "omdhekkens",
                                     "islavarek_anperfydh")
omdhoen_imperative = RannowVerbAnreyth("omdhoen", "NULL", "NULL", "omdhog",
                                       "omdheges", "omdheges", "omdhegyn",
                                       "omdhegewgh", "omdhegens", "gorhemmyn")
omdhoen_pastparticiple = "omdhegys"
omdhoen_tenses = [omdhoen_pres, omdhoen_preterite, omdhoen_imperfect,
                  omdhoen_pluperfect, omdhoen_pressubj, omdhoen_impfsubj,
                  omdhoen_imperative]
omdhoen_inflected = RannowVerbAnreythOllAmser("omdhoen")
omdhoen_inflected.add_tense_list(omdhoen_tenses, omdhoen_pastparticiple)

#RI
ri_pres = RannowVerbAnreyth("ri", "rer", "rov", "redh", "re", "re", "ren",
                            "rowgh", "rons", "a-lemmyn")
ri_preterite = RannowVerbAnreyth("ri", "ros", "res", "resys", "ros", "ros",
                                 "resen", "resowgh", "rosons", "tremenys")
ri_imperfect = RannowVerbAnreyth("ri", "res", "ren", "res", "ri", "ri", "ren",
                                 "rewgh", "rens", "anperfydh")
ri_pluperfect = RannowVerbAnreyth("ri", "rosys", "rosen", "roses", "rosa",
                                  "rosa", "rosen", "rosewgh", "rosens",
                                  "gorperfydh")
ri_pressubj = RannowVerbAnreyth("ri", "roller", "rylliv", "rylli", "rollo",
                                "rollo", "ryllyn", "ryllowgh", "rollons",
                                "islavarek_a-lemmyn")
ri_impfsubj = RannowVerbAnreyth("ri", "rollys", "rollen", "rolles", "rolla",
                                "rolla", "rollen", "rollewgh", "rollens",
                                "islavarek_anperfydh")
ri_imperative = RannowVerbAnreyth("ri", "NULL", "NULL", "ro", "res", "res",
                                  "ren", "rewgh", "rens", "gorhemmyn")
ri_pastparticiple = "res"
ri_tenses = [ri_pres, ri_preterite, ri_imperfect, ri_pluperfect, ri_pressubj,
             ri_impfsubj, ri_imperative]
ri_inflected = RannowVerbAnreythOllAmser("ri")
ri_inflected.add_tense_list(ri_tenses, ri_pastparticiple)
# ro/roy kyns kessonenn / bogalenn
# ro/roy used before consonant/vowel


#DRI
# kepar ha RI
# conjugated as for RI
dri_pres = RannowVerbAnreyth("dri", "drer", "drov", "dredh", "dre", "dre",
                             "dren", "drowgh", "drons", "a-lemmyn")
dri_preterite = RannowVerbAnreyth("dri", "dros", "dres", "dresys", "dros",
                                  "dros", "dresen", "dresowgh", "drosons",
                                  "tremenys")
dri_imperfect = RannowVerbAnreyth("dri", "dres", "dren", "dres", "dri", "dri",
                                  "dren", "drewgh", "drens", "anperfydh")
dri_pluperfect = RannowVerbAnreyth("dri", "drosys", "drosen", "droses",
                                   "drosa", "drosa", "drosen", "drosewgh",
                                   "drosens", "gorperfydh")
dri_pressubj = RannowVerbAnreyth("dri", "droller", "drylliv", "drylli",
                                 "drollo", "drollo", "dryllyn", "dryllowgh",
                                 "drollons", "islavarek_a-lemmyn")
dri_impfsubj = RannowVerbAnreyth("dri", "drollys", "drollen", "drolles",
                                 "drolla", "drolla", "drollen", "drollewgh",
                                 "drollens", "islavarek_anperfydh")
dri_imperative = RannowVerbAnreyth("dri", "NULL", "NULL", "dro", "dres",
                                   "dres", "dren", "drewgh", "drens",
                                   "gorhemmyn")
dri_pastparticiple = "dres"
dri_tenses = [dri_pres, dri_preterite, dri_imperfect, dri_pluperfect,
              dri_pressubj, dri_impfsubj, dri_imperative]
dri_inflected = RannowVerbAnreythOllAmser("dri")
dri_inflected.add_tense_list(dri_tenses, dri_pastparticiple)
# doro/doroy kyns kessonenn /bogalenn
#doro/doroy before const/vowel

#TI 'swear
ti_pres = RannowVerbAnreyth("ti", "ter", "tov", "tedh", "te", "te", "ten",
                            "towgh", "tons", "a-lemmyn")
ti_preterite = RannowVerbAnreyth("ti", "tos", "tes", "tesys", "tos", "tos",
                                 "tesen", "tesowgh", "tosons", "tremenys")
ti_imperfect = RannowVerbAnreyth("ti", "tes", "ten", "tes", "te", "te", "ten",
                                 "tewgh", "tens", "anperfydh")
ti_pluperfect = RannowVerbAnreyth("ti", "tosys", "tosen", "toses", "tosa",
                                  "tosa", "tosen", "tosewgh", "tosens",
                                  "gorperfydh")
ti_pressubj = RannowVerbAnreyth("ti", "toller", "tylliv", "tylli", "tollo",
                                "tollo", "tyllyn", "tyllowgh", "tollons",
                                "islavarek_a-lemmyn")
ti_impfsubj = RannowVerbAnreyth("ti", "tollys", "tollen", "tolles", "tolla",
                                "tolla", "tollen", "tollewgh", "tollens",
                                "islavarek_anperfydh")
ti_imperative = RannowVerbAnreyth("ti", "NULL", "NULL", "to", "tes", "tes",
                                  "ten", "tewgh", "tens", "gorhemmyn")
ti_pastparticiple = "tes"
ti_tenses = [ti_pres, ti_preterite, ti_imperfect, ti_pluperfect, ti_pressubj,
             ti_impfsubj, ti_imperative]
ti_inflected = RannowVerbAnreythOllAmser("ti")
ti_inflected.add_tense_list(ti_tenses, ti_pastparticiple)
# ti 'to' yw reyth
# ti 'roof' is regular (not implemented)

#DYLLO
dyllo_pres = RannowVerbAnreyth("dyllo", "dyllir", "dyllav", "dyllydh", "dyllo",
                               "dyllo", "dyllyn", "dyllowgh", "dyllons",
                               "a-lemmyn")
dyllo_preterite = RannowVerbAnreyth("dyllo", "dellos", "delles", "dellesys",
                                    "dellos", "dellos", "dellesyn",
                                    "dellesowgh", "dellesons", "tremenys")
dyllo_imperfect = RannowVerbAnreyth("dyllo", "dyllys", "dyllyn", "dyllys",
                                    "dylli", "dylli", "dyllyn", "dyllewgh",
                                    "dyllens", "anperfydh")
dyllo_pluperfect = RannowVerbAnreyth("dyllo", "dyllsys", "dyllsen", "dyllses",
                                     "dyllsa", "dyllsa", "dyllsen", "dyllsewgh",
                                     "dyllsens", "gorperfydh")
dyllo_pressubj = RannowVerbAnreyth("dyllo", "dyller", "dylliv", "dylli",
                                   "dello", "dello", "dyllyn", "dyllowgh",
                                   "dellons", "islavarek_a-lemmyn")
dyllo_impfsubj = RannowVerbAnreyth("dyllo", "dellys", "dellen", "delles",
                                   "della", "della", "dellen", "dellewgh",
                                   "dellens", "islavarek_anperfydh")
dyllo_imperative = RannowVerbAnreyth("dyllo", "NULL", "NULL", "dyllo",
                                     "dylles", "dylles", "dyllyn", "dyllewgh",
                                     "dyllens", "gorhemmyn")
dyllo_pastparticiple = "dyllys"
dyllo_tenses = [dyllo_pres, dyllo_preterite, dyllo_imperfect, dyllo_pluperfect,
                dyllo_pressubj, dyllo_impfsubj, dyllo_imperative]
dyllo_inflected = RannowVerbAnreythOllAmser("dyllo")
dyllo_inflected.add_tense_list(dyllo_tenses, dyllo_pastparticiple)

#GUL

gul_pres = RannowVerbAnreyth("gul", "gwrer", "gwrav", "gwredh", "gwra", "gwra",
                             "gwren", "gwrewgh", "gwrons", "a-lemmyn")
gul_preterite = RannowVerbAnreyth("gul", "gwrug", "gwrug", "gwrussys", "gwrug",
                                  "gwrug", "gwrussyn", "gwrussowgh",
                                  "gwrussons", "tremenys")
gul_imperfect = RannowVerbAnreyth("gul", "gwres", "gwren", "gwres", "gwre",
                                  "gwre", "gwren", "gwrewgh", "gwrens",
                                  "anperfydh")
gul_pluperfect = RannowVerbAnreyth("gul", "gwrussys", "gwrussen", "gwrusses",
                                   "gwrussa", "gwrussa", "gwrussen",
                                   "gwrussewgh", "gwrussens", "gorperfydh")
gul_pressubj = RannowVerbAnreyth("gul", "gwreller", "gwrylliv", "gwrylli",
                                 "gwrello", "gwrello", "gwryllyn", "gwryllowgh",
                                 "gwrellons", "islavarek_a-lemmyn")
gul_impfsubj = RannowVerbAnreyth("gul", "gwrellys", "gwrellen", "gwrelles",
                                 "gwrella", "gwrella", "gwrellen", "gwrellewgh",
                                 "gwrellens", "islavarek_anperfydh")
gul_imperative = RannowVerbAnreyth("gul", "NULL", "NULL", "gwra", "gwres",
                                   "gwres", "gwren", "gwrewgh", "gwrens",
                                   "gorhemmyn")
gul_pastparticiple = "gwrys"
gul_tenses = [gul_pres, gul_preterite, gul_imperfect, gul_pluperfect,
              gul_pressubj, gul_impfsubj, gul_imperative]
gul_inflected = RannowVerbAnreythOllAmser("gul")
gul_inflected.add_tense_list(gul_tenses, gul_pastparticiple)

#OMWUL
# kepar ha GUL
# conjugated as GUL
omwul_pres = RannowVerbAnreyth("omwul", "omwrer", "omwrav", "omwredh", "omwra",
                               "omwra", "omwren", "omwrewgh", "omwrons",
                               "a-lemmyn")
omwul_preterite = RannowVerbAnreyth("omwul", "omwrug", "omwrug", "omwrussys",
                                    "omwrug", "omwrug", "omwrussyn",
                                    "omwrussowgh", "omwrussons", "tremenys")
omwul_imperfect = RannowVerbAnreyth("omwul", "omwres", "omwren", "omwres",
                                    "omwre", "omwre", "omwren", "omwrewgh",
                                    "omwrens", "anperfydh")
omwul_pluperfect = RannowVerbAnreyth("omwul", "omwrussys", "omwrussen",
                                     "omwrusses", "omwrussa", "omwrussa",
                                     "omwrussen", "omwrussewgh", "omwrussens",
                                     "gorperfydh")
omwul_pressubj = RannowVerbAnreyth("omwul", "omwreller", "omwrylliv",
                                   "omwrylli", "omwrello", "omwrello",
                                   "omwryllyn", "omwryllowgh", "omwrellons",
                                   "islavarek_a-lemmyn")
omwul_impfsubj = RannowVerbAnreyth("omwul", "omwrellys", "omwrellen",
                                   "omwrelles", "omwrella", "omwrella",
                                   "omwrellen", "omwrellewgh", "omwrellens",
                                   "islavarek_anperfydh")
omwul_imperative = RannowVerbAnreyth("omwul", "NULL", "NULL", "omwra",
                                     "omwres", "omwres", "omwren", "omwrewgh",
                                     "omwrens", "gorhemmyn")
omwul_pastparticiple = "omwrys"
omwul_tenses = [omwul_pres, omwul_preterite, omwul_imperfect, omwul_pluperfect,
                omwul_pressubj, omwul_impfsubj, omwul_imperative]
omwul_inflected = RannowVerbAnreythOllAmser("omwul")
omwul_inflected.add_tense_list(omwul_tenses, omwul_pastparticiple)

#MYNNES
mynnes_pres = RannowVerbAnreyth("mynnes", "mynnir", "mynnav", "mynnydh",
                                "mynn", "mynn", "mynnyn", "mynnowgh",
                                "mynnons", "a-lemmyn")
mynnes_preterite = RannowVerbAnreyth("mynnes", "mynnas", "mynnis", "mynnsys",
                                     "mynnas", "mynnas", "mynnsyn",
                                     "mynnsowgh", "mynnsons", "tremenys")
mynnes_imperfect = RannowVerbAnreyth("mynnes", "mynnys", "mynnen", "mynnes",
                                     "mynna", "mynna", "mynnen", "mynnewgh",
                                     "mynnens", "anperfydh")
mynnes_pluperfect = RannowVerbAnreyth("mynnes", "mynnsys", "mynnsen",
                                      "mynnses", "mynnsa", "mynnsa", "mynnsen",
                                      "mynnsewgh", "mynnsens", "gorperfydh")
mynnes_pressubj = RannowVerbAnreyth("mynnes", "mynner", "mynniv", "mynni",
                                    "mynno", "mynno", "mynnyn", "mynnowgh",
                                    "mynnons", "islavarek_a-lemmyn")
mynnes_impfsubj = RannowVerbAnreyth("mynnes", "mynnys", "mynnen", "mynnes",
                                    "mynna", "mynna", "mynnen", "mynnewgh",
                                    "mynnens", "islavarek_anperfydh")
mynnes_tenses = [mynnes_pres, mynnes_preterite, mynnes_imperfect,
                 mynnes_pluperfect, mynnes_pressubj, mynnes_impfsubj]
# nag eus gorhemmyn
# no imperative
mynnes_inflected = RannowVerbAnreythOllAmser("mynnes")
mynnes_inflected.add_tense_list(mynnes_tenses)

#GALLOES
galloes_pres = RannowVerbAnreyth("galloes", "gyllir", "gallav", "gyllydh",
                                 "gyll", "gyll", "gyllyn", "gyllowgh",
                                 "gyllons", "a-lemmyn")
galloes_preterite = RannowVerbAnreyth("galloes", "gallas", "gyllis", "gyllsys",
                                      "gallas", "gallas", "gyllsyn",
                                      "gyllsowgh", "gallsons", "tremenys")
galloes_imperfect = RannowVerbAnreyth("galloes", "gyllys", "gyllyn", "gyllys",
                                      "gylli", "gylli", "gyllyn", "gyllewgh",
                                      "gyllens", "anperfydh")
galloes_pluperfect = RannowVerbAnreyth("galloes", "gallses", "gallsen",
                                       "gallses", "gallsa", "gallsa",
                                       "gallsen", "gallsewgh", "gallsens",
                                       "gorperfydh")
galloes_pressubj = RannowVerbAnreyth("galloes", "galler", "gylliv", "gylli",
                                     "gallo", "gallo", "gyllyn", "gyllowgh",
                                     "gallons", "islavarek_a-lemmyn")
galloes_impfsubj = RannowVerbAnreyth("galloes", "galles", "gallen", "galles",
                                     "galla", "galla", "gallen", "gallewgh",
                                     "gallens", "islavarek_anperfydh")
galloes_tenses = [galloes_pres, galloes_preterite, galloes_imperfect,
                  galloes_pluperfect, galloes_pressubj, galloes_impfsubj]
# nag eus gorhemmyn
# no imperative
#pluperfect conditional is gallser (not implemented)
galloes_inflected = RannowVerbAnreythOllAmser("galloes")
galloes_inflected.add_tense_list(galloes_tenses)

# BRYJYON
bryjyon_pres = RannowVerbAnreyth("bryjyon", "bryjir", "brojyav", "bryjydh",
                                 "bros", "bros", "bryjyn", "bryjyowgh",
                                 "brojyons", "a-lemmyn")
bryjyon_preterite = RannowVerbAnreyth("bryjyon", "brojyas", "bryjis",
                                      "bryjsys", "brojyas", "brojyas",
                                      "bryjsyn", "bryjsowgh", "brojsons",
                                      "tremenys")
bryjyon_imperfect = RannowVerbAnreyth("bryjyon", "bryjys", "brojyen",
                                      "brojyes", "brojya", "brojya", "brojyen",
                                      "brojyewgh", "brojyens", "anperfydh")
bryjyon_pluperfect = RannowVerbAnreyth("bryjyon", "bryjsys", "brojsen",
                                       "brojses", "brojsa", "brojsa",
                                       "brojsen", "brojsewgh", "brojsens",
                                       "gorperfydh")
bryjyon_pressubj = RannowVerbAnreyth("bryjyon", "brocchyer", "brycchiv",
                                     "brycchi", "brocchyo", "brocchyo",
                                     "brycchyn", "brycchyowgh", "brocchyons",
                                     "islavarek_a-lemmyn")
bryjyon_impfsubj = RannowVerbAnreyth("bryjyon", "brycchys", "brocchyen",
                                     "brycchyes", "brocchya", "brocchya",
                                     "brocchyen", "brocchyewgh", "brocchyens",
                                     "islavarek_anperfydh")
bryjyon_imperative = RannowVerbAnreyth("bryjyon", "NULL", "NULL", "bros",
                                       "brojyes", "brojyes", "bryjyn",
                                       "bryjyewgh", "brojyens", "gorhemmyn")
bryjyon_tenses = [bryjyon_pres, bryjyon_preterite, bryjyon_imperfect,
                  bryjyon_pluperfect, bryjyon_pressubj, bryjyon_impfsubj,
                  bryjyon_imperative]
bryjyon_inflected = RannowVerbAnreythOllAmser("bryjyon")
bryjyon_inflected.add_tense_list(bryjyon_tenses)

# verbow defowtek
# defective verbs
verbs_defective = ["hwarvos", "darvos", "bern", "darwar", "degoedh", "koedh",
                   "delledh", "deur", "hweles", "medhes", "pargh", "paragh",
                   "res", "skila", "tann", "war"]
#BERN
bern_pres = RannowVerbAnreyth("bern", "NULL", "NULL", "NULL", "bern", "bern",
                              "NULL", "NULL", "NULL", "a-lemmyn")
bern_tenses = [bern_pres]
bern_inflected = RannowVerbAnreythOllAmser("bern")
bern_inflected.add_tense_list(bern_tenses)

#DARWAR
darwar_imperative = RannowVerbAnreyth("darwar", "NULL", "NULL", "darwar",
                                      "NULL", "NULL", "NULL", "darwaryewgh",
                                      "NULL", "gorhemmyn")
darwar_tenses = [darwar_imperative]
darwar_inflected = RannowVerbAnreythOllAmser("darwar")
darwar_inflected.add_tense_list(darwar_tenses)

#DEGOEDH
degoedh_pres = RannowVerbAnreyth("degoedh", "NULL", "NULL", "NULL", "degoedh",
                                 "degoedh", "NULL", "NULL", "NULL", "a-lemmyn")
degoedh_preterite = RannowVerbAnreyth("degoedh", "NULL", "NULL", "NULL",
                                      "degoedhva", "degoedhva", "NULL", "NULL",
                                      "NULL", "tremenys")
degoedh_imperfect = RannowVerbAnreyth("degoedh", "NULL", "NULL", "NULL",
                                      "degoedho", "degoedho", "NULL", "NULL",
                                      "NULL", "anperfydh")
degoedh_pluperfect = RannowVerbAnreyth("degoedh", "NULL", "NULL", "NULL",
                                       "degoedhvia", "degoedhvia", "NULL",
                                       "NULL", "NULL", "gorperfydh")
degoedh_pressubj = RannowVerbAnreyth("degoedh", "NULL", "NULL", "NULL",
                                     "degoedhvo", "degoedhvo", "NULL", "NULL",
                                     "NULL", "islavarek_a-lemmyn")
degoedh_impfsubj = RannowVerbAnreyth("degoedh", "NULL", "NULL", "NULL",
                                     "degoedhva", "degoedhva", "NULL", "NULL",
                                     "NULL", "islavarek_anperfydh")
degoedh_tenses = [degoedh_pres, degoedh_preterite, degoedh_pluperfect,
                  degoedh_pressubj, degoedh_impfsubj]
degoedh_inflected = RannowVerbAnreythOllAmser("degoedh")
degoedh_inflected.add_tense_list(degoedh_tenses)

#KOEDH
koedh_pres = RannowVerbAnreyth("koedh", "NULL", "NULL", "NULL", "koedh",
                               "koedh", "NULL", "NULL", "NULL", "a-lemmyn")
koedh_preterite = RannowVerbAnreyth("koedh", "NULL", "NULL", "NULL", "koedhva",
                                    "koedhva", "NULL", "NULL", "NULL",
                                    "tremenys")
koedh_imperfect = RannowVerbAnreyth("koedh", "NULL", "NULL", "NULL", "koedho",
                                    "koedho", "NULL", "NULL", "NULL",
                                    "anperfydh")
koedh_pluperfect = RannowVerbAnreyth("koedh", "NULL", "NULL", "NULL",
                                     "koedhvia", "koedhvia", "NULL", "NULL",
                                     "NULL", "gorperfydh")
koedh_pressubj = RannowVerbAnreyth("koedh", "NULL", "NULL", "NULL", "koedhvo",
                                   "koedhvo", "NULL", "NULL", "NULL",
                                   "islavarek_a-lemmyn")
koedh_impfsubj = RannowVerbAnreyth("koedh", "NULL", "NULL", "NULL", "koedhva",
                                   "koedhva", "NULL", "NULL", "NULL",
                                   "islavarek_anperfydh")
koedh_tenses = [koedh_pres, koedh_preterite, koedh_pluperfect, koedh_pressubj,
                koedh_impfsubj]
koedh_inflected = RannowVerbAnreythOllAmser("koedh")
koedh_inflected.add_tense_list(koedh_tenses)

#DELLEDH
delledh_pres = RannowVerbAnreyth("delledh", "NULL", "NULL", "NULL", "delledh",
                                 "delledh", "NULL", "NULL", "NULL", "a-lemmyn")
delledh_tenses = [delledh_pres]
delledh_inflected = RannowVerbAnreythOllAmser("delledh")
delledh_inflected.add_tense_list(delledh_tenses)

#DEUR
deur_pres = RannowVerbAnreyth("deur", "NULL", "NULL", "NULL", "deur", "deur",
                              "NULL", "NULL", "NULL", "a-lemmyn")
deur_tenses = [deur_pres]
deur_inflected = RannowVerbAnreythOllAmser("deur")
deur_inflected.add_tense_list(deur_tenses)

#MEDHES
medhes_pres = RannowVerbAnreyth("medhes", "yn-medhir", "yn-medhav",
                                "yn-medhydh", "yn-medh", "yn-medh",
                                "yn-medhyn", "yn-medhowgh", "yn-medhons",
                                "a-lemmyn")
medhes_tenses = [medhes_pres]
medhes_inflected = RannowVerbAnreythOllAmser("medhes")
medhes_inflected.add_tense_list(medhes_tenses)

#PARGH/PARAGH - verbal noun only

#RES
res_pres = RannowVerbAnreyth("res", "NULL", "NULL", "NULL", "res", "res",
                             "NULL", "NULL", "NULL", "a-lemmyn")
res_tenses = [res_pres]
res_inflected = RannowVerbAnreythOllAmser("res")
res_inflected.add_tense_list(res_tenses)

#SKILA
skila_pres = RannowVerbAnreyth("skila", "NULL", "NULL", "NULL", "skila",
                               "skila", "NULL", "NULL", "NULL", "a-lemmyn")
skila_tenses = [skila_pres]
skila_inflected = RannowVerbAnreythOllAmser("skila")
skila_inflected.add_tense_list(skila_tenses)

#TANN
tann_imperative = RannowVerbAnreyth("tann", "NULL", "NULL", "tann", "NULL",
                                    "NULL", "NULL", "tannewgh", "NULL",
                                    "gorhemmyn")
tann_tenses = [tann_imperative]
tann_inflected = RannowVerbAnreythOllAmser("tann")
tann_inflected.add_tense_list(tann_tenses)


#WAR
war_imperative = RannowVerbAnreyth("war", "NULL", "NULL", "war", "NULL",
                                   "NULL", "NULL", "waryewgh", "NULL",
                                   "gorhemmyn")
war_tenses = [war_imperative]
war_inflected = RannowVerbAnreythOllAmser("war")
war_inflected.add_tense_list(war_tenses)

irregverbs_all = {"bos":bos_inflected, "y'm beus":ymbeus_inflected,
                  "piw":piw_inflected, "godhvos":godhvos_inflected,
                  "tyli":tyli_inflected, "attyli":attyli_inflected,
                  "hwarvos":hwarvos_inflected, "darvos":darvos_inflected,
                  "klywes":klywes_inflected, "omglywes":omglywes_inflected,
                  "mos":mos_inflected, "dos":dos_inflected,
                  "doen":doen_inflected, "omdhoen":omdhoen_inflected,
                  "ri":ri_inflected, "dri":dri_inflected, "ti":ti_inflected,
                  "dyllo":dyllo_inflected, "gul":gul_inflected,
                  "omwul":omwul_inflected, "mynnes":mynnes_inflected,
                  "galloes":galloes_inflected, "bern":bern_inflected,
                  "darwar":darwar_inflected, "degoedh":degoedh_inflected,
                  "koedh":koedh_inflected, "delledh":delledh_inflected,
                  "deur":deur_inflected, "medhes":medhes_inflected,
                  "res":res_inflected, "skila":skila_inflected,
                  "tann":tann_inflected, "war":war_inflected,
                  "bryjyon":bryjyon_inflected}

def make_tense_dict(list_tenses, past_pl="NULL"):
    """
    y telledh bos list_tenses rol taklennow RannowVerbAnreyth
    list_tenses should be a list of RannowVerbAnreyth objects
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
    lenlastconstclust = len(lastcon)
    pos = len(verbstr)-lenlastconstclust
    return lastcon, pos, lenlastconstclust

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
        endings = endings_alltenses.tense_endings(tensesDict[tense])
    if tense < 7:
        # for all tenses except past participle
        ending = endings.person_ending(person)
    if tense == 7: # if past participle
        ending = endings
    origending = ending #before addition of suffixed pronoun
    if (suffix_pro == 1)and(person > 0)and(tense != 7):
        # if there should be suffixed pronouns, and it isn't impersonal or ppl
        ending = ending + " " + suffixed_pros[person]
    if (suffix_pro == 2)and(person > 0)and(tense != 7):
        # if there should be emphatic suffixed pronouns, and not impersonal or ppl
        ending = ending + " " + suffixed_pros_emph[person]
    # verbow a worfenn gans -he:
    # verbs ending in -he:
    if verb[-2:] == "he":
        if tense == 0 and (person == 3)or(person == 4):
            # 3s a-lemmyn a'th eus a wosa an ben
            # 3s. pres has a not just stem alone
            ending = "a"
        if origending != "":
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
    # verbow a worfenn gans -ya
    # verbs ending in -ya
    if stem[-1] == "y":
        # -y- yw gwithys heb y arall, i po s yn penn po nag eus penn
        # -y- retained except where another y, i or s occurs in the ending
        # or where there is no suffix (3s pres, 2s imperative)
        if origending != "":
            if (origending[0] == "y") or (origending[0] == "i") or (
                    origending[0] == "s"):
                stem = stem[:-1]
        if origending == "":
            stem = stem[:-1]
    # verbow gans maneruster bogalenn
    # verbs with vowel affectation

    # type TAVA:
    # yma a diwettha bogalenn an ben
    # a is last vowel of stem
    # tardra --> terdrys
    if verb in verbs_tava:
        # a-->e mar bogalenn y'n penn  -i-, -y-, po -owgh
        # a-->e when vowel of ending is -i-, -y-, or -owgh
        # hag yn 2pl gorhemmyn kyns -ewgh
        # also in 2pl imperative before -ewgh
        if origending != "":
            if (origending[0] in ["i", "y"]) or (origending == "owgh") or (
                    (origending == "ewgh")and(person == 6)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if laststemvowel == "a":
                    if (tense == 4)or(tense == 5):
                        # chanjys dhe -y- yn islavarek
                        # in subjunctive further affected to -y-
                        stem = stem[:pos] + "y" + stem[pos+1:]
                    else:
                        stem = stem[:pos] + "e" + stem[pos+1:]

    if (verb in ["amma", "ranna"]):
        # AMMA, RANNA - a-->y
        if origending != "":
            if (origending[0] in ["i", "y"]) or (origending == "owgh") or (
                    (origending == "ewgh")and(person == 2)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if laststemvowel == "a":
                    stem = stem[:pos] + "y" + stem[pos+1:]

    if verb in ["pregowtha"]:
        # pregowtha ow-->ew
        if origending != "":
            if (origending[0] in ["i", "y"]) or (origending == "owgh") or (
                    (origending == "ewgh")and(person == 2)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if laststemvowel == "o":
                    stem = stem[:pos] + "e" + stem[pos+1:]

    if (verb in ["dannvon", "daskorr"]):
        # dannvon, daskorr o-->e
        if origending != "":
            if (origending[0] in ["i", "y"]) or (origending == "owgh") or (
                    (origending == "ewgh")and(person == 2)and(tense == 6)):
                laststemvowel, pos = lastvowel(stem)
                if laststemvowel == "o":
                    stem = stem[:pos] + "e" + stem[pos+1:]
    # type IGERI
    # gwitha bogalenn ben derowel -a- po -o- yn amserowa syw:
    # retain original stem vowel -a- or -o- in following tenses:
    # pres/future 1s
    # preterite 3s and 3p
    # pluperfect all persons
    # subjuctive pres 3s. and 3p.
    # subjunctive imp. all persons
    # imperative 2s.
    if verb in verbs_igeri_o:
        if ((tense == 0)and(person == 1))or(((tense == 1)or(tense == 4))and(
                (person == 3)or(person == 4)or(person == 7)))or(tense == 3)or(
                    tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if laststemvowel == "e":
                stem = stem[:pos] + "o" + stem[pos+1:]
        if verb == "dedhwi":
            if (tense == 1)and((person == 3)or(person == 4)):
                stem = "dedhow"
    if verb in verbs_igeri_a:
        if ((tense == 0)and(person == 1))or(((tense == 1)or(tense == 4))and(
                (person == 3)or(person == 4)or(person == 7)))or(tense == 3)or(
                    tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
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
    if verb in verbs_erghi_a:
        if ((tense == 0)and(person == 1))or((tense == 1)and(person == 7))or(
                tense == 3)or((tense == 4)and((person == 3)or(person == 4)or(
                    person == 7)))or(tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if laststemvowel == "e":
                stem = stem[:pos] + "a" + stem[pos+1:]
        if verb == "drehevel":
            # drehevel 3s. pres/fut drehav, dreha, or derav,
            # 2s imperv. drehav/dreva, 3s. pret. drehevis/derevis
            if ((tense == 0)and((person == 3)or(person == 4)))or(
                    (tense == 6)and(person == 2)):
                stem = "drehav"
        if verb == "gweskel":
            # gweskel has 3s. pres/fut gwysk, past participle gwyskys, loses k in some parts of verb
            if ((tense == 0)and((person == 3)or(person == 4)))or(tense == 7):
                stem = "gwysk"
    if verb in verbs_erghi_o:
        if ((tense == 0)and(person == 1))or((tense == 1)and(person == 7))or(
                tense == 3)or((tense == 4)and((person == 3)or(person == 4)or(
                    person == 7)))or(tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
            if laststemvowel == "e":
                stem = stem[:pos] + "o" + stem[pos+1:]
        if verb == "dinewi"and tense == 0 and ((person == 3)or(person == 4)):
            # dinewi has 3s. pres/fut dinwa
            stem = "dinwa"

    if (verb in three_s_presfut_y) and tense == 0 and ((person == 3)or(person == 4)):
        # group of verbs narrow vowel in 3s. pres/fut (sect 192 of Wella Brown 3rd ed.)
        laststemvowel, pos = lastvowel(stem)
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
    if verb in verbs_gelwel:
        if ((tense == 0)and(person == 1))or((tense == 1)and(person == 7))or(
                tense == 3)or((tense == 4)and((person == 3)or(person == 4)or(
                    person == 7)))or(tense == 5)or((tense == 6)and(person == 2)):
            laststemvowel, pos = lastvowel(stem)
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
    if verb in verbs_hwithra:
        # print(stem)
        if ((tense == 0)and((person == 3)or(person == 4)))or((tense == 6)and(person == 2)):
            # in 3s. pres/future and 2s. imperative
            # a vowel is introduced usually -e-
            # sometimes -o- or -y-
            if verb in ["resna", "sokra"]:
                vowel = "o"
            else:
                if verb in ["fekla", "takla"]:
                    vowel = "y"
                else:
                    vowel = "e"
            stem = stem[:-1]+vowel+stem[-1]
        if origending != "":
            if origending[0] == "s":
                # when verbal ending starts with an -s-
                # the final consonant of the stem may drop out and be shortened
                # and an apostrophe introduced
                stem = stem[:-1]+"'"

    # GWYSTLA type
    # final consonant is -l-, -m-, -n- or -r- preceded by two adjacent consonants.
    if verb in verbs_gwystla:
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
    if verb in verbs_lesta:
        if origending != "":
            if origending[0] == "s":
                stem = stem[:-1]+"'"

    if (verb == "diskwedhes")and(tense == 0)and((person == 3)or(person == 4)):
        stem = "diskwa"
    if (verb == "drehevel")and(tense == 0)and((person == 3)or(person == 4)):
        stem = "drehav"
    if (verb == "gortos")and(tense == 0)and((person == 3)or(person == 4)):
        stem = "gorta"
    if (verb == "hwilas")and(tense == 0)and((person == 3)or(person == 4)):
        stem = "hwila"

    # DYBRI
    # vowel affectation in stem
    # y --> e e.g. in dybri
    # in pres pers 3,4,6,7
    # pres subj pers 3,4
    # imp subj all pers
    # imperative pers 2
    if verb in verbs_dybri:
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
    if tense == "devedhek" and verb not in verbs_devedhek:
        # only a few verbs have a simple future tense
        # if not return invalid
        return False
    if tense == "anperfydh_usadow" and verb not in verbs_anperfydh_usadow:
        # only a few verbs have a separate habitual imperfect
        # if not return invalid
        return False
    if tense in ["a-lemmyn_hir_indef", "anperfydh_hir", "a-lemmyn_hir_def",
                 "a-lemmyn_hir_aff"] and verb != 'bos':
        # the long forms which are particular to bos
        return False
    if tense == "perfydh" and verb not in verbs_perfydh:
        return False
    return True

def inflektya(verb, person, tense, suffix_pro=0):
    """ person: 0=imp,1=1s,2=2s,3=3sm,4=3sf,5=1p,6=2p,7=3p
     tense: 0=present, 1=preterite, 2=imperfect, 3=pluperfect, 4=subjpres, 5=subjimp
    6=imperative,7=past_participle,8=future,9=habitual imperfect
    0=longform_present_indef,11=longform_imperfect,12=longform_present_defni
    3=longform_present_aff,14=perfect
    expect string for the tense """

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

    if verb in verbs_stemnoun:
        stem = verb
    if ("islavarek" in tense)and(verb not in verbs_gwystla)and(verb[-2:] != "ia"):
        # kesson a wra dewblek po kaleshe y'n islavarek
        # double/harden consonants in subjunctive
        # but not generally in verbs_gwystla
        # and not in verbs ending -ia
        lastconststem = lastconsonant(stem)[0]
        # print(lastconststem)
        if lastconststem in stem_changes.keys():
            # do a string replace, but first reverse the stem, and the
            # arguments for replace, so that it is only done once
            # for the last time lastconststem occurs in stem
            stem = stem[::-1].replace(lastconststem[::-1],
                                      stem_changes[lastconststem][::-1], 1)[::-1]
    regular = verb not in irregverbs_all.keys()
    if regular:
        return inflektya_reyth(verb, stem, person, tenses_code_dict[tense], suffix_pro)

    if not regular:
        if tense == "ppl":
            inflectedverb = irregverbs_all[verb].getppl()
        else:
            inflectedverb = irregverbs_all[verb].get_inf_verb(tense, person)
            if (suffix_pro == 1)and(person > 0):
                inflectedverb += " " + suffixed_pros[person]
            if (suffix_pro == 2)and(person > 0):
                inflectedverb += " " + suffixed_pros_emph[person]
        return inflectedverb, 1

# IRREGULAR
# bos, y'm beus, darvos, dos, godhvos, hwarvos, klywes, mos, piw, tyli
# doen, dri, dyllo, gul, ri, ti

#prepositions
endings_A = {1:"av", 2:"as", 3:"o", 4:"i", 5:"an", 6:"owgh", 7:"a"}
endings_B = {1:"ov", 2:"os", 3:"o", 4:"i", 5:"on", 6:"owgh", 7:"a"}
endings_C = {1:"iv", 2:"is", 3:"o", 4:"i", 5:"yn", 6:"owgh", 7:"a"}
endings_D = {1:"", 2:"", 3:"", 4:"", 5:"", 6:"", 7:""}
# dhe, gans irregular
a_stems = {1:"ahan", 2:"ahan", 3:"anodh", 4:"anedh", 5:"ahan", 6:"ahan", 7:"anedh"}
agovis_stems = {1:"a'm govis", 2:"a'th wovis", 3:"a'y wovis", 4:"a'y govis", 5:"a'gan govis",
                6:"a'gas govis", 7:"a'ga govis"}
a_ugh_stems = {1:"a-ugh", 2:"a-ugh", 3:"a-ught", 4:"a-ught", 5:"a-ugh", 6:"a-ugh", 7:"a-ught"}
dhe_stems = {1:"dhymm", 2:"dhis", 3:"dhodho", 4:"dhedhi", 5:"dhyn", 6:"dhywgh", 7:"dhedha"}
dre_stems = {1:"dredh", 2:"dredh", 3:"dredh", 4:"dredh", 5:"dredh", 6:"dredh", 7:"dredh"}
dres_stems = {1:"dres", 2:"dres", 3:"drest", 4:"drest", 5:"dres", 6:"dres", 7:"drest"}
erbynn_stems = {1:"er ow fynn", 2:"er dha bynn", 3:"er y bynn", 4:"er hy fynn", 5:"er agan pynn",
                6:"er agas pynn", 7:"er aga fynn"}
gans_stems = {1:"genev", 2:"genes", 3:"ganso", 4:"gensi", 5:"genen", 6:"genowgh", 7:"gansa"}
heb_stems = {1:"heb", 2:"heb", 3:"hebdh", 4:"hebdh", 5:"heb", 6:"heb", 7:"hebdh"}
orth_stems = {1:"orth", 2:"orth", 3:"ort", 4:"ort", 5:"orth", 6:"orth", 7:"ort"}
diworth_stems = {1:"diworth", 2:"diworth", 3:"diwort", 4:"diwort", 5:"diworth", 6:"diworth",
                 7:"diwort"}
a_dhiworth_stems = {1:"a-dhiworth", 2:"a-dhiworth", 3:"a-dhiwort", 4:"a-dhiwort", 5:"a-dhiworth",
                    6:"a-dhiworth", 7:"a-dhiwort"}
dhiworth_stems = {1:"dhiworth", 2:"dhiworth", 3:"dhiwort", 4:"dhiwort", 5:"dhiworth", 6:"dhiworth",
                  7:"dhiwort"}
rag_stems = {1:"rag", 2:"rag", 3:"ragdh", 4:"rygdh", 5:"rag", 6:"rag", 7:"ragdh"}
a_rag_stems = {1:"a-rag", 2:"a-rag", 3:"a-ragdh", 4:"a-rygdh", 5:"a-rag", 6:"a-rag", 7:"a-ragdh"}
a_dherag_stems = {1:"a-dherag", 2:"a-dherag", 3:"a-dheragdh", 4:"a-dherygdh", 5:"a-dherag",
                  6:"a-dherag", 7:"a-dheragdh"}
derag_stems = {1:"derag", 2:"derag", 3:"deragdh", 4:"derygdh", 5:"derag", 6:"derag", 7:"deragdh"}
dherag_stems = {1:"dherag", 2:"dherag", 3:"dheragdh", 4:"dherygdh", 5:"dherag", 6:"dherag",
                7:"dheragdh"}
ryb_stems = {1:"ryb", 2:"ryb", 3:"rybdh", 4:"rybdh", 5:"ryb", 6:"ryb", 7:"rybdh"}
war_stems = {1:"warn", 2:"warn", 3:"warnodh", 4:"warnedh", 5:"warn", 6:"warn", 7:"warnedh"}
diwar_stems = {1:"diwarn", 2:"diwarn", 3:"diwarnodh", 4:"diwarnedh", 5:"diwarn", 6:"diwarn",
               7:"diwarnedh"}
a_dhiwar_stems = {1:"a-dhiwarn", 2:"a-dhiwarn", 3:"a-dhiwarnodh", 4:"a-dhiwarnedh", 5:"a-dhiwarn",
                  6:"a-dhiwarn", 7:"a-dhiwarnedh"}
warlergh_stems = {1:"war ow lergh", 2:"war dha lergh", 3:"war y lergh", 4:"war hy lergh",
                  5:"war agan lergh", 6:"war agas lergh", 7:"war aga lergh"}
yn_stems = {1:"ynn", 2:"ynn", 3:"ynn", 4:"ynn", 5:"ynn", 6:"ynn", 7:"ynn"}
yn_dann_stems = {1:"yn-dann", 2:"yn-dann", 3:"yn-dann", 4:"yn-dann", 5:"yn-dann", 6:"yn-dann",
                 7:"yn-dann"}
a_dhann_stems = {1:"a-dhann", 2:"a-dhann", 3:"a-dhann", 4:"a-dhann", 5:"a-dhann", 6:"a-dhann",
                 7:"a-dhann"}
yntra_stems = {1:"yntredh", 2:"yntredh", 3:"yntredh", 4:"yntredh", 5:"yntredh", 6:"yntredh",
               7:"yntredh"}
yn_herwydh_stems = {1:"yn ow herwydh", 2:"yn dha herwydh", 3:"yn y herwydh", 4:"yn hy herwydh",
                    5:"yn agan herwydh", 6:"yn agas herwydh", 7:"yn aga herwydh"}
yn_kyrghynn_stems = {1:"yn ow hyrghynn", 2:"yn dha gyrghynn", 3:"yn y gyrghynn", 4:"yn hy hyrghynn",
                     5:"yn agan kyrghynn", 6:"yn agas kyrghynn", 7:"yn aga hyrghynn"}
yn_kever_stems = {1:"yn ow hever", 2:"yn dha gever", 3:"yn y gever", 4:"yn hy hever",
                  5:"yn agan kever", 6:"yn agas kever", 7:"yn aga hever"}
yn_le_stems = {1:"yn ow le", 2:"yn dha le", 3:"yn y le", 4:"yn hy le", 5:"yn agan le",
               6:"yn agas le", 7:"yn aga le"}
yn_mysk_stems = {1:"yn ow mysk", 2:"yn dha vysk", 3:"yn y vysk", 4:"yn hy mysk", 5:"yn agan mysk",
                 6:"yn agas mysk", 7:"yn aga mysk"}
yn_ogas_stems = {1:"yn ow ogas", 2:"yn dha ogas", 3:"yn y ogas", 4:"yn hy ogas", 5:"yn agan ogas",
                 6:"yn agas ogas", 7:"yn aga ogas"}
prep_stems_all = {"a":a_stems, "a-govis":agovis_stems, "a-ugh":a_ugh_stems, "dhe":dhe_stems,
                  "dre":dre_stems, "dres":dres_stems, "erbynn":erbynn_stems, "gans":gans_stems,
                  "heb":heb_stems, "orth":orth_stems, "diworth":diworth_stems,
                  "a-dhiworth":a_dhiworth_stems, "dhiworth":dhiworth_stems, "rag":rag_stems,
                  "a-rag":a_rag_stems, "a-dherag":a_dherag_stems, "derag":derag_stems,
                  "dherag":dherag_stems, "ryb":ryb_stems, "war":war_stems, "diwar":diwar_stems,
                  "a-dhiwar":a_dhiwar_stems, "warlergh":warlergh_stems, "yn":yn_stems,
                  "yn-dann":yn_dann_stems, "a-dhann":a_dhann_stems, "yntra":yntra_stems,
                  "yn herwydh":yn_herwydh_stems, "yn kyrghynn":yn_kyrghynn_stems,
                  "yn kever":yn_kever_stems, "yn le":yn_le_stems, "yn mysk":yn_mysk_stems,
                  "yn ogas":yn_ogas_stems}
prep_endings_all = {"a":endings_A, "a-govis":endings_D, "a-ugh":endings_B, "dhe":endings_D,
                    "dre":endings_B, "dres":endings_B, "erbynn":endings_D, "gans":endings_D,
                    "heb":endings_B, "orth":endings_C, "diworth":endings_C, "a-dhiworth":endings_C,
                    "dhiworth":endings_C, "rag":endings_B, "a-rag":endings_B, "a-dherag":endings_B,
                    "derag":endings_B, "dherag":endings_B, "ryb":endings_B, "war":endings_A,
                    "diwar":endings_A, "a-dhiwar":endings_A, "warlergh":endings_D, "yn":endings_B,
                    "yn-dann":endings_B, "a-dhann":endings_B, "yntra":endings_B,
                    "yn herwydh":endings_D, "yn kyrghynn":endings_D, "yn kever":endings_D,
                    "yn le":endings_D, "yn mysk":endings_D, "yn ogas":endings_D}

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

    if prep_stems_all.has_key(prepos) and prep_endings_all.has_key(prepos):
        inflectedprep = prep_stems_all[prepos][person] + prep_endings_all[prepos][person]
    else:
        print("Rager {prepos} yw anaswonnys.\n\
Preposition {prepos} is unknown".format(prepos=prepos))
        return invalidinput, 0
    ending = ""
    if (prepos == "dhe")and(suffix_pro > 0)and((person == 1)or(person == 2)):
        ending += "o"
    if (suffix_pro == 1)and(person > 0):
        ending += " " + suffixed_pros[person]
    if (suffix_pro == 2)and(person > 0):
        ending += " " + suffixed_pros_emph[person]
    inflectedprep = inflectedprep + ending
    return inflectedprep, 1

def rol_personys_amserow(verb):
    """
    pryntya rol a personys ha'n amserow rag verb
    print a list of persons for each tense of verb
    """
    print("Verb {verb}:".format(verb=verb.upper()))

    if verb not in irregverbs_all.keys():
        tlist = [tensesDict[t] for t in range(8)]
        t_en_list = [tensesDictEN[t] for t in range(8)]
    else:
        tlist = irregverbs_all[verb].tenses_list
        t_en_list = irregverbs_all[verb].tenses_en_list

    for t, t_en in zip(tlist, t_en_list):
        print("\nAmser: {amser} {tenseEN}".format(amser=t.capitalize().ljust(20),
                                                  tenseEN=tEN.capitalize().rjust(20)))
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

verbs_devedhek = ["bos", "y'm beus", "piw", "godhvos", "tyli", "attyli", "hwarvos"]
verbs_anperfydh_usadow = ["bos", "y'm beus", "piw"]
verbs_perfydh = ["mos", "mones", "dos", "dones"]

if __name__ == '__main__':
    run_testcode()
