# coding=utf-8
# David Trethewey 26-08-2015
import sys
import string

import mutatya

numarray = ["onan","dew","tri","peswar","pymp",
            "hwegh","seyth","eth","naw","deg",
            "unnek","dewdhek","trydhek","peswardhek","pymthek",
            "hwetek","seytek","etek","nownsek","ugens"]

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
        return "tri " + mutatya.mutate(noun, 3)

def firstpartnoun(num, noun, fem=False):
    # give number 1-19 or first part of compound
    if num > 4:
        # direct lookup for numbers up to 20
        firstpart_k = numarray[num-1] + " " + noun
        return firstpart_k
    else:
        # override for numbers 1-4 to handle mutation
        # and feminine forms if 'fem' is True
        # mutation should only happen for 1,3,4 for fem. nouns
        # variable fem keeps track of gender
        if num == 4:
            if fem:
                firstpart_k = "peder " + noun #feminine form
            else:
                firstpart_k = firstpart_k = numarray[num-1] + " " + noun
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
    if not(isinstance(num,int)):
        print("num is not an integer. attempting conversion...")
        num = int(num)
        if num < 0:
            print("num is negative, multiplying by -1")
            num = num * -1
        print("num={n}".format(n=num))
        
    if num == 0:
        # returns empty string
        # could do '<noun> vyth' perhaps?
        # but would need to handle recursive call
        # differently from call from top-level 
        num_k = ""
    if num >0 and num < 21:     
        num_k = firstpartnoun(num, noun, fem)
        
    if num>20 and num<40:
        # numbers 21 to 39
        num_k = firstpartnoun(num-20,noun,fem) + " warn ugens"
            
    if (num>39 and num<100)or(num>119 and num<200):
        # numbers 40 to 199 excluding 100-119
        firstpart = num % 20
        secondpart = num / 20
        num_k = firstpartnoun(firstpart,noun,fem) + " ha " + numarray[secondpart-1] + " ugens"
        if num == 50:
            # override for num=50
            num_k = "hanterkans " + noun
            
    if num==100:
        num_k = "kans " + noun
        
    if num>100 and num < 120:
        num_k = "kans "+noun+" ha "+numarray[num-101]

    if num>199 and num<1000:
        ha = "ha "
        kansow = num / 100
        if num % 100 == 0:
            num_k = numarray[kansow-1] + " kans " + noun
        else:
            num_k = numarray[kansow-1] + " kans "+ha + numberkw_noun(num % 100,noun)
        if kansow == 3:
            if num == 300:
                num_k = "tri hans " + noun
            else:
                num_k = "tri hans "+ha + numberkw_noun(num % 100,noun)
                
    if num==1000:
       num_k = "mil "+ mutatya.mutate(noun,2)
       
    if num>1000 and num < 2000:
        num_k = "mil ha "+ numberkw_noun(num % 1000,noun)
        
    if num>1999 and num<21000:
        if (num % 1000 > 0)and(num % 1000 < 100)and(((num % 1000) % 20 ==0)or(num % 1000 < 20)):
            ha = "ha "
        else:
            ha = ""
        if num % 1000 == 0:
            num_k = numberkw(num/1000) + " mil " + numberkw_noun(num % 1000,noun)
        else:
            if (num/1000)==2:
                num_k = "dew vil "+ha+ numberkw_noun(num % 1000,noun)
            else:
                num_k = numberkw(num/1000) + " mil "+ha + numberkw_noun(num % 1000,noun)
                
    if num>20999 and num<40000:
        num_k = numberkw((num % 20000)/1000)+" warn ugens a vilyow ha " + numberkw(num % 1000) + " a " + mutatya.mutate(noun,2)+npl
        if num % 1000 == 0:
            num_k = numberkw((num % 20000)/1000)+" warn ugens a vilyow a " + mutatya.mutate(noun,2)+npl
            
    if num>39999 and num<100000:
        num_k = numberkw((num % 20000)/1000) +  " ha " + numberkw(num/20000) + " ugens a vilyow ha " + numberkw(num % 1000) + " a " + mutatya.mutate(noun,2)+npl
        if num % 1000 == 0:
            num_k = numberkw((num % 20000)/1000) +  " ha " + numberkw(num/20000) + " ugens a vilyow a " + mutatya.mutate(noun,2)+npl

    if num>99999 and num<1000000:
        num_k = numberkw(num/1000) + " a vilyow ha " + numberkw(num % 1000) +" a " + mutatya.mutate(noun,2) + npl
        if (num % 1000) == 0:
            num_k = numberkw(num/1000) + " a vilyow a " + mutatya.mutate(noun,2) + npl
        if num < 200000:
            num_k = "kans ha "+ numberkw((num-100000)/1000) + " a vilyow ha " + numberkw(num % 1000) + " a " + mutatya.mutate(noun,2) + npl
            if (num % 1000) == 0:
                num_k = "kans ha "+ numberkw((num-100000)/1000) + " a vilyow a " + mutatya.mutate(noun,2) + npl
        if (num % 100000) == 0:
            num_k = numberkw(num/100000) + " kans mil " + mutatya.mutate(noun,2)
        if num == 100000:
            num_k = "kans mil "+ mutatya.mutate(noun,2)
    if num>999999 and num<2000000:
        if (num % 1000000 < 100)and(((num % 1000000)%20 ==0)or(num % 1000000 < 20)):
            num_k = "milvil ha " + numberkw(num-1000000) + " a " + mutatya.mutate(noun,2) + npl
        else:
            num_k = "milvil " + numberkw(num-1000000) + " a " + mutatya.mutate(noun,2) + npl 
    if num>1999999 and num<20000001:
        if (num % 1000000 < 100)and(((num % 1000000)%20 ==0)or(num % 1000000 < 20)):
            num_k = numberkw(num/1000000) + " milvil ha " + numberkw(num % 1000000) + " a " + mutatya.mutate(noun,2) + npl
        else:
            num_k = numberkw(num/1000000) + " milvil " + numberkw(num % 1000000) + " a " + mutatya.mutate(noun,2) + npl
    if num>20000000 and num<1000000000:
        if (num % 1000000 < 100)and(((num % 1000000)%20 ==0)or(num % 1000000 < 20)):
            num_k = numberkw(num/1000000) + " a vilvilyow ha " + numberkw(num % 1000000) + " a " + mutatya.mutate(noun,2) + npl
        else:
            num_k = numberkw(num/1000000) + " a vilvilyow " + numberkw(num % 1000000) + " a " + mutatya.mutate(noun,2) + npl
    if num>999999999 and num<2000000000:
        if (num % 1000000000 < 100)and(((num % 1000000000)%20 ==0)or(num % 1000000000 < 20)):
            num_k = "bilvil ha " + numberkw(num-1000000000) + " a " + mutatya.mutate(noun,2) + npl
        else:
            num_k = "bilvil " + numberkw(num-1000000000) + " a " + mutatya.mutate(noun,2) + npl
            
    if num>1999999999 and num<20000000001:
        if (num % 1000000000 < 100)and(((num % 1000000000)%20 ==0)or(num % 1000000000 < 20)):
            num_k = numberkw(num/1000000000) + " bilvil ha " + numberkw(num % 1000000000) + " a " + mutatya.mutate(noun,2) + npl
        else:
            num_k = numberkw(num/1000000000) + " bilvil " + numberkw(num % 1000000000) + " a " + mutatya.mutate(noun,2) + npl
    #if num>2e10 and num < 1e12:
    if num>2e10:
        num_k = numberkw(num/1000000000) + " a bilvilyow " + numberkw(num % 1000000000) + " a " + mutatya.mutate(noun,2) + npl # I have missed the mutation to distinguish milvil from bilvil
    num_k = num_k.replace("  "," ")
    num_k = num_k.replace("ha u","hag u")
    num_k = num_k.replace("ha e","hag e")
    num_k = num_k.replace("ha o","hag o")
    num_k = num_k.replace("tri kans","tri hans")
    num_k = num_k.replace("deg ha dew ugens","hanterkans")

    return num_k    

def numberkw(num):
    if num == 0:
        num_k = ""
    if num >0 and num < 21:
        num_k = numarray[num-1]
    if num>20 and num<40:
        num_k = numarray[num-21] + " warn ugens"

    if (num>39 and num<100)or(num>119 and num<200):
        firstpart = num % 20
        secondpart = num / 20

        num_k = numarray[firstpart-1] +" ha " + numarray[secondpart-1] + " ugens"
        if firstpart == 0:
            num_k = numarray[secondpart-1] + " ugens"
        if num == 50:
            num_k = "hanterkans"
    if num==100:
        num_k = "kans"
    if num>100 and num < 120:
        num_k = "kans ha "+numarray[num-101]
    if num>199 and num<1000:
        kansow = num / 100
        num_k = numarray[kansow-1] + " kans " + numberkw(num % 100)
        if kansow == 3:
            num_k = "tri hans " + numberkw(num % 100)

    if num>999 and num < 2000:
        num_k = "mil ha "+ numberkw(num % 1000)
    if num>1999 and num<21000:
        if (num % 1000 > 0)and(num % 1000 < 100)and(((num % 1000) % 20 ==0)or(num % 1000 < 20)):
            ha = "ha "
        else:
            ha = ""
        num_k = numberkw(num/1000) + " mil "+ha + numberkw(num % 1000)
    if num>20999 and num<40000:
        num_k = numberkw((num % 20000)/1000) + " warn ugens a vilyow ha" + numberkw(num % 1000)
    if num>39999 and num<100000:
        num_k = numberkw((num % 20000)/1000) +  " ha " + numberkw(num/20000) + " ugens a vilyow ha " + numberkw(num % 1000)
    if num>99999 and num<1000000:
        num_k = numberkw(num/1000) + " a vilyow ha " + numberkw(num % 1000)
        if (num % 1000) == 0:
            num_k = numberkw(num/1000) + " a vilyow"
        if num < 200000:
            num_k = "kans ha "+ numberkw((num-100000)/1000) + " a vilyow ha " + numberkw(num % 1000)
            if (num % 1000) == 0:
                num_k = "kans ha "+ numberkw((num-100000)/1000) + " a vilyow"
        if (num % 100000) == 0:
            num_k = numberkw(num/100000) + " kans mil"
        if num == 100000:
            num_k = "kans mil"
    if num>999999 and num<2000000:
        if (num % 1000000 < 100)and(((num % 1000000)%20 ==0)or(num % 1000000 < 20)):            
            num_k = "milvil ha " + numberkw(num-1000000)
        else:
            num_k = "milvil " + numberkw(num-1000000)
    if num>1999999 and num<20000001:
        if (num % 1000000 < 100)and(((num % 1000000)%20 ==0)or(num % 1000000 < 20)):
            num_k = numberkw(num/1000000) + " milvil ha " + numberkw(num % 1000000)
        else:
            num_k = numberkw(num/1000000) + " milvil " + numberkw(num % 1000000)
    if num>20000000 and num<1000000000:
        if (num % 1000000 < 100)and(((num % 1000000)%20 ==0)or(num % 1000000 < 20)):
            num_k = numberkw(num/1000000) + " a vilvilyow ha " + numberkw(num % 1000000)
        else:
            num_k = numberkw(num/1000000) + " a vilvilyow " + numberkw(num % 1000000)
    if num>999999999 and num<2000000000:
        if (num % 1000000000 < 100)and(((num % 1000000000)%20 ==0)or(num % 1000000000 < 20)):        
            num_k = "bilvil ha" + numberkw(num-1000000000)
        else:
            num_k = "bilvil " + numberkw(num-1000000000)
    if num>1999999999 and num<20000000001:
        if (num % 1000000000 < 100)and(((num % 1000000000)%20 ==0)or(num % 1000000000 < 20)):
            num_k = numberkw(num/1000000000) + " bilvil ha " + numberkw(num % 1000000000)
        else:
            num_k = numberkw(num/1000000000) + " bilvil " + numberkw(num % 1000000000)
#    if num>2e10 and num < 1e12:
    if num>2e10:
        num_k = numberkw(num/1000000000) + " a bilvilyow " + numberkw(num % 1000000000)
    
    num_k = num_k.replace("  "," ")
    num_k = num_k.replace("ha u","hag u")
    num_k = num_k.replace("ha e","hag e")
    num_k = num_k.replace("ha o","hag o")
    num_k = num_k.replace("tri kans","tri hans")
    num_k = num_k.replace("deg ha dew ugens","hanterkans")

    return num_k    
    


def interactiveTest():
    number = raw_input("Enter number as integer:")
    number_int = int(number)
    noun = raw_input("Enter noun:")        
    if noun == '':
        print(numberkw(number_int))
    else:
        isfem = raw_input("type 'f' if the noun is feminine:")
        if isfem.lower() == 'f':
            fem = True
    print numberkw_noun(number_int,noun,fem)
    
def basicTests():
    underline = "-"*50
    ki = "ki"
    for n in range(10):
        print ("{n:4d}: {k:s}".format(n=n+1,k=numberkw_noun(n+1,ki)))
    for n in range(12,132,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,ki)))
    for n in range(13,133,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,ki)))
    print(underline)
    kath = "kath"
    kath_f = True
    for n in range(10):
        print ("{n:4d}: {k:s}".format(n=n+1,k=numberkw_noun(n+1,kath,kath_f,"es")))
    for n in range(12,132,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,kath,kath_f,"es")))
    for n in range(13,133,10):
        print ("{n:4d}: {k:s}".format(n=n,k=numberkw_noun(n,kath,kath_f,"es")))
    testns = [50,200, 275, 300, 337, 1000, 1777, 2015, 2364, 5676, 16754, 70001, 567576,1000004,2000001,2000123,60000003, 60437464,378675476,9000000001,9000000017,9001000007]
    for n in testns:
        print ("{n:15d}: {k:s}".format(n=n,k=numberkw_noun(n,kath,kath_f,"es")))
if __name__ == "__main__":
    basicTests()
    #interactiveTest()
