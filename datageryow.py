import mutatya
import inflektya

def addallmutatedforms(listwords):
    """ add all possible mutated forms to a list of words """
    mutatedwords = []
    for w in listwords:
        for i in [2,3,4,5,6]:
            mutatedwords.append(mutatya.mutate(w,i))
    for w in mutatedwords:
        if w not in listwords:
            listwords.append(w)

def addallinflectedforms(listwords,listverbs):
    """ add the inflected forms of the verbs in listverbs to listwords """
    # the tenses of the verb expected by inflektya.inflektya()
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
    inflectedverbparts = []
    for verb in listverbs:
        inflectedverbparts.append(verb)        
        for per in range(8):
            for tense in range(8):
                # inflect verb for the person per and tense. 0 is to not have the suffixed pron.
                inflectedverbparts.append(inflektya.inflektya(verb,per,tensesDict[tense],0)[0])
    for v in inflectedverbparts:
        if v not in listwords:
            listwords.append(v)


## data for treuslytherenna.py ##
            
#polysyllables that nevertheless have 'oo' in SWF
SWF_oowords = ['boesa', 'poesa', 'diboes', 'kettoeth', 'degoedh', 'a-droes']

# words which abnormally have o rather than oo for a monosyllable
SWF_owords = ['koen','troen','oen','goer','hwoer','woer','koer','noeth']
# but if koen gets mutated to goen, we don't know that it should be gon
# rather than goon. goen is also a worn which is goon in SWF.

# syllables that are <oo> in SWF in stressed syllables in polysyllabic words
# but 'food' is boos in SWF, plural is bosow but verb 'to feed' is boosa.
# similarly 'poos' weight, pl. posow, but poosa to weigh.
# also diboos despite 2 syllables.
# however 'soon' - blessing but 'sona' to bless.
SWF_oosyls = ['skoedh']

# prefixes with secondary stress - which keep their doubled consonants
prefixes_2ndstress = ["kamm","penn","pell","korr"]

# words which have -ll in KK but 1 final l in SWF 
words_SWF_one_l = ["arall", "erell", "astell", "botell", "dorgell", "estyll",
                   "fatell", "gevell", "graghell", "kanstell", "kastell",
                   "kettell", "kuntell", "mantell", "omguntell", "oygell",
                   "pabell", "padell", "pannell", "pastell", "porghell",
                   "radell", "skavell", "skitell", "skudell", "stevell",
                   "tagell", "talgell", "torthell", "towell"]

# words that retain kk in SWF rather than ck.
words_SWF_kk = ["bykken", "lakka", "tykki", "tykkiow"]
verbs_SWF_kk = ["okkupya"]

# words that had yw yn earlier Kernewek Kemmyn but uw in Gerlyver Meur and SWF
words_uw = ["dyw", "dywses", "dywow","gyw", "dywes", "dywesow","gywow","gywa",
            "didhyw", "didhywydh", "didhywydhyon", "didhywydhes", "didhywydhesow",
            "dywonieth", "dywonydh", "dywonydhyon", "dywonydhes", "dywonydhesow",
            "ryw", "rywyon", "rywek","plyw","plywow","plywek","plywogyon","plywoges", "plywogesow"]

verbs_uw = ["gywa"]

# words that have a KK half-long y which doesn't become e in SWF
# likely not yet a complete list   
words_y = ["spyrys", "kynsa", "ynter", "ylyn", "pympes", "ydhyn", "dhy'hwi", "chyften", "byghan",
           "trynses", "kryjyans", "vydholl", "vytholl", "bythkweth", "krysi", "ystynn", "dybri",
           "slynkya", "kyni", "kessydhya", "kessydhyans", "pygans", "bynytha", "bynitha", "ysow",
           "dyskans", "myrghes", "kyrghes", "kyrghys", "lyver", "lyvrow", "bryntin", "possybyl",
           "possybylta", "possybyltas","anpossybyl", "onpossybyl", "anpossybylta", "onpossybylta",
           "anpossybylytas", "onpossybylytas", "dyski", "pysi", "mynysenn"]

verbs_y = ["krysi", "slynkya", "kyni", "kessydhya", "dybri", "dyski", "pysi"]    

addallinflectedforms(words_uw,verbs_uw)
addallmutatedforms(words_uw)
# avoid turning 'yw' etc. to uw
wrong_mut_gyw = [w for w in words_uw if w[:2]=='yw']
for w in wrong_mut_gyw:
    words_uw.remove(w)


addallinflectedforms(words_y, verbs_y)
addallmutatedforms(words_y)            

addallmutatedforms(SWF_oowords)
addallmutatedforms(SWF_owords)
# remove 'goen' - this is interpreted as a word where it becomes goon
# rather than mutated 'koen' which is 'kon'-->'gon' in SWF
SWF_owords.remove("goen")
#print(SWF_oowords)
#print(SWF_owords)

## data for sylabelenn_ranna_kw.py ##


# words that have unusual stress

# words of more than one syllable stress on final syllable
final_syl_stress_words = ['ages','ahwer','androw','ankoth','ankres','attal',
                          'avel','aweyl','boban','boken','bulhorn','bysmer',
                          'byttegyns','byttele','degoedh','dihwans',
                          'a-dhihwans','demmas','devis','devri','tevri',
                          'diank','dohajydh','dolos',
                          'dremas','drog-atti','eghan','godhor','godramm',
                          'goeldheys','myghtern','nahen','nameur','nammnygen',
                          'namoy','naneyl','piwpynag','poken','pygans','pynag',
                          'pyseul','seulabrys','seuladhydh','soweth','toetta',
                          'war-barth','warbarth','yma','ymons','ynwedh','ytho',
                          'evy','tejy','eev','hyhi','nyni',
                          'hwyhwi','ynsi','yn-bann','yn-dann','ynbann',
                          'yndann','a-ji','a-dhann','dygoel','dygweyth',
                          'a-rag','dherag','a-dherag',
                          'a-dhiworth','omri','omdowl', 'dibygans',
                          'diber-dowr','diwvanek-plat', 'a-droes']

addallmutatedforms(final_syl_stress_words)    

# words of 3 or more syls. stressed on first syl.
first_syl_stress_words = ['arader','aradror','kenedhel','kelegel','kenderow',
                          'klabytter','lelduri','lenduri','tulyfant',
                          'hardigras','oratri','trayturi','genedhel',
                          'henedhel','gelegel','helegel','genderow',
                          'henderow','glabytter','dulyfant','thulyfant',
                          'drayturi','thrayturi']

# words of 4 or more syls. stressed on 2nd syl.
second_syl_stress_words = ['keniterow','dygynsete','geniterow','heniterow',
                           'dhygynsete']

# particles and words that do not carry stress
unstressed_monosyls = ['an','a','y','re','ny','yth','nyns','na','nag','ow',
                       'dha','hy','vy','jy','ma','ha','hag','pan','mar','mars',
                       'dhe','po','bo','mes','rag','may','mayth','kyn','kynth',
                       'dell']
    
# 2 syllable words with di- that are stressed on the first syllable
words_di_stress1 = ["dial", "dibegh", "dibenn", "dibra", "diek", "dien",
                    "difenn", "dilesh", "dillas", "dinan", "dinas", "dinek",
                    "diner", "disel", "diskan", "diskar", "diskeudh", "dismyk",
                    "distowgh", "disya", "divers", "divyn", "diwarr",
                    "diwbaw", "diwbleth", "diwdhorn", "diwedh", "diwen",
                    "diwes", "diwfer", "diwfordh", "diwgell", "diwglun",
                    "diwla", "diwlens", "diwroev", "diwros", "diwskeodh",
                    "diwvogh", "diwvregh", "diwvronn", "diwweus", "diwweyth"]

addallmutatedforms(words_di_stress1)

# words that use <c> in SWF in place of s in KK

words_c = ["abesedari", "abesedaris", "assendyans", "dissernyans",
           "dissernyansow", "prosess", "prosessys", "prosessyon", "prosessyons",
           "pynsel", "pynsels", "pynser", "pynseryow", "resevans", "resevansow",
           "gorsita", "gorsitys", "gromersi", "mersi", "nisita", "pennsita",
           "pennsitys", "polisi", "polisis", "prinsipata", "prinsipatys",
           "rekonsilyans", "rekonsilyansow", "sosyal", "sosyalieth",
           "sosyalydh", "sosyalydhyon", "sosyalydhes", "sosyalydhesow",
           "sosyalydhek", "sosyologieth", "sosyologiethek", "sosyologydh",
           "sosyologydhyon", "sosyologydhes", "sosyologydhesow", "akusasyon",
           "akusasyons", "deklarasyon", "deklarasyons", "fondasyon",
           "fondasyons", "fysysyen", "fysysyens", "mensyon", "mensyons",
           "menystrasyon", "menystrasyons", "nasyon", "nasyons", "nasyonal",
           "optysyan", "optysyans", "optysyanes", "optysyanesow", "potensyal",
           "potensyals", "presyous", "revelasyon", "revelasyons", "salvasyon",
           "salvasyons", "spesyli", "stasyon", "stasyons", "tradisyon",
           "tradisyons", "tradisyonal", "vokasyon", "selder", "selders",
           "sellulos", "selluloyd", "sentimeter", "sentimetrow", "sertan",
           "sider", "siders", "sidi", "sidis", "sigar", "sigarow", "sigarik",
           "sigarigow", "sinema", "sinemas", "sirk", "sirkow", "sita", "sitys",
           "sivil","chyfsita","chyfsitys"]
# words that have a SWF <c> in place of KK <s> but also retain <syon> elsewhere
# in the word
words_c_syon = ["prosessyon", "prosessyons"]
           
           
verbs_c = ["assendya", "desessya", "desevya", "dissernya", "konsevya",
           "prosedya", "prosessya", "reseva", "rekonsilya", "sertifia",
           "sessya"]    
verbs_infl = []
 
addallinflectedforms(words_c, verbs_c)
addallinflectedforms(verbs_infl, verbs_c)
addallmutatedforms(words_c)
addallmutatedforms(verbs_infl)
addallmutatedforms(words_c_syon)            
addallmutatedforms(words_SWF_kk)
addallinflectedforms(words_SWF_kk, verbs_SWF_kk)
