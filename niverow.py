# coding=utf-8
# David Trethewey
# updated 14-09-2016
import sys
import mutatya

numarray = ["onan","dew","tri","peswar","pymp",
            "hwegh","seyth","eth","naw","deg",
            "unnek","dewdhek","trydhek","peswardhek","pymthek",
            "hwetek","seytek","etek","nownsek","ugens"]
numarray_ord = ["kynsa", "nessa", "tressa", "peswora", "pympes",
                "hweghves", "seythves", "ethves", "nawves", "degves",
                "unnegves", "dewdhegves", "trydhegves", "peswardhegves",
                "pymthegves", "hwetegves", "seytegves", "etegves",
                "nownsegves", "ugensves"]

def unnnoun(noun, fem=False):
    if fem:
        mstate = 2
    else:
        mstate = 1
    return "unn "+mutatya.mutate(noun,mstate)

def dewnoun(noun, fem=False):
    if fem:
        return "diw " + mutatya.mutate(noun,2) #feminine form
    else:
        return "dew " + mutatya.mutate(noun,2)
    
def trinoun(noun, fem=False):
    if fem:
        return "teyr " + mutatya.mutate(noun,3) #feminine form
    else:
        return "tri " + mutatya.mutate(noun,3)

def firstpartnoun(num, noun, fem=False):
    if num == 0:
        return ""
    # give number 1-19 or first part of compound
    if num > 4:
        # direct lookup for numbers up to 20
        firstpart_k = numarray[num-1] + " " + noun
        return firstpart_k
    else:
        # override for numbers 1-4 to handle mutation
        # and feminine forms if 'fem' is True
        # mutation should only happen for 1 for fem. nouns
        # mutation for both masc. and fem. for 2, 3
        # and use of feminine forms for 2, 3, 4 for fem. nouns
        # variable fem keeps track of gender
        if num == 4:
            if fem:
                firstpart_k = "peder " + noun # feminine form
            else:
                firstpart_k = numarray[num-1] + " " + noun
            return firstpart_k
        if num == 3:
            firstpart_k = trinoun(noun,fem)
            return firstpart_k
        if num == 2:
            firstpart_k = dewnoun(noun, fem)
            return firstpart_k
        if num == 1:
            firstpart_k = unnnoun(noun,fem)
            return firstpart_k
            

def numberkw_noun(num, noun, fem=False, npl = "ow"):
    """ Returns numeral <num> in Cornish compounded with <noun>

    <fem> is a boolean variable specifying whether the noun is feminine
    <npl> is the plural of <noun>. if it isn't specified default to
    <noun>+'ow'
    """
    
    # default plural suffix -ow
    if npl == "ow":
        npl = noun+npl
        
    if not(isinstance(num,int)):
        print("num is not an integer. attempting conversion...")
        num = int(num)
        if num < 0:
            print("num is negative, multiplying by -1")
            num = num * -1
        print("num={n}".format(n=num))
        
    if num == 0:
        num_k = "zero a {n}".format(n=mutatya.mutate(npl,2))
        return num_k
        
    if num > 0 and num < 21:     
        num_k = firstpartnoun(num, noun, fem)
        
    if num > 20 and num < 40:
        # numbers 21 to 39
        num_k = firstpartnoun(num-20,noun,fem) + " warn ugens"
            
    if (num > 39 and num < 100)or(num > 119 and num < 200):
        # numbers 40 to 199 excluding 100-119
        firstpart = num % 20
        secondpart = num // 20
        if firstpart == 0:
            num_k = numarray[secondpart-1] + " ugens " + noun
        else:
            num_k = firstpartnoun(firstpart,noun,fem) + " ha " + numarray[secondpart-1] + " ugens"
        if num == 50:
            # override for num=50
            num_k = "hanterkans " + noun
            
    if num == 100:
        num_k = "kans " + noun
        
    if num > 100 and num < 120:
        num_k = "kans "+noun+" ha "+numarray[num-101]

    if num > 199 and num < 1000:
        ha = " ha "
        kansow = num // 100
        if num % 100 == 0:
            num_k = numarray[kansow-1] + " kans " + noun
        else: 
            if num % 100 < 21 or num % 20 == 0:
                num_k = numarray[kansow-1] + " kans "+ noun + ha + numberkw(num % 100)
            else:
                num_k = numberkw(num) + " a " + mutatya.mutate(npl,2)
                                
    if num > 999 and num < 21000:
        if num == 1000:
            num_k = "mil "+ mutatya.mutate(noun,2)
        else:
            if num % 1000 == 0:
                num_k = numberkw(1000 * num//1000) + " " + mutatya.mutate(noun,2)
            else:
                if num % 1000 < 21 or (num % 1000 < 200 and num % 20 == 0) or num % 100 == 0:
                    num_k = numberkw(1000*(num//1000)) + " " + mutatya.mutate(noun,2) + " ha " + numberkw(num % 1000)
                else:
                    num_k = numberkw(num) + " a " + mutatya.mutate(npl,2)

    if num > 20999 and num < 40000:
        num_k = numberkw(num) + " a " + mutatya.mutate(npl,2)
            
    if num > 39999 and (num < 100000)or(num % 20000 == 0 and num <200000):
        num_k = numberkw(num) + " a " + mutatya.mutate(npl,2)
        if num % 20000 == 0:
            num_k = numberkw(num//20000) + " ugens mil " + mutatya.mutate(noun,2)

    elif num > 99999 and num < 1000000:
        num_k = numberkw(num) +" a " + mutatya.mutate(npl,2)
        if num % 100000 == 0:
            num_k = numberkw(num//100000) + " kans mil " + mutatya.mutate(noun,2)
        if num == 100000:
            num_k = "kans mil "+ mutatya.mutate(noun,2)
    if num > 999999 and num < 2000000:
        if num == 1000000:
            num_k = "milvil " + mutatya.mutate(noun,2)
        else:
            num_k = numberkw(num) +  " a " + mutatya.mutate(npl,2)
            
    if num > 1999999 and num < 20000001:
        if num % 1000000 == 0:
            num_k = numberkw(num // 1000000) + " milvil " + mutatya.mutate(noun,2)
            return num_k
        else:
            num_k = numberkw(num) +  " a " + mutatya.mutate(npl,2)

    if num > 20000000 and num < 1000000000:
        if num % 20000000 == 0 and num < 200000000:
            num_k = numberkw(num//1000000) + " milvil " + mutatya.mutate(noun,2)
        else:
            num_k = numberkw(num) +  " a " + mutatya.mutate(npl,2)

    if num > 999999999 and num < 2000000000:
        num_k = numberkw(num) +  " a " + mutatya.mutate(npl,2)
            
    if num > 1999999999 and num < 20000000001:
        num_k = numberkw(num) +  " a " + mutatya.mutate(npl,2)

    if num > 2e10:
        num_k = numberkw(num) +  " a " + mutatya.mutate(npl,2)

    num_k = num_k.replace("  "," ")
    num_k = num_k.replace("ha u","hag u")
    num_k = num_k.replace("ha e","hag e")
    num_k = num_k.replace("ha o","hag o")
    num_k = num_k.replace("tri kans","tri hans")
    num_k = num_k.replace("deg ha dew ugens","hanterkans")

    # return the result
    return num_k    

def numberkw(num):
    """ return the Cornish for the numeral <num> without a noun """
    num = int(num)
    if num == 0:
        num_k = "mann"
    if num > 0 and num < 21:
        num_k = numarray[num-1]
    if num > 20 and num < 40:
        num_k = numarray[num-21] + " warn ugens"

    if (num > 39 and num < 100)or(num > 119 and num < 200):
        firstpart = num % 20
        secondpart = num // 20

        num_k = numarray[firstpart-1] +" ha " + numarray[secondpart-1] + " ugens"
        if firstpart == 0:
            num_k = numarray[secondpart-1] + " ugens"
        if num == 50:
            num_k = "hanterkans"

    if num == 100:
        num_k = "kans"
    if num > 100 and num < 120:
        num_k = "kans ha "+ numberkw(num-100)
    if num > 199 and num < 1000:
        kansow = num // 100
        if num % 100 < 21 or num % 20 == 0 or num % 100 == 50:
            if num % 100 == 0:
                num_k = numarray[kansow-1] + " kans"
            else:
                num_k = numarray[kansow-1] + " kans ha " + numberkw(num % 100)
        else:
            num_k = numarray[kansow-1] + " kans, " + numberkw(num % 100)

    if num % 1000 < 200 and(num % 20 == 0 or num % 1000 < 21):
        ha = " ha "
    else:
        ha = ", "
    if num == 1000:
        num_k = "mil"
    if num > 1000 and num < 2000:
        num_k = "mil"+ ha+ numberkw(num % 1000)

    if num > 1999 and num < 21000:
        if num % 1000 == 0:
            num_k = numberkw(num//1000) + " mil"
        else:
            num_k = numberkw(num//1000) + " mil"+ha + numberkw(num % 1000)
    if num > 20999 and num < 40000:
        if num % 1000  == 0:
            num_k = numberkw((num % 20000)//1000) + " mil warn ugens"
        else:            
            num_k = numberkw((num % 20000)//1000) + " mil warn ugens"+ha+ numberkw(num % 1000)
    if (num >39999 and num<100000) or (num % 20000 ==0)and(num<200000):
        if num == 100000:
            num_k = "kans mil"        
        elif num % 20000 == 0:
            num_k = numberkw(num//20000) + " ugens mil"
        elif num % 1000 == 0:
            num_k = numberkw((num % 20000)//1000) + " mil ha "+ numberkw(num//20000) + " ugens"
        else:
            num_k = numberkw((num % 20000)//1000) + " mil ha "+ numberkw(num//20000) + " ugens" +ha+ numberkw(num % 1000)
    elif num > 99999 and num < 1000000:
        num_k = numberkw(num//1000) + " a vilyow" + ha + numberkw(num % 1000)
        if num % 1000 == 0:
            num_k = numberkw(num//1000) + " a vilyow"
        if num < 200000:
            num_k = "kans ha "+ numberkw((num-100000)//1000) + " a vilyow" +ha + numberkw(num % 1000)
            if num % 1000 == 0:
                num_k = "kans ha "+ numberkw((num-100000)//1000) + " a vilyow"
        if num % 100000 == 0:
            num_k = numberkw(num//100000) + " kans mil"
        else:
            if num % 20000 == 0 and num < 200000:
                num_k = numberkw(num//20000) + " ugens mil"

    if num > 999999 and num < 2000000:
        if num == 1000000:
            num_k = "milvil"
        else:
            if ((num % 1000000 < 200)and(num % 20 == 0)) or (num % 1000000 < 20) or ((num % 1000000 < 1000)and(num % 100 == 0)):            
                num_k = "milvil ha " + numberkw(num-1000000)
            else:
                num_k = "milvil, " + numberkw(num-1000000)
    if num > 1999999 and num < 20000001:
        if num % 1000000 == 0:
            num_k = numberkw(num//1000000) + " milvil"
        else:
            if ((num % 1000000 < 200)and(num % 20 == 0))or(num % 1000000 < 20) or ((num % 1000000 < 1000)and(num % 100 == 0)):
                num_k = numberkw(num//1000000) + " milvil ha " + numberkw(num % 1000000)
            else:
                num_k = numberkw(num//1000000) + " milvil, " + numberkw(num % 1000000)
    if num > 20000000 and num < 1000000000:
        if num % 20000000 == 0 and num < 200000000:
            num_k = numberkw(num // 1000000) + " milvil"
        else:
            if num % 1000000 == 0:
                num_k = numberkw(num//1000000) + " a vilvilyow"
            else:
                if ((num % 1000000 < 200)and(num % 20 == 0))or(num % 1000000 < 20) or ((num % 1000000 < 1000)and(num % 100 == 0)):
                    num_k = numberkw(num//1000000) + " a vilvilyow ha " + numberkw(num % 1000000)
                else:
                    num_k = numberkw(num//1000000) + " a vilvilyow, " + numberkw(num % 1000000)
    if num > 999999999 and num < 2000000000:
        if num == 1000000000:
            num_k = "bilvil"
        else:
            if ((num % 1000000000 < 200)and(num % 20 == 0))or(num % 1000000000 < 20) or ((num % 1000000000 < 1000)and(num % 100 == 0)):        
                num_k = "bilvil ha" + numberkw(num-1000000000)
            else:
                num_k = "bilvil, " + numberkw(num-1000000000)
    if num > 1999999999 and num < 20000000001:
        if num % 1000000000 == 0:
            num_k = numberkw(num // 1000000000) + " bilvil"
        else:
            if ((num % 1000000000 < 200)and(num % 20 == 0))or(num % 1000000000 < 20) or ((num % 1000000000 < 1000)and(num % 100 == 0)):
                num_k = numberkw(num//1000000000) + " bilvil ha " + numberkw(num % 1000000000)
            else:
                num_k = numberkw(num//1000000000) + " bilvil, " + numberkw(num % 1000000000)

    if num > 2e10:
        num_k = numberkw(num//1000000000) + " a bilvilyow, " + numberkw(num % 1000000000)
    
    num_k = num_k.replace("  "," ")
    num_k = num_k.replace("ha u","hag u")
    num_k = num_k.replace("ha e","hag e")
    num_k = num_k.replace("ha o","hag o")
    num_k = num_k.replace("tri kans","tri hans")
    num_k = num_k.replace("deg ha dew ugens","hanterkans")
    num_k = num_k.replace("dew mil", "dew vil")

    return num_k    
    
def numberkw_float(num):
    if num < 0.0:
        return "minus " + numberkw_float(-1*num)
    num_k = numberkw(int(num))
    if num == int(num) or num == 0:
        return num_k
    else:
        decdigits = str(num).split(".")[1]
        num_k = num_k + " poynt "
        for d in decdigits:
            num_k = num_k + numberkw(int(d)) + ", "
        if num_k[-2:] == ", ":
            num_k = num_k[:-2]
        return num_k
        
def numberkw_float_noun(num, noun, fem=False, npl = "ow"):
    if num == int(abs(num)):
        return numberkw_noun(num,noun,fem,npl)
    else:
        num_k = numberkw_float(num)
        num_k += " a "
        # default plural suffix -ow
        if npl == "ow":
            npl = noun+npl
        num_k += mutatya.mutate(npl,2)
        return num_k

def numberkw_ord(num):
    num = int(num)
    assert(num>0), "number should be positive"
    assert(num<=1000), "only numbers up to 1000 implemented so far"
    if num <=20:
        return numarray_ord[num-1]
    
    if num > 20 and num < 40:
        num_k = numarray_ord[num-21] + " warn ugens"

    if (num > 39 and num < 100)or(num > 119 and num < 200):
        firstpart = num % 20
        secondpart = num // 20

        num_k = numarray_ord[firstpart-1] +" ha " + numarray[secondpart-1] + " ugens"
        if firstpart == 0:
            num_k = numarray[secondpart-1] + " ugensves"
    if num == 100:
        num_k = "kansves"
    if num > 100 and num < 120:
        num_k = "kans ha "+ numberkw_ord(num-100)
    if num > 199 and num < 1000:
        kansow = num // 100
        if num % 100 < 21 or num % 20 == 0 or num % 100 == 50:
            if num % 100 == 0:
                num_k = numarray[kansow-1] + " kansves"
            else:
                num_k = numarray[kansow-1] + " kans ha " + numberkw_ord(num % 100)
        else:
            num_k = numarray[kansow-1] + " kans, " + numberkw_ord(num % 100)

    if num % 1000 < 200 and(num % 20 == 0 or num % 1000 < 21):
        ha = " ha "
    else:
        ha = ", "
    if num == 1000:
        num_k = "milves"
    return num_k
    
class NiferCymraeg:
    def __init__(self):
        self.numarray = ["un", "dau", "tri", "pedwar", "pump",
                         "chwech", "saith", "wyth", "naw", "deg"]
        self.numarray_dep = ["un", "dau", "tri", "pedwar", "pum",
                         "chwe", "saith", "wyth", "naw", "deg"]
        self.numarray_f = ["un", "dwy", "tair", "pedair", "pump",
                           "chwech", "saith", "wyth", "naw", "deg"]
    
        # handle 12, 15, 18, 20 as exceptions
        self.numarray_ord = ["cyntaf", "ail", "trydydd", "pedwerydd", "pumed",
                             "chweched", "seithfed", "wythfed", "nawfed", "degfed"]

        self.maxTrad = 20

    def replaces(self, num_cy):
        num_cy = num_cy.replace("  "," ")
        num_cy = num_cy.replace("a u","ac u")
        num_cy = num_cy.replace("a e","ac e")
        num_cy = num_cy.replace("a ê","ac ê")
        num_cy = num_cy.replace("a o","ac o")
        num_cy = num_cy.replace("a ô","ac ô")
        num_cy = num_cy.replace("a w","ac w")
        num_cy = num_cy.replace("a ŵ","ac ŵ")
        num_cy = num_cy.replace("tri can","tri chan") 
        num_cy = num_cy.replace("dau mil", "dau vil")
        return num_cy
    
    def setMaxTrad(self, maxTrad):
        self.maxTrad = maxTrad
        
    def numbercy(self, num, dep=False):
        """ return the Welsh for the numeral <num> without a noun """
        num = int(num)
        if num == 0:
            num_cy = "dim"
        if num > 0 and num <= 10:
            if dep:
                num_cy = self.numarray_dep[num-1]
            else:
                num_cy = self.numarray[num-1]
        if num > 10 and num < 200:
            if num > self.maxTrad:
                num_cy = self.numbercyDeg(num)
            else:
                num_cy = self.numbercyUgain(num)
        elif num >= 200:
            if num < 1000:
                tensunits = num % 100
                hundreds = num // 100
                if tensunits == 0:
                    num_cy = self.numarray_dep[hundreds-1] + " cant"
                else:
                    num_cy =  self.numarray_dep[hundreds-1] + " cant a " + mutatya.mutate_cy(self.numbercy(tensunits), 3)
            if num == 1000:
                num_cy = "mil"
            if num % 1000 < 200 and(num % 20 == 0 or num % 1000 < 21):
                a = " a "
                mutatst = 3
            else:
                a = ", "
                mutatst = 1

            if num > 1000 and num < 2000:
                num_cy = "mil"+ a+ mutatya.mutate_cy(self.numbercy(num % 1000), mutatst)

            if num > 1999 and num < 21000:
                if num % 1000 == 0:
                    num_cy = self.numbercy(num//1000, dep=True) + " mil"
                else:
                    num_cy = self.numbercy(num//1000, dep=True) + " mil"+a + mutatya.mutate_cy(self.numbercy(num % 1000), mutatst)
            if num > 20999 and num < 200000:
                if num % 1000 == 0:
                    num_cy = self.numbercyDeg(num//1000) + " mil"
                else:
                    num_cy = self.numbercyDeg(num // 1000) + " mil " + self.numbercy(num % 1000)
            if num > 199999 and num < 1000000:
                if num % 100000 == 0:
                    num_cy = self.numarray_dep[(num // 100000)-1] + " can mil"
                if num % 1000 == 0:
                    num_cy = self.numarray_dep[(num // 100000)-1] + " cant "+ self.numbercyDeg((num%100000)//1000) + " mil"
                else:
                    num_cy = self.numarray_dep[(num // 100000)-1] + " cant "+ self.numbercyDeg((num%100000)//1000) + " mil " +  self.numbercy(num % 1000)
            if num == 1000000:
                num_cy = "miliwn"
            if num % 1000000 < 200 and(num % 20 == 0 or num % 1000 < 21):
                a = " a "
                mutatst = 3
            else:
                a = ", "
                mutatst = 1
            if num > 1000000 and num < 2000000:
                num_cy = "miliwn"+ a+ mutatya.mutate_cy(self.numbercy(num % 1000000), mutatst)

            if num > 1999999 and num < 21000000:
                if num % 1000000 == 0:
                    num_cy = self.numbercy(num//1000000, dep=True) + " miliwn"
                else:
                    num_cy = self.numbercy(num//1000000, dep=True) + " miliwn"+a + mutatya.mutate_cy(self.numbercy(num % 1000000), mutatst)
            if num > 20999999 and num < 200000000:
                if num % 1000000 == 0:
                    num_cy = self.numbercyDeg(num//1000000) + " miliwn"
                else:
                    num_cy = self.numbercyDeg(num // 1000000) + " miliwn " + self.numbercy(num % 1000000)
            if num > 199999999 and num < 1000000000:
                if num % 100000000 == 0:
                    num_cy = self.numarray_dep[(num // 100000000)-1] + " can miliwn"
                if num % 1000000 == 0:
                    num_cy = self.numarray_dep[(num // 100000000)-1] + " cant "+ self.numbercyDeg((num%100000000)//1000000) + " miliwn"
                else:
                    num_cy = self.numarray_dep[(num // 100000000)-1] + " cant "+ self.numbercyDeg((num%100000000)//1000000) + " miliwn " +  self.numbercy(num % 1000000)            
                # not yet implemented behaviour for larger numbers
            if num == 1e9:
                num_cy = "biliwn"
            if num > 1e9:
                num_cy = str(num)

        num_cy = self.replaces(num_cy)              
        return num_cy
            

    def numbercyDeg(self, num):
        assert num > 10
        assert num < 200
        if num < 100:
            tens = num // 10
            units = num % 10
            if units == 0:
                num_cy = self.numarray_dep[tens-1] + " deg"
            else:
                num_cy = self.numarray_dep[tens-1] + " deg "+self.numarray[units-1]
        elif num > 100:
            tens = (num-100) // 10
            units = num % 10
            if units == 0:            
                num_cy = "cant " + self.numarray_dep[tens-1] + " deg"
            elif tens == 0:
                num_cy = "cant a "+mutatya.mutate_cy(self.numarray[units-1], 3)
            else:
                num_cy = "cant " + self.numarray_dep[tens-1] + " deg "+self.numarray[units-1]
        else:
            num_cy = "cant"
        return num_cy

    def numbercyUgain(self, num):
        assert num > 10
        assert num < 200
        if num > 10 and num < 15:
            num_cy = self.numarray[num-11] + " ar ddeg"
        if num == 12:
            num_cy = "dauddeg"
        if num == 15:
            num_cy = "pymtheg"
        if num > 15 and num < 20:
            num_cy = self.numarray[num-16] + " ar bymtheg"
        if num == 18:
            num_cy = "deunaw"
        if num == 20:
            num_cy = "ugain"
        if num > 20 and num < 40:
            num_cy = self.numbercy(num-20) + " ar hugain"
        if num == 40:
            num_cy = "deugain"
        if (num > 40 and num < 100) or (num > 119 and num < 200):
            firstpart = num % 20
            secondpart = num // 20
            if firstpart == 0:
                if num == 60:
                    num_cy = "trigain"
                elif num == 120:
                    num_cy = "chweugain"
                else:
                    num_cy = self.numbercy(secondpart, dep=True) + " ugain"
            else:
                if num == 50:
                    num_cy = "hanner cant"
                else:
                    num_cy = self.numbercy(firstpart) + " a "+ mutatya.mutate_cy(self.numbercy(secondpart, dep=True), 3) + " ugain"
        if num == 100:
            num_cy = "cant"
        if num > 100 and num < 120:
            firstpart = num % 20
            secondpart = num // 20
            num_cy = "cant a "+ self.numbercy(num-100)
                    
            num_cy = self.numbercy(firstpart) + " a " + mutatya.mutate_cy(self.numbercy(secondpart, dep=True), 3) + " ugain"

        return num_cy

    def firstpartnouncy(self, num, noun, fem=False):
        assert num < 20
        if num == 0:
            return ""
        if num > 15:
            if num == 18:
                firstpart_cy = "deunaw "+noun
            elif num == 15:
                firstpart_cy = "pymtheg "+noun
            else:    
                firstpart_cy = self.firstpartnouncy(num-15, noun, fem) + " ar bymtheg"
        elif num > 10:
            if num == 12:
                firstpart_cy = "dauddeg "+noun
            else:
                firstpart_cy = self.firstpartnouncy(num-10, noun, fem) + " ar ddeg"
            
        # give number 1-9 or first part of compound
        elif num > 4:
            # direct lookup for numbers up to 10
            if num == 6:
                firstpart_cy = "chwe " + mutatya.mutate_cy(noun, 3)
            else:
                firstpart_cy = self.numarray_dep[num-1] + " " + noun
            
        else:
            # override for numbers 1-4 to handle mutation
            # and feminine forms if 'fem' is True
            # mutation should only happen for 1,3,4 for fem. nouns
            # variable fem keeps track of gender

            if num == 4:
                if fem:
                    firstpart_cy = "pedair " + noun # feminine form
                else:
                    firstpart_cy = "pedwar " + noun
            if num == 3:
                if fem:
                    firstpart_cy = "tair " + noun
                else:
                    firstpart_cy = "tri " + mutatya.mutate_cy(noun, 3)
            if num == 2:
                if fem:
                    firstpart_cy = "dwy " + mutatya.mutate_cy(noun, 2)
                else:
                    firstpart_cy = "dau " + mutatya.mutate_cy(noun, 2)
            if num == 1:
                if fem:
                    firstpart_cy = "un " + mutatya.mutate_cy(noun, 2)
                else:
                    firstpart_cy = "un " + noun
        return firstpart_cy
    
    def numbercy_noun(self, num, noun, fem=False, npl = "au"):
        """ Returns numeral <num> in Welsh compounded with <noun>

        <fem> is a boolean variable specifying whether the noun is feminine
        <npl> is the plural of <noun>. if it isn't specified default to
        <noun>+'ow'
        """
        # default plural suffix -ow
        if npl == "au":
            npl = noun+npl
        if not(isinstance(num,int)):
            print("num is not an integer. attempting conversion...")
            num = int(num)
            if num < 0:
                print("num is negative, multiplying by -1")
                num = num * -1
            print("num={n}".format(n=num))

        if num == 0:
            num_cy = "dim o {n}".format(n=mutatya.mutate_cy(npl, 2))
        elif num > self.maxTrad or num > 49:
            num_cy = self.numbercy(num) + " o {n}".format(n=mutatya.mutate_cy(npl, 2))
        elif num > 0 and num < 20:
            num_cy = self.firstpartnouncy(num, noun, fem)
        elif num == 20:
            num_cy = "ugain " + noun
        elif num > 20 and num < 40:
            num_cy = self.firstpartnouncy(num-20, noun, fem) + " ar hugain"
        elif num == 40:
            num_cy = "deugain " + noun
        elif num > 40:
            num_cy = self.firstpartnouncy(num-40, noun, fem) + " a deugain"
        num_cy = self.replaces(num_cy)              
        return num_cy

    def numbercy_float(self, num):
        if num < 0.0:
            return "minws " + self.numbercy_float(-1*num)
        num_cy = self.numbercy(int(num))
        if num == int(num) or num == 0:
            return num_cy
        else:
            decdigits = str(num).split(".")[1]
            num_cy = num_cy + " pwynt "
            for d in decdigits:
                num_cy = num_cy + self.numbercy(int(d)) + ", "
            if num_cy[-2:] == ", ":
                num_cy = num_cy[:-2]
            return num_cy            
        
    def numbercy_float_noun(self, num, noun, fem=False, npl = "au"):
        if num == int(abs(num)):
            return self.numbercy_noun(num,noun,fem,npl)
        else:
            num_cy = self.numbercy_float(num)
            num_cy += " o "
            # default plural suffix -ow
            if npl == "au":
                npl = noun+npl
            num_cy += mutatya.mutate_cy(npl,2)
            return num_cy
        
def interactiveTest():
    if sys.version_info[0] < 3:
        number = raw_input("Enter number as integer:")
    else:
        number = input("Enter number as integer:")
    try:
        number_int = int(number)
    except:
        return None
    if sys.version_info[0] < 3:
        noun = raw_input("Enter noun:")
    else:
        noun = input("Enter noun:")
    if noun == '':
        print(numberkw(number_int))
    else:
        if sys.version_info[0] < 3:
            isfem = raw_input("type 'f' if the noun is feminine:")
        else:
            isfem = input("type 'f' if the noun is feminine:")
        if isfem.lower() == 'f':
            fem = True
        else:
            fem = False
        if number_int > 220:
            if sys.version_info[0] < 3:
                npl = raw_input("What is the plural of the noun?")
            else:
                npl = input("What is the plural of the noun?")
            if npl == "":
                npl = "ow"
        else:
            # this won't be used for num < 221
            npl = "ow"
        print(numberkw_noun(number_int,noun,fem,npl))
    if sys.version_info[0] < 3:
        num2 = raw_input("Enter floating point number:")
    else:
        num2 = input("Enter floating point number:")
    num2 = float(num2)
    print(numberkw_float(num2))
    
def basicTests():
    underline = "-"*50
    ki = "ki"
    ki_f = False
    ki_pl = "keun"
    for n in range(10):
        print ("{n:4d}: {k:s}".format(n=n+1,k=numberkw_noun(n+1,ki)))
    for n in range(12,132,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,ki)))
    for n in range(13,133,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,ki)))
    print(underline)
    kath = "kath"
    kath_f = True
    kath_pl = "kathes"
    for n in range(10):
        print ("{n:4d}: {k:s}".format(n=n+1,k=numberkw_noun(n+1,kath,kath_f,kath_pl)))
    for n in range(12,162,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,kath,kath_f,kath_pl)))
    for n in range(13,163,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,kath,kath_f,kath_pl)))
    print(underline)
    testns = [50,121,200, 216, 234, 275, 300, 360, 421, 1000, 1109, 1300, 1777, 1880, 2015, 2364, 7700, 16754, 20000, 36000, 60000, 70000, 70001, 567576,1000000,1000004,2000001,2000123,8000000,60000000,60000003, 60437464,378675476,9000000001,9000000017,9001000007]
    for n in testns:
        print ("{n:15d}: {k:s}".format(n=n,k=numberkw_noun(n,kath,kath_f,kath_pl)))
    print(underline)
    for n in testns:
        print ("{n:15d}: {k:s}".format(n=n,k=numberkw_noun(n,ki,ki_f,ki_pl)))
    print(underline)

def cymraegTests():
    cyN = NiferCymraeg()
    testNums = [1,3,7,11,15, 17, 18, 25, 36, 50,
                51, 72, 100, 105, 140, 147, 200, 217,
                232, 500, 1000, 4000, 5674, 14562,
                27865, 79562, 105689, 170000, 1000000,
                1000001, 7000000, 756345234, 100000000, 2345565785]
    print("Prawfau Niferau Cymraeg")
    for t in testNums:
        print("{n}: {c}".format(n=t, c=cyN.numbercy(t)))
    print("setting MaxTrad = 10")
    cyN.setMaxTrad(10)
    for t in testNums:
        print("{n}: {c}".format(n=t, c=cyN.numbercy(t)))
    print("setting MaxTrad = 200")
    cyN.setMaxTrad(200)
    for t in testNums:
        print("{n}: {c}".format(n=t, c=cyN.numbercy(t)))
    print("setting MaxTrad = 50")
    cyN.setMaxTrad(50)
    for t in testNums[:20]:
        print("{n}: {c}".format(n=t, c=cyN.numbercy_noun(t, "cath", True, "cathod")))
    print("setting MaxTrad = 10")
    cyN.setMaxTrad(10)
    for t in testNums[:20]:
        print("{n}: {c}".format(n=t, c=cyN.numbercy_noun(t, "cath", True, "cathod")))    
if __name__ == "__main__":
    basicTests()
    print()
    interactiveTest()
    cymraegTests()
