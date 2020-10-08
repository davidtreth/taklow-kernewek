// porting niverow.py to Javascript
// David Trethewey October 2020

var numarray = ["onan","dew","tri","peswar","pymp",
            "hwegh","seyth","eth","naw","deg",
            "unnek","dewdhek","trydhek","peswardhek","pymthek",
            "hwetek","seytek","etek","nownsek","ugens"];
var numarray_ord = ["kynsa", "nessa", "tressa", "peswora", "pympes",
                "hweghves", "seythves", "ethves", "nawves", "degves",
                "unnegves", "dewdhegves", "trydhegves", "peswardhegves",
                "pymthegves", "hwetegves", "seytegves", "etegves",
                "nownsegves", "ugensves"];

function numberkw(num) {
    /* return the Cornish for the numeral <num> without a noun */
    num = parseInt(num);
    var num_k = "";
    var firstpart = 0;
    var secondpart = 0;
    if (num === 0) {
        num_k = "mann";
    }
    if ((num > 0)&&(num < 21)) {
        num_k = numarray[num-1];
    }
    if ((num > 20)&&(num < 40)) {
        num_k = numarray[num-21] + " warn ugens";
    }

    if (((num > 39)&&(num < 100))||((num > 119)&&(num < 200))) {
        firstpart = num % 20;
        secondpart = Math.floor(num / 20);
        num_k = numarray[firstpart-1] +" ha " + numarray[secondpart-1] + " ugens";
        if (firstpart === 0) {
            num_k = numarray[secondpart-1] + " ugens";
        }
        if (num == 50) {
            num_k = "hanterkans";
        }
    }
    if (num === 100) {
        num_k = "kans";
    }
    if ((num > 100)&&(num < 120)) {
        num_k = "kans ha "+ numberkw(num-100);
    }
    if ((num > 199)&&(num < 1000)) {        
        var kansow = Math.floor(num / 100);
        if ((num % 100 < 21)||(num % 20 === 0)||(num % 100 === 50)) {
            if (num % 100 === 0) {
                num_k = numarray[kansow-1] + " kans";
            }
            else {
                num_k = numarray[kansow-1] + " kans ha " + numberkw(num % 100);
            }
        }
        else {
            num_k = numarray[kansow-1] + " kans, " + numberkw(num % 100);
        }
    }
    var ha = "";
    if ((num % 1000 < 200)&&((num % 20 === 0)||(num % 1000 < 21))) {
        ha = " ha ";
    }
    else {
        ha = ", ";
    }
    if (num === 1000) {
        num_k = "mil";
    }
    if ((num > 1000)&&(num < 2000)) {
        num_k = "mil"+ ha+ numberkw(num % 1000);
    }
    if ((num > 1999)&&(num < 21000)) {
        if (num % 1000 === 0) {
            num_k = numberkw(Math.floor(num/1000)) + " mil";
        }
        else {
            num_k = numberkw(Math.floor(num/1000)) + " mil"+ha + numberkw(num % 1000);
        }
    }
    if ((num > 20999) && (num < 40000)) {
        if (num % 1000 === 0) {
            num_k = numberkw(Math.floor((num % 20000)/1000)) + " mil warn ugens";
        }
        else {            
            num_k = numberkw(Math.floor((num % 20000)/1000)) + " mil warn ugens"+ha+ numberkw(num % 1000);
        }
    }
    if (((num > 39999) && (num<100000)) || ((num % 20000 ===0)&&(num>39999)&&(num<200000))) {
        if (num === 100000) {
            num_k = "kans mil";        
        }
        else if (num % 20000 === 0) {
            num_k = numberkw(Math.floor(num/20000)) + " ugens mil";
        }
        else if (num % 1000 === 0) {
            num_k = numberkw(Math.floor((num % 20000)/1000)) + " mil ha "+ numberkw(Math.floor(num/20000)) + " ugens";
        }
        else {
            num_k = numberkw(Math.floor((num % 20000)/1000)) + " mil ha "+ numberkw(Math.floor(num/20000)) + " ugens" +ha+ numberkw(num % 1000);
        }
    }
    else if ((num > 99999)&&(num < 1000000)) {

        if (num < 200000) {
            num_k = "kans ha "+ numberkw(Math.floor((num-100000)/1000)) + " a vilyow" +ha + numberkw(num % 1000);
            if (num % 1000 == 0) {
                num_k = "kans ha "+ numberkw(Math.floor((num-100000)/1000)) + " a vilyow";
            }
        }
        if (num % 100000 === 0) {
            num_k = numberkw(Math.floor(num/100000)) + " kans mil";
        }
        else {
            if ((num % 20000 === 0)&&(num < 200000)) {
                num_k = numberkw(Math.floor(num/20000)) + " ugens mil"
            }
            else {                
                if (num % 1000 === 0) {
                    num_k = numberkw(Math.floor(num/1000)) + " a vilyow";
                }       
                else {
                    num_k = numberkw(Math.floor(num/1000)) + " a vilyow" + ha + numberkw(num % 1000);
                }         
            }
        }
    }
    
    if ((num > 999999)&&(num < 2000000)) {
        if (num === 1000000) {
            num_k = "milvil";
        }
        else {
            if (((num % 1000000 < 200)&&(num % 20 === 0))||(num % 1000000 < 20)||((num % 1000000 < 1000)&&(num % 100 === 0))) {            
                num_k = "milvil ha " + numberkw(num-1000000);
            }
            else {
                num_k = "milvil, " + numberkw(num-1000000);
            }
        }
    }
    if ((num > 1999999)&&(num < 20000001)) {
        if (num % 1000000 === 0) {
            num_k = numberkw(num/1000000) + " milvil";
        }
        else {
            if (((num % 1000000 < 200)&&(num % 20 === 0))||(num % 1000000 < 20)||((num % 1000000 < 1000)&&(num % 100 === 0))) {
                num_k = numberkw(Math.floor(num/1000000)) + " milvil ha " + numberkw(num % 1000000);
            }
            else {
                num_k = numberkw(Math.floor(num/1000000)) + " milvil, " + numberkw(num % 1000000);
            }
        }
    }
    if ((num > 20000000) && (num < 1000000000)) {
        if ((num % 20000000 === 0) && (num < 200000000)) {
            num_k = numberkw(num / 1000000) + " milvil";
        }
        else {
            if (num % 1000000 === 0) {
                num_k = numberkw(num/1000000) + " a vilvilyow"
            }
            else {
                if (((num % 1000000 < 200)&&(num % 20 === 0))||(num % 1000000 < 20)||((num % 1000000 < 1000)&&(num % 100 === 0))) {
                    num_k = numberkw(Math.floor(num/1000000)) + " a vilvilyow ha " + numberkw(num % 1000000);
                }
                else {
                    num_k = numberkw(Math.floor(num/1000000)) + " a vilvilyow, " + numberkw(num % 1000000);
                    }
                }
            }
    }
    if ((num > 999999999) && (num < 2000000000)) {
        if (num === 1000000000) {
            num_k = "bilvil";
        }
        else {
            if (((num % 1000000000 < 200)&&(num % 20 === 0))||(num % 1000000000 < 20)||((num % 1000000000 < 1000)&&(num % 100 === 0))) {        
                num_k = "bilvil ha" + numberkw(num-1000000000);
            }
            else {
                num_k = "bilvil, " + numberkw(num-1000000000);
            }
            }
    }
    if ((num > 1999999999) && (num < 20000000001)) {
        if (num % 1000000000 === 0) {
            num_k = numberkw(Math.floor(num / 1000000000)) + " bilvil";
        }
        else {
            if (((num % 1000000000 < 200)&&(num % 20 === 0))||(num % 1000000000 < 20)||((num % 1000000000 < 1000)&&(num % 100 === 0))) {
                num_k = numberkw(Math.floor(num/1000000000)) + " bilvil ha " + numberkw(num % 1000000000);
            }
            else {
                num_k = numberkw(Math.floor(num/1000000000)) + " bilvil, " + numberkw(num % 1000000000);
            }
        }
    }
    if (num > 2e10) {
        if (num % 1000000000 === 0) {
            num_k = numberkw(Math.floor(num/1000000000)) + " a bilvilyow";
        }
        else {
        num_k = numberkw(Math.floor(num/1000000000)) + " a bilvilyow, " + numberkw(num % 1000000000);
    }
    }
    num_k = num_k.replace("  "," ");
    num_k = num_k.replace("ha u","hag u");
    num_k = num_k.replace("ha e","hag e");
    num_k = num_k.replace("ha o","hag o");
    num_k = num_k.replace("tri kans","tri hans");
    num_k = num_k.replace("deg ha dew ugens","hanterkans");
    num_k = num_k.replace("dew mil", "dew vil");

    return num_k;    
}
function unnnoun(noun, fem=false) {
    var mstate = 1;
    if (fem) {
        mstate = 2;
    }
    return "unn "+mutate(noun,mstate);
}

function dewnoun(noun, fem=false) {
    if (fem) {
        return "diw " + mutate(noun,2);  // feminine form
    }
    else {
        return "dew " + mutate(noun,2);
    }
}
    
function trinoun(noun, fem=false) {
    if (fem) {
        return "teyr " + mutate(noun,3); // feminine form
    }
    else {
        return "tri " + mutate(noun,3);
    }
}

function firstpartnoun(num, noun, fem=false) {
    if (num === 0) {
        return "";
    }
    // give number 1-19 or first part of compound
    var firstpart_k = "";
    if ((num > 4)||((num === 4)&&(!(fem)))) {
        // direct lookup for numbers up to 20
        firstpart_k = numarray[num-1] + " " + noun;        
    }
    else {
        /* override for numbers 1-4 to handle mutation
         and feminine forms if 'fem' is true
         mutation should only happen for 1 for fem. nouns
         mutation for both masc. and fem. for 2, 3
         and use of feminine forms for 2, 3, 4 for fem. nouns
         variable fem keeps track of gender */
        if ((num === 4)&&(fem)) {
            firstpart_k = "peder " + noun; // feminine form            
            }            
        if (num === 3) {
            firstpart_k = trinoun(noun,fem);
        }
        if (num === 2) {
            firstpart_k = dewnoun(noun, fem);
        }
        if (num === 1) {
            firstpart_k = unnnoun(noun,fem);
        }        
    }
    return firstpart_k;
}
            

function numberkw_noun(num, noun, fem=false, npl = "ow") {
    /* Returns numeral <num> in Cornish compounded with <noun>

    <fem> is a boolean variable specifying whether the noun is feminine
    <npl> is the plural of <noun>. if it isn't specified default to
    <noun>+'ow'
    */
    var num_k = "";
    var n = "";
    var firstpart = 0;
    var secondpart = 0;
    var ha = "";
    var kansow = 0;
    
    // default plural suffix -ow
    if (npl === "ow") {
        npl = noun+npl;
    }
    if (num === 0) {
        n = mutate(npl,2);
        num_k = `zero a ${n}`;
        return num_k;
    }    
    else if (num !== parseInt(num)) {
        console.log("num is not an integer. attempting conversion...");
        num = parseInt(num);
        if (num < 0) {
            console.log("num is negative, multiplying by -1");
            num = num * -1;
        }        
        console.log(`num=${num}`);
    }
        
    if ((num > 0) && (num < 21)) {
        num_k = firstpartnoun(num, noun, fem);
    }
        
    if ((num > 20) && (num < 40)) {
        // numbers 21 to 39
        num_k = firstpartnoun(num-20,noun,fem) + " warn ugens";
    }
                
    if (((num > 39) && (num < 100))||((num > 119) && num < 200)) {
        // numbers 40 to 199 excluding 100-119
        firstpart = num % 20;
        secondpart = Math.floor(num / 20);
        if (firstpart === 0) {
            num_k = numarray[secondpart-1] + " ugens " + noun;
        }
        else {
            num_k = firstpartnoun(firstpart,noun,fem) + " ha " + numarray[secondpart-1] + " ugens";
        }
        if (num === 50) {
            // override for num=50
            num_k = "hanterkans " + noun;
        }
    }
    if (num === 100) {
        num_k = "kans " + noun;
    }
    if ((num > 100) && (num < 120)) {
        num_k = "kans "+noun+" ha "+numarray[num-101];
    }
    if ((num > 199) && (num < 1000)) {
        ha = " ha ";
        kansow = Math.floor(num / 100);
        if (num % 100 === 0) {
            num_k = numarray[kansow-1] + " kans " + noun;
        }
        else { 
            if ((num % 100 < 21) || (num % 20 === 0)) {
                num_k = numarray[kansow-1] + " kans "+ noun + ha + numberkw(num % 100);
            }
            else {
                num_k = numberkw(num) + " a " + mutate(npl,2);
            }
        }
    }
    if ((num > 999) && (num < 21000)) {
        if (num === 1000) {
            num_k = "mil "+ mutate(noun,2);
        }
        else {
            if (num % 1000 === 0) {
                num_k = numberkw(1000 * Math.floor(num/1000)) + " " + mutate(noun,2);
            }
            else {
                if ((num % 1000 < 21) || ((num % 1000 < 200) && (num % 20 === 0)) || (num % 100 === 0)) {
                    num_k = numberkw(1000*Math.floor(num/1000)) + " " + mutate(noun,2) + " ha " + numberkw(num % 1000);
                }
                else {
                    num_k = numberkw(num) + " a " + mutate(npl,2);
                }
                }
        }
    }
    if ((num > 20999) && (num < 40000)) {
        num_k = numberkw(num) + " a " + mutate(npl,2);
        }
    if (((num > 39999) && (num < 100000))||((num % 20000 === 0) && (num <200000))) {
        num_k = numberkw(num) + " a " + mutate(npl,2);
        if (num % 20000 === 0) {
            num_k = numberkw(Math.floor(num/20000)) + " ugens mil " + mutate(noun,2);
        }
    }
    else if ((num > 99999) && (num < 1000000)) {
        num_k = numberkw(num) +" a " + mutate(npl,2)
        if (num % 100000 === 0) {
            num_k = numberkw(Math.floor(num/100000)) + " kans mil " + mutate(noun,2);
        }
        if (num === 100000) {
            num_k = "kans mil "+ mutate(noun,2);
        }
    }
    if ((num > 999999) && (num < 2000000)) {
        if (num === 1000000) {
            num_k = "milvil " + mutate(noun,2);
        }
        else {
            num_k = numberkw(num) +  " a " + mutate(npl,2);
        }
    }
    if ((num > 1999999) && (num < 20000001)) {
        if (num % 1000000 === 0) {
            num_k = numberkw(Math.floor(num / 1000000)) + " milvil " + mutate(noun,2);
            return num_k;
        }
        else {
            num_k = numberkw(num) +  " a " + mutate(npl,2);
        }
    }

    if ((num > 20000000) && (num < 1000000000)) {
        if ((num % 20000000 === 0) && (num < 200000000)) {
            num_k = numberkw(Math.floor(num/1000000)) + " milvil " + mutate(noun,2);
        }
        else {
            num_k = numberkw(num) +  " a " + mutate(npl,2);
        }
    }
    if ((num > 999999999) && (num < 2000000000)) {
        num_k = numberkw(num) +  " a " + mutate(npl,2);
    }
    if ((num > 1999999999) && (num < 20000000001)) {
        num_k = numberkw(num) +  " a " + mutate(npl,2);
    }
    if (num > 2e10) {
        num_k = numberkw(num) +  " a " + mutate(npl,2);
    }

    num_k = num_k.replace("  "," ");
    num_k = num_k.replace("ha u","hag u");
    num_k = num_k.replace("ha e","hag e");
    num_k = num_k.replace("ha o","hag o");
    num_k = num_k.replace("tri kans","tri hans");
    num_k = num_k.replace("deg ha dew ugens","hanterkans");

    // return the result
    return num_k;    
}

function jsniverkw() {
  var inp, outp, inpint;
  // get value of text input
  inp = document.getElementById("kwtekstniver").value;
  if (inp === "") {
    outp = "An kyst yw gwag. Res yw dhywgh gorra niver";
    }
    else {
        if (inp === "0") {
         outp = numberkw_float(0);
        }    
        else if (inp) {
        inp = Number(inp);
        outp = numberkw_float(inp);
        }
        else {
        outp = "Nyns yw hemma niver. Res yw dhywgh gorra niver yn niverennow";
        }   
    }
document.getElementById("niver").innerHTML = outp;  
}

function klerhe(form, output) {
    /* first argument is the id of a form to be reset
     * second is id of HTML element of the output */
    document.getElementById(form).reset();
    document.getElementById(output).innerHTML = "";
}

    
function numberkw_float(num) {
    if (num < 0.0) {
        return "minus " + numberkw_float(-1*num);
    }
    var num_k;
    if (num === 0) {
        num_k = numberkw(num);
        return num_k;
    }
    else if (num === parseInt(num)) {
        num_k = numberkw(parseInt(num));
        return num_k;
    }
    else {
        num_k = numberkw(parseInt(num));        
        var decdigits = num.toString().split(".")[1];
        num_k = num_k + " poynt ";
        var d;
        for (d of decdigits) {
            num_k = num_k + numberkw(parseInt(d)) + ", ";
        }
        if (num_k.slice(-2) === ", ") {
            num_k = num_k.slice(0,-2);
        }
        return num_k;
    }
}
        
function numberkw_float_noun(num, noun, fem=false, npl = "ow") {
    if (num === parseInt(Math.abs(num))) {
        return numberkw_noun(num,noun,fem,npl);
    }
    else {
        num_k = numberkw_float(num);
        num_k += " a ";
        // default plural suffix -ow
        if (npl === "ow") {
            npl = noun+npl;
        }
        num_k += mutate(npl,2);
        return num_k;
    }
}
function jsnivernounkw() {
  var inp, inpn, inppln, outp, inpint;
  // get value of text input
  inp = document.getElementById("kwtekstnivern").value;
  inpn = document.getElementById("kwtekstnivernoun").value;
  inppln = document.getElementById("kwtekstniverpluralnoun").value;
  var fem = document.getElementById("femnoun").checked;
  
  if (inp === "") {
    outp = "An kyst yw gwag. Res yw dhywgh gorra niver";
    }
    else {
        if (inpn === "") {
            inpn = "[n]";
        }
        if (inppln === ""){
           // default plural suffix -ow
           inppln = "ow"; 
        }
        if (inp === "0") {
         outp = numberkw_float_noun(0, inpn, fem, inppln);
        }    
        else if (inp) {
        inp = Number(inp);
        outp = numberkw_float_noun(inp, inpn, fem, inppln);
        }
        else {
        outp = "Nyns yw hemma niver. Res yw dhywgh gorra niver yn niverennow";
        }   
    }
document.getElementById("nivernoun").innerHTML = outp;  
}
/*
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
*/
