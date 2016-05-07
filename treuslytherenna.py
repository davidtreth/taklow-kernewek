from __future__ import print_function
import syllabenn_ranna_kw
import datageryow
import argparse
import codecs

# TODO
# vocalic alternation e.g. byw but bewnans, bewnansow
# benyn, benenes
# often KK half-long <y> --> SWF <e>
# also some unstressed <y> in final syllable of root --> <e>
# now implemented but needs more testing

# use of c in place of s in some words e.g. cider, cita, polici
# now implemented but needs more testing

# not implemented yet:
# use of z zebra, Zimbabwe
# need to find which words use z in SWF
# hyphenation - currently leaves as it is
# changes of individual lexical items
# dhyworth/dyworth
# ynkleudhva --> ynkladhva
            
def convert_oe(inputsyl, SWF_ooword):
    ''' Take a syllable and change 'oe' to 'oo' or 'o' if appropriate '''
    outputgrapheme = inputsyl.grapheme
    if inputsyl.monosyl:
        # for monosyllables...
        if inputsyl.grapheme.lower() in datageryow.SWF_owords:
            # check if its one of those monosyls that go oe->o
            # despite a long vowel
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
        if (inputsyl.grapheme.lower() in datageryow.SWF_oosyls and inputsyl.stressed) or SWF_ooword:
            outputgrapheme = inputsyl.grapheme.replace("oe","oo")
        else:
            # otherwise 'oe' --> 'o'
            outputgrapheme = inputsyl.grapheme.replace("oe","o")
    inputsyl.grapheme=outputgrapheme

def convert_yw(inputsyl):
    """ vocalic alternation for words with <yw> in earlier Kemmyn and <ew> in current KK and SWF
        and words that had <yw> in earlier Kemmyn but <uw> in current KK and SWF """
    outputgrapheme = inputsyl.grapheme
    if inputsyl.graphGer.lower() in datageryow.words_uw:
        outputgrapheme = outputgrapheme.replace("yw","uw")
    # this doesn't actually happen for all polysyllables
    if not(inputsyl.monosyl) and not(inputsyl.final) and inputsyl.structure[0] == 'C':
        outputgrapheme = outputgrapheme.replace("yw","ew")
    inputsyl.grapheme=outputgrapheme

def convert_y(inputsyl):
    """ vocalic alternation for half-long KK y vowels that go to e in SWF 
    there are likely a number of false positives e.g. mynysenn -> *mynesen """
    # e.g. benynes --> benenes
    # 1/2 long KK y becomes e
    if inputsyl.graphGer.lower() not in datageryow.words_y:
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
    """ change certain double consonants to single """
    outputgrapheme = inputsyl.grapheme
    # kk -> ck except for a few words that retain kk
    if inputsyl.graphGer.lower() not in datageryow.words_SWF_kk:
        outputgrapheme = outputgrapheme.replace("kk","ck")
    # for unstressed syllables, excluding certain prefixes
    if inputsyl.stressed == False and inputsyl.grapheme.lower() not in datageryow.prefixes_2ndstress:
        outputgrapheme = outputgrapheme.replace("mm","m")
        outputgrapheme = outputgrapheme.replace("nn","n")
        # final syllables - ll and rr
        if inputsyl.final:
            # the suffix for 'tool' or 'device' is now -ell in SWF
            # however there is KK kastell SWF kastel
            # KK arall/erell SWF aral/erel
            if inputsyl.graphGer.lower() in datageryow.words_SWF_one_l:
                outputgrapheme = outputgrapheme.replace("ll","l")
            outputgrapheme = outputgrapheme.replace("rr","r")
    inputsyl.grapheme = outputgrapheme


def convert_s_c(inputword):
    """ in some words, change s to c. This is done by 
    lookup basically """
    if inputword.graph in datageryow.words_c:
        outputgraph = inputword.graph.replace("se","ce")
        outputgraph = outputgraph.replace("si", "ci")
        outputgraph = outputgraph.replace("syal", "cyal")
        outputgraph = outputgraph.replace("syol", "cyol")
        if inputword.graph not in datageryow.words_c_syon:
            outputgraph = outputgraph.replace("syon", "cyon")
        outputgraph = outputgraph.replace("sysy", "cycy")
        outputgraph = outputgraph.replace("syan", "cyan")
        # reverse some possible incorrect substitutions
        # in the endings of inflected verbs
        if inputword.graph in datageryow.verbs_infl:
            if outputgraph[-5:] == "cewgh":
                outputgraph = outputgraph[:-5]+"sewgh"
            if outputgraph[-4:] == "cens":
                outputgraph = outputgraph[:-4]+"sens"
            if outputgraph[-3:] in ["cen","ces","cis"]:
                outputgraph = outputgraph[:-3]+"s"+outputgraph[-2:]        
        inputword.graph = outputgraph

def convert_misc(inputword):
    """ Various lexical level substitutions """
    # diworth --> dhyworth, diwar --> dhywar
    # subst diwor- --> dhywor-, diwar- --> dhywar-  but don't change diwarr
    # a-dhiworth --> a-dhyworth subst a-dhiwo- --> a-dhywo-
    # a-dhiwar --> a-dhywar subst a-dhiwa- --> a-dhywa
    outputgraph = inputword.graph
    if inputword.graph.lower() == "diwarr":
        pass
    elif inputword.graph.lower()[:5] == "diwar":
        outputgraph = inputword.graph.replace("diwar","dhywar")
    elif inputword.graph.lower()[:5] == "diwor":
        outputgraph = inputword.graph.replace("diwor","dhywor")
    elif inputword.graph.lower()[:7] == "a-dhiwo" or inputword.graph.lower()[:7] == "a-dhiwa":
        outputgraph = inputword.graph.replace("dhiw","dhyw")
    # seythun --> seythen
    if inputword.graph.lower()[:7] == "seythun":
        outputgraph = inputword.graph.replace("seythun","seythen")
    # ynys --> enys
    if inputword.graph.lower()[:4] in ["ynys", "ynes"]:
        # second y of ynys may have been changed to e by vowel affectation method
        outputgraph = inputword.graph.replace("yn","en",1)
    # ynkleudhva --> ynkladhva
    if inputword.graph.lower()[:10] == "ynkleudhva":
        outputgraph = inputword.graph.replace("ynkleudhva","ynkladhva")
    # chyf --> chif
    if inputword.graph.lower()[:4] == "chyf" and not(inputword.graph.lower()[:5] in ["chyff","chyft"]):
        # don't change chyffar or chyften
        outputgraph = inputword.graph.replace("chyf","chif")
    # okkupya
    if inputword.graph.lower()[:4] == "okku":
        outputgraph = inputword.graph.replace("okk","ok",1)
    inputword.graph = outputgraph

def syl_KK2FSS(inputsyl, inputword):
    inputgraph = inputword.graph.lower()
    # turn KK 'oe' to 'oo' or 'o'
    convert_oe(inputsyl, inputword.graph.lower() in datageryow.SWF_oowords)
    # vocalic alternation
    convert_yw(inputsyl)
    convert_y(inputsyl)
    # turn some double consts into single
    convert_double_consts(inputsyl)
    # replace the plaintext syllable list
    inputword.sls = [s.grapheme for s in inputword.slsObjs]
    # build spelling of word from spelling of syllables
    inputword.graph = ''.join(inputword.sls)
    # substitute c for s where necessary
    convert_s_c(inputword)
    # miscellaneous lexical level substitutions
    convert_misc(inputword)


def word_KK2FSS():
    pass

def line_KK2FSS():
    pass

def text_KK2FSS():
    pass
            
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

    f = codecs.open(args.inputfile,"r",encoding='utf-8',errors='replace')
    fwds = True
    #fwds = False
    if args.line:
        # read file line by line
        inputtext = f.readlines()
        for line in inputtext:
            rannans = syllabenn_ranna_kw.RannaSyllabenn(line)            
            print("KK: {k}".format(k=line.lstrip()),end = "")
            # build up line in SWF
            outline = ''
            for i in rannans.geryow:
                # go through word by word
                g = syllabenn_ranna_kw.Ger(i,rannans,fwds)
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
                    if len(g.slsObjs) == 0 or inputgraph != inputgraphseg:
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
        rannans = syllabenn_ranna_kw.RannaSyllabenn(inputtext)
        
        punctchars = ".,;:!?()-"
        for i in rannans.geryow:
            g = syllabenn_ranna_kw.Ger(i,rannans,fwds)
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
