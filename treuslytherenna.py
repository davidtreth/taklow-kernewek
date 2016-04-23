from __future__ import print_function
import sylabelenn_ranna_kw
import mutatya
import inflektya
import argparse
import codecs

# TODO - vocalic alternation e.g. byw but bewnans, bewnansow
# benyn, benenes
# often KK half-long <y> --> SWF <e>
# also some unstressed <y> in final syllable of root --> <e>

# use of c in place of s in some words e.g. cider, cita, polici
# use of z zebra, Zimbabwe
# hyphenation
# dhyworth/dyworth
# ynkleudhva --> ynkladhva


    
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
        for per in range(8):
            for tense in range(8):
                # inflect verb for the person per and tense. 0 is to not have the suffixed pron.
                inflectedverbparts.append(inflektya.inflektya(verb,per,tensesDict[tense],0)[0])
    for v in inflectedverbparts:
        if v not in listwords:
            listwords.append(v)

#polysyllables that nevertheless have 'oo' in SWF
SWF_oowords = ['boesa','poesa','diboes','kettoeth','degoedh']

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
words_SWF_one_l = ["arall","erell","kastell","kanstell","kuntell"]

# words that retain kk in SWF rather than ck.
words_SWF_kk = ["bykken", "vykken", "lakka", "okkupya", "tykki", "tykkiow"]

# words that had yw yn earlier Kernewek Kemmyn but uw in Gerlyver Meur and SWF
words_uw = ["dyw", "dhyw", "dywses", "dhywses", "dywow", "dhywow","gyw","wyw",
            "duwes", "duwesow", "dhuwes", "dhuwesow", "gywow", "wywow","gywa",
            "didhyw", "didhywydh", "didhywydhyon", "didhywydhes", "didhywydhesow",
            "dywonieth", "dywonydh", "dywonydhyon", "dywonydhes", "dywonydhesow",
            "ryw", "rywyon", "rywek"]

# words that have a KK half-long y which doesn't become e in SWF
# likely not yet a complete list   
words_y = ["spyrys", "kynsa", "ynter", "ylyn", "pympes", "ydhyn", "dhy'hwi", "chyften", "byghan",
           "trynses", "kryjyans", "vydholl", "vytholl", "bythkweth", "krysi", "ystynn", "dybri",
           "slynkya", "kyni", "kessydhya", "kessydhyans", "pygans", "bynytha", "bynitha", "ysow",
           "dyskans", "myrghes", "kyrghes", "kyrghys", "lyver", "lyvrow", "bryntin", "possybyl",
           "possybylta", "possybyltas","anpossybyl", "onpossybyl", "anpossybylta", "onpossybylta",
           "anpossybylytas", "onpossybylytas", "dyski", "pysi"]

verbs_y = ["krysi", "slynkya", "kyni", "kessydhya", "dybri", "dyski", "pysi"]    
addallinflectedforms(words_y, verbs_y)
addallmutatedforms(words_y)            

# print(words_y)
            
def convert_oe(inputsyl, SWF_ooword):
    ''' Take a syllable and change 'oe' to 'oo' or 'o' if appropriate '''
    outputgrapheme = inputsyl.grapheme
    
    if inputsyl.monosyl:
        if inputsyl.grapheme.lower() in SWF_owords:
            outputgrapheme =  inputsyl.grapheme.replace("oe","o")
        else:
            if inputsyl.structure == 'CVC' or inputsyl.structure == 'CV':
                # if it's a long vowel, 'oe' goes to 'oo'
                if inputsyl.lengtharray[1]>2:
                    outputgrapheme = inputsyl.grapheme.replace("oe","oo")
                else:
                    # for short vowels, 'oe' goes to 'o'
                    outputgrapheme = inputsyl.grapheme.replace("oe","o")
            if inputsyl.structure == 'VC':
                if inputsyl.lengtharray[0]>2:
                    outputgrapheme = inputsyl.grapheme.replace("oe","oo")
                else:
                    outputgrapheme = inputsyl.grapheme.replace("oe","o")
    else:
        # for polysyllables, only a few select words have 'oe' --> 'oo'        
        if (inputsyl.grapheme.lower() in SWF_oosyls and inputsyl.stressed) or SWF_ooword:
            outputgrapheme = inputsyl.grapheme.replace("oe","oo")
        else:
            # otherwise 'oe' --> 'o'
            outputgrapheme = inputsyl.grapheme.replace("oe","o")
    inputsyl.grapheme=outputgrapheme

def convert_yw(inputsyl):
    """ vocalic alternation for words with <yw> in earlier Kemmyn and <ew> in current KK and SWF
        and words that had <yw> in earlier Kemmyn but <uw> in current KK and SWF """
    outputgrapheme = inputsyl.grapheme
    if inputsyl.graphGer.lower() in words_uw:
        outputgrapheme = outputgrapheme.replace("yw","uw")
    # this doesn't actually happen for all polysyllables
    if not(inputsyl.monosyl) and not(inputsyl.final) and inputsyl.structure[0] == 'C':
        outputgrapheme = outputgrapheme.replace("yw","ew")
    inputsyl.grapheme=outputgrapheme

def convert_y(inputsyl):
    """ vocalic alternation for half-long KK y vowels that go to e in SWF """
    # e.g. benynes --> benenes
    # 1/2 long KK y becomes e
    if inputsyl.graphGer.lower() not in words_y:
        # if it isn't one of the exceptions that retain y
        # find length of vowel and quality
        if inputsyl.structure[0] == 'C':
            vowellength = inputsyl.lengtharray[1]
            vowel = inputsyl.sylparts[1]
        elif inputsyl.structure[0] == 'V':
            vowellength = inputsyl.lengtharray[0]
            vowel = inputsyl.sylparts[0]
        # select half-long vowels, that are y (not ay, ey, oy)
        # and not syllables ending in a vowel (often should have been a consonantal y
        # e.g. in -ya words)
        if vowellength == 2 and vowel == 'y' and inputsyl.structure[-1] != 'V':
            if args.verberr and 'y' in inputsyl.grapheme:
                print("convert_y")
                print(inputsyl.sylparts)
            outputgrapheme = inputsyl.grapheme.replace("y","e")
            inputsyl.grapheme = outputgrapheme

def convert_double_consts(inputsyl):
    outputgrapheme = inputsyl.grapheme
    # kk -> ck except for a few words that retain kk
    if inputsyl.graphGer.lower() not in words_SWF_kk:
        outputgrapheme = outputgrapheme.replace("kk","ck")
    # for unstressed syllables, excluding certain prefixes
    if inputsyl.stressed == False and inputsyl.grapheme.lower() not in prefixes_2ndstress:
        outputgrapheme = outputgrapheme.replace("mm","m")
        outputgrapheme = outputgrapheme.replace("nn","n")
        # final syllables - ll and rr
        if inputsyl.final:
            # the suffix for 'tool' or 'device' is now -ell in SWF
            # however there is KK kastell SWF kastel
            # KK arall/erell SWF aral/erel
            if inputsyl.graphGer.lower() in words_SWF_one_l:
                outputgrapheme = outputgrapheme.replace("ll","l")
            outputgrapheme = outputgrapheme.replace("rr","r")
    inputsyl.grapheme = outputgrapheme

def syl_KK2FSS(inputsyl, inputword):
    # turn KK 'oe' to 'oo' or 'o'
    convert_oe(inputsyl, inputword.graph in SWF_oowords)
    # vocalic alternation
    convert_yw(inputsyl)
    convert_y(inputsyl)
    # turn some double consts into single
    convert_double_consts(inputsyl)
    # replace the plaintext syllable list
    inputword.sls = [s.grapheme for s in inputword.slsObjs]
    # build spelling of word from spelling of syllables
    inputword.graph = ''.join(inputword.sls)

            
if __name__ == '__main__':
    """
    If invoked at the command-line
    """
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    # take the input from a file specified
    # by a command line argument
    parser.add_argument("inputfile", type=str,
                         help="Specify the input text file containing Cornish text.")
    parser.add_argument("--short",action="store_true",
                        help="Short output for each word, i.e. only transliterated text, rather than details and syllable lengths")
    parser.add_argument("--line",action="store_true",
                        help="Line by line mode. Uses shorter reporting of each word, in form of interlinear input and SWF text .")
    parser.add_argument("--verberr",action="store_true",
                        help="Verbose mode for errors, e.g. flagging up segmentation failures etc.")

    args = parser.parse_args()
    # Check that the input parameter has been specified.
    if args.inputfile == None:
        # Print an error message if not and exit.
        print("Error: No input file provided.")
        sys.exit()

    addallmutatedforms(SWF_oowords)
    addallmutatedforms(SWF_owords)
    # remove 'goen' - this is interpreted as a word where it becomes goon
    # rather than mutated 'koen' which is 'kon'-->'gon' in SWF
    SWF_owords.remove("goen")
    #print(SWF_oowords)
    #print(SWF_owords)

    f = codecs.open(args.inputfile,"r",encoding='utf-8',errors='replace')
    fwds = True
    #fwds = False
    if args.line:
        # read file line by line
        inputtext = f.readlines()
        for line in inputtext:
            rannans = sylabelenn_ranna_kw.RannaSyllabelenn(line)            
            print("KK: {k}".format(k=line.lstrip()),end = "")
            # build up line in SWF
            outline = ''
            for i in rannans.geryow:
                # go through word by word
                g = sylabelenn_ranna_kw.Ger(i,rannans,fwds)
                if g.graph != '':
                    inputgraph = g.graph
                    #if args.verberr:
                    #    print("input: {i}".format(i=inputgraph))
                    if len(g.slsObjs) > 0:
                        # if it is a word, loop through syllables
                        # and build up the spelling after segmentation
                        # but before the KK-->SWF conversion
                        inputsyls = [s.grapheme for s in g.slsObjs]
                        inputgraphseg = ''.join(inputsyls)
                        if inputgraph != inputgraphseg:
                            # if the segmentation has not consumed all of the input
                            # the portion that failed is recorded and used later
                            failedend = inputgraph.split(inputgraphseg)[1]
                            if args.verberr:
                                print("Segmentation failure: input {i}, output {o}".format(i=inputgraph,o=inputgraphseg))
                                print("failed end: {f}".format(f=failedend))
                        for s in g.slsObjs:
                            # print("syllable {s}".format(s=s.grapheme))
                            syl_KK2FSS(s,g)

                    else:
                        failedend = ''
                        # if there are no syllables found
                        # generally will be a punctuation character
                        if not(g.graph[0].isalpha() or g.graph[0].isdigit()) and g.graph[0] not in '(-':
                            # if it isn't a letter or digit or ( or -
                            # take the last character off (prevents spaces before commas and fullstops etc.)
                            outline = outline[:-1]
                        # where no syllables were found, don't change the input spelling
                        g.graph = inputgraph
                    if inputgraph != inputgraphseg:
                        # if the segmentation failed, append the failed end
                        # though perhaps should simply return input
                        # becasue these are liable to be personal name
                        # non-Cornish place names, or unassimilated loanwords
                        g.graph += failedend

                    # add word to the output line
                    outline += g.graph                    
                    if g.graph != '(':
                        # add spaces between words except before a bracket
                        outline += ' '                        
            print("FSS: {f}\n".format(f=outline))
    else:
        inputtext = f.read()
        rannans = sylabelenn_ranna_kw.RannaSyllabelenn(inputtext)
        
        punctchars = ".,;:!?()-"
        for i in rannans.geryow:
            g = sylabelenn_ranna_kw.Ger(i,rannans,fwds)
            inputgraph = g.graph
            if g.graph != '' and g.graph not in punctchars:
                # don't display words that are only punctuation characters
                if not(args.short):
                    # long form syllable details
                    g.diskwedh()

                # record input spelling before KK-->SWF
                inputsyls = [s.grapheme for s in g.slsObjs]
                inputgraphseg = ''.join(inputsyls)
                if inputgraph != inputgraphseg:
                    # if the segmentation has not consumed all of the input
                    # the portion that failed is recorded and used later
                    if inputgraphseg != '':
                        failedend = inputgraph.replace("-","").split(inputgraphseg)[1]
                    else:
                        if inputgraph.isalpha() or inputgraph[0] == "'":
                            failedend = inputgraph
                        else:
                            failedend = ''
                    if args.verberr:
                        print("Segmentation failure: input {i}, output {o}".format(i=inputgraph,o=inputgraphseg))
                        print("failed end: {f}".format(f=failedend))

                for s in g.slsObjs:
                    # convert syllable
                    syl_KK2FSS(s,g)
                    
                if inputgraph != inputgraphseg and inputgraphseg != '':
                    # if the segmentation failed, append the failed end
                    # though perhaps should simply return input
                    # becasue these are liable to be personal name
                    # non-Cornish place names, or unassimilated loanwords
                    g.graph += failedend

                # in short form, don't have a new line between words
                if args.short:
                    print("{w} ".format(w=g.graph), end="")
                else:
                    print("FSS: {w}\n".format(w=g.graph))
