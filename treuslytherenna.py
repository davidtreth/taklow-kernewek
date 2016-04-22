from __future__ import print_function
import sylabelenn_ranna_kw
import mutatya
import argparse
import codecs

# TODO - vocalic alternation e.g. byw but bewnans, bewnansow
# often KK half-long <y> --> SWF <e>
# also some unstressed <y> in final syllable of root --> <e>

# use of c in place of s in some words e.g. cider, cita, polici
# use of z zebra, Zimbabwe
# hyphenation
# dhyworth/dyworth
# ynkleudhva --> ynkladhva

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


def convert_oe(inputsyl, SWF_ooword):
    ''' Take a syllable and change 'oe' to 'oo' or 'o' if appropriate '''
    outputgrapheme = inputsyl.grapheme
    
    if inputsyl.monosyl:
        if inputsyl.grapheme in SWF_owords:
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
        if (inputsyl.grapheme in SWF_oosyls and inputsyl.stressed) or SWF_ooword:
            outputgrapheme = inputsyl.grapheme.replace("oe","oo")
        else:
            # otherwise 'oe' --> 'o'
            outputgrapheme = inputsyl.grapheme.replace("oe","o")
    inputsyl.grapheme=outputgrapheme

def convert_yw(inputsyl):
    outputgrapheme = inputsyl.grapheme
    # this doesn't actually happen for all polysyllables
    if not(inputsyl.monosyl):
        outputgrapheme = inputsyl.grapheme.replace("yw","ew")
    inputsyl.grapheme=outputgrapheme

def convert_double_consts(inputsyl):
    outputgrapheme = inputsyl.grapheme
    if inputsyl.graphGer not in words_SWF_kk:
        outputgrapheme = outputgrapheme.replace("kk","ck")
    if inputsyl.stressed == False and inputsyl.grapheme not in prefixes_2ndstress:
        outputgrapheme = outputgrapheme.replace("mm","m")
        outputgrapheme = outputgrapheme.replace("nn","n")
        if inputsyl.final:
            # the suffix for 'tool' or 'device' is now -ell in SWF
            # however there is KK kastell SWF kastel
            # KK arall/erell SWF aral/erel
            if inputsyl.graphGer in words_SWF_one_l:
                outputgrapheme = outputgrapheme.replace("ll","l")
            outputgrapheme = outputgrapheme.replace("rr","r")
    inputsyl.grapheme = outputgrapheme


    
def addallmutatedforms(listwords):
    mutatedwords = []
    for w in listwords:
        for i in [2,3,4,5,6]:
            addword = mutatya.mutate(w,i)
            mutatedwords.append(mutatya.mutate(w,i))
    for w in mutatedwords:
        if w not in listwords:
            listwords.append(w)
   
            
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
                    if len(g.slsObjs) > 0:
                        # if it is a word, loop through syllables
                        for s in g.slsObjs:
                            # turn KK 'oe' to 'oo' or 'o'
                            # SWF_oowords is a list of words that
                            # keep 'oo' in polysyllables
                            convert_oe(s, g.graph in SWF_oowords)
                            # vocalic alternation
                            # not yet used
                            #convert_yw(s)
                            # turn some double consts into single
                            convert_double_consts(s)
                        g.sls = [s.grapheme for s in g.slsObjs]
                        # build spelling of word from spelling of syllables
                        g.graph = ''.join(g.sls)
                    else:
                        if not(g.graph[0].isalpha() or g.graph[0].isdigit()) and g.graph[0] not in '(-':
                            # if it isn't a letter or digit or ( or -
                            # take the last character off (prevents spaces before commas and fullstops etc.)
                            outline = outline[:-1]
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
            if g.graph != '' and g.graph not in punctchars:
                # don't display words that are only punctuation characters
                if not(args.short):
                    # long form syllable details
                    g.diskwedh()
                for s in g.slsObjs:
                    # turn KK 'oe' to 'oo' or 'o'
                    convert_oe(s, g.graph in SWF_oowords)
                    # vocalic alternation, not yet used
                    #convert_yw(s)
                    # turn some double consts into single
                    convert_double_consts(s)
                g.sls = [s.grapheme for s in g.slsObjs]
                g.graph = ''.join(g.sls)
                # in short form, don't have a new line between words
                if args.short:
                    print("{w} ".format(w=g.graph), end="")
                else:
                    print("FSS: {w}\n".format(w=g.graph))
