# coding=utf-8
import sys
import nltk
sys.path.append("../")
import niverow


def replacefigs(digits):
    num = int(digits)
    num_kw = niverow.numberkw(num)
    return num_kw

def niverow2kwtext(inputtext):
    words = nltk.word_tokenize(inputtext)
    words = [replacefigs(w) if w.isdigit() else w for w in words]
    return " ".join(words)

if __name__ == "__main__":
    print(niverow2kwtext("99 a boteli gwyrdh usi ow sevel war an fos"))
