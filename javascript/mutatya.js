// porting mutatya.py to Javascript
// David Trethewey October 2020
// This doesn't actually determine whether
// a word should mutate
//
// all it does is take a word and mutation state 
// from 1 to 6
// in function mutate(word, mutationstate)
// and return the mutated form
//
// 1 = no mutation
// 2 = soft mutation k-->g, p-->b etc.
// 3 = breathed mutation p->f k->h t->th
// 4 = hard mutation g->k d->t b->p
// 5 = mixed I
// 6 = mixed II after 'th
//
// or for Welsh in fuction mutate_cy(word, mutationstate)
// mutation state can be one of 1, 2, 7, 8
// where 7 = nasal mutation
//       8 = mixed mutation after neg. part. ni
//           either soft or breathed depending on
//           initial letter
//
// it will try to return it in the same case
// i.e. lower, UPPER, or Title


// from https://www.w3docs.com/snippets/javascript/how-to-convert-string-to-title-case-with-javascript.html
function toTitleCase(str) {
  return str.replace(
    /\w\S*/g,
    function (txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    }
  );
}

function caseFormat(word, outputcase) {
    // outputcase determines 
    // capitalisation of output
    if (outputcase === 'lower') {
        return word.toLowerCase();
    }
    else if (outputcase === 'upper') {
        return word.toUpperCase();
    }
    else if (outputcase === 'title') {
        return toTitleCase(word);
    }
    else {
    return word;
    }
}

function findOutputCase(word) {
    var outputcase = 'lower'; // default
    if (word === word.toLowerCase()) {
        outputcase = 'lower';
    }
    else if (word === word.toUpperCase()){
        outputcase = 'upper';
    }
    else if (word === toTitleCase(word)){
        outputcase = 'title';
    }
    return outputcase;
}

function mutate(word,mutationstate, trad=false) {
     
    //take word as a str 
    //and mutationstate as integer from 1-6
    //use variable outputcase
    //to return word in same capitalisation
    //as it went in
    //note that non-standard capITALization
    //will be turned lower case
    //variable trad set to True will expect and return
    //traditional graphs as in SWF/T
    

    var outputcase = findOutputCase(word);
    word = word.toLowerCase();
    // default to no mutation if mutationstate isn't what is
    // expected (int from 1-6)
    var mutationstatearr = [1,2,3,4,5,6];
    if (mutationstatearr.indexOf(mutationstate) === -1){
        // if not an integer between 1 and 6, set it to 1
        mutationstate = 1;
    }

    if (mutationstate === 1){
        // unmutated
        return caseFormat(word,outputcase);
    }
    var newword;
    if (mutationstate == 2){
        // lentition
        newword = word;
        // exception for Gorsedh -> An Orsedh
        if ((word.substring(0,7) === "gorsedh") || (word.substring(0,7) === "gorseth")){
            newword = word.substring(1);
            return caseFormat(newword,outputcase);
}
        if ((word.substring(0,2) === "go")||(word.substring(0,2) === "gu")||(word.substring(0,3) === "gro")||(word.substring(0,3) === "gru")){
            newword = "w" + word.substring(1);
            return caseFormat(newword,outputcase);
}
        if (word.charAt(0) === "g"){
            newword = word.substring(1);
        }
        if ((word.charAt(0) === "b")||(word.charAt(0) === "m")){
            newword = "v" + word.substring(1);
        }
        if (word.charAt(0) === "k"){
            newword = "g" + word.substring(1);
        }
        if (trad && ((word.charAt(0) === "c" && word.substring(0,2) !== "ch")||(word.substring(0,2) === "qw"))){
            // if using traditional spelling recognise initial c
            newword = "g" + word.substring(1);
        }
        if (word.substring(0,2) === "ch"){
            newword = "j" + word.substring(2);
        }
        if (word.charAt(0) === "d"){
            if (word.substring(0,4) === "dydh") {
                newword = "j"+word.substring(1);
            }
            else
            {
                newword = "dh" + word.substring(1);
            }
            }
        if (word.charAt(0) === "p"){
            newword = "b" + word.substring(1);
        }
        if (word.charAt(0) === "t"){
            newword = "d" + word.substring(1);
        }
        return caseFormat(newword,outputcase);
    }

    if (mutationstate === 3){
        // breathed mutation
        newword = word;
        var nonmutarr = ['kl', 'kr', 'cl', 'cr'];
        if (word.charAt(0) === "k"){
            
            if (!(nonmutarr.includes(word.substring(0,2)))){
                newword = "h" + word.substring(1);
            }
        }
        if (trad && word.charAt(0) === "c"){
            if (!(nonmutarr.includes(word.substring(0,2)))){
                newword = "h" + word.substring(1);
            }
        }
        if (trad && word.substring(0,2) === "qw"){
            newword = "wh" + word.substring(2);
        }
        if (word.charAt(0) === "p"){
            newword = "f" + word.substring(1);
        }
        if (word.charAt(0) === "t"){
            newword = "th" + word.substring(1);
        }
        return caseFormat(newword,outputcase);
    }

    if (mutationstate === 4){
        // hard mutation
        newword = word;
        if (word.charAt(0) === "b"){
            newword = "p" + word.substring(1);
        }
        if (word.charAt(0) === "d"){
            newword = "t" + word.substring(1);
        }
        if (word.charAt(0) === "g"){
            var tradc = 'einyw';
            if (trad && tradc.indexOf(word.charAt(1))){
                newword = "c" + word.substring(1);
            }
            else if (trad && word.charAt(1) === "w"){
                newword = "q" + word.substring(1);
            }
            else{
                newword = "k" + word.substring(1);
            }
            }
        return caseFormat(newword,outputcase);
    }

    if (mutationstate === 5){
        // mixed mutation
        newword = word;
        if (word.charAt(0) === "b"){
            newword = "f" + word.substring(1);
        }
        if (word.charAt(0) === "d"){
            newword = "t" + word.substring(1);
        }
        if (word.charAt(0) === "m"){
            newword = "f" + word.substring(1);
        }
        if ((word.substring(0,2) === "go")||(word.substring(0,2) === "gu")||(word.substring(0,3) === "gro")||(word.substring(0,3) === "gru")){
            if (trad){
                newword = "wh" + word.substring(1);
            }
            else {
                newword = "hw" + word.substring(1);
            }
            return caseFormat(newword,outputcase)
        }
        if (word.substring(0,2) === "gw" && trad){
            newword = "wh"+ word.substring(2);
        }
        else {
            if (word.charAt(0) === "g"){
                newword = "h"+ word.substring(1);
            }
        }
        return caseFormat(newword,outputcase);
    }

    if (mutationstate === 6){
        // the mixed mutation after 'th infixed pronoun
        newword = word;
        if (word.charAt(0) === "b"){
            newword = "v" + word.substring(1);
        }
        if (word.charAt(0) === "d"){
            newword = "t" + word.substring(1);
        }
        if (word.charAt(0) === "m"){
            newword = "v" + word.substring(1);
        }        
        // exception for Gorsedh -> An Orsedh
        if ((word.substring(0,7) === "gorsedh") || (word.substring(0,7) === "gorseth")){
            newword = word.substring(1);
            return caseFormat(newword,outputcase)
        }
        if ((word.substring(0,2) === "go")||(word.substring(0,2) === "gu")||(word.substring(0,3) === "gro")||(word.substring(0,3) === "gru")){
            newword = "w" + word.substring(1);
            return caseFormat(newword,outputcase)
        }
        if (word.charAt(0) === "g"){
            newword = "h" + word.substring(1);
        }
        if (word.substring(0,2) === "gw"){
            newword = word.substring(1);
        }
        return caseFormat(newword,outputcase);
    }
}

function basicTests(objID){
    // test code - doesn't do all cases
    var objinnerHTML = "";
    var kath = "kath";
    var kath2 = "Kath";
    var kath3 = "KATH";
    var kath4 = "kaTH";
    var gwari = "gwari";
    var expl = {1:"No Mutation",
                2:"Soft Mutation\nvarious causes e.g. fem. sing. nouns after article, A verbal particle",
                3:"Breathed Mutation\ne.g. after 'ow' possessive pronoun = E. 'my'",
                4:"Hard Mutation\ne.g. after present participle 'ow'",
                5:"Mixed Mutation\ne.g. after Y verbal particle",
                6:"Mixed mutation after 'th (infixed pronoun 2p sing.)"};
    var underline = "-".repeat(30);
    objinnerHTML = objinnerHTML + underline + "<br>";
    for (s = 0; s < 6; s++){
        objinnerHTML = objinnerHTML + expl[s+1] + "<br>";
        var m = s+1;
        var r;
        r=mutate(kath,m);
        objinnerHTML = objinnerHTML + `mutate(${kath},${m}) = ${r}` + "<br>";
        r=mutate(kath2,m);
        objinnerHTML = objinnerHTML + `mutate(${kath},${m}) = ${r}` + "<br>";
        r=mutate(kath3,m);
        objinnerHTML = objinnerHTML + `mutate(${kath3},${m}) = ${r}` + "<br>";
        r=mutate(kath4,m);
        objinnerHTML = objinnerHTML + `mutate(${kath4},${m}) = ${r}` + "<br>";
        r=mutate(gwari,m);
        objinnerHTML = objinnerHTML + `mutate(${gwari},${m}) = ${r}` + "<br>";
        objinnerHTML = objinnerHTML + underline + "<br>";
           }
    objinnerHTML = objinnerHTML +"note - doesn't preserve capitalisation of non-standard capiTALISed input";
    document.getElementById(objID).innerHTML = objinnerHTML;
}
function jsmutate(mstate) {
  var inp, outp;
  // get value of text input
  x = document.getElementById("kwtekst").value;
  if (x == "") {
    outp = "An kyst yw gwag. Res yw dhywgh gorra nebes tekst";
}
else
{
    outp = mutate(x, mstate);
}
document.getElementById("mut").innerHTML = outp;
}

console.log(caseFormat("dYDH dA NORVYS", "lower"));
console.log(caseFormat("dYDH dA NORVYS", "upper"));
console.log(caseFormat("dYDH dA NORVYS", "title"));

console.log(findOutputCase("dydh da norvys"));
console.log(findOutputCase("DYDH DA NORVYS"));
console.log(findOutputCase("Dydh Da Norvys"));

