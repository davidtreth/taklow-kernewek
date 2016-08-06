import treuslytherenna as tr
import datainflektya
import imp
imp.reload(datainflektya)
from datainflektya import *
""" turn the data in datainflektya into SWF """

def convert_verb_SWF(verbAnreyth):
    """ convert the verb to SWF """
    if " " not in verbAnreyth.verbnoun:
        verbAnreyth.verbnoun = tr.wordstr_KK2FSS(verbAnreyth.verbnoun, True, False)
    for t in verbAnreyth.dict_tenses.keys():
        # print t
        # print verbAnreyth.dict_tenses[t]
        try:
            for r in verbAnreyth.dict_tenses[t].keys():
                if verbAnreyth.dict_tenses[t][r] != "NULL":
                    # print(verbAnreyth.dict_tenses[t][r])
                    if " " in verbAnreyth.dict_tenses[t][r]:
                        verbAnreyth.dict_tenses[t][r] = tr.text_KK2FSS(verbAnreyth.dict_tenses[t][r], True, False)
                        verbAnreyth.dict_tenses[t][r] = verbAnreyth.dict_tenses[t][r].replace("  "," ")
                    else:
                        verbAnreyth.dict_tenses[t][r] = tr.wordstr_KK2FSS(verbAnreyth.dict_tenses[t][r], True, False)
                    # print(verbAnreyth.dict_tenses[t][r])
        except:
            # for ppl
            # print(verbAnreyth.dict_tenses[t])
            verbAnreyth.dict_tenses[t] = tr.wordstr_KK2FSS(verbAnreyth.dict_tenses[t], True, False)
        # print verbAnreyth.dict_tenses[t]

def conv_verblist_SWF(verblist):
    """ convert a list of words to SWF """
    for v in verblist:
        if " " in v:
            swfv = v
        else:
            swfv = tr.wordstr_KK2FSS(v, True, False)
        if swfv != v:
            # print(v, swfv)
            verblist.remove(v)
            verblist.append(swfv)

# list of lists containing the various special cases
verblists_all = [verbs_stemnoun, verbs_i_3sp, verbs_klywes, verbs_i_imp, verbs_amaya, verbs_tava,
                 verbs_gwana, verbs_amma, verbs_fyllel, verbs_pregowtha, verbs_dannvon, verbs_igeri_o,
                 verbs_dedhwi, verbs_igeri_a, verbs_erghi_o, verbs_dinewi, verbs_erghi_a, verbs_heveli,
                 verbs_gweskel, three_s_presfut_y, verbs_lesta, verbs_gwystla, verbs_pe, verbs_hwithra,
                 verbs_resna, verbs_fekla, verbs_delivra, verbs_ankombra, verbs_gelwel, verbs_irregular,
                 verbs_dybri, verbs_devedhek, verbs_anperfydh_usadow, verbs_perfydh]

# convert the list of lists to SWF
for vlist in verblists_all:
    conv_verblist_SWF(vlist)            

# convert irregular verbs
for irreg in irregverbs_all.keys():
    convert_verb_SWF(irregverbs_all[irreg])
    if " " not in irreg:
        irrswf = tr.text_KK2FSS(irreg, True, False).strip()
    else:
        irrswf = irreg
    if irrswf != irreg:
        irregverbs_all[irrswf] = irregverbs_all[irreg]
        irregverbs_all.pop(irreg)
