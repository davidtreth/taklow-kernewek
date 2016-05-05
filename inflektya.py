# David Trethewey
# vershyon 24-04-2016
"""
An module ma a wra inflektya verbow Kernewek
This module inflects Cornish verbs
"""
import re

class lostow_personek:
    """
    taklenn a wra gwitha lostow personek dhe unn amser verb
    an object to hold the personal endings for a verb tense
    """
    def __init__(self, anpersonek, my, ty, ev, hi, ni, hwi, i, amser):
        self.lostow = [anpersonek, my, ty, ev, hi, ni, hwi, i]
        self.lostowDict = {0:anpersonek, 1:my, 2:ty, 3:ev, 4:hi, 5:ni, 6:hwi, 7:i}
        self.amser = amser
    def personEnding(self,personnum):
        return self.lostowDict[personnum]


class lostow_personek_2:
    """
    klass dhe wul taklennow a wra gwitha lostow personek an verbow yn pub amser
    a class to create objects to hold personal endings of all tenses in a verb
    """
    def __init__(self, lostowDict):        
         """
         lostowDict a wra gwitha an lostow yn gerlyver 
         gans yndeks an amser
         rag ensample lostowDict["a-lemmyn"] = lostow_alemmyn
         ha lostow_alemmyn yw taklenn lostow_personek 

         lostowDict holds the endings in a dictionary 
         indexed by the tense
         e.g. lostowDict["a-lemmyn"] = lostow_alemmyn
         where lostow_alemmyn is a lostow_personek object
         """
         self.lostowDict = lostowDict
    def tenseEndings(self,tense):
         """
         kavoes lostow rag unn amser
         return endings for a tense
         """
         return self.lostowDict[tense]

class rannowVerbAnreyth: 
    """
    verb anreyth inflektys - unn amser
    inflected irregular verb of one tense
    """
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

    def __init__(self,verbnoun, anpersonek, my, ty, ev, hi, ni, hwi, i, amser):
        self.verbnoun = verbnoun
        self.rannow = [anpersonek, my, ty, ev, hi, ni, hwi, i]
        self.rannowDict = {0:anpersonek, 1:my, 2:ty, 3:ev, 4:hi, 5:ni, 6:hwi, 7:i}
        self.amser = amser
        self.amserEN = rannowVerbAnreyth.amserowEN[amser]
        
class rannowVerbAnreythOllAmser: 
    """
    kyst rag rannow verb anreyth
    container for parts of irregular verb
    """
    def __init__(self, verbnoun):
        """ 
        mar nag yw an verb defektiv, y fydh ganso
        amserow 0-7 ha martesen moy
        nebes verbow ny'th eus PPL
        gerlyver amserow yn dictTenses
        pub alhwedh yn dictTenses yw amser
        value yw taklenn rannowVerbAnreyth

        if not defective, it will have tenses 0-7 and maybe more
         a few verbs don't have past participle
         dictionary of tenses in dictTenses
         each key in dictTenses is tense
         value is rannowVerbAnreyth object
        """
        self.verbnoun = verbnoun
        self.tensesList = []
        self.tensesENList = []
        self.dictTenses = {}
    def addTense(self, tense):
        """
        y telledh bos tense taklenn rannowVerbAnreyth
        tense should be rannowVerbAnreyth object
        """
        self.tensesList.append(tense.amser)
        self.tensesENList.append(tense.amserEN)
        self.dictTenses[tense.amser] = tense.rannowDict
    def addPPL(self, PPL):
        """
        keworra PPL dhe self.dictTenses
        add past participle to self.dictTenses
        """
        self.dictTenses["ppl"] = PPL
    def addTenseList(self, tenseList, PPL = "NULL"):
        """
        keworra rol a amserow orth self.dictTenses
        add a list of tenses to self.dictTenses
        """
        for t in tenseList:
            self.addTense(t)
        if PPL != "NULL":
            self.addPPL(PPL)
    def getPPL(self):
        return self.dictTenses["ppl"]
    def getInfVerb(self,tense,person):
        """
        kavoes verb inflektys gans an amser ha'n person
        get the inflected verb for the tense and person
        """
        if self.dictTenses.has_key(tense):
            return self.dictTenses[tense][person]
        else:
            print("Nyns eus amser {t} dhe verb {v}.\nVerb {v} doesn't have tense {t}".format(v=self.verbnoun, t=tense))
            return "NULL"
# lostow verbow reyth
# regular verb endings
endings_present = lostow_personek("ir","av","ydh","","","yn","owgh","ons","a-lemmyn")
endings_preterite = lostow_personek("as","is","sys","as","as","syn","sowgh","sons","tremenys")
# lostow rag verbow gans i
# endings for verbs that use the i vowel 
endings_preterite_i = lostow_personek("is","is","sys","is","is","syn","sowgh","sons","tremenys")
endings_imperfect = lostow_personek("ys","en","es","a","a","en","ewgh","ens","anperfydh")
endings_imperfect_i = lostow_personek("ys","yn","ys","i","i","yn","ewgh","ens","anperfydh")
endings_pluperfect = lostow_personek("sys","sen","ses","sa","sa","sen","sewgh","sens","gorperfydh")
endings_subj_pres = lostow_personek("er","iv","i","o","o","yn","owgh","ons","islavarek_a-lemmyn")
endings_subj_imp = lostow_personek("ys","en","es","a","a","en","ewgh","ens","islavarek_anperfydh")
endings_imperative = lostow_personek("","","","es","es","yn","ewgh","ens","gorhemmyn")

tensesDict = {0:"a-lemmyn",1:"tremenys",2:"anperfydh",3:"gorperfydh",4:"islavarek_a-lemmyn",5:"islavarek_anperfydh",6:"gorhemmyn",7:"ppl"}
# notenn - nyns eus 1s ha anpersonek dhe'n amser gorhemmyn
# note - 1s and impersonal do not exist for imperative
ending_pastparticiple = "ys"
suffixed_pros = {1:"vy",2:"jy",3:"ev",4:"hi",5:"ni",6:"hwi",7:"i"}
suffixed_pros_emph = {1:"evy",2:"tejy",3:"eev",4:"hyhi",5:"nyni",6:"hwyhwi",7:"ynsi"}

endings_alltenses = lostow_personek_2({endings_present.amser: endings_present,
                                       endings_preterite.amser: endings_preterite,
                                       endings_imperfect.amser: endings_imperfect,
                                       endings_pluperfect.amser: endings_pluperfect,
                                       endings_subj_pres.amser: endings_subj_pres,
                                       endings_subj_imp.amser: endings_subj_imp,
                                       endings_imperative.amser: endings_imperative,
                                       "ppl": ending_pastparticiple})
# lostow rag verbow gans i
# endings for verbs that use the i vowel 
endings_alltenses_i = lostow_personek_2({endings_present.amser:endings_present.lostowDict,
                                         endings_preterite_i.amser:endings_preterite_i.lostowDict,
                                         endings_imperfect_i.amser:endings_imperfect_i.lostowDict,
                                         endings_pluperfect.amser:endings_pluperfect.lostowDict,
                                         endings_subj_pres.amser:endings_subj_pres.lostowDict,
                                         endings_subj_imp.amser:endings_subj_imp.lostowDict,
                                         endings_imperative.amser:endings_imperative.lostowDict,
                                         "ppl":ending_pastparticiple})

# verbow ha'n ben an keth ha'n hanow verbek
# verbs with stem same as verbal noun
verbs_stemnoun = ["arvedh","arveth","astell","aswonn","daffar","dalleth","dannvon","daskorr","dendil","dervynn","dewis","diank","diberth","difenn","difres","dolos","dyerbynn","godhav","godros","gorhrmmynn","gormel","gromyal","gwari","gweres","hepkorr","hembronk","hunros","kanmel","kemmynn","kuntell","kynnik","meythrin","omdhal","omguntell","omwen","pe","powes","pregowth","sommys","tynkyal","yes"]

# verbow gans bogalenn i yn 3s tremenys
# verbs with i vowel in 3s preterite
verbs_i_3sp = ["aswonn","attylli","brewi","dagrewi","dedhewi","dehweles","demmedhi","derivas","diank","dinewi","dineythi","diskrysi","distrui","domhwel","dybri","dynnerghi","erghi","godhav","gorhemmynn","gorthybi","hedhi","heveli","kemmynna","kentrewi","kreuni","krysi","mollethi","ombrederi","omhweles","prederi","pysi","synsi","tevi","tybi","yeuni"]
# ha'n verbow gans -el
# plus all verbs in -el (not yet implemented)

# verbow gans bogalenn i yn anperfydh
# verbs with i vowel in imperfect
verbs_i_imp = ["amma","aswonn","dalleth","dannvon","dervynn","dewis","diberth","difenn","doen","dyllo","folhwerthin","galloes","godhav","gonis","govynn","hembronk","hwerthin","lavasos","minhwerthin","omladh"]

#plus all verbs in -el, -es (except klywes and mynnes), -he and -i
verbs_tava = ["tava","tardra","kachya","kampya","shakya","talkya"]
verbs_igeri_o = ["ankevi","dasseni","dasserghi","dedhwi","goderri","kelli","kelmi","keski","kregi","lenki","leski","megi","pedri","perthi","previ","renki","seni","serri","telli","terri","treghi"]
verbs_igeri_a = ["dalleth","diberth","hwerthin","minhwerthin","peski"]
verbs_erghi_o = ["dagrewi","dedhewi","dinewi","kentrewi","kewsel","kynyewel","mollethi"]
verbs_erghi_a = ["densel","diank","drehevel","dynnerghi","fyllel","godhevel","gweskel","heveli","lemmel","leverel","sevel","terlemmel","tewel","tyli","attyli"]
three_s_presfut_y = ["eva","galloes","gedya","gweskel","kavoes","kelli","pobas","tevi"]
verbs_lesta = ["bostya","diwiska","dyski","gweskel","gwiska","kestya","koska","leski","mostya","ostya","peski","raska","restya","rostya","tergoska","trestya"]
verbs_gwystla = ["dampnya","entra","gustla","gwandra","handla","hwystra","kentra","moldra","restra","sklandra","sompna","tardra","tempra","terlentri"]
verbs_hwithra = ["hwithra","dybri","fagla","gwedhra","hwedhla","hwyrni","ladra","lymna","medra","meythrin","pedri","pobla","ravna","sotla","sugna","trobla","resna","sokra","fekla","takla"]
verbs_gelwel = ["gelwel","henwel","lenwel","merwel","selwel"]
verbs_irregular = ["bos","y'm beus","darvos","dos","godhvos","hwarvos","klywes","omglywes","mos","piw","tyli","attyli","doen","omdhoen","dri","dyllo","gul","ri","ti","bryjyon"]
# vowel affectation y--> e in stem in some persons e.g. deber
verbs_dybri = ["dybri"]
# chanjyow ben kalesheans po dewblekheans
# hardening or doubling in ending of the stem
stem_changes = {"b":"pp","bl":"ppl","br":"ppr","ch":"cch","d":"t","dh":"tth","dhl":"tthl","dhr":"tthr","dhw":"tthw","dr":"ttr","f":"ff","g":"kk","gh":"ggh","gl":"kkl","gn":"kkn","he":"hah","j":"cch","k":"kk","kl":"kkl","kn":"kkn","kr":"kkr","l":"ll","ld":"lt","ldr":"ltr","lv":"lf","m":"mm","mbl":"mpl","mbr":"mpr","n":"nn","nd":"nt","ndl":"ntl","ndr":"ntr","ng":"nk","ngr":"nkr","nj":"nch","p":"pp","r":"rr","rd":"rt","rdr":"rtr","rdh":"rth","rg":"rk","rj":"rch","rv":"rf","s":"ss","sh":"ssh","sl":"ssl","sn":"ssn","sw":"ssw","t":"tt","th":"tth","thl":"tthl","thr":"tthr","tl":"ttl","v":"ff","vn":"ffn","vr":"ffr"}
vowels = ["a","e","i","o","u"]

# Verbow Anreyth
# Irregular verbs
# BOS
#need extra parameter to decide short/long
#say long = 0 or long = 1
#and another to distinguish usi/yma/eus and ymons/esons
#definite = 1 or definite = 0 to distinguish yma/usi from yma/eus
#affirmative = 1/0 to use yma/ymons in affirmative and usi/eus or esons in neg/interrog
# at present the above are implemented as separate tenses

#bos_shortpres = rannowVerbAnreyth("bos","or","ov","os","yw","yw","on","owgh","yns","a-lemmyn_berr")
# use short form as a default to avoid key error in dictionary
bos_shortpres = rannowVerbAnreyth("bos","or","ov","os","yw","yw","on","owgh","yns","a-lemmyn")
bos_preterite = rannowVerbAnreyth("bos","beus","beuv","beus","beu","beu","beun","bewgh","bons","tremenys")
#bos_shortimperfect = rannowVerbAnreyth("bos","os","en","es","o","o","en","ewgh","ens","anperfydh_berr")
bos_shortimperfect = rannowVerbAnreyth("bos","os","en","es","o","o","en","ewgh","ens","anperfydh")
bos_pluperfect = rannowVerbAnreyth("bos","bies","bien","bies","bia","bia","bien","biewgh","biens","gorperfydh")
bos_pressubj = rannowVerbAnreyth("bos","ber","biv","bi","bo","bo","byn","bowgh","bons","islavarek_a-lemmyn")
bos_impfsubj = rannowVerbAnreyth("bos","bes","ben","bes","be","be","ben","bewgh","bens","islavarek_anperfydh")
bos_imperative = rannowVerbAnreyth("bos","NULL","NULL","bydh","bedhes","bedhes","bedhen","bedhewgh","bedhens","gorhemmyn")
bos_pastparticiple="bedhys" #used only in compounds
bos_future = rannowVerbAnreyth("bos","bydher","bydhav","bydhydh","bydh","bydh","bydhyn","bydhowgh","bydhons","devedhek")
bos_habitimperfect = rannowVerbAnreyth("bos","bedhes","bedhen","bedhes","bedha","bedha","bedhen","bedhewgh","bedhens","anperfydh_usadow")
bos_longpres_indef = rannowVerbAnreyth("bos","eder","esov","esos","eus","eus","eson","esowgh","esons","a-lemmyn_hir_indef")
bos_longpres_defni = rannowVerbAnreyth("bos","eder","esov","esos","usi","usi","eson","esowgh","esons","a-lemmyn_hir_def")
bos_longpres_aff = rannowVerbAnreyth("bos","eder","esov","esos","yma","yma","eson","esowgh","ymons","a-lemmyn_hir_aff")
bos_longimpf = rannowVerbAnreyth("bos","eses","esen","eses","esa","esa","esen","esewgh","esens","anperfydh_hir")
bos_tenses = [bos_shortpres,bos_preterite,bos_shortimperfect,bos_pluperfect,bos_pressubj,bos_impfsubj,bos_imperative,bos_future,bos_habitimperfect,bos_longpres_indef,bos_longimpf,bos_longpres_defni,bos_longpres_aff]
bos_inflected = rannowVerbAnreythOllAmser("bos")
bos_inflected.addTenseList(bos_tenses,bos_pastparticiple)


# Y'M BEUS
# y'th eus devedhek sempel hag anperfydh usadow
# has simple future and habitual imperfect
ymbeus_pres = rannowVerbAnreyth("y'm beus","NULL","y'm beus","y'th eus","y'n jeves","y's teves","y'gan beus","y'gas beus","y's teves","a-lemmyn")
ymbeus_preterite = rannowVerbAnreyth("y'm beus","NULL","y'm beu","y'feu","y'n jeva","y's teva","y'gan beu","y'gas beu","y's teva","tremenys")
ymbeus_imperfect = rannowVerbAnreyth("y'm beus","NULL","y'm bo","y'th o","y'n jevo","y's tevo","y'gan bo","y'gas bo","y's tevo","anperfydh")
ymbeus_pluperfect = rannowVerbAnreyth("y'm beus","NULL","y'm bo","y'th o","y'n jevo","y's tevo","y'gan bo","y'gas bo","y's tevo","gorperfydh")
ymbeus_pressubj = rannowVerbAnreyth("y'm beus","NULL","y'm bo","y'fo","y'n jeffo","y's teffo","y'gan bo","y'gas bo","y's teffo","islavarek_a-lemmyn")
ymbeus_impfsubj = rannowVerbAnreyth("y'm beus","NULL","y'm be","y'fe","y'n jeffa","y's teffa","y'gan be","y'gas be","y's teffa","islavarek_anperfydh")
ymbeus_future = rannowVerbAnreyth("y'm beus","NULL","y'm bydh","y'fydh","y'n jevydh","y's tevydh","y'gan bydh","y'gas bydh","y's tevydh","devedhek")
ymbeus_habitimperfect = rannowVerbAnreyth("y'm beus","NULL","y'm bedha","y'fedha","y'n jevedha","y's tevedha","y'gan bedha","y'gas bedha","y's tevedha","anperfydh_usadow")
ymbeus_tenses = [ymbeus_pres,ymbeus_preterite,ymbeus_imperfect,ymbeus_pluperfect,ymbeus_pressubj,ymbeus_impfsubj,ymbeus_future,ymbeus_habitimperfect]
# nag eus gorhemmyn
# no imperative
ymbeus_inflected = rannowVerbAnreythOllAmser("y'm beus")
ymbeus_inflected.addTenseList(ymbeus_tenses)

# PIW 
# y'th eus devedhek sempel hag anperfydh usadow
# has simple future and habitual imperfect
piw_pres =  rannowVerbAnreyth("piw","piwor","piwov","piwos","piw","piw","piwon","piwowgh","piwyns","a-lemmyn")
piw_preterite  = rannowVerbAnreyth("piw","piwor","piwev","piwes","piwva","piwva","piwven","piwvewgh","piwvons","tremenys")
piw_imperfect = rannowVerbAnreyth("piw","piwer","piwen","piwes","piwo","piwo","piwen","piwewgh","piwens","anperfydh")
piw_pluperfect = rannowVerbAnreyth("piw","piwor","piwvien","piwvies","piwvia","piwvia","piwvien","piwviewgh","piwviens","gorperfydh")
piw_pressubj = rannowVerbAnreyth("piw","piwver","piwviv","piwvi","piwvo","piwvo","piwvyn","piwvowgh","piwvons","islavarek_a-lemmyn")
piw_impfsubj = rannowVerbAnreyth("piw","piwves","piwven","piwves","piwva","piwva","piwven","piwvewgh","piwvens","islavarek_anperfydh")
piw_future = rannowVerbAnreyth("piw","piwor","piwvydhav","piwvydhydh","piwvydh","piwvydh","piwvydhyn","piwvydhowgh","piwvydhons","devedhek")
piw_habitimperfect = rannowVerbAnreyth("piw","piwvedhes","piwvedhen","piwvedhes","piwvedha","piwvedha","piwvedhen","piwvedhewgh","piwvedhens","anperfydh_usadow")
piw_tenses = [piw_pres,piw_preterite,piw_imperfect,piw_pluperfect,piw_pressubj,piw_impfsubj,piw_future,piw_habitimperfect]
# nag eus gorhemmyn
# no imperative
piw_inflected = rannowVerbAnreythOllAmser("piw")
piw_inflected.addTenseList(piw_tenses)

# GODHVOS
# a'th eus devedhek sempel mes nag anperfydh usadow
# has simple future but not habitual imperfect
godhvos_pres = rannowVerbAnreyth("godhvos","godhor","gonn","godhes","goer","goer","godhon","godhowgh","godhons","a-lemmyn")
#2s pres/fut may contract to gosta

godhvos_preterite = rannowVerbAnreyth("godhvos","godhves","godhvev","godhves","godhva","godhva","godhven","godhvewgh","godhvons","tremenys")

godhvos_imperfect = rannowVerbAnreyth("godhvos","godhyes","godhyen","godhyes","godhya","godhya","godhyen","godhyewgh","godhyens","anperfydh")

godhvos_pluperfect = rannowVerbAnreyth("godhvos","godhvies","godhvien","godhvies","godhvia","godhvia","godhvien","godhviewgh","godhviens","gorperfydh")

godhvos_pressubj = rannowVerbAnreyth("godhvos","godher","godhviv","godhvi","godhvo","godhvo","godhvyn","godhvowgh","godhvons","islavarek_a-lemmyn")

godhvos_impfsubj = rannowVerbAnreyth("godhvos","godhves","godhven","godhves","godhve","godhve","godhven","godhvewgh","godhvens","islavarek_anperfydh")

godhvos_imperative = rannowVerbAnreyth("godhvos","NULL","NULL","godhvydh","godhvydhes","godhvydhes","godhvydhyn","godhvydhewgh","godhvydhens","gorhemmyn")

godhvos_pastparticiple = "godhvedhys"

godhvos_future = rannowVerbAnreyth("godhvos","godhvydher","godhvydhav","godhvydhydh","godhvydh","godhvydh","godhvydhyn","godhvydhowgh","godhvydhons","devedhek")

godhvos_tenses = [godhvos_pres,godhvos_preterite,godhvos_imperfect,godhvos_pluperfect,godhvos_pressubj,godhvos_impfsubj,godhvos_imperative,godhvos_future]
godhvos_inflected = rannowVerbAnreythOllAmser("godhvos")
godhvos_inflected.addTenseList(godhvos_tenses,godhvos_pastparticiple)

# TYLI
# a'th eus devedhek sempel mes nag anperfydh usadow
# has simple future but not habitual imperfect
tyli_pres = rannowVerbAnreyth("tyli","tylir","talav","tylydh","tal","tal","tylyn","tylowgh","talons","a-lemmyn")
tyli_preterite = rannowVerbAnreyth("tyli","tylys","tylis","tylsys","tylis","tylis","tylsyn","tylsowgh","talsons","tremenys")
tyli_imperfect = rannowVerbAnreyth("tyli","teles","telen","teles","tela","tela","telen","telewgh","telens","anperfydh")
tyli_pluperfect = rannowVerbAnreyth("tyli","talvies","talvien","talvies","talvia","talvia","talvien","talviewgh","talviens","gorperfydh")
tyli_pressubj = rannowVerbAnreyth("tyli","taller","tylliv","tylli","tallo","tallo","tyllyn","tyllowgh","tallons","islavarek_a-lemmyn")
tyli_impfsubj = rannowVerbAnreyth("tyli","tallfes","tallfen","tallfes","tallfa","tallfa","tallfen","tallfewgh","tallfens","islavarek_anperfydh")
tyli_imperative = rannowVerbAnreyth("tyli","NULL","NULL","tal","teles","teles","telen","telewgh","telens","gorhemmyn")

tyli_pastparticiple = "tylys"
tyli_future = rannowVerbAnreyth("tyli","talvydher","talvydhav","talvydhydh","talvydh","talvydh","talvydhyn","talvydhowgh","talvydhons","devedhek")

tyli_tenses = [tyli_pres,tyli_preterite,tyli_imperfect,tyli_pluperfect,tyli_pressubj,tyli_impfsubj,tyli_imperative,tyli_future]
tyli_inflected = rannowVerbAnreythOllAmser("tyli")
tyli_inflected.addTenseList(tyli_tenses,tyli_pastparticiple)

# ATTYLI 
# kepar ha TYLI
# conjugated as TYLI
attyli_pres = rannowVerbAnreyth("attyli","attylir","attalav","attylydh","attal","attal","attylyn","attylowgh","attalons","a-lemmyn")
attyli_preterite = rannowVerbAnreyth("attyli","attylys","attylis","attylsys","attylis","attylis","attylsyn","attylsowgh","attalsons","tremenys")
attyli_imperfect = rannowVerbAnreyth("attyli","atteles","attelen","atteles","attela","attela","attelen","attelewgh","attelens","anperfydh")
attyli_pluperfect = rannowVerbAnreyth("attyli","attalvies","attalvien","attalvies","attalvia","attalvia","attalvien","attalviewgh","attalviens","gorperfydh")
attyli_pressubj = rannowVerbAnreyth("attyli","attaller","attylliv","attylli","attallo","attallo","attyllyn","attyllowgh","attallons","islavarek_a-lemmyn")
attyli_impfsubj = rannowVerbAnreyth("attyli","attallfes","attallfen","attallfes","attallfa","attallfa","attallfen","attallfewgh","attallfens","islavarek_anperfydh")
attyli_imperative = rannowVerbAnreyth("attyli","NULL","NULL","attal","atteles","atteles","attelen","attelewgh","attelens","gorhemmyn")

attyli_pastparticiple = "attylys"
attyli_future = rannowVerbAnreyth("attyli","attalvydher","attalvydhav","attalvydhydh","attalvydh","attalvydh","attalvydhyn","attalvydhowgh","attalvydhons","devedhek")

attyli_tenses = [attyli_pres,attyli_preterite,attyli_imperfect,attyli_pluperfect,attyli_pressubj,attyli_impfsubj,attyli_imperative,attyli_future]
attyli_inflected = rannowVerbAnreythOllAmser("attyli")
attyli_inflected.addTenseList(attyli_tenses,attyli_pastparticiple)

# HWARVOS
# 3s yn unnsel
# only found in 3s
hwarvos_pres = rannowVerbAnreyth("hwarvos","NULL","NULL","NULL","hwer","hwer","NULL","NULL","NULL","a-lemmyn")
hwarvos_preterite = rannowVerbAnreyth("hwarvos","NULL","NULL","NULL","hwarva","hwarva","NULL","NULL","NULL","tremenys")
hwarvos_imperfect = rannowVerbAnreyth("hwarvos","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","anperfydh")
hwarvos_pluperfect = rannowVerbAnreyth("hwarvos","NULL","NULL","NULL","hwarvia","hwarvia","NULL","NULL","NULL","gorperfydh")
hwarvos_pressubj = rannowVerbAnreyth("hwarvos","NULL","NULL","NULL","hwarvo","hwarvo","NULL","NULL","NULL","islavarek_a-lemmyn")
hwarvos_impfsubj = rannowVerbAnreyth("hwarvos","NULL","NULL","NULL","hwarva","hwarva","NULL","NULL","NULL","islavarek_anperfydh")
hwarvos_pastparticiple = "hwarvedhys"
hwarvos_future = rannowVerbAnreyth("hwarvos","NULL","NULL","NULL","hwyrvydh","hwyrvydh","NULL","NULL","NULL","devedhek")
hwarvos_tenses = [hwarvos_pres,hwarvos_preterite,hwarvos_pluperfect,hwarvos_pressubj,hwarvos_impfsubj,hwarvos_future]
hwarvos_inflected = rannowVerbAnreythOllAmser("hwarvos")
hwarvos_inflected.addTenseList(hwarvos_tenses,hwarvos_pastparticiple)

# DARVOS
# only 3s pret and past participle
# 3s tremenys ha PPL yn unnsel
darvos_preterite = rannowVerbAnreyth("darvos","NULL","NULL","NULL","darva","darva","NULL","NULL","NULL","tremenys")
darvos_pastparticiple = "darvedhys"
darvos_tenses = [darvos_preterite]
darvos_inflected = rannowVerbAnreythOllAmser("darvos")
darvos_inflected.addTenseList(darvos_tenses,darvos_pastparticiple)

# KLYWES
# no simple future or habitual imperfect

klywes_pres = rannowVerbAnreyth("klywes","klywir","klywav","klywydh","klyw","klyw","klywyn","klywowgh","klywons","a-lemmyn")
klywes_preterite =  rannowVerbAnreyth("klywes","klywas","klywis","klywsys","klywas","klywas","klywsyn","klywsowgh","klywsons","tremenys")
klywes_imperfect =  rannowVerbAnreyth("klywes","klywes","klywen","klywes","klywo","klywo","klywen","klywewgh","klywens","anperfydh")
klywes_pluperfect = rannowVerbAnreyth("klywes","klywsys","klywsen","klywses","klywsa","klywsa","klywsen","klywsewgh","klywsens","gorperfydh")
klywes_pressubj = rannowVerbAnreyth("klywes","klywver","klywviv","klywvi","klywvo","klywvo","klywvyn","klywvowgh","klywvons","islavarek_a-lemmyn")
klywes_impfsubj = rannowVerbAnreyth("klywes","klywves","klywven","klywves","klywva","klywva","klywven","klywvewgh","klywvens","islavarek_anperfydh")
klywes_imperative = rannowVerbAnreyth("klywes","NULL","NULL","klyw","klywes","klywes","klywyn","klywewgh","klywens","gorhemmyn")
klywes_pastparticiple = "klywys"
klywes_tenses = [klywes_pres,klywes_preterite,klywes_imperfect,klywes_pluperfect,klywes_pressubj,klywes_impfsubj,klywes_imperative]
klywes_inflected = rannowVerbAnreythOllAmser("klywes")
klywes_inflected.addTenseList(klywes_tenses,klywes_pastparticiple)

#OMGLYWES similarly conjugated
omglywes_pres = rannowVerbAnreyth("omglywes","omglywir","omglywav","omglywydh","omglyw","omglyw","omglywyn","omglywowgh","omglywons","a-lemmyn")
omglywes_preterite =  rannowVerbAnreyth("omglywes","omglywas","omglywis","omglywsys","omglywas","omglywas","omglywsyn","omglywsowgh","omglywsons","tremenys")
omglywes_imperfect =  rannowVerbAnreyth("omglywes","omglywes","omglywen","omglywes","omglywo","omglywo","omglywen","omglywewgh","omglywens","anperfydh")
omglywes_pluperfect = rannowVerbAnreyth("omglywes","omglywsys","omglywsen","omglywses","omglywsa","omglywsa","omglywsen","omglywsewgh","omglywsens","gorperfydh")
omglywes_pressubj = rannowVerbAnreyth("omglywes","omglywver","omglywviv","omglywvi","omglywvo","omglywvo","omglywvyn","omglywvowgh","omglywvons","islavarek_a-lemmyn")
omglywes_impfsubj = rannowVerbAnreyth("omglywes","omglywves","omglywven","omglywves","omglywva","omglywva","omglywven","omglywvewgh","omglywvens","islavarek_anperfydh")
omglywes_imperative = rannowVerbAnreyth("omglywes","NULL","NULL","omglyw","omglywes","omglywes","omglywyn","omglywewgh","omglywens","gorhemmyn")
omglywes_pastparticiple = "omglywys"
omglywes_tenses = [omglywes_pres,omglywes_preterite,omglywes_imperfect,omglywes_pluperfect,omglywes_pressubj,omglywes_impfsubj,omglywes_imperative]
omglywes_inflected = rannowVerbAnreythOllAmser("omglywes")
omglywes_inflected.addTenseList(omglywes_tenses,omglywes_pastparticiple)


# MOS/MONES
# a'th eus amser perfydh
# special perfect tense
mos_pres = rannowVerbAnreyth("mos","er","av","edh","a","a","en","ewgh","ons","a-lemmyn")
mos_preterite = rannowVerbAnreyth("mos","es","yth","ythys","eth","eth","ethen","ethewgh","ethons","tremenys")
mos_imperfect = rannowVerbAnreyth("mos","es","en","es","e","e","en","ewgh","ens","anperfydh")
mos_pluperfect = rannowVerbAnreyth("mos","NULL","gylsen","gylses","galsa","galsa","gylsen","gylsewgh","gylsens","gorperfydh")
mos_perfect = rannowVerbAnreyth("mos","NULL","galsov","galsos","gallas","gallas","galson","galsowgh","galsons","perfydh")
mos_pressubj = rannowVerbAnreyth("mos","eller","ylliv","ylli","ello","ello","yllyn","yllowgh","ellons","islavarek_a-lemmyn")
mos_impfsubj = rannowVerbAnreyth("mos","elles","ellen","elles","ella","ella","ellen","ellewgh","ellens","islavarek_anperfydh")
mos_imperative = rannowVerbAnreyth("mos","NULL","NULL","ke","es","es","deun","kewgh","ens","gorhemmyn")
mos_pastparticiple = "gyllys"
mos_tenses = [mos_pres,mos_preterite,mos_imperfect,mos_pluperfect,mos_pressubj,mos_impfsubj,mos_imperative,mos_perfect]
mos_inflected = rannowVerbAnreythOllAmser("mos")
mones_inflected = rannowVerbAnreythOllAmser("mones")
mos_inflected.addTenseList(mos_tenses,mos_pastparticiple)
mones_inflected.addTenseList(mos_tenses,mos_pastparticiple)


# DOS/DONES
# a'th eus amser perfydh
# special perfect tense
dos_pres = rannowVerbAnreyth("dos","deer","dov","deudh","deu","deu","deun","dewgh","dons","a-lemmyn")
dos_preterite = rannowVerbAnreyth("dos","deuthes","deuth","deuthys","deuth","deuth","deuthen","deuthewgh","deuthons","tremenys")
dos_imperfect = rannowVerbAnreyth("dos","des","den","des","do","do","den","dewgh","dens","anperfydh")
dos_pluperfect = rannowVerbAnreyth("dos","dothyes","dothyen","dothyes","dothya","dothya","dothyen","dothyewgh","dothyens","gorperfydh")
dos_perfect = rannowVerbAnreyth("dos","deuves","deuvev","deuves","deuva","deuva","deuven","deuvewgh","deuvons","perfydh")
dos_pressubj = rannowVerbAnreyth("dos","deffer","dyffiv","dyffi","deffo","deffo","dyffyn","dyffowgh","deffons","islavarek_a-lemmyn")
dos_impfsubj = rannowVerbAnreyth("dos","deffes","deffen","deffes","deffa","deffa","deffen","deffewgh","deffens","islavarek_anperfydh")
dos_imperative = rannowVerbAnreyth("dos","NULL","NULL","deus","des","des","deun","dewgh","dens","gorhemmyn")
dos_pastparticiple = "devedhys"
dos_tenses = [dos_pres,dos_preterite,dos_imperfect,dos_pluperfect,dos_pressubj,dos_impfsubj,dos_imperative,dos_perfect]
dos_inflected = rannowVerbAnreythOllAmser("dos")
dones_inflected = rannowVerbAnreythOllAmser("dones")
dos_inflected.addTenseList(dos_tenses,dos_pastparticiple)
dones_inflected.addTenseList(dos_tenses,dos_pastparticiple)

#DOEN
doen_pres = rannowVerbAnreyth("doen","degir","degav","degedh","deg","deg","degon","degowgh","degons","a-lemmyn")
doen_preterite = rannowVerbAnreyth("doen","dug","dug","duges","dug","dug","dugon","dugowgh","dugons","tremenys")
doen_imperfect = rannowVerbAnreyth("doen","degys","degyn","degys","degi","degi","degyn","degewgh","degens","anperfydh")
doen_pluperfect = rannowVerbAnreyth("doen","degsys","degsen","degses","degsa","degsa","degsen","degsewgh","degsens","gorperfydh")
doen_pressubj = rannowVerbAnreyth("doen","dokker","dykkiv","dykki","dokko","dokko","dykkyn","dykkowgh","dokkons","islavarek_a-lemmyn")
doen_impfsubj = rannowVerbAnreyth("doen","dekkys","dekken","dekkes","dekka","dekka","dekken","dekkewgh","dekkens","islavarek_anperfydh")
doen_imperative = rannowVerbAnreyth("doen","NULL","NULL","dog","deges","deges","degyn","degewgh","degens","gorhemmyn")
doen_pastparticiple = "degys"
doen_tenses = [doen_pres,doen_preterite,doen_imperfect,doen_pluperfect,doen_pressubj,doen_impfsubj,doen_imperative]
doen_inflected = rannowVerbAnreythOllAmser("doen")
doen_inflected.addTenseList(doen_tenses,doen_pastparticiple)

# OMDHOEN
# kepar ha doen
# conjugated as for doen
omdhoen_pres = rannowVerbAnreyth("omdhoen","omdhegir","omdhegav","omdhegedh","omdheg","omdheg","omdhegon","omdhegowgh","omdhegons","a-lemmyn")
omdhoen_preterite = rannowVerbAnreyth("omdhoen","omdhug","omdhug","omdhuges","omdhug","omdhug","omdhugon","omdhugowgh","omdhugons","tremenys")
omdhoen_imperfect = rannowVerbAnreyth("omdhoen","omdhegys","omdhegyn","omdhegys","omdhegi","omdhegi","omdhegyn","omdhegewgh","omdhegens","anperfydh")
omdhoen_pluperfect = rannowVerbAnreyth("omdhoen","omdhegsys","omdhegsen","omdhegses","omdhegsa","omdhegsa","omdhegsen","omdhegsewgh","omdhegsens","gorperfydh")
omdhoen_pressubj = rannowVerbAnreyth("omdhoen","omdhokker","omdhykkiv","omdhykki","omdhokko","omdhokko","omdhykkyn","omdhykkowgh","omdhokkons","islavarek_a-lemmyn")
omdhoen_impfsubj = rannowVerbAnreyth("omdhoen","omdhekkys","omdhekken","omdhekkes","omdhekka","omdhekka","omdhekken","omdhekkewgh","omdhekkens","islavarek_anperfydh")
omdhoen_imperative = rannowVerbAnreyth("omdhoen","NULL","NULL","omdhog","omdheges","omdheges","omdhegyn","omdhegewgh","omdhegens","gorhemmyn")
omdhoen_pastparticiple = "omdhegys"
omdhoen_tenses = [omdhoen_pres,omdhoen_preterite,omdhoen_imperfect,omdhoen_pluperfect,omdhoen_pressubj,omdhoen_impfsubj,omdhoen_imperative]
omdhoen_inflected = rannowVerbAnreythOllAmser("omdhoen")
omdhoen_inflected.addTenseList(omdhoen_tenses,omdhoen_pastparticiple)

#RI
ri_pres = rannowVerbAnreyth("ri","rer","rov","redh","re","re","ren","rowgh","rons","a-lemmyn")
ri_preterite = rannowVerbAnreyth("ri","ros","res","resys","ros","ros","resen","resowgh","rosons","tremenys")
ri_imperfect = rannowVerbAnreyth("ri","res","ren","res","ri","ri","ren","rewgh","rens","anperfydh")
ri_pluperfect = rannowVerbAnreyth("ri","rosys","rosen","roses","rosa","rosa","rosen","rosewgh","rosens","gorperfydh")
ri_pressubj = rannowVerbAnreyth("ri","roller","rylliv","rylli","rollo","rollo","ryllyn","ryllowgh","rollons","islavarek_a-lemmyn")
ri_impfsubj = rannowVerbAnreyth("ri","rollys","rollen","rolles","rolla","rolla","rollen","rollewgh","rollens","islavarek_anperfydh")
ri_imperative = rannowVerbAnreyth("ri","NULL","NULL","ro","res","res","ren","rewgh","rens","gorhemmyn")
ri_pastparticiple = "res"
ri_tenses = [ri_pres,ri_preterite,ri_imperfect,ri_pluperfect,ri_pressubj,ri_impfsubj,ri_imperative]
ri_inflected = rannowVerbAnreythOllAmser("ri")
ri_inflected.addTenseList(ri_tenses,ri_pastparticiple)
# ro/roy kyns kessonenn / bogalenn
# ro/roy used before consonant/vowel


#DRI
# kepar ha RI 
# conjugated as for RI
dri_pres = rannowVerbAnreyth("dri","drer","drov","dredh","dre","dre","dren","drowgh","drons","a-lemmyn")
dri_preterite = rannowVerbAnreyth("dri","dros","dres","dresys","dros","dros","dresen","dresowgh","drosons","tremenys")
dri_imperfect = rannowVerbAnreyth("dri","dres","dren","dres","dri","dri","dren","drewgh","drens","anperfydh")
dri_pluperfect = rannowVerbAnreyth("dri","drosys","drosen","droses","drosa","drosa","drosen","drosewgh","drosens","gorperfydh")
dri_pressubj = rannowVerbAnreyth("dri","droller","drylliv","drylli","drollo","drollo","dryllyn","dryllowgh","drollons","islavarek_a-lemmyn")
dri_impfsubj = rannowVerbAnreyth("dri","drollys","drollen","drolles","drolla","drolla","drollen","drollewgh","drollens","islavarek_anperfydh")
dri_imperative = rannowVerbAnreyth("dri","NULL","NULL","dro","dres","dres","dren","drewgh","drens","gorhemmyn")
dri_pastparticiple = "dres"
dri_tenses = [dri_pres,dri_preterite,dri_imperfect,dri_pluperfect,dri_pressubj,dri_impfsubj,dri_imperative]
dri_inflected = rannowVerbAnreythOllAmser("dri")
dri_inflected.addTenseList(dri_tenses,dri_pastparticiple)
# doro/doroy kyns kessonenn /bogalenn
#doro/doroy before const/vowel

#TI 'swear
ti_pres = rannowVerbAnreyth("ti","ter","tov","tedh","te","te","ten","towgh","tons","a-lemmyn")
ti_preterite = rannowVerbAnreyth("ti","tos","tes","tesys","tos","tos","tesen","tesowgh","tosons","tremenys")
ti_imperfect = rannowVerbAnreyth("ti","tes","ten","tes","te","te","ten","tewgh","tens","anperfydh")
ti_pluperfect = rannowVerbAnreyth("ti","tosys","tosen","toses","tosa","tosa","tosen","tosewgh","tosens","gorperfydh")
ti_pressubj = rannowVerbAnreyth("ti","toller","tylliv","tylli","tollo","tollo","tyllyn","tyllowgh","tollons","islavarek_a-lemmyn")
ti_impfsubj = rannowVerbAnreyth("ti","tollys","tollen","tolles","tolla","tolla","tollen","tollewgh","tollens","islavarek_anperfydh")
ti_imperative = rannowVerbAnreyth("ti","NULL","NULL","to","tes","tes","ten","tewgh","tens","gorhemmyn")
ti_pastparticiple = "tes"
ti_tenses = [ti_pres,ti_preterite,ti_imperfect,ti_pluperfect,ti_pressubj,ti_impfsubj,ti_imperative]
ti_inflected = rannowVerbAnreythOllAmser("ti")
ti_inflected.addTenseList(ti_tenses,ti_pastparticiple)
# ti 'to' yw reyth
# ti 'roof' is regular (not implemented)

#DYLLO
dyllo_pres = rannowVerbAnreyth("dyllo","dyllir","dyllav","dyllydh","dyllo","dyllo","dyllyn","dyllowgh","dyllons","a-lemmyn")
dyllo_preterite = rannowVerbAnreyth("dyllo","dellos","delles","dellesys","dellos","dellos","dellesyn","dellesowgh","dellesons","tremenys")
dyllo_imperfect = rannowVerbAnreyth("dyllo","dyllys","dyllyn","dyllys","dylli","dylli","dyllyn","dyllewgh","dyllens","anperfydh")
dyllo_pluperfect = rannowVerbAnreyth("dyllo","dyllsys","dyllsen","dyllses","dyllsa","dyllsa","dyllsen","dyllsewgh","dyllsens","gorperfydh")
dyllo_pressubj = rannowVerbAnreyth("dyllo","dyller","dylliv","dylli","dello","dello","dyllyn","dyllowgh","dellons","islavarek_a-lemmyn")
dyllo_impfsubj = rannowVerbAnreyth("dyllo","dellys","dellen","delles","della","della","dellen","dellewgh","dellens","islavarek_anperfydh")
dyllo_imperative = rannowVerbAnreyth("dyllo","NULL","NULL","dyllo","dylles","dylles","dyllyn","dyllewgh","dyllens","gorhemmyn")
dyllo_pastparticiple = "dyllys"
dyllo_tenses = [dyllo_pres,dyllo_preterite,dyllo_imperfect,dyllo_pluperfect,dyllo_pressubj,dyllo_impfsubj,dyllo_imperative]
dyllo_inflected = rannowVerbAnreythOllAmser("dyllo")
dyllo_inflected.addTenseList(dyllo_tenses,dyllo_pastparticiple)

#GUL

gul_pres = rannowVerbAnreyth("gul","gwrer","gwrav","gwredh","gwra","gwra","gwren","gwrewgh","gwrons","a-lemmyn")
gul_preterite = rannowVerbAnreyth("gul","gwrug","gwrug","gwrussys","gwrug","gwrug","gwrussyn","gwrussowgh","gwrussons","tremenys")
gul_imperfect = rannowVerbAnreyth("gul","gwres","gwren","gwres","gwre","gwre","gwren","gwrewgh","gwrens","anperfydh")
gul_pluperfect = rannowVerbAnreyth("gul","gwrussys","gwrussen","gwrusses","gwrussa","gwrussa","gwrussen","gwrussewgh","gwrussens","gorperfydh")
gul_pressubj = rannowVerbAnreyth("gul","gwreller","gwrylliv","gwrylli","gwrello","gwrello","gwryllyn","gwryllowgh","gwrellons","islavarek_a-lemmyn")
gul_impfsubj = rannowVerbAnreyth("gul","gwrellys","gwrellen","gwrelles","gwrella","gwrella","gwrellen","gwrellewgh","gwrellens","islavarek_anperfydh")
gul_imperative = rannowVerbAnreyth("gul","NULL","NULL","gwra","gwres","gwres","gwren","gwrewgh","gwrens","gorhemmyn")
gul_pastparticiple = "gwrys"
gul_tenses = [gul_pres,gul_preterite,gul_imperfect,gul_pluperfect,gul_pressubj,gul_impfsubj,gul_imperative]
gul_inflected = rannowVerbAnreythOllAmser("gul")
gul_inflected.addTenseList(gul_tenses,gul_pastparticiple)

#OMWUL
# kepar ha GUL
# conjugated as GUL
omwul_pres = rannowVerbAnreyth("omwul","omwrer","omwrav","omwredh","omwra","omwra","omwren","omwrewgh","omwrons","a-lemmyn")
omwul_preterite = rannowVerbAnreyth("omwul","omwrug","omwrug","omwrussys","omwrug","omwrug","omwrussyn","omwrussowgh","omwrussons","tremenys")
omwul_imperfect = rannowVerbAnreyth("omwul","omwres","omwren","omwres","omwre","omwre","omwren","omwrewgh","omwrens","anperfydh")
omwul_pluperfect = rannowVerbAnreyth("omwul","omwrussys","omwrussen","omwrusses","omwrussa","omwrussa","omwrussen","omwrussewgh","omwrussens","gorperfydh")
omwul_pressubj = rannowVerbAnreyth("omwul","omwreller","omwrylliv","omwrylli","omwrello","omwrello","omwryllyn","omwryllowgh","omwrellons","islavarek_a-lemmyn")
omwul_impfsubj = rannowVerbAnreyth("omwul","omwrellys","omwrellen","omwrelles","omwrella","omwrella","omwrellen","omwrellewgh","omwrellens","islavarek_anperfydh")
omwul_imperative = rannowVerbAnreyth("omwul","NULL","NULL","omwra","omwres","omwres","omwren","omwrewgh","omwrens","gorhemmyn")
omwul_pastparticiple = "omwrys"
omwul_tenses = [omwul_pres,omwul_preterite,omwul_imperfect,omwul_pluperfect,omwul_pressubj,omwul_impfsubj,omwul_imperative]
omwul_inflected = rannowVerbAnreythOllAmser("omwul")
omwul_inflected.addTenseList(omwul_tenses,omwul_pastparticiple)

#MYNNES
mynnes_pres = rannowVerbAnreyth("mynnes","mynnir","mynnav","mynnydh","mynn","mynn","mynnyn","mynnowgh","mynnons","a-lemmyn")
mynnes_preterite = rannowVerbAnreyth("mynnes","mynnas","mynnis","mynnsys","mynnas","mynnas","mynnsyn","mynnsowgh","mynnsons","tremenys")
mynnes_imperfect = rannowVerbAnreyth("mynnes","mynnys","mynnen","mynnes","mynna","mynna","mynnen","mynnewgh","mynnens","anperfydh")
mynnes_pluperfect = rannowVerbAnreyth("mynnes","mynnsys","mynnsen","mynnses","mynnsa","mynnsa","mynnsen","mynnsewgh","mynnsens","gorperfydh")
mynnes_pressubj = rannowVerbAnreyth("mynnes","mynner","mynniv","mynni","mynno","mynno","mynnyn","mynnowgh","mynnons","islavarek_a-lemmyn")
mynnes_impfsubj = rannowVerbAnreyth("mynnes","mynnys","mynnen","mynnes","mynna","mynna","mynnen","mynnewgh","mynnens","islavarek_anperfydh")
mynnes_tenses = [mynnes_pres,mynnes_preterite,mynnes_imperfect,mynnes_pluperfect,mynnes_pressubj,mynnes_impfsubj]
# nag eus gorhemmyn
# no imperative
mynnes_inflected = rannowVerbAnreythOllAmser("mynnes")
mynnes_inflected.addTenseList(mynnes_tenses)

#GALLOES
galloes_pres = rannowVerbAnreyth("galloes","gyllir","gallav","gyllydh","gyll","gyll","gyllyn","gyllowgh","gyllons","a-lemmyn")
galloes_preterite = rannowVerbAnreyth("galloes","gallas","gyllis","gyllsys","gallas","gallas","gyllsyn","gyllsowgh","gallsons","tremenys")
galloes_imperfect = rannowVerbAnreyth("galloes","gyllys","gyllyn","gyllys","gylli","gylli","gyllyn","gyllewgh","gyllens","anperfydh")
galloes_pluperfect = rannowVerbAnreyth("galloes","gallses","gallsen","gallses","gallsa","gallsa","gallsen","gallsewgh","gallsens","gorperfydh")
galloes_pressubj = rannowVerbAnreyth("galloes","galler","gylliv","gylli","gallo","gallo","gyllyn","gyllowgh","gallons","islavarek_a-lemmyn")
galloes_impfsubj = rannowVerbAnreyth("galloes","galles","gallen","galles","galla","galla","gallen","gallewgh","gallens","islavarek_anperfydh")
galloes_tenses = [galloes_pres,galloes_preterite,galloes_imperfect,galloes_pluperfect,galloes_pressubj,galloes_impfsubj]
# nag eus gorhemmyn
# no imperative
#pluperfect conditional is gallser (not implemented)
galloes_inflected = rannowVerbAnreythOllAmser("galloes")
galloes_inflected.addTenseList(galloes_tenses)

# BRYJYON
bryjyon_pres = rannowVerbAnreyth("bryjyon","bryjir","brojyav","bryjydh","bros","bros","bryjyn","bryjyowgh","brojyons","a-lemmyn")
bryjyon_preterite = rannowVerbAnreyth("bryjyon","brojyas","bryjis","bryjsys","brojyas","brojyas","bryjsyn","bryjsowgh","brojsons","tremenys")
bryjyon_imperfect = rannowVerbAnreyth("bryjyon","bryjys","brojyen","brojyes","brojya","brojya","brojyen","brojyewgh","brojyens","anperfydh")
bryjyon_pluperfect = rannowVerbAnreyth("bryjyon","bryjsys","brojsen","brojses","brojsa","brojsa","brojsen","brojsewgh","brojsens","gorperfydh")
bryjyon_pressubj = rannowVerbAnreyth("bryjyon","brocchyer","brycchiv","brycchi","brocchyo","brocchyo","brycchyn","brycchyowgh","brocchyons","islavarek_a-lemmyn")
bryjyon_impfsubj = rannowVerbAnreyth("bryjyon","brycchys","brocchyen","brycchyes","brocchya","brocchya","brocchyen","brocchyewgh","brocchyens","islavarek_anperfydh")
bryjyon_imperative = rannowVerbAnreyth("bryjyon","NULL","NULL","bros","brojyes","brojyes","bryjyn","bryjyewgh","brojyens","gorhemmyn")
bryjyon_tenses = [bryjyon_pres,bryjyon_preterite,bryjyon_imperfect,bryjyon_pluperfect,bryjyon_pressubj,bryjyon_impfsubj,bryjyon_imperative]
bryjyon_inflected = rannowVerbAnreythOllAmser("bryjyon")
bryjyon_inflected.addTenseList(bryjyon_tenses)

# verbow defowtek
# defective verbs 
verbs_defective = ["hwarvos","darvos","bern","darwar","degoedh","koedh","delledh","deur","hweles","medhes","pargh","paragh","res","skila","tann","war"]
#BERN
bern_pres = rannowVerbAnreyth("bern","NULL","NULL","NULL","bern","bern","NULL","NULL","NULL","a-lemmyn")
bern_tenses = [bern_pres]
bern_inflected = rannowVerbAnreythOllAmser("bern")
bern_inflected.addTenseList(bern_tenses)

#DARWAR
darwar_imperative = rannowVerbAnreyth("darwar","NULL","NULL","darwar","NULL","NULL","NULL","darwaryewgh","NULL","gorhemmyn")
darwar_tenses = [darwar_imperative]
darwar_inflected = rannowVerbAnreythOllAmser("darwar")
darwar_inflected.addTenseList(darwar_tenses)

#DEGOEDH
degoedh_pres = rannowVerbAnreyth("degoedh","NULL","NULL","NULL","degoedh","degoedh","NULL","NULL","NULL","a-lemmyn")
degoedh_preterite = rannowVerbAnreyth("degoedh","NULL","NULL","NULL","degoedhva","degoedhva","NULL","NULL","NULL","tremenys")
degoedh_imperfect = rannowVerbAnreyth("degoedh","NULL","NULL","NULL","degoedho","degoedho","NULL","NULL","NULL","anperfydh")
degoedh_pluperfect = rannowVerbAnreyth("degoedh","NULL","NULL","NULL","degoedhvia","degoedhvia","NULL","NULL","NULL","gorperfydh")
degoedh_pressubj = rannowVerbAnreyth("degoedh","NULL","NULL","NULL","degoedhvo","degoedhvo","NULL","NULL","NULL","islavarek_a-lemmyn")
degoedh_impfsubj = rannowVerbAnreyth("degoedh","NULL","NULL","NULL","degoedhva","degoedhva","NULL","NULL","NULL","islavarek_anperfydh")
degoedh_tenses = [degoedh_pres,degoedh_preterite,degoedh_pluperfect,degoedh_pressubj,degoedh_impfsubj]
degoedh_inflected = rannowVerbAnreythOllAmser("degoedh")
degoedh_inflected.addTenseList(degoedh_tenses)

#KOEDH
koedh_pres = rannowVerbAnreyth("koedh","NULL","NULL","NULL","koedh","koedh","NULL","NULL","NULL","a-lemmyn")
koedh_preterite = rannowVerbAnreyth("koedh","NULL","NULL","NULL","koedhva","koedhva","NULL","NULL","NULL","tremenys")
koedh_imperfect = rannowVerbAnreyth("koedh","NULL","NULL","NULL","koedho","koedho","NULL","NULL","NULL","anperfydh")
koedh_pluperfect = rannowVerbAnreyth("koedh","NULL","NULL","NULL","koedhvia","koedhvia","NULL","NULL","NULL","gorperfydh")
koedh_pressubj = rannowVerbAnreyth("koedh","NULL","NULL","NULL","koedhvo","koedhvo","NULL","NULL","NULL","islavarek_a-lemmyn")
koedh_impfsubj = rannowVerbAnreyth("koedh","NULL","NULL","NULL","koedhva","koedhva","NULL","NULL","NULL","islavarek_anperfydh")
koedh_tenses = [koedh_pres,koedh_preterite,koedh_pluperfect,koedh_pressubj,koedh_impfsubj]
koedh_inflected = rannowVerbAnreythOllAmser("koedh")
koedh_inflected.addTenseList(koedh_tenses)

#DELLEDH
delledh_pres = rannowVerbAnreyth("delledh","NULL","NULL","NULL","delledh","delledh","NULL","NULL","NULL","a-lemmyn")
delledh_tenses = [delledh_pres]
delledh_inflected = rannowVerbAnreythOllAmser("delledh")
delledh_inflected.addTenseList(delledh_tenses)

#DEUR
deur_pres = rannowVerbAnreyth("deur","NULL","NULL","NULL","deur","deur","NULL","NULL","NULL","a-lemmyn")
deur_tenses = [deur_pres]
deur_inflected = rannowVerbAnreythOllAmser("deur")
deur_inflected.addTenseList(deur_tenses)

#MEDHES
medhes_pres = rannowVerbAnreyth("medhes","yn-medhir","yn-medhav","yn-medhydh","yn-medh","yn-medh","yn-medhyn","yn-medhowgh","yn-medhons","a-lemmyn")
medhes_tenses = [medhes_pres]
medhes_inflected = rannowVerbAnreythOllAmser("medhes")
medhes_inflected.addTenseList(medhes_tenses)

#PARGH/PARAGH - verbal noun only

#RES
res_pres =  rannowVerbAnreyth("res","NULL","NULL","NULL","res","res","NULL","NULL","NULL","a-lemmyn")
res_tenses = [res_pres]
res_inflected = rannowVerbAnreythOllAmser("res")
res_inflected.addTenseList(res_tenses)

#SKILA
skila_pres = rannowVerbAnreyth("skila","NULL","NULL","NULL","skila","skila","NULL","NULL","NULL","a-lemmyn")
skila_tenses = [skila_pres]
skila_inflected = rannowVerbAnreythOllAmser("skila")
skila_inflected.addTenseList(skila_tenses)

#TANN
tann_imperative = rannowVerbAnreyth("tann","NULL","NULL","tann","NULL","NULL","NULL","tannewgh","NULL","gorhemmyn")
tann_tenses = [tann_imperative]
tann_inflected = rannowVerbAnreythOllAmser("tann")
tann_inflected.addTenseList(tann_tenses)


#WAR
war_imperative = rannowVerbAnreyth("war","NULL","NULL","war","NULL","NULL","NULL","waryewgh","NULL","gorhemmyn")
war_tenses = [war_imperative]
war_inflected = rannowVerbAnreythOllAmser("war")
war_inflected.addTenseList(war_tenses)

irregverbs_all = {"bos":bos_inflected,"y'm beus":ymbeus_inflected,"piw":piw_inflected,"godhvos":godhvos_inflected,"tyli":tyli_inflected,"attyli":attyli_inflected,"hwarvos":hwarvos_inflected,"darvos":darvos_inflected,"klywes":klywes_inflected,"omglywes":omglywes_inflected,"mos":mos_inflected,"dos":dos_inflected,"doen":doen_inflected,"omdhoen":omdhoen_inflected,"ri":ri_inflected,"dri":dri_inflected,"ti":ti_inflected,"dyllo":dyllo_inflected,"gul":gul_inflected,"omwul":omwul_inflected,"mynnes":mynnes_inflected,"galloes":galloes_inflected,"bern":bern_inflected,"darwar":darwar_inflected,"degoedh":degoedh_inflected,"koedh":koedh_inflected,"delledh":delledh_inflected,"deur":deur_inflected,"medhes":medhes_inflected,"res":res_inflected,"skila":skila_inflected,"tann":tann_inflected,"war":war_inflected,"bryjyon":bryjyon_inflected}

def makeTenseDict(listTenses,pastPL = "NULL"):
    """ 
    y telledh bos listTenses rol taklennow rannowVerbAnreyth
    listTenses should be a list of rannowVerbAnreyth objects
    """
    outDict= {}
    for t in listTenses:
        outDict[t.amser] = t.rannowDict
    if pastPL != "NULL":
        outDict["ppl"] = pastPL
    return outDict

def lastvowel(verbstr):
    if verbstr[-1] in vowels:
        finalvowel=verbstr[-1]
        pos = len(verbstr)-1
        return finalvowel,pos
    else:
        return lastvowel(verbstr[:-1])
        
def lastconsonant(verbstr):
    # kavoes an diwettha kessonenn
    # returns last consonant cluster for hardening/doubling in subjunctive
    consonants = re.split(r'[aeiouy]',verbstr)
    lastconsonant = consonants[-1]
    lenlastconstclust = len(lastconsonant)
    pos = len(verbstr)-lenlastconstclust
    return lastconsonant,pos,lenlastconstclust

def inflektya_reyth(verb,stem,person,tense,suffix_pro):        
        if tense<8:
            endings = endings_alltenses.tenseEndings(tensesDict[tense])
        if tense<7:
            ending = endings.personEnding(person)
        if tense==7: # if past participle
            ending = endings
        if (suffix_pro == 1)and(person>0):
            ending = ending + " " + suffixed_pros[person]
        if (suffix_pro == 2)and(person>0):
            ending = ending + " " + suffixed_pros_emph[person]
    # verbow a worfenn gans -he:        
    # verbs ending in -he:
        if verb[-2:] == "he":
            if tense==0 and (person == 3)or(person==4):
                # 3s a-lemmyn a'th eus a wosa an ben
                # 3s. pres has a not just stem alone
                ending = "a"
            if not(ending==""):     
                if ending[0] == "s":
                    # mars eus -s- gorra a kyns an -s-
                    # where there is an -s- an a is added before the s 
                    ending = "a"+ending
            if (tense==4)or(tense == 5):
                # -ah- yn islavarek
                # subjunctive has extra -ah-
                ending = "ah"+ending
            if tense == 7:
                # yma -es dhe'n ben yn PPL
                # past participle adds -es to the stem.
                ending = "es"
    # verbow a worfenn gans -ya        
    # verbs ending in -ya
        if (stem[-1]=="y"):
            # -y- yw gwithys heb y arall, i po s yn penn po nag eus penn
            # -y- retained except where another y, i or s occurs in the ending
            # or where there is no suffix (3s pres, 2s imperative)
            if(not(ending=="")):
                if (ending[0]=="y") or (ending[0]=="i") or (ending[0]=="s"):
                    stem = stem[:-1]
            if(ending==""):
                stem=stem[:-1]
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
            if not(ending==""):
                if (ending[0] in ["i","y"]) or (ending == "owgh") or ((ending=="ewgh")and(person==6)and(tense==6)):
                    laststemvowel,pos = lastvowel(stem)
                    if laststemvowel == "a":
                        if ((tense==4)or(tense==5)):
                                # chanjys dhe -y- yn islavarek
                                # in subjunctive further affected to -y-
                                stem=stem[:pos]+"y"+stem[pos+1:]
                        else:
                                stem=stem[:pos]+"e"+stem[pos+1:]                    

        if (verb in ["amma","ranna"]):
            # AMMA, RANNA - a-->y
            if not(ending==""):
                if (ending[0] in ["i","y"]) or (ending == "owgh") or ((ending=="ewgh")and(person==2)and(tense==6)):
                    laststemvowel,pos = lastvowel(stem)
                    if laststemvowel == "a":
                        stem=stem[:pos]+"y"+stem[pos+1:]
    
    
        if verb in ["pregowtha"]:
            # pregowtha ow-->ew
            if not(ending==""):
                if (ending[0] in ["i","y"]) or (ending == "owgh") or ((ending=="ewgh")and(person==2)and(tense==6)):
                    laststemvowel,pos = lastvowel(stem)
                    if laststemvowel == "o":
                        stem=stem[:pos]+"e"+stem[pos+1:]

        if (verb in ["dannvon","daskorr"]):
            # dannvon, daskorr o-->e
            if not(ending==""):
                if (ending[0] in ["i","y"]) or (ending == "owgh") or ((ending=="ewgh")and(person==2)and(tense==6)):
                    laststemvowel,pos = lastvowel(stem)
                    if laststemvowel == "o":
                        stem=stem[:pos]+"e"+stem[pos+1:]
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
            if ((tense==0)and(person==1))or(((tense==1)or(tense==4))and((person==3)or(person==4)or(person==7)))or(tense==3)or(tense==5)or((tense==6)and(person==2)):
                laststemvowel,pos = lastvowel(stem)
                if laststemvowel == "e":
                        stem=stem[:pos]+"o"+stem[pos+1:]   
            if verb == "dedhwi":
                if (tense==1)and((person==3)or(person==4)):
                    stem = "dedhow"
        if verb in verbs_igeri_a:
            if ((tense==0)and(person==1))or(((tense==1)or(tense==4))and((person==3)or(person==4)or(person==7)))or(tense==3)or(tense==5)or((tense==6)and(person==2)):
                laststemvowel,pos = lastvowel(stem)
                if laststemvowel == "e":
                        stem=stem[:pos]+"a"+stem[pos+1:]   

    #type ERGHI
    # maneruster bogalenn kepar hag igeri hag ynwedh chanj bogalenn dhe'n 3s tremenys
    # same kind of vowel affectation as igeri with addition of 3s. preterite, ending in -is also has a vowel change
    # retains original stem vowel in 
    # pres/future 1s
    # preterite 3p only
    # pluperfect all persons
    # subjunctive pres./fut. 3s. and 3p.
    # subjunctive imp. all persons
    # imperative 2s'
        if verb in verbs_erghi_a:
           if ((tense==0)and(person==1))or((tense==1)and(person==7))or(tense==3)or((tense==4)and((person==3)or(person==4)or(person==7)))or(tense==5)or((tense==6)and(person==2)):
               laststemvowel,pos=lastvowel(stem)
               if laststemvowel=="e":
                   stem=stem[:pos]+"a"+stem[pos+1:]
           if verb=="drehevel":
               # drehevel 3s. pres/fut drehav, dreha, or derav, 2s imperv. drehav/dreva, 3s. pret. drehevis/derevis
               if ((tense==0)and((person==3)or(person==4)))or((tense==6)and(person==2)):
                   stem = "drehav"
           if verb=="gweskel":
               # gweskel has 3s. pres/fut gwysk, past participle gwyskys, loses k in some parts of verb
               if ((tense==0)and((person==3)or(person==4)))or(tense==7):
                   stem = "gwysk"
        if verb in verbs_erghi_o:
           if ((tense==0)and(person==1))or((tense==1)and(person==7))or(tense==3)or((tense==4)and((person==3)or(person==4)or(person==7)))or(tense==5)or((tense==6)and(person==2)):
               laststemvowel,pos=lastvowel(stem)
               if laststemvowel=="e":
                   stem=stem[:pos]+"o"+stem[pos+1:]
           if verb=="dinewi"and tense==0 and ((person==3)or(person==4)):
               # dinewi has 3s. pres/fut dinwa
               stem = "dinwa"

        if (verb in three_s_presfut_y) and tense==0 and ((person==3)or(person==4)):
            # group of verbs narrow vowel in 3s. pres/fut (sect 192 of Wella Brown 3rd ed.)
            laststemvowel,pos=lastvowel(stem)
            if laststemvowel=="o":
                stem=stem[:pos]+"e"+stem[pos+1:]
            else:
                stem=stem[:pos]+"y"+stem[pos+1:]
    # godhevel has alternative verbal noun godhav
    # not implemented

    # GELWEL type conjugated as erghi
    # stem ends in -l, -n, or -r followed by -w- 
    # original stem vowel is -a-
    # -o- placed before -w- in 3s. pres/fut
    # galwsons/gawlsons 3p. pret., pluperfect
        if verb in verbs_gelwel:
           if ((tense==0)and(person==1))or((tense==1)and(person==7))or(tense==3)or((tense==4)and((person==3)or(person==4)or(person==7)))or(tense==5)or((tense==6)and(person==2)):
               laststemvowel,pos=lastvowel(stem)
               if laststemvowel=="e":
                   stem=stem[:pos]+"a"+stem[pos+1:]
           if (tense==0)and((person==3)or(person==4)):
               stem = stem[:-2]+"ow"
           #optional
           if ((tense==1)and(person==7))or(tense==3):
               stem = stem[:-2]+stem[-1]+stem[-2]
               
    # HWITHRA type
    # stem ends in two consonant sounds, the second of which is -l-, -m-, -n-, or -r-
    # delivra changes -vr- to -rv- 3s. pres/fut, 2s. imperative, + where ending starts with an s
    # NOT IMPLEMENTED 
    # in subjunctives consonant before lrmn undergoes hardening of doubling
        # print(verb,stem, tense)
        # print(verb in verbs_hwithra)
        if verb in verbs_hwithra:
            # print(stem)
            if ((tense==0)and((person==3)or(person==4)))or((tense==6)and(person==2)):
                # in 3s. pres/future and 2s. imperative
                # a vowel is introduced usually -e-
                # sometimes -o- or -y-
                if verb in ["resna","sokra"]:
                    vowel = "o"
                else:
                    if verb in ["fekla","takla"]:
                        vowel = "y"
                    else:
                        vowel = "e"
                stem = stem[:-1]+vowel+stem[-1]
            if not(ending==""):
                if ending[0]=="s":
                    # when verbal ending starts with an -s-
                    # the final consonant of the stem may drop out and be shortened
                    # and an apostrophe introduced
                    stem = stem[:-1]+"'"

    # GWYSTLA type
    # final consonant is -l-, -m-, -n- or -r- preceded by two adjacent consonants. 
        if verb in verbs_gwystla:
            vowel = "e"
            if ((tense==0)and((person==3)or(person==4)))or((tense==6)and(person==2)):
                # in 3s. pres/fut and 2s. imperative, an -e- is put before the final consonant
                stem = stem[:-1]+vowel+stem[-1]
            if not(ending==""):
                if ending[0]=="s":
                    # when verbal ending starts with an -s-
                    # -e- is put before the final consonant of the stem
                    # and verb remains uncontracted
                    stem=stem[:-1]+vowel+stem[-1]
            if (tense==4)or(tense==5): 
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
            if not(ending==""):
                if ending[0]=="s":
                    stem = stem[:-1]+"'"
                    
        if (verb == "diskwedhes")and(tense==0)and((person==3)or(person==4)):
            stem = "diskwa"
        if (verb == "drehevel")and(tense==0)and((person==3)or(person==4)):
            stem = "drehav"
        if (verb == "gortos")and(tense==0)and((person==3)or(person==4)):
            stem = "gorta"
        if (verb == "hwilas")and(tense==0)and((person==3)or(person==4)):
            stem = "hwila"

    # DYBRI
    # vowel affectation in stem
    # y --> e e.g. in dybri
    # in pres pers 3,4,6,7
    # pres subj pers 3,4
    # imp subj all pers
    # imperative pers 2
        if verb in verbs_dybri:
                if ((tense == 0) and (person in [1,3,4,6,7])) or ((tense == 4) and (person in [0,3,4,7])) or (tense == 5) or ((tense == 6) and (person == 2)):
                    stem = stem.replace("y","e",1)

    # return the result
        inflectedverb = stem+ending
        return inflectedverb,1

def inflektyaValidatePerson(person):
    # expect an integer from 0 to 7
    try:
        person = int(person)
        if person not in range(8):
            return False
        else:
            return True
    except ValueError:
        return False

def inflektyaValidateTense(verb,person,tense):
    if tense not in tensesDict.values():
        # validate tense parameter
        return False
    if ((person==0)or(person==1))and(tense=="gorhemmyn"): 
        # impersonal and 1s don't exist in imperative
        # nyns eus anpersonek ha'n 1s y'n gorhemmyn
        # print "invalid tense/person combination"
        return False
    if tense=="devedhek" and verb not in verbs_devedhek:
        # only a few verbs have a simple future tense
        # if not return invalid
        return False
    if tense=="anperfydh_usadow" and verb not in verbs_anperfydh_usadow:
        # only a few verbs have a separate habitual imperfect
        # if not return invalid
        return False
    if tense in ["a-lemmyn_hir_indef", "anperfydh_hir","a-lemmyn_hir_def","a-lemmyn_hir_aff"] and verb != 'bos':
        # the long forms which are particular to bo
        return False
    if tense == "perfydh" and verb not in verbs_perfydh:
        return False
    return True
    
def inflektya(verb,person,tense,suffix_pro=0,longform=0,definite=0):
    # person: 0=imp,1=1s,2=2s,3=3sm,4=3sf,5=1p,6=2p,7=3p
    # tense: 0=present, 1=preterite, 2=imperfect, 3=pluperfect, 4=subjpres, 5=subjimp
    # 6=imperative,7=past_participle,8=future,9=habitual imperfect
    # 10=longform_present_indef,11=longform_imperfect,12=longform_present_defni
    # 13=longform_present_aff,14=perfect
    # expect string for the tense
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
    tensesCodeDict = {v:k for k,v in tensesDict.items()}
    
    # yma amser devedhek, anperfydh usadow ha perfydh dhe nebes verbow
    # certain verbs have simple future, habitual imperfect, perfect
    # nebes verbow yw defowtek
    # certain verbs are incomplete/defective

    # suffix_pro: flag to say whether to include suffixed pronoun
    if suffix_pro not in [0,1,2]:
        # if it is anything other than 0,1,2
        # set to 0 i.e. no suffixed pronoun
        suffix_pro = 0
    invalidinput ="NULL"
    # successflag = 1 if successful, 0 if error
    if not(inflektyaValidatePerson(person)):
        return invalidinput,0
    else:
        person = int(person)
        
    if not(inflektyaValidateTense(verb,person,tense)):
        # if the tense is invalid for the verb, return a NULL
        return invalidinput,0
    vowels = ['a','e','i','o','u']
    if (verb[-1] in vowels):
        stem = verb[:-1]
    if not(verb[-1] in vowels):
        stem = verb
    if (verb[-2:] == "el")or(verb[-2:] == "es")or(verb[-2:]=="as")or(verb[-2:]=="os"):
        stem = verb[:-2]
    if (verb[-3:] == "oes"):
        stem = verb[:-3]

    if verb in verbs_stemnoun:
        stem = verb
    if ("islavarek" in tense)and(not(verb in verbs_gwystla)): 
        # kesson a wra dewblek po kaleshe y'n islavarek
        # double/harden consonants in subjunctive
        lastconststem,pos,length = lastconsonant(stem)
        if lastconststem in stem_changes.keys():
            stem = stem[:(0-length)]+stem_changes[lastconststem]
    regular = not(verb in irregverbs_all.keys())
    if regular == True: 
        return inflektya_reyth(verb,stem,person,tensesCodeDict[tense],suffix_pro)

    if regular == False:
        if tense == "ppl":
            inflectedverb = irregverbs_all[verb].getPPL()
        else:
            inflectedverb = irregverbs_all[verb].getInfVerb(tense,person)
            if (suffix_pro == 1)and(person>0):
                inflectedverb += " " + suffixed_pros[person]
            if (suffix_pro == 2)and(person>0):
                inflectedverb += " " + suffixed_pros_emph[person]
        return inflectedverb,1

# IRREGULAR
# bos, y'm beus, darvos, dos, godhvos, hwarvos, klywes, mos, piw, tyli
# doen, dri, dyllo, gul, ri, ti

#prepositions
endings_A = {1:"av",2:"as",3:"o",4:"i",5:"an",6:"owgh",7:"a"}
endings_B = {1:"ov",2:"os",3:"o",4:"i",5:"on",6:"owgh",7:"a"}
endings_C = {1:"iv",2:"is",3:"o",4:"i",5:"yn",6:"owgh",7:"a"}
endings_D = {1:"",2:"",3:"",4:"",5:"",6:"",7:""}
# dhe, gans irregular
a_stems = {1:"ahan",2:"ahan",3:"anodh",4:"anedh",5:"ahan",6:"ahan",7:"anedh"}
agovis_stems = {1:"a'm govis",2:"a'th wovis",3:"a'y wovis",4:"a'y govis",5:"a'gan govis",6:"a'gas govis",7:"a'ga govis"}
a_ugh_stems = {1:"a-ugh",2:"a-ugh",3:"a-ught",4:"a-ught",5:"a-ugh",6:"a-ugh",7:"a-ught"}
dhe_stems = {1:"dhymm",2:"dhis",3:"dhodho",4:"dhedhi",5:"dhyn",6:"dhywgh",7:"dhedha"}
dre_stems = {1:"dredh",2:"dredh",3:"dredh",4:"dredh",5:"dredh",6:"dredh",7:"dredh"}
dres_stems = {1:"dres",2:"dres",3:"drest",4:"drest",5:"dres",6:"dres",7:"drest"}
erbynn_stems = {1:"er ow fynn",2:"er dha bynn",3:"er y bynn",4:"er hy fynn",5:"er agan pynn",6:"er agas pynn",7:"er aga fynn"}
gans_stems = {1:"genev",2:"genes",3:"ganso",4:"gensi",5:"genen",6:"genowgh",7:"gansa"}
heb_stems = {1:"heb",2:"heb",3:"hebdh",4:"hebdh",5:"heb",6:"heb",7:"hebdh"}
orth_stems = {1:"orth",2:"orth",3:"ort",4:"ort",5:"orth",6:"orth",7:"ort"}
diworth_stems = {1:"diworth",2:"diworth",3:"diwort",4:"diwort",5:"diworth",6:"diworth",7:"diwort"}
a_dhiworth_stems = {1:"a-dhiworth",2:"a-dhiworth",3:"a-dhiwort",4:"a-dhiwort",5:"a-dhiworth",6:"a-dhiworth",7:"a-dhiwort"}
dhiworth_stems = {1:"dhiworth",2:"dhiworth",3:"dhiwort",4:"dhiwort",5:"dhiworth",6:"dhiworth",7:"dhiwort"}
rag_stems = {1:"rag",2:"rag",3:"ragdh",4:"rygdh",5:"rag",6:"rag",7:"ragdh"}
a_rag_stems = {1:"a-rag",2:"a-rag",3:"a-ragdh",4:"a-rygdh",5:"a-rag",6:"a-rag",7:"a-ragdh"}
a_dherag_stems = {1:"a-dherag",2:"a-dherag",3:"a-dheragdh",4:"a-dherygdh",5:"a-dherag",6:"a-dherag",7:"a-dheragdh"}
derag_stems = {1:"derag",2:"derag",3:"deragdh",4:"derygdh",5:"derag",6:"derag",7:"deragdh"}
dherag_stems = {1:"dherag",2:"dherag",3:"dheragdh",4:"dherygdh",5:"dherag",6:"dherag",7:"dheragdh"}
ryb_stems = {1:"ryb",2:"ryb",3:"rybdh",4:"rybdh",5:"ryb",6:"ryb",7:"rybdh"}
war_stems = {1:"warn",2:"warn",3:"warnodh",4:"warnedh",5:"warn",6:"warn",7:"warnedh"}
diwar_stems = {1:"diwarn",2:"diwarn",3:"diwarnodh",4:"diwarnedh",5:"diwarn",6:"diwarn",7:"diwarnedh"}
a_dhiwar_stems = {1:"a-dhiwarn",2:"a-dhiwarn",3:"a-dhiwarnodh",4:"a-dhiwarnedh",5:"a-dhiwarn",6:"a-dhiwarn",7:"a-dhiwarnedh"}
warlergh_stems = {1:"war ow lergh",2:"war dha lergh",3:"war y lergh",4:"war hy lergh",5:"war agan lergh",6:"war agas lergh",7:"war aga lergh"}
yn_stems = {1:"ynn",2:"ynn",3:"ynn",4:"ynn",5:"ynn",6:"ynn",7:"ynn"}
yn_dann_stems = {1:"yn-dann",2:"yn-dann",3:"yn-dann",4:"yn-dann",5:"yn-dann",6:"yn-dann",7:"yn-dann"}
a_dhann_stems = {1:"a-dhann",2:"a-dhann",3:"a-dhann",4:"a-dhann",5:"a-dhann",6:"a-dhann",7:"a-dhann"}
yntra_stems =  {1:"yntredh",2:"yntredh",3:"yntredh",4:"yntredh",5:"yntredh",6:"yntredh",7:"yntredh"}
yn_herwydh_stems = {1:"yn ow herwydh",2:"yn dha herwydh",3:"yn y herwydh",4:"yn hy herwydh",5:"yn agan herwydh",6:"yn agas herwydh",7:"yn aga herwydh"}
yn_kyrghynn_stems = {1:"yn ow hyrghynn",2:"yn dha gyrghynn",3:"yn y gyrghynn",4:"yn hy hyrghynn",5:"yn agan kyrghynn",6:"yn agas kyrghynn",7:"yn aga hyrghynn"}
yn_kever_stems = {1:"yn ow hever",2:"yn dha gever",3:"yn y gever",4:"yn hy hever",5:"yn agan kever",6:"yn agas kever",7:"yn aga hever"}
yn_le_stems = {1:"yn ow le",2:"yn dha le",3:"yn y le",4:"yn hy le",5:"yn agan le",6:"yn agas le",7:"yn aga le"}
yn_mysk_stems = {1:"yn ow mysk",2:"yn dha vysk",3:"yn y vysk",4:"yn hy mysk",5:"yn agan mysk",6:"yn agas mysk",7:"yn aga mysk"}
yn_ogas_stems = {1:"yn ow ogas",2:"yn dha ogas",3:"yn y ogas",4:"yn hy ogas",5:"yn agan ogas",6:"yn agas ogas",7:"yn aga ogas"}
prep_stems_all = {"a":a_stems,"a-govis":agovis_stems,"a-ugh":a_ugh_stems,"dhe":dhe_stems,"dre":dre_stems,"dres":dres_stems,"erbynn":erbynn_stems,"gans":gans_stems,"heb":heb_stems,"orth":orth_stems,"diworth":diworth_stems,"a-dhiworth":a_dhiworth_stems,"dhiworth":dhiworth_stems,"rag":rag_stems,"a-rag":a_rag_stems,"a-dherag":a_dherag_stems,"derag":derag_stems,"dherag":dherag_stems,"ryb":ryb_stems,"war":war_stems,"diwar":diwar_stems,"a-dhiwar":a_dhiwar_stems,"warlergh":warlergh_stems,"yn":yn_stems,"yn-dann":yn_dann_stems,"a-dhann":a_dhann_stems,"yntra":yntra_stems,"yn herwydh":yn_herwydh_stems,"yn kyrghynn":yn_kyrghynn_stems,"yn kever":yn_kever_stems,"yn le":yn_le_stems,"yn mysk":yn_mysk_stems,"yn ogas":yn_ogas_stems}
prep_endings_all = {"a":endings_A,"a-govis":endings_D,"a-ugh":endings_B,"dhe":endings_D,"dre":endings_B,"dres":endings_B,"erbynn":endings_D,"gans":endings_D,"heb":endings_B,"orth":endings_C,"diworth":endings_C,"a-dhiworth":endings_C,"dhiworth":endings_C,"rag":endings_B,"a-rag":endings_B,"a-dherag":endings_B,"derag":endings_B,"dherag":endings_B,"ryb":endings_B,"war":endings_A,"diwar":endings_A,"a-dhiwar":endings_A,"warlergh":endings_D,"yn":endings_B,"yn-dann":endings_B,"a-dhann":endings_B,"yntra":endings_B,"yn herwydh":endings_D,"yn kyrghynn":endings_D,"yn kever":endings_D,"yn le":endings_D,"yn mysk":endings_D,"yn ogas":endings_D}

def inflektya_prepos(prepos,person,suffix_pro=0):
    """
    inflektya prepos rag person
    suffix_pro a wra determya mars eus raghenwyn a syw
    0 = nag eus, 1 = raghanow a syw, 2 = raghanow emphatek a syw
    inflect prepos for person 
    suffix_pro determines whether a suffixed pronoun follows
    0 = none, 1 = normal suff.pro., 2 = emphatic suff. pro.
    """
    invalidinput = 'NULL'
    if not(inflektyaValidatePerson(person)):
        return invalidinput,0
    else:
        person = int(person)
        
    if prep_stems_all.has_key(prepos) and prep_endings_all.has_key(prepos):
        inflectedprep = prep_stems_all[prepos][person] + prep_endings_all[prepos][person]
    else:
        print("Rager {prepos} yw anaswonnys.\nPreposition {prepos} is unknown".format(prepos=prepos))
        return invalidinput, 0
    ending = ""
    if (prepos == "dhe")and(suffix_pro>0)and((person==1)or(person==2)):
        ending += "o"
    if (suffix_pro == 1)and(person>0):
        ending += " " + suffixed_pros[person]
    if (suffix_pro == 2)and(person>0):
        ending += " " + suffixed_pros_emph[person]
    inflectedprep = inflectedprep + ending
    return inflectedprep,1

def rolPersonysAmserow(verb):
    """
    pryntya rol a personys ha'n amserow rag verb
    print a list of persons for each tense of verb
    """
    print("Verb {verb}:".format(verb=verb.upper()))

    if not(verb in irregverbs_all.keys()):
        tlist = [tensesDict[t] for t in range(8)]
        tENlist = [tensesDictEN[t] for t in range(8)]
    else:
        tlist = irregverbs_all[verb].tensesList
        tENlist = irregverbs_all[verb].tensesENList
        
    for t,tEN in zip(tlist,tENlist):
        print("\nAmser: {amser} {tenseEN}".format(amser=t.capitalize().ljust(20), tenseEN=tEN.capitalize().rjust(20)))
        if t == "ppl":
            print("{person}: {inflVerb}".format(person="PPL".ljust(14),inflVerb = inflektya(verb,1,t,1)[0]).rjust(12))
        else:
            for p in range(8):
                print("{person}: {inflVerb}".format(person = personDict[p].ljust(14), inflVerb = inflektya(verb,p,t,1)[0]).rjust(12))
    print("\n")

def rolPersonysPrepos(prepos):
    """
    pryntya rol a personys rag prepos
    print a list of persons for a preposition
    """
    print("Preposition {p}:".format(p=prepos.upper()))
    for p in range(7):
        print("{person}: {inflPrep}".format(person = personDict[p+1].ljust(14), inflPrep = inflektya_prepos(prepos,p+1,1)[0].rjust(12)))
    print("\n")

def rolPersonysAmserInteract():
    verb = raw_input("Ro an verb dhe inflektya mar pleg. Ro 'q' dhe kwittya. \nEnter the verb to inflect please. Enter 'q' to quit.\n\n")
    if verb.lower() != 'q':
        rolPersonysAmserow(verb)
        return 0
    else:
        return 1
def rolPersonysPreposInteract():
    prepos = raw_input("Ro an rager dhe inflektya mar pleg. Ro 'q' dhe kwittya. \nEnter the preposition to inflect please. Enter 'q' to quit.\n\n")
    if prepos.lower() != 'q':
        rolPersonysPrepos(prepos)
        return 0
    else:
        return 1

def runTestCode():
    rolPersonysAmserow("prena")
    rolPersonysAmserow("bos")
    rolPersonysAmserow("y'm beus")
    rolPersonysAmserow("godhvos")
    rolPersonysAmserow("mos")
    rolPersonysAmserow("dos")
    rolPersonysAmserow("ri")
    rolPersonysAmserow("doen")
    rolPersonysAmserow("gul")
    rolPersonysAmserow("mynnes")
    rolPersonysAmserow("galloes")
    rolPersonysPrepos("dhe")
    rolPersonysPrepos("gans")
    rolPersonysPrepos("dres")
    q=0
    while q==0:
        q = rolPersonysAmserInteract()
    q=0
    while q==0:
        q = rolPersonysPreposInteract()

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
verbs_perfydh = ["mos","mones","dos","dones"]

if __name__ == '__main__':     
    runTestCode()

