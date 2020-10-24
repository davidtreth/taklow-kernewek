/*  David Trethewey
 based on apposyans_awgrymGUI.py
 ported to Javascript October 2020

assume namespace niverow.js is also available
*/

class KwizAwgrym {
    constructor() {
        this.title = "Kwiz Awgrym";
        // initialise parameters
        this.niverewn = 0;
        this.nivergwrys = 0;
        this.poyntys = 0;
        this.Ngovynn = 20;
        this.gorthypkewar = 0;
        this.kaletter = 2;        
        this.oberyans = 1;
        this.kaletter_text = {1:"Es", 2: "Kres", 3:"Kales", 4:"Pur Gales"};
        this.oberyans_text = {1:"Keworra po marnas", 2: "Keworra", 3:"Marnas"};
        // correct answer as text and figures
        this.gorthyptekst = "";
        this.gorthypbys = "";
        this.starttime = 0;
}
    chooseMaxN() {
    /* based on difficulty choose maximum size of numbers """
    * easy allowed only numbers up to 10
    * and supresses negative answers to subtractions
    * medium up to 20, and hard up to 40 */
    var maxNdict = {1: 10, 2: 20, 3:40, 4:100};       
    return maxNdict[this.kaletter];
    }
    
    diskwedhgovynn(tekst) {
        /* display the question */
        document.getElementById('govynn').innerHTML = tekst;
    }
    
    chekkGorthyp(g, kewar) {
     /* check answer against the correct one, returning a bool and a message */
    if (isNaN(g)) {
        return [false, `<div class='kystmesajerr'>Nag yw ${g} niver</div>`];
    }
    else {
        g = parseInt(g);
        if (g === kewar) {
            return [true, `<div class='kystmesajewn'><span>Ty a ros ${g}</span><span>Ewn os</span></div>`];
        }
        else {
            return [false, `<div class='kystmesajkamm'><span>Ty a ros ${g}</span><span>Kamm os</span></div>`];
        }
    }
    }    
    
    keworra() {
    var n, x1, x2, keworrans, gov;
    /* ask an addition question */
    n = this.chooseMaxN();
    // random numbers in question
    x1 = Math.ceil(Math.random() * n);
    x2 = Math.ceil(Math.random() * n);
    // calculate answer
    keworrans = x1 + x2;
    // store sum and answer as text and figures
    this.gorthyptekst = `${numberkw(x1)} + ${numberkw(x2)} = ${numberkw(keworrans)}`;
    this.gorthypbys = `${x1} + ${x2} = ${keworrans}`;
    if (this.kaletter < 4) {
        gov = `Pyth yw ${numberkw(x1)} ha ${numberkw(x2)}?`;
    }
    else {
        gov = `Pyth yw ${numberkw(x1)} + ${numberkw(x2)}?`;
        }
    gov = gov.replace("ha u","hag u");
    gov = gov.replace("ha e","hag e");
    gov = gov.replace("ha o","hag o");
    // display the question
    this.diskwedhgovynn(gov);
    return keworrans;
    }
    marnas() {
        /* ask a subtraction question */
    var n, x1, x2, marnasyans, gov, es;
    n = this.chooseMaxN();        
    // random numbers in question
    x1 = Math.ceil(Math.random() * n);
    x2 = Math.ceil(Math.random() * n);
    console.log(this.kaletter, x1, "-", x2);
    if (this.kaletter === 1) {
        es = true;
    }
    else {
        es = false;}
    while ((es)&&(x2 > x1)) {
        /* choose again if difficulty is easy
        and result is negative */
    x1 = Math.ceil(Math.random() * n);
    x2 = Math.ceil(Math.random() * n);        
    }
    // calculate answer
    marnasyans = x1 - x2;
    // store sum and answer as text and figures
    this.gorthyptekst = `${numberkw(x1)} - ${numberkw(x2)} = ${numberkw_float(marnasyans)}`;
    this.gorthypbys = `${x1} - ${x2} = ${marnasyans}`;
    if (this.kaletter < 4) {
        gov = `Pyth yw ${numberkw(x1)} marnas ${numberkw(x2)}?`;
    }
    else {
        gov = `Pyth yw ${numberkw(x1)} - ${numberkw(x2)}?`;
        }        
    this.diskwedhgovynn(gov);
    return marnasyans;
}
govynn1() {
/* ask a question, choosing addition or subtraction */
var r, garray, g, gorthyp;
var d = new Date();
this.starttime = d.getTime();
r = this.oberyans;
console.log(this.oberyans, this.oberyans_text[r]);
if (r === 1) {
    // random choice + or -
    r = Math.floor(Math.random() * 2) + 2;        
}
else {
    r = this.oberyans;
    console.log(r);
}
if (r === 2) {
    gorthyp = this.keworra();
}
else if (r === 3) {
    gorthyp = this.marnas();
}
return gorthyp;
}

rigorthyp() {
    var g, niver, output, kewarder, d, t, tekst, fcolour;
    if (this.nivergwrys >= this.Ngovynn) {
        return undefined;
    }
    g = document.getElementById("gorthyp").value;
    console.log(g);
    if ((isNaN(g))||g==="") {
        output = "<div class='kystmesajerr'>Res yw gorra niver y'n kyst\n avel bysies, rag ensample '42'</div>";
        niver = -99;
        document.getElementById("kystmesaj").innerHTML = output;        
    }
    else {
        niver = parseFloat(g);
        this.nivergwrys += 1;
    }
    document.getElementById("kwizgorthyp").reset();
    document.getElementById("gorthyp").focus()
    console.log(niver);
    if (niver !== -99) {
        kewarder = this.chekkGorthyp(niver, this.gorthypkewar);
        if (kewarder[0]) {
        // correct answer
        d = new Date();
        t = d.getTime() - this.starttime;
        t = t / 1000;
        /* increment total points by at least 1 point
         * and up to an extra 1 point for speed */
        this.poyntys += Math.max((10.0-t)/10.0, 0) + 1;
        this.niverewn += 1;
        tekst = `<div class='kystmesajgorthyptekst'><span>${this.gorthyptekst}</span><span>${this.gorthypbys}</span></div>${kewarder[1]}<div class='kystmesajresults'><span class='kystmesajtime'>${t.toFixed(1)}s</span><span class='kystmesajniver'>${this.niverewn}/${this.nivergwrys}</span><span class='kystmesajpoyntys'>sommenn poyntys = ${this.poyntys.toFixed(2)}</span></div>`;
        fcolour = "dark green";
        }
    else {
        // if the answer was wrong
    tekst = `<div class='kystmesajgorthyptekst'><span>${this.gorthyptekst}</span><span>${this.gorthypbys}</span></div>${kewarder[1]}<div class='kystmesajresults'><span class='kystmesajniver'>${this.niverewn}/${this.nivergwrys}</span><span class='kystmesajpoyntys'>sommenn poyntys = ${this.poyntys.toFixed(2)}</span></div>`;
    fcolour = "dark red";        
    }
    document.getElementById("kystmesaj").innerHTML = tekst;
    document.getElementById("kystmesaj").style.color = fcolour;
    /*  go to next question */    
    if (this.nivergwrys < this.Ngovynn) {
        // ask next question
        this.gorthypkewar = this.govynn1();             
    }
    else {
        // finish if the required number of questions have been asked  
        this.gorfenna();
        }
    }
}

bonuspoyntys(bonus=5) {
    /* points bonus for getting all correct */
    this.poyntys += bonus;    
} 

gorfenna() {
/* give report of user's number correct, and score */
    var bonusmsg, endmsg;
    if (this.niverewn === this.Ngovynn) {
        this.bonuspoyntys();
        bonusmsg = "<div class='kystmesajpubewn'><span>Keslowena!</span><span>Ty a worthybis pub govynn yn ewn.</span><p>Bonus a bymp poynt yw genes!</p></div>";
    }
    else if (this.niverewn === 0){
        bonusmsg = "<div class='kystmesajpubkamm'><span>Truan!</span><span>Ty a worthybis pub govynn yn kamm!</span><p>Martesen kath a gerdhas a-dro dha vysowek!</p></div>";
    }
    else {
        bonusmsg = "";
    }
    endmsg = `<div class='kystmesajend'>Ty a wrug ${this.niverewn} kewar a ${this.Ngovynn}. ${bonusmsg}Dha skor yw ${this.poyntys.toFixed(2)} a boyntys</div>`;
    document.getElementById('govynn').innerHTML = "<em>Chanj an dewisow mar mynn'ta ha gwask 'Dalleth' dhe wul an kwiz arta!</em>";    
    document.getElementById("kystmesaj").innerHTML = endmsg;    
    
}

dalleth() {
    /* clear answer box, and reset parameters */
    document.getElementById("gorthyp").innerHTML = "";
    document.getElementById("kystmesaj").innerHTML = "";
    document.getElementById("gorthyp").focus()
    this.niverewn = 0;
    this.nivergwrys = 0;
    this.poyntys = 0;
    this.Ngovynn = 20;
    this.gorthypkewar = this.govynn1();
}
}
function setKaletterjs(kwiz) {
    const rbs = document.querySelectorAll('input[name="kaletter"]');
    let kaletter;
    for (const rb of rbs) {
        if (rb.checked) {
            kaletter = parseInt(rb.value);
            console.log("kaletter: "+kaletter+" "+kwiz.kaletter_text[kaletter]);
            break;
        }
    }    
    kwiz.kaletter = kaletter;
}
function setOberyansjs(kwiz)
{
    const rbs = document.querySelectorAll('input[name="ober"]');
    let ober;
    for (const rb of rbs) {
        if (rb.checked) {
            ober = parseInt(rb.value);
            console.log("oberyans: " + ober+" "+kwiz.oberyans_text[ober]);
            break;
        }
    }    
    kwiz.oberyans = ober;
}
kwiz = new KwizAwgrym();
