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
    if (mutationstate === 2){
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
            if (trad && tradc.indexOf(word.charAt(1))===-1){
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
                if (!((word.substring(0,2) === "gl") || (word.substring(0,2) === "gr")))
                {
                newword = "h"+ word.substring(1);
                }
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
            if (!((word.substring(0,2) === "gl") || (word.substring(0,2) === "gr")))
            {
            newword = "h" + word.substring(1);
            }
        }
        if (word.substring(0,2) === "gw"){
            newword = word.substring(1);
        }
        return caseFormat(newword,outputcase);
    }
}

function mutate_cy(word, mutationstate) {
    /*
    take Welsh word as a str
    and mutationstate as integer 1-3 or 7, 8
    use variable outputcase
    to return word in same capitalisation
    as it went in
    note that non-standard capITALization
    will be turned lower case
    1 = unmutated
    2 = soft mutation
    3 = aspirate mutation
    7 = nasal mutation
    8 = mixed mutation (after negative particle
    Ni - may by written or not, where 
    those letters that undergo aspirate mutation
    do so, and other letters undergo soft mutation)
    */
    var outputcase = findOutputCase(word);
    word = word.toLowerCase();
    // default to no mutation if mutationstate isn't what is
    // expected (int 1-3,7-8)
    var mutationstatearr = [1,2,3,7,8];
    if (mutationstatearr.indexOf(mutationstate) === -1){
        // if not an integer in 1-3 or 7-8, set it to 1
        mutationstate = 1;
    }
    if (mutationstate === 1){
    return caseFormat(word, outputcase);
    }
    var newword;
    if (mutationstate === 2){
        // lentition
        newword = word;        
    if (word.charAt(0) === "g") {
        newword = word.substring(1);
        }
    if ((word.charAt(0) === "b")||(word.charAt(0) === "m")) {
        newword = "f" + word.substring(1);
        }
    if ((word.charAt(0) === "c")&&(word.substring(0,2) !== "ch")) {
        newword = "g" + word.substring(1);
        }
    if ((word.charAt(0) === "d")&&(word.substring(0,2) !== "dd")) {
        newword = "d" + word;
        }
    if ((word.charAt(0) === "p")&&(word.substring(0,2) !== "ph")) {
        newword = "b" + word.substring(1);
        }
    if ((word.charAt(0) === "t")&&(word.substring(0,2) !== "th")) {
        newword = "d" + word.substring(1); 
        }   
    if (word.substring(0,2) === "ll") {
        newword = word.substring(1); 
        }
    if (word.substring(0,2) === "rh") {
        newword = "r" + word.substring(2);
        }
    return caseFormat(newword, outputcase);
    }       
    if (mutationstate === 3){
        // breathed mutation
        newword = word;
    if ((word.charAt(0) === "c")&&(word.substring(0,2) !== "ch")) {
        newword = "ch" + word.substring(1);
    }
    if ((word.charAt(0) === "p")&&(word.substring(0,2) !== "ph")) {
        newword = "ph" + word.substring(1);
        }
    if ((word.charAt(0) === "t")&&(word.substring(0,2) !== "th")) {
        newword = "th" + word.substring(1); 
        }                
    return caseFormat(newword, outputcase);
    }
    if (mutationstate === 7){
        // nasal mutation
        newword = word; 
    if ((word.charAt(0) === "c")&&(word.substring(0,2) !== "ch")) {
        newword = "ngh" + word.substring(1);
    }
    if ((word.charAt(0) === "p")&&(word.substring(0,2) !== "ph")) {
        newword = "mh" + word.substring(1);
        }
    if ((word.charAt(0) === "t")&&(word.substring(0,2) !== "th")) {
        newword = "nh" + word.substring(1); 
        }
    if (word.substring(0,2) === "th") {
        newword = "nh" + word.substring(2); 
        }
    if (word.charAt(0) === "b") {
        newword = "m" + word.substring(1);
        }
    if ((word.charAt(0) === "d")&&(word.substring(0,2) !== "dd")) {
        newword = "n" + word.substring(1);
        }
    if (word.charAt(0) === "g") {
        newword = "ng" + word.substring(1);
        }
    return caseFormat(newword, outputcase);                                   
    }
    if (mutationstate === 8){
        // mixed mutation
        newword = word;
        var cpt = "cpt"; 
        if (cpt.indexOf(word.charAt(0)) !== -1) {
            newword = mutate_cy(word, 3)
        }
        else {
            newword = mutate_cy(word, 2)
        }
        return caseFormat(newword, outputcase);
    }
            
}

function rev_mutate_cy(word, listmode = false) {
    /* Takes a word and outputs all possible words that could mutate to it
    By default it will output a dictionary indexed by numbers [1, 2, 3, 7],
    if listmode is set to True, it will be a flat list with duplicates
    removed
    */
    var outputcase = findOutputCase(word);
    word = word.toLowerCase();

    // assume initial mh- nh- ng- ngh- dd- only occur in mutated forms
    // unmutated initial ph- th- are rare but do exist
    var unmutated = {1:[], 2:[], 3:[], 7:[]};
    var mutonly = ["dd", "mh", "nh", "ng"];
    var vowels_rl = "aâeêëiîïloöôruûwŵyŷ";
    var rhll = ["rh", "ll"];
    var ngnh = ["ng", "nh"];
    if ((word.substring(0,3) !== "ngh") && (mutonly.indexOf(word.substring(0,2)) === -1)) {
        unmutated[1].push(word);
    }
    // g->0
    if ((vowels_rl.indexOf(word.charAt(0)) !== -1) && (rhll.indexOf(word.substring(0,2)) === -1)) {
        unmutated[2].push("g"+word);
    }
    if ((word.charAt(0) === "f") && (word.substring(0,2) !== "ff")) {
        unmutated[2].push("b" + word.substring(1));
        unmutated[2].push("m" + word.substring(1));
    }
    if (word.charAt(0) === "g") {
        unmutated[2].push("c" + word.substring(1));
    }
    if (word.substring(0,2) === "dd") {
        unmutated[2].push("d" + word.substring(2));
    }
    if (word.charAt(0) === "b") {
        unmutated[2].push("p" + word.substring(1));
    }
    if ((word.charAt(0) === "d") && (word.substring(0,2) !== "dd")) {
        unmutated[2].push("t" + word.substring(1));
    }
    if ((word.charAt(0) === "l") && (word.substring(0,2) !== "ll")) {
        unmutated[2].push("ll" + word.substring(1));
    }
    if ((word.charAt(0) === "r") && (word.substring(0,2) !== "rh")) {
        unmutated[2].push("rh" + word.substring(1));
    }
    if (word.substring(0,2) === "ch") {
        unmutated[3].push("c"+word.substring(2));
    }
    if (word.substring(0,2) === "ph") {
        unmutated[3].push("p"+word.substring(2));
    }
    if (word.substring(0,2) === "th") {
        unmutated[3].push("t"+word.substring(2));
    }
    if (word.substring(0,3) === "ngh") {
        unmutated[7].push("c"+word.substring(3));
    }
    if (word.substring(0,2) === "mh") {
        unmutated[7].push("p"+word.substring(2));
    }
    if ((word.substring(0,2) === "ng") && (word.substring(0,3) !== "ngh")) {
        unmutated[7].push("g"+word.substring(2));
    }
    if (word.substring(0,2) === "nh") {
        unmutated[7].push("t"+word.substring(2));
    }
    if ((word.charAt(0) === "m") && (word.substring(0,2) !== "mh")) {
        unmutated[7].push("b"+word.substring(1));
    }
    if ((word.charAt(0) === "n") && (ngnh.indexOf(word.substring(0,2)) === -1)) {
        unmutated[7].push("d"+word.substring(1));
    }
    
    var unmutatedcasef = {};
    const states = Object.keys(unmutated);
    console.log(states);
    var outw;
    states.forEach((key, index) => {
        unmutatedcasef[key] = [];
        console.log(unmutated[key]);
        for (w of unmutated[key]) {
            outw = caseFormat(w, outputcase);
            unmutatedcasef[key].push(outw);
        }
    });
    if (listmode) {
        var unmutlist = [];
        Object.values(unmutatedcasef).forEach(val => {
            unmutlist = unmutlist.concat(val);
        });
        var uniqunmutlist = [];
        unmutlist.forEach((w) => {
            if (!uniqunmutlist.includes(w)) {
                uniqunmutlist.push(w);
            }
        });
        uniqunmutlist.sort();
        return uniqunmutlist;
    }
    else {
        console.log(unmutatedcasef);
        return unmutatedcasef;
    }
}

function basicTests(objID){
    // test code - doesn't do all cases
    if (document.getElementById(objID).innerHTML === "") {
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
else 
{
    document.getElementById(objID).innerHTML = "";
}
}
function jsmutate(mstate) {
  var inp, outp;
  // get value of text input
  inp = document.getElementById("kwtekst").value;
  var trad = document.getElementById("tradkw").checked;
  
  if (inp == "") {
    outp = "An kyst yw gwag. Res yw dhywgh gorra nebes tekst";
}
else
{
    outp = mutate(inp, mstate, trad);
}
document.getElementById("mut").innerHTML = outp;
}

function jsmutate_all() {
  var inp, outp;
  // get value of text input
  inp = document.getElementById("kwtekst").value;
  var trad = document.getElementById("tradkw").checked;
  if (inp == "") {
    outp = "An kyst yw gwag. Res yw dhywgh gorra nebes tekst";
}
else
{
    var outp1 = "<tr><td>Heb treylyans</td><td><sup>1</sup>"+mutate(inp, 1, trad)+"</td></tr>";
    var outp2 = "<tr><td>Treylans medhel</td><td><sup>2</sup>"+mutate(inp, 2, trad)+"</td></tr>";
    var outp3 = "<tr><td>Treylans hwythsonek</td><td><sup>3</sup>"+mutate(inp, 3, trad)+"</td></tr>";
    var outp4 = "<tr><td>Treylans kales</td><td><sup>4</sup>"+mutate(inp, 4, trad)+"</td></tr>";
    var outp5 = "<tr><td>Treylans kemmyskys</td><td><sup>5</sup>"+mutate(inp, 5, trad)+"</td></tr>";
    var outp6 = "<tr><td>Treylans kemmyskys wosa 'th</td><td><sup>5</sup>"+mutate(inp, 6, trad)+"</td></tr>";
    outp = "<table>" + outp1 + outp2 + outp3 + outp4 + outp5 + outp6 + "</table>";
}
document.getElementById("mut").innerHTML = outp;
}
function jsrevmutate() {
  var inp, outp;
  // get value of text input
  inp = document.getElementById("kwtekst").value;
  var trad = document.getElementById("tradkw").checked;
  if (inp == "") {
    outp = "An kyst yw gwag. Res yw dhywgh gorra nebes tekst";
}
else
{
    outp = format_rev_mutate(rev_mutate(inp, listmode=false, trad=trad), kw=true);
}
document.getElementById("mut").innerHTML = outp;
}
function jsmutate_cy(mstate) {
  var inp, outp;
  // get value of text input
  x = document.getElementById("cytekst").value;
  if (x == "") {
    outp = "Mae'r cist yn wag. Mae rhaid i chi ysgrifennu testun";
}
else
{
    outp = mutate_cy(x, mstate);
}
document.getElementById("mutcy").innerHTML = outp;
}

function jsmutate_cy_all() {
  var inp, outp;
  // get value of text input
  x = document.getElementById("cytekst").value;
  if (x == "") {
    outp = "Mae'r cist yn wag. Mae rhaid i chi ysgrifennu testun";
}
else
{
    var outp1 = "<tr><td>Ffurf heb treiglad</td><td>"+mutate_cy(x, 1)+"</td></tr>";
    var outp2 = "<tr><td>Treiglad meddal</td><td>"+mutate_cy(x, 2)+"</td></tr>";
    var outp3 = "<tr><td>Treiglad llais</td><td>"+mutate_cy(x, 3)+"</td></tr>";
    var outp7 = "<tr><td>Treiglad trwynol</td><td>"+mutate_cy(x, 7)+"</td></tr>";
    var outp8 = "<tr><td>Treiglad cymysg</td><td>"+mutate_cy(x, 8)+"</td></tr>";
    outp = "<table>" + outp1 + outp2 + outp3 + outp7 + outp8 + "</table>";
}
document.getElementById("mutcy").innerHTML = outp;
}
function jsrevmutate_cy() {
  var inp, outp;
  // get value of text input
  x = document.getElementById("cytekst").value;
  if (x == "") {
    outp = "Mae'r cist yn wag. Mae rhaid i chi ysgrifennu testun";
}
else
{
    outp = format_rev_mutate(rev_mutate_cy(x, listmode= false), kw=false, cy=true);
}
document.getElementById("mutcy").innerHTML = outp;
}
function rev_mutate(word, listmode = false, trad = false) {
    /* takes a word and outputs all possible words that could mutate to it 

     By default it will output a dictionary indexed by number 1 to 6, if listmode
     is set to True, it will be a flat list with duplicates removed */
    
    var outputcase = findOutputCase(word);
    word = word.toLowerCase();
    /* we assume the word can be unmutated.
     generally true, though initial dh- before mutation
     is rare and limited mainly to compounds of preposition dhe */
    var unmutated = {1:[word], 2:[], 3:[], 4:[], 5:[], 6:[]};
    if ((word.substring(0,2) === "wo")||(word.substring(0,2) === "wu")||(word.substring(0,3) === "wro")||(word.substring(0,3) === "wru")){
        // g->w
        unmutated[2].push("g"+word.substring(1));
    }
    var letter2g = "aeilnuwy";
    var letter2gr = ["ra", "re", "ri", "ry"];
    var gorsedh = ["orsedh", "orseth"];
    var tradc = 'einyw';

    if (((letter2g.indexOf(word.charAt(0))>-1) || (letter2gr.indexOf(word.substring(0,2))>-1)||(gorsedh.indexOf(word.substring(0,6))>-1))&& !((word.substring(0,2) === "wh") && trad)) {
        unmutated[2].push("g"+word);
    }
    if (word.charAt(0) === "v") {
        unmutated[2].push("b" + word.substring(1));
        unmutated[2].push("m" + word.substring(1));
    }
    if (word.charAt(0) === "g") {
        if (trad && tradc.indexOf(word.charAt(1)) === -1) {
            unmutated[2].push("c" + word.substring(1));
        }
        else if (trad && word.charAt(1) === "w") {
            unmutated[2].push("q" + word.substring(1));
        }
        else {
            unmutated[2].push("k" + word.substring(1));
        }
    }
    if (word.charAt(0) === "j") {
        if (word.substring(0,4) === "jydh") {
            unmutated[2].push("d" + word.substring(1));
        }
        else {
            unmutated[2].push("ch" + word.substring(1));
        }
    }
    if (word.substring(0,2) === "dh") {
        unmutated[2].push("d" + word.substring(2));
    }
    if (word.charAt(0) === "b") {
        unmutated[2].push("p" + word.substring(1));
    }
    if ((word.charAt(0) === "d") && (word.substring(0,2) !== "dh")) {
        unmutated[2].push("t" + word.substring(1));
    }

    if (word.charAt(0) === "h") {
        if (trad && (tradc.indexOf(word.charAt(1)) === -1)) {
            unmutated[3].push("c" + word.substring(1));
        }
        else {
            unmutated[3].push("k" + word.substring(1));
        }
    }
    if (trad && word.substring(0,2) === "wh") {
        unmutated[3].push("qw" + word.substring(2));
    }
    if (word.charAt(0) === "f") {
        unmutated[3].push("p" + word.substring(1));
    }
    if (word.substring(0,2) === "th") {
        unmutated[3].push("t" + word.substring(2));
    }
    if (word.charAt(0) === "p") {
        unmutated[4].push("b" + word.substring(1));
    }
    if (word.charAt(0) === "t" && word.substring(0,2) !== "th") {
        unmutated[4].push("d" + word.substring(1));
    }
    if (word.charAt(0) === "k") {
        unmutated[4].push("g" + word.substring(1));
    }
    if (trad && word.charAt(0) === "c" && (tradc.indexOf(word.charAt(1)) === -1)) {
        unmutated[4].push("g" + word.substring(1));
    }
    if (trad && word.substring(0,2) === "qw") {
        unmutated[4].push("g" + word.substring(1));
    }
    if (word.charAt(0) === "f") {
        unmutated[5].push("b" + word.substring(1));
        unmutated[5].push("m" + word.substring(1));
    }
    if ((word.charAt(0) === "t") && (word.substring(0,2) !== "th")) {
        unmutated[5].push("d" + word.substring(1));
    }
    if ((word.substring(0,3) === "hwo")||(word.substring(0,3) === "hwu")||(word.substring(0,4) === "hwro")||(word.substring(0,4) === "hwru")) {
        unmutated[5].push("g" + word.substring(2));
    }
    if (trad && ((word.substring(0,3) === "who")||(word.substring(0,3) === "whu")||(word.substring(0,4) === "whro")||(word.substring(0,4) === "whru"))) {
        unmutated[5].push("g" + word.substring(2));
    }
    if (word.charAt(0) === "h") {
        unmutated[5].push("g"+ word.substring(1));
    }
    if (trad && word.substring(0,2) === "wh") {
        unmutated[5].push("gw"+ word.substring(2));
    }
    if (word.charAt(0) === "v") {
        unmutated[6].push("b" + word.substring(1));
        unmutated[6].push("m" + word.substring(1));        
    }
    if ((word.charAt(0) === "t") && (word.substring(0,2) !== "th")) {
        unmutated[6].push("d" + word.substring(1));
    }
    // exception for Gorsedh -> An Orsedh
    if (trad) {
        if ((gorsedh.indexOf(word.substring(0,6))>-1) || ((word.charAt(0) === "w") && (word.charAt(1) != "h"))) {
            unmutated[6].push("g" + word);
        }
    }
    else {
        if ((gorsedh.indexOf(word.substring(0,6))>-1) || (word.charAt(0) === "w")) {
            unmutated[6].push("g" + word)
        }
        }
    if ((word.substring(0,2) === "wo")||(word.substring(0,2) === "wu")||(word.substring(0,3) === "wro")||(word.substring(0,3) === "wru")) {
        unmutated[6].push("g" + word.substring(1));
    }
    if ((word.charAt(0) === "h") && (word.charAt(1) != "w")) {
        unmutated[6].push("g" + word.substring(1));
    }


    var unmutatedcasef = {};
    const states = Object.keys(unmutated);
    var outw;
    states.forEach((key, index) => {
        unmutatedcasef[key] = []
        for (w of unmutated[key]) {
            outw = caseFormat(w, outputcase);
            unmutatedcasef[key].push(outw);
        }
    });

    if (listmode) {
        var unmutlist = [];
        Object.values(unmutatedcasef).forEach(val => {
            unmutlist = unmutlist.concat(val);
        });
        var uniqunmutlist = [];
        unmutlist.forEach((w) => {
            if (!uniqunmutlist.includes(w)) {
                uniqunmutlist.push(w);
            }
        });
        uniqunmutlist.sort();
        return uniqunmutlist;
    }
    else {
        return unmutatedcasef;
    }
}
    
function format_rev_mutate(revmdict, kw=false, cy=false) {
    /* return a formatted output of the reversed mutation dictionary 

    If kw is True, the explanation is in Cornish
    */
    const states = Object.keys(revmdict);
    if (states.indexOf(7)>-1) {
        cy = true;
    }
    if (kw) {
        mdesc = {1:"Furv didreylys: ",
                 2:"Treylyans medhel (studh 2) diworth: ",
                 3:"Treylyans hwythsonek (studh 3) diworth: ",
                 4:"Treylyans kales (studh 4) diworth: ",
                 5:"Treylyans kemmyskys (studh 5) diworth: ",
                 6:"Treylyans kemmyskys (wosa raghanow stegys a-ji 'th) diworth: "};
        output = "Y halsa bos an ger:<br>";
    }
    else if (cy)  {
        mdesc = {1:"Ffurf heb treiglad: ",
                 2:"Treiglad meddal oddi wrth: ",
                 3:"Treiglad llais oddi wrth: ",
                 7:"Treiglad trwynol oddi wrth: "};
        output = "Gall bod y gair:<br>";
    }
    else {
        mdesc = {1:"Unmutated form: ",
                 2:"Soft mutation (2nd state) of: ",
                 3:"Breathed mutation (3rd state) of: ",
                 4:"Hard mutation (4th state) of: ",
                 5:"Mixed mutation (5th state) of: ",
                 6:"Mixed mutation (after infixed pronoun 'th) of: "};
        output = "The word could be:<br>";
    }
    output = output + "<table>";
    const descstates = Object.keys(mdesc);
    descstates.forEach((key, index) => {
        console.log(key);
        console.log(mdesc[key]);
        if (revmdict[key].length > 0) {
            output = output + "<tr><td>" + mdesc[key] + "</td>";
            for (w of revmdict[key]) {
                output = output + "<td>"+w+"</td>"
            }
            output = output + "</tr>"
        }
    });
    output = output + "</table>";
    return output;
}

function basicTests_cy(objID) {
    if (document.getElementById(objID).innerHTML === "") {
    // test code - doesn't do all cases
    var objinnerHTML = "";
    var kath = "cath";
    var kath2 = "Cath";
    var kath3 = "CATH";
    var kath4 = "caTH";
    var gwari = "gwari";
    var pen = "pen";
    var tad = "tad";
    var beic = "beic";
    var draig = "draig";
    var llan = "llan50goch";
    var mor = "môr";
    var rhwyfo = "rhwyfo";
    var prynu = "prynais";
    var gwerthu = "gwerthais";
    
    var expl = {1:"No Mutation", 2:"Soft Mutation\nvarious causes e.g. fem. sing. nouns after article, dy 'you' sg. poss. pron.", 3:"Breathed Mutation\ne.g. after 'a' and",7:"Nasal mutation\ne.g. after fy 'my' or yn 'in'"};
    var underline = "-".repeat(30);
    objinnerHTML = objinnerHTML + underline + "<br>";
    var mstates = [1,2,3,7];
    var r;
    for (s of mstates) {
        objinnerHTML = objinnerHTML + expl[s]+"<br>";
        r = mutate_cy(kath, s);
        objinnerHTML = objinnerHTML + `mutate_cy(${kath},${s}) = ${r}` + "<br>";
        r = mutate_cy(kath2,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${kath2},${s}) = ${r}` + "<br>";
        r = mutate_cy(kath3,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${kath3},${s}) = ${r}` + "<br>";
        r = mutate_cy(kath4,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${kath4},${s}) = ${r}` + "<br>";
        r = mutate_cy(gwari,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${gwari},${s}) = ${r}` + "<br>";
        r = mutate_cy(pen,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${pen},${s}) = ${r}` + "<br>";
        r = mutate_cy(tad,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${tad},${s}) = ${r}` + "<br>";
        r = mutate_cy(beic,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${beic},${s}) = ${r}` + "<br>";
        r = mutate_cy(draig,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${draig},${s}) = ${r}` + "<br>";
        r = mutate_cy(llan,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${llan},${s}) = ${r}` + "<br>";
        r = mutate_cy(mor,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${mor},${s}) = ${r}` + "<br>";
        r = mutate_cy(rhwyfo,s);
        objinnerHTML = objinnerHTML + `mutate_cy(${rhwyfo},${s}) = ${r}` + "<br>";
        objinnerHTML = objinnerHTML + underline+"<br>";
    }
    objinnerHTML = objinnerHTML + "Mixed mutation after Ni negative particle, which is not always actually written/spoken but mutation remains." + "<br>";
    r = mutate_cy(gwerthu,8);
    objinnerHTML = objinnerHTML + `mutate_cy(${gwerthu}, 8) = ${r}` + "<br>";
    r = mutate_cy(prynu,8);
    objinnerHTML = objinnerHTML + `mutate_cy(${prynu}, 8) = ${r}` + "<br>";
    
    objinnerHTML = objinnerHTML + "note - doesn't preserve capitalisation of non-standard capiTALISed input";
    document.getElementById(objID).innerHTML = objinnerHTML;
}
else {
    document.getElementById(objID).innerHTML = "";
}
}

function reverseTests(objID) {
    /* test reverse mutation */
    if (document.getElementById(objID).innerHTML === "") {
    var objinnerHTML = "";
    objinnerHTML = objinnerHTML + "main form" + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("gath"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("hath"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("voes"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("fos"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("den"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("dhen"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("tas"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("thas"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("weli"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("kwari"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("hwari"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("whari"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("gweth"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("jydh"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("japel"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("kara"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("cara"), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + "trad form" + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("gath", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("hath", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("voes", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("fos", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("den", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("dhen", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("tas", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("thas", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("weli", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("kwari", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("hwari", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("whari", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("gweth", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("jydh", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("japel", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("kara", false, true), kw=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rev_mutate("cara", false, true), kw=true) + "<br>";
    document.getElementById(objID).innerHTML = objinnerHTML;
}
else {
    document.getElementById(objID).innerHTML = "";
}
}

function reverseTests_cy(objID) {
    if (document.getElementById(objID).innerHTML === "") {
    var objinnerHTML = "";
    var p = rev_mutate_cy("bren", listmode= false);
    var t = rev_mutate_cy("dad", listmode= false);
    var g = rev_mutate_cy("gam", listmode= false);
    var f = rev_mutate_cy("faich", listmode= false);
    var dd = rev_mutate_cy("ddyn", listmode= false);
    var g2 = rev_mutate_cy("air", listmode= false);
    var ll = rev_mutate_cy("lais", listmode= false);
    var rh = rev_mutate_cy("res", listmode= false);
    var mh = rev_mutate_cy("mhren", listmode= false);
    var nh = rev_mutate_cy("nhad", listmode= false);
    var ngh= rev_mutate_cy("ngham", listmode= false);
    var m = rev_mutate_cy("maich", listmode= false);
    var n = rev_mutate_cy("nyn", listmode= false);
    var ng = rev_mutate_cy("ngŵr", listmode= false);
    var ph = rev_mutate_cy("phren", listmode= false);
    var th = rev_mutate_cy("thad", listmode= false);
    var ch = rev_mutate_cy("cham", listmode= false);
    objinnerHTML = objinnerHTML + format_rev_mutate(p, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(t, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(g, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(f, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(dd, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(g2, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(ll, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(rh, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(mh, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(nh, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(ngh, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(m, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(n, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(ng, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(ph, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(th, kw=false, cy=true) + "<br>";
    objinnerHTML = objinnerHTML + format_rev_mutate(ch, kw=false, cy=true) + "<br>";
    document.getElementById(objID).innerHTML = objinnerHTML;
}
else {
    document.getElementById(objID).innerHTML = "";
}
}

console.log(caseFormat("dYDH dA NORVYS", "lower"));
console.log(caseFormat("dYDH dA NORVYS", "upper"));
console.log(caseFormat("dYDH dA NORVYS", "title"));

console.log(findOutputCase("dydh da norvys"));
console.log(findOutputCase("DYDH DA NORVYS"));
console.log(findOutputCase("Dydh Da Norvys"));

