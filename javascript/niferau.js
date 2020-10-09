// porting niverow.py to Javascript (functions for Cymraeg)
// David Trethewey October 2020

class NiferCymraeg {
    constructor() {
        this.numarray = ["un", "dau", "tri", "pedwar", "pump",
                         "chwech", "saith", "wyth", "naw", "deg"];
        this.numarray_dep = ["un", "dau", "tri", "pedwar", "pum",
                         "chwe", "saith", "wyth", "naw", "deg"];
        this.numarray_f = ["un", "dwy", "tair", "pedair", "pump",
                           "chwech", "saith", "wyth", "naw", "deg"];    
        // handle 12, 15, 18, 20 as exceptions
        this.numarray_ord = ["cyntaf", "ail", "trydydd", "pedwerydd", "pumed",
                             "chweched", "seithfed", "wythfed", "nawfed", "degfed"];
        // default to using traditional numbers up to 20
        this.maxTrad = 20;
}
    replaces(num_cy) {
        num_cy = num_cy.replace("  "," ");
        num_cy = num_cy.replace("a u","ac u");
        num_cy = num_cy.replace("a e","ac e");
        num_cy = num_cy.replace("a ê","ac ê");
        num_cy = num_cy.replace("a o","ac o");
        num_cy = num_cy.replace("a ô","ac ô");
        num_cy = num_cy.replace("a w","ac w");
        num_cy = num_cy.replace("a ŵ","ac ŵ");
        num_cy = num_cy.replace("tri can","tri chan");
        num_cy = num_cy.replace("dau mil", "dau fil");
        return num_cy;
    }
    set setMaxTrad(maxTrad) {
        this.maxTrad = maxTrad;
    }
    numbercy(num, dep=false) {
        /* return the Welsh for the numeral <num> without a noun */        
        num = parseInt(num);
        // console.log(num);
        var num_cy = "";
        var tensunits = 0;
        var hundreds = 0;
        var a = ""; // joining elements with a (and( or with a comma
        var mutatst = 1; // a (and) causes breathed mutation
        if (num === 0) {
            num_cy = "dim"
        }
        if ((num > 0) && (num <= 10)) {
            if (dep) {
                num_cy = this.numarray_dep[num-1];
            }
            else {
                num_cy = this.numarray[num-1];
            }
        }
        if ((num > 10) && (num < 200)) {
            if (num > this.maxTrad) {
                if ((num > 100)&&(num % 100 < this.maxTrad)) {
                num_cy = "cant a " + mutate_cy(this.numbercy(num-100), 3);
                }
                else {
                num_cy = this.numbercyDeg(num);
                }
            }
            else {
                num_cy = this.numbercyUgain(num);
            }
        }
        if (num >= 200) {            
            if (num < 1000) {
                tensunits = num % 100;
                hundreds = Math.floor(num / 100);
                if (tensunits === 0) {
                    num_cy = this.numarray_dep[hundreds-1] + " cant";
                    }
                else {
                    num_cy =  this.numarray_dep[hundreds-1] + " cant a " + mutate_cy(this.numbercy(tensunits), 3);
                    }
                }
            if (num === 1000) {
                num_cy = "mil";
            }
            if ((num % 1000 < 200)&&((num % 20 === 0)||(num % 1000 < 21))) {
                a = " a ";
                mutatst = 3;
                }
            else {
                a = ", ";
                mutatst = 1;
                }
            if ((num > 1000) && (num < 2000)) {
                num_cy = "mil"+ a+ mutate_cy(this.numbercy(num % 1000), mutatst);
            }
            if ((num > 1999) && (num < 21000)) {
                if (num % 1000 === 0) {
                    num_cy = this.numbercy(Math.floor(num/1000), dep=true) + " mil";
                }
                else {
                    num_cy = this.numbercy(Math.floor(num/1000), dep=true) + " mil"+a + mutate_cy(this.numbercy(num % 1000), mutatst);
                }
            }
            if ((num > 20999) && (num < 200000)) {
                if (num % 1000 === 0) {
                    num_cy = this.numbercyDeg(Math.floor(num/1000)) + " mil";
                }
                else {
                    num_cy = this.numbercyDeg(Math.floor(num / 1000)) + " mil " + this.numbercy(num % 1000);
                }
            }
            if ((num > 199999) && (num < 1000000)) {
                if (num % 100000 === 0) {
                    num_cy = this.numarray_dep[Math.floor(num / 100000)-1] + " can mil";
                }
                else if (num % 1000 === 0) {
                    num_cy = this.numarray_dep[Math.floor(num / 100000)-1] + " cant "+ this.numbercyDeg(Math.floor((num%100000)/1000)) + " mil";
                }
                else {
                    num_cy = this.numarray_dep[Math.floor(num / 100000)-1] + " cant "+ this.numbercyDeg(Math.floor((num%100000)/1000)) + " mil " +  this.numbercy(num % 1000);
                }
            }
            if (num === 1000000) {
                num_cy = "miliwn";
            }
            if ((num % 1000000 < 200) &&((num % 20 === 0) || (num % 1000 < 21))) {
                a = " a ";
                mutatst = 3;
            }
            else {
                a = ", ";
                mutatst = 1;
            }
            if ((num > 1000000) && (num < 2000000)) {
                num_cy = "miliwn"+ a+ mutate_cy(this.numbercy(num % 1000000), mutatst);
            }
            if ((num > 1999999) && (num < 21000000)) {
                if (num % 1000000 === 0) {
                    num_cy = this.numbercy(Math.floor(num/1000000), dep=true) + " miliwn";
                }
                else {
                    num_cy = this.numbercy(Math.floor(num/1000000), dep=true) + " miliwn"+a + mutate_cy(this.numbercy(num % 1000000), mutatst);
                }
            }
            if ((num > 20999999) && (num < 200000000)) {
                if (num % 1000000 === 0) {
                    num_cy = this.numbercyDeg(Math.floor(num/1000000)) + " miliwn";
                }
                else {
                    num_cy = this.numbercyDeg(Math.floor(num / 1000000)) + " miliwn " + this.numbercy(num % 1000000);
                }
            }
            if ((num > 199999999) && (num < 1000000000)) {
                if (num % 100000000 === 0) {
                    num_cy = this.numarray_dep[Math.floor(num / 100000000)-1] + " can miliwn";
                }
                else if (num % 1000000 === 0) {
                    num_cy = this.numarray_dep[Math.floor(num / 100000000)-1] + " cant "+ this.numbercyDeg(Math.floor((num%100000000)/1000000)) + " miliwn";
                }
                else {
                    num_cy = this.numarray_dep[Math.floor(num / 100000000)-1] + " cant "+ this.numbercyDeg(Math.floor((num%100000000)/1000000)) + " miliwn " +  this.numbercy(num % 1000000);
                }
            }
            // not yet implemented behaviour for larger numbers
            if (num === 1e9) {
                num_cy = "biliwn";
            }
            if (num > 1e9) {
                num_cy = num.toString();
            }
            }

        num_cy = this.replaces(num_cy);
        return num_cy;
       } 

    numbercyDeg(num) {
        var tens = 0;
        var units = 0;
        var num_cy = "";
        var mstate = 1;
        if ((num <= 10)||(num >= 200)) {
            console.log("numbercyDeg(num) expects num between 11-199");
        }
        if (num < 100) {
            tens = Math.floor(num / 10);
            units = num % 10;
            if (tens === 2) {
                mstate = 2;
            }
            if (units === 0) {
                num_cy = this.numarray_dep[tens-1] + " " + mutate_cy("deg", mstate);
            }
            else {
                num_cy = this.numarray_dep[tens-1] + " " + mutate_cy("deg ", mstate)+this.numarray[units-1];
            }
        }
        else if (num > 100) {
            tens = Math.floor((num-100) / 10);
            units = num % 10;
            if (tens === 2) {
                mstate = 2;
            }            
            if (units === 0) {            
                num_cy = "cant " + this.numarray_dep[tens-1] + " " + mutate_cy("deg", mstate);
            }
            else if (tens === 0) {
                num_cy = "cant a "+mutate_cy(this.numarray[units-1], 3);
            }
            else {
                num_cy = "cant " + this.numarray_dep[tens-1] + " " + mutate_cy("deg ", mstate)+this.numarray[units-1];
            }
            }
        else {
            num_cy = "cant";
        }
        return num_cy;
    }

    numbercyUgain(num) {
        var firstpart = 0;
        var secondpart = 0;
        var num_cy = "";
        var dep;
        if ((num <= 10)||(num >= 200)) {
            console.log("numbercyUgain(num) expects num between 11-199");
        }
        if ((num > 10) && (num < 15)) {
            num_cy = this.numarray[num-11] + " ar ddeg";
        }
        if (num === 12) {
            num_cy = "dauddeg";
        }
        if (num === 15) {
            num_cy = "pymtheg";
        }
        if ((num > 15) && (num < 20)) {
            num_cy = this.numarray[num-16] + " ar bymtheg";
        }
        if (num === 18) {
            num_cy = "deunaw";
        }
        if (num === 20) {
            num_cy = "ugain"
        }
        if ((num > 20) && (num < 40)) {
            num_cy = this.numbercy(num-20) + " ar hugain";
        }
        if (num === 40) {
            num_cy = "deugain";
        }
        if (((num > 40) && (num < 100)) || ((num > 119) && (num < 200))) {
            firstpart = num % 20;
            secondpart = Math.floor(num / 20);
            if (firstpart === 0) {
                if (num === 60) {
                    num_cy = "trigain";
                }
                else if (num === 120) {
                    num_cy = "chweugain";
                }
                else {
                    num_cy = this.numbercy(secondpart, dep=true) + " ugain";
                }
            }
            else {
                if (num === 50) {
                    num_cy = "hanner cant"
                }
                else {
                    num_cy = this.numbercy(firstpart) + " a "+ mutate_cy(this.numbercy(secondpart, dep=true), 3) + " ugain";
                }
                }
            }
        if (num === 100) {
            num_cy = "cant";
        }
        if ((num > 100) && (num < 120)) {
            firstpart = num % 20;
            secondpart = Math.floor(num / 20);
            num_cy = "cant a "+ this.numbercy(num-100);                    
        }
        return num_cy;
}
    firstpartnouncy(num, noun, fem=false) {
        var firstpart_cy = "";
        if (num > 19) {
            console.log("firstpartnouncy(num, noun) expects num < 20");
        }    
        if (num === 0) {
            return "";
        }
        if (num > 15) {
            if (num === 18) {
                firstpart_cy = "deunaw "+noun;
            }
            else if (num === 15) {
                firstpart_cy = "pymtheg "+noun;
            }
            else {
                firstpart_cy = this.firstpartnouncy(num-15, noun, fem) + " ar bymtheg";
            }
        }
        else if (num > 10) {
            /* not implemented at present:
             * nasal mutation of dauddeg,  pymtheg, deunaw
             * for blynedd, blwydd, diwrnod
             * and change of deg --> -eng before m for 12, 15
             */
            if (num === 12) {                
                firstpart_cy = "dauddeg "+noun;
            }
            else {
                firstpart_cy = this.firstpartnouncy(num-10, noun, fem) + " ar ddeg";
            }
        }            
        // give number 1-9 or first part of compound
        else if (num > 4) {
            // direct lookup for numbers up to 10
            /* not implemented at present: 
             * according to "A Welsh Grammar" (Stephen L. Williams):
             * mutations for 7, 8 (soft, but not always observed)
             * 7, 8 (nasal only for blynedd, blwydd, diwrnod(sometimes))
             * 9, 10 (nasal only for blynedd, blwydd, diwrnod)
             * 10 change of deg --> -eng before m
             */
            if (num === 6) {
                firstpart_cy = "chwe " + mutate_cy(noun, 3);
            }
            else {
                firstpart_cy = this.numarray_dep[num-1] + " " + noun;
            }
        }
        else {
            /* override for numbers 1-4 to handle mutation
             and feminine forms if 'fem' is True
             mutation should only happen for 1 for fem. nouns
             and use feminine forms for 2, 3, 4 with fem. nouns
             variable fem keeps track of gender */
            if (num === 4) {
                if (fem) {
                    firstpart_cy = "pedair " + noun; // feminine form
                }
                else {
                    firstpart_cy = "pedwar " + noun;
                }
            }
            if (num === 3) {
                if (fem) {
                    firstpart_cy = "tair " + noun;
                }
                else {
                    firstpart_cy = "tri " + mutate_cy(noun, 3);
                }
            }
            if (num === 2) {
                if (fem) {
                    firstpart_cy = "dwy " + mutate_cy(noun, 2);
                }
                else {
                    firstpart_cy = "dau " + mutate_cy(noun, 2);
                }
            }
            if (num === 1) {
                if (fem) {
                    firstpart_cy = "un " + mutate_cy(noun, 2);
                }
                else {
                    firstpart_cy = "un " + noun;
                }
            }
        }
        return firstpart_cy;
    }
    numbercy_noun(num, noun, fem=false, npl = "au")
    {
        /* Returns numeral <num> in Welsh compounded with <noun>

        <fem> is a boolean variable specifying whether the noun is feminine
        <npl> is the plural of <noun>. if it isn't specified default to
        <noun>+'ow'
        */
        // default plural suffix -au
        var num_cy = "";
        if (npl === "au") {
            npl = noun+npl;
        }
        
        if (num === 0) {
        var n = mutate(npl,2);
        num_cy = `dim o ${n}`;
        return num_cy;
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
        /* use a plural noun for all numbers over 49 except 100
        *  or where the decimal system is used
        *  remember to change the last condition if changing the number 49
        *  not implemented at present: 
        *  nasal mutation of ugain, can 
        *  for blynedd, blwydd, diwrnod
        */
        if ((num === 100)&&(this.maxTrad >= 100)) {
            num_cy = "can " + noun;
        }
        else if ((num > this.maxTrad) || (num > 49)) {
            num_cy = `${this.numbercy(num)} o ${mutate_cy(npl, 2)}`;
        }
        else if ((num > 0) && (num < 20)) {
            num_cy = this.firstpartnouncy(num, noun, fem);
        }
        else if (num === 20) {
            num_cy = "ugain " + noun;
        }
        else if ((num > 20) && (num < 40)) {
            num_cy = this.firstpartnouncy(num-20, noun, fem) + " ar hugain";
        }
        else if (num === 40) {
            num_cy = "deugain " + noun;
        }
        else if (num > 40) {
            num_cy = this.firstpartnouncy(num-40, noun, fem) + " a deugain";
        }
        num_cy = this.replaces(num_cy);
        return num_cy;
    }
    numbercy_float(num)
    {
    var num_cy = "";
    if (num < 0.0) {
        return "minws " + this.numbercy_float(-1*num);
    }
    if (num === 0) {
        num_cy = this.numbercy(num);
        return num_cy;
    }
    else if (num === parseInt(num)) {
        num_cy = this.numbercy(parseInt(num));
        return num_cy;
    }
    else {
        num_cy = this.numbercy(parseInt(num));        
        var decdigits = num.toString().split(".")[1];
        num_cy = num_cy + " pwynt ";
        var d;
        for (d of decdigits) {
            num_cy = num_cy + this.numbercy(parseInt(d)) + ", ";
        }
        if (num_cy.slice(-2) === ", ") {
            num_cy = num_cy.slice(0,-2);
        }
        return num_cy;
    }
    }
    numbercy_float_noun(num, noun, fem=false, npl = "au")
    {
    var num_cy = "";
    if (num === parseInt(Math.abs(num))) {
        return this.numbercy_noun(num,noun,fem,npl);
    }
    else {
        num_cy = this.numbercy_float(num);
        num_cy += " a ";
        // default plural suffix -au
        if (npl === "au") {
            npl = noun+npl;
        }
        num_cy += mutate_cy(npl,2);
        return num_cy;
        }        
    }
jsnifercy()
{
  var inp, outp, inpint;
  // get value of text input
  inp = document.getElementById("cytekstnifer").value;
  if (inp === "") {
    outp = "Y bocs yw gwag. Mae rhaid i chi rhowch nifer";
    }
    else {
        if (inp === "0") {
         outp = this.numbercy_float(0);
        }    
        else if (inp) {
        inp = Number(inp);
        outp = this.numbercy_float(inp);
        }
        else {
        outp = "Nac ydy hwn nifer. Mae rhaid i chi rhowch nifer mewn digidau";
        }   
    }
document.getElementById("nifer").innerHTML = outp;  
}

klerhe(form, output)
{
    /* first argument is the id of a form to be reset
     * second is id of HTML element of the output */
    document.getElementById(form).reset();
    document.getElementById(output).innerHTML = "";
}    

jsnifernouncy()
{
  var inp, inpn, inppln, outp, inpint;
  // get value of text input
  inp = document.getElementById("cytekstnifern").value;
  inpn = document.getElementById("cytekstnifernoun").value;
  inppln = document.getElementById("cytekstniferpluralnoun").value;
  var fem = document.getElementById("femnoun").checked;
  
  if (inp === "") {
    outp = "Y bocs yw gwag. Mae rhaid i chi rhowch nifer";
    }
    else {
        if (inpn === "") {
            inpn = "[n]";
        }
        if (inppln === ""){
           // default plural suffix -au
           inppln = "au"; 
        }
        if (inp === "0") {
         outp = this.numbercy_float_noun(0, inpn, fem, inppln);
        }    
        else if (inp) {
        inp = Number(inp);
        outp = this.numbercy_float_noun(inp, inpn, fem, inppln);
        }
        else {
        outp = "Nac ydy hwn nifer. Mae rhaid i chi rhowch nifer mewn digidau";
        }   
    }
document.getElementById("nifernoun").innerHTML = outp;
}
}
function setMaxTradjs(cyN)
{
    const rbs = document.querySelectorAll('input[name="trad"]');
    let maxtrad;
    for (const rb of rbs) {
        if (rb.checked) {
            maxtrad = rb.value;
            console.log(maxtrad);
            break;
        }
    }
    
    cyN.maxTrad = maxtrad;
}  
cyN = new NiferCymraeg();

function cymraegTests(objID) {
    if (document.getElementById(objID).innerHTML === "") {
    var objinnerHTML = "";
    var t;
    cyN = new NiferCymraeg();
    var testNums = [1,3,7,11,15, 17, 18, 25, 36, 50,
                51, 72, 100, 105, 140, 147, 200, 217,
                232, 500, 1000, 4000, 5674, 14562,
                27865, 79562, 105689, 170000, 1000000,
                1000001, 7000000, 756345234, 100000000, 2345565785];
    objinnerHTML += "<h3>Prawfau Niferau Cymraeg</h3>";    
    objinnerHTML += "<h4>Using default maxTrad = 20</h4>";
    objinnerHTML += "<table>";
    for (t of testNums) {            
        objinnerHTML += `<tr><td>${t}</td><td>:</td><td>${cyN.numbercy(t)}</td></tr>`;
    }
    objinnerHTML += "</table>";
    objinnerHTML += "<h4>setting maxTrad = 10</h4>";        
    cyN.maxTrad = 10;
    objinnerHTML += "<table>";
    for (t of testNums) {
        objinnerHTML += `<tr><td>${t}</td><td>:</td><td>${cyN.numbercy(t)}</td></tr>`;
    }
    objinnerHTML += "</table>";
    objinnerHTML += "<h4>setting maxTrad = 200</h4>";
    cyN.maxTrad = 200;
    objinnerHTML += "<table>";
    for (t of testNums) {
        objinnerHTML += `<tr><td>${t}</td><td>:</td><td>${cyN.numbercy(t)}</td></tr>`;
    }
    objinnerHTML += "</table>";
    objinnerHTML += "<h3>Prawfau niferau gydag enw</h3>";    
    objinnerHTML += "<h4>setting maxTrad = 50</h4>";
    cyN.maxTrad = 50;
    objinnerHTML += "<table>";
    for (t of testNums.slice(0,20)) {
        objinnerHTML += `<tr><td>${t}</td><td>:</td><td>${cyN.numbercy_noun(t, "cath", true, "cathod")}</td></tr>`;
    }
    objinnerHTML += "</table>";
    objinnerHTML += "<h4>setting maxTrad = 10</h4>";    
    cyN.maxTrad =10;
    objinnerHTML += "<table>";
    for (t of testNums.slice(0,20)) {
        objinnerHTML += `<tr><td>${t}</td><td>:</td><td>${cyN.numbercy_noun(t, "cath", true, "cathod")}</td></tr>`;
    }
    objinnerHTML += "</table>";
    document.getElementById(objID).innerHTML = objinnerHTML;
}
else {
    document.getElementById(objID).innerHTML = "";
    }
}
