# -*- coding: utf-8 -*-
# create a letter frequency distribution for the Universal Declaration of
# Human Rights in every language that the Python NLTK has it
# by default output to a HTML file

import cornish_corpus
import nltk

udhrlangs = nltk.corpus.udhr.fileids()
udhrtexts = [nltk.corpus.udhr.words(f) for f in udhrlangs]

# turn all digraphs off, otherwise could get odd results
# if the substitution letters used internally actually exist in the lang
output = cornish_corpus.MostFreqLetters(udhrtexts, udhrlangs, False, False, False)

print(output)

# set to HTML output
htmlout = True

if htmlout:
    outfilename = "udhr.html"
    outfile = file(outfilename, "w")
    output = output.split("Text:")

    htmlout = u"<!DOCTYPE html><meta charset='UTF-8'>\n<html><style>td{width:auto; text-align: center; padding:10px; border:none;}\ntr:nth-child(even){background-color: Gainsboro;}</style><head><title>Letter Distribution of UDHR</title>\n</head>\n<body><h2>Letter frequency distributions in the Universal Declaration of Human Rights</h2>"
    for i in output:
        if "Letters" in i:
            langname, rest = i.split("Letters")

            htmlout += "<div id='{langn}'><h3>Language: {langn}</h3><div><h5>Letters ".format(langn=langname.strip())
            lines = rest.split("\n")
            for l in lines:
                if "frequency" in l:
                    htmlout += l+"</h5><table>"
                elif ":" in l:
                    tdivs = l.split(":")
                    htmlout += "<tr>"
                    for d in tdivs:
                        htmlout += "<td>"+d.strip()+"</td>"
                    htmlout += "</tr>"
            htmlout += "</table></div></div>"

    htmlout += "</body></html>"
    outfile.write(htmlout)
    outfile.close()
