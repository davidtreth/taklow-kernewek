# coding=utf-8
from __future__ import print_function
import syllabenn_ranna_kw
import datageryow
import argparse
import codecs
import string
import re

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
        # and not final syllables
        if vowellength == 2 and vowel == 'y' and inputsyl.structure[-1] != 'V' and not(inputsyl.final):
            #if args.verberr and 'y' in inputsyl.grapheme:
            #    print("convert_y")
            #    print(inputsyl.sylparts)
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
    outputgraph = inputword.graph
    if inputword.graph.lower() in datageryow.words_c:
        outputgraph = outputgraph.replace("se","ce")
        outputgraph = outputgraph.replace("si", "ci")
        outputgraph = outputgraph.replace("syal", "cyal")
        outputgraph = outputgraph.replace("syol", "cyol")
        if inputword.graph not in datageryow.words_c_syon:
            outputgraph = outputgraph.replace("syon", "cyon")
        outputgraph = outputgraph.replace("sysy", "cycy")
        outputgraph = outputgraph.replace("syan", "cyan")
    if inputword.graph.lower() in datageryow.words_sh_c:
        outputgraph = outputgraph.replace("shy", "cy")
        outputgraph = outputgraph.replace("sh", "cy")
    # reverse some possible incorrect substitutions
    # in the endings of inflected verbs
    if inputword.graph.lower() in datageryow.verbs_infl:
        if outputgraph[-5:] == "cewgh":
            outputgraph = outputgraph[:-5]+"sewgh"
        if outputgraph[-4:] == "cens":
            outputgraph = outputgraph[:-4]+"sens"
        if outputgraph[-3:] in ["cen","ces","cis"]:
            outputgraph = outputgraph[:-3]+"s"+outputgraph[-2:]        
    inputword.graph = outputgraph

def convert_misc(inputword, inputgraph):
    """ Various lexical level substitutions 
    inputword is a Ger object after syllable level substitutions
    inputgraph is the original KK spelling """
    # diworth --> dhyworth, diwar --> dhywar
    # subst diwor- --> dhywor-, diwar- --> dhywar-  but don't change diwarr
    # a-dhiworth --> a-dhyworth subst a-dhiwo- --> a-dhywo-
    # a-dhiwar --> a-dhywar subst a-dhiwa- --> a-dhywa
    outputgraph = inputword.graph
    if inputgraph.lower() == "diwarr":
        outputgraph = "diwar"
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
    """ do syllable level substitutions """
    inputgraph = inputword.graph.lower()
    inputsyl.grapheme = inputsyl.grapheme.lower()
    # turn KK 'oe' to 'oo' or 'o'
    convert_oe(inputsyl, inputgraph in datageryow.SWF_oowords)
    # vocalic alternation
    convert_yw(inputsyl)
    convert_y(inputsyl)
    # turn some double consts into single
    convert_double_consts(inputsyl)
    

def wordlevelsubs_KK2FSS(inputword, inputgraph):
    """ concatenate the processed syllable spellings
    into a new word spelling and make any necessary word
    level substitutions 
    inputword is a Ger object after syllable level substitutions
    inputgraph is the original KK spelling """
    # replace the plaintext syllable list
    inputword.sls = [s.grapheme for s in inputword.slsObjs]
    # build spelling of word from spelling of syllables
    inputword.graph = ''.join(inputword.sls)
    # substitute c for s where necessary
    convert_s_c(inputword)
    # miscellaneous lexical level substitutions
    convert_misc(inputword, inputgraph)
    
def word_KK2FSS(ger,verberr=False):
    """ expect Ger object and convert its spelling to SWF """
    if ger.graph != '':
        # record input spelling before KK-->SWF
        inputgraph = ger.graph
        s = re.split('[a-zA-Z]+', inputgraph)
        firstalpha = len(s[0])
        if firstalpha == len(inputgraph):
            capital = False
        else:
            capital = inputgraph[firstalpha].isupper()
        allcaps = inputgraph.isupper()
        ger.graph = ger.graph.lower()
        if len(ger.slsObjs) > 0:
            # if it is a word, loop through syllables
            # and build up the spelling after segmentation
            # but before the KK-->SWF conversion
            inputsyls = [s.grapheme.lower() for s in ger.slsObjs]
            inputgraphseg = ''.join(inputsyls)
            if inputgraph.lower() != inputgraphseg:
                # if the segmentation has not consumed all of the input
                # the portion that failed is recorded and used later
                failedend = inputgraph.lower().split(inputgraphseg)[1]
                if verberr:
                    print("Segmentation failure: input {i}, output {o}".format(i=inputgraph,o=inputgraphseg))
                    print("failed end: {f}".format(f=failedend))
            for s in ger.slsObjs:
                # loop through the syllables and change the spellings
                # print("syllable {s}".format(s=s.grapheme))
                syl_KK2FSS(s,ger)
                # print("syllable {s}".format(s=s.grapheme))
            wordlevelsubs_KK2FSS(ger, inputgraph)
        else:
            failedend = ''
            # if there are no syllables found
            # generally will be a punctuation character
            if not(ger.graph[0].isalpha() or ger.graph[0].isdigit()) and ger.graph[0] not in '[{(-':
                # if it isn't a letter or digit or open bracket or hyphen
                # where no syllables were found, don't change the input spelling                
                ger.graph = inputgraph
        if len(ger.slsObjs) == 0 or inputgraph.lower() != inputgraphseg:
            # if the segmentation failed, append the failed end
            # though perhaps should simply return input
            # becasue these are liable to be personal name
            # non-Cornish place names, or unassimilated loanwords
            ger.graph += failedend
        if capital:            
            nonalpha = ger.graph[:firstalpha]            
            alpha = string.capwords(ger.graph[firstalpha:])
            ger.graph = nonalpha + alpha
        if allcaps:
            ger.graph = ger.graph.upper()
                

def line_KK2FSS(line,fwds=False,longform=True, verberr=False):
    """ take line of text and convert to SWF """
    rannans = syllabenn_ranna_kw.RannaSyllabenn(line)
    if longform:            
        outputtext = "KK: {k}".format(k=line.strip())
    # build up line in SWF
    outline = ''
    for i in rannans.geryow:
        # go through word by word
        g = syllabenn_ranna_kw.Ger(i,rannans,fwds)
        if len(g.slsObjs) == 0 and g.graph:
            if not(g.graph[0].isalpha() or g.graph[0].isdigit()) and g.graph[0] not in '[{(-':
                # if it isn't a letter or digit or open bracket or hyphen
                # take the last character of the line off
                # (prevents spaces before commas and fullstops etc.)
                outline = outline[:-1]
        word_KK2FSS(g,verberr)    
        # add word to the output line
        # print(g.graph)
        outline += g.graph                    
        if g.graph not in '([{':
            # add spaces between words except after an open bracket or trailing hyphen
            if g.graph[-1] == "-" and len(g.graph)>1:
                pass
            else:
                outline += ' '
    if longform:
        outputtext += "\nFSS: {f}".format(f=outline)
    else:
        outputtext = outline
    return outputtext

def text_KK2FSS(inputtext,fwds=False,longform=False,verberr=False):
    """ take an input text and convert to SWF word by word """
    rannans = syllabenn_ranna_kw.RannaSyllabenn(inputtext)
    punctchars = ".,;:!?()-"
    outputtext = ''
    for i in rannans.geryow:
        g = syllabenn_ranna_kw.Ger(i,rannans,fwds)
        if len(g.slsObjs) == 0 and g.graph:
            if not(g.graph[0].isalpha() or g.graph[0].isdigit()) and g.graph[0] not in '[{(-':
                # if it isn't a letter or digit or ( or -
                # take the last character of the line off
                # (prevents spaces before commas and fullstops etc.)
                outputtext = outputtext[:-1]
        inputgraph = g.graph
        if longform and g.graph != '' and g.graph not in punctchars:
            # don't display words that are only punctuation characters
            # long form syllable details
            outputtext += "\n".join(g.longoutput())+"\n"
        word_KK2FSS(g,verberr)
        if longform:
            outputtext += "FSS: {w}\n\n".format(w=g.graph)
        else:
            outputtext += "{w} ".format(w=g.graph)
    return outputtext

def wordstr_KK2FSS(inputword, fwds=False, verberr=False):
    """ expect a single word to convert from KK to SWF """
    rannans = syllabenn_ranna_kw.RannaSyllabenn(inputword)
    g = syllabenn_ranna_kw.Ger(inputword, rannans, fwds)
    word_KK2FSS(g, verberr)
    return g.graph
            
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
    parser.add_argument("--backwards",action="store_true",
                        help="Backwards segmentation from end of each word. Default is to start at the beginning.")

    args = parser.parse_args()
    # Check that the input parameter has been specified.
    if args.inputfile == None:
        # Print an error message if not and exit.
        print("Error: No input file provided.")
        sys.exit()

    f = codecs.open(args.inputfile,"r",encoding='utf-8',errors='replace')
    
    if args.backwards:
        fwds = False
    else:
        fwds = True

    if args.line:
        # read file line by line
        inputtext = f.readlines()
        for line in inputtext:
            line = syllabenn_ranna_kw.preprocess2ASCII(line)
            outline = line_KK2FSS(line, fwds, not(args.short), args.verberr)
            if args.short:
                print(outline)
            else:
                print(outline+"\n")
    else:
        inputtext = f.read()
        inputtext = syllabenn_ranna_kw.preprocess2ASCII(inputtext)
        print (text_KK2FSS(inputtext, fwds, not(args.short), args.verberr))
