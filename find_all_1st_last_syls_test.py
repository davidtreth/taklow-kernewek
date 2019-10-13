import syllabenn_ranna_kw as syl
import argparse
import codecs

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
    args = parser.parse_args()
    # Check that the input parameter has been specified.
    if args.inputfile == None:
        inputtext = input("Gorra geryow mar pleg:")
    else:
        f = codecs.open(args.inputfile,"r",encoding="utf-8",errors="replace")
        inputtext = f.read()
        inputtext = syl.preprocess2ASCII(inputtext)
    rannans = syl.RannaSyllabenn(inputtext)
    print("pub kynsa syllabenn:")
    for g in rannans.geryow:
        print(g)
        print("kynsa syllabennow possybl", rannans.match_syl_all(g, syl.kwKemmynDevRegExp.kynsaRegExp, fwd=True))
        print("diwettha syllabennow possybl", rannans.match_syl_all(g, syl.kwKemmynDevRegExp.diwetRegExp, fwd=False))
