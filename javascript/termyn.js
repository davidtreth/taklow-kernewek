/*  David Trethewey
 based on termyn.py
 ported to Javascript October 2020
*/
class Gorhemmyn {    
    // what time to change the greeting
    /* static class fields are a fairly new feature 
     * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
     * so put into contructor instead 
    static bora = 3;
    static myttin = 7;
    static dydh = 11;
    static dohajydh = 14;
    static gorthugher = 18;
    static nos = 23;
    */
    constructor() {
        var bora = 3;
        var myttin = 7;
        var dydh = 11;
        var dohajydh = 14;
        var gorthugher = 18;
        var nos = 23;        
        var t = new Date();
        var our = t.getHours();
        this.gorhemmyn = "Dydh da"; // default
        console.log(nos)
        if ((our >= nos) || (our < bora)) {
            this.gorhemmyn = "Nos da";
            }
        if ((our >= bora) && (our < myttin)) {
            this.gorhemmyn = "Bora da";
            }
        if ((our >= myttin) && (our < dydh)) {
            this.gorhemmyn = "Myttin da";
            }
        if ((our >= dydh) && (our < dohajydh)) {
            this.gorhemmyn = "Dydh da";
            }
        if ((our >= dohajydh) && (our < gorthugher)) {
            this.gorhemmyn = "Dohajydh da";
            }
        if ((our >= gorthugher) && (our < nos)) {
            this.gorhemmyn = "Gorthugher da";
            }
        }
   }         
            
var misyow = {0:"Genver",
          1:"Hwevrer",
          2:"Meurth",
          3:"Ebrel",
          4:"Me",
          5:"Metheven",
          6:"Gortheren",
          7:"Est",
          8:"Gwynngala",
          9:"Hedra",
          10:"Du",
          11:"Kevardhu"};

var dydhyow = {1:"Dy' Lun",
           2:"Dy' Meurth",
           3:"Dy' Mergher",
           4:"Dy' Yow",
           5:"Dy' Gwener",
           6:"Dy' Sadorn",
           0:"Dy' Sul"};

function termyn_approx(hour, minute) {
    var hoursfrac = hour + minute/60.0;
    var hourint = 0;
    var termyn = "";
    hoursfrac *= 4.0;
    hoursfrac = Math.round(hoursfrac);
    hoursfrac /= 4.0;
    console.log(hoursfrac);
    hourint = Math.floor(hoursfrac);
    if (hoursfrac % 1 === 0) {
        termyn = get_hour(hourint, 0);
    }
    if (hoursfrac % 1 === 0.25) {
        termyn = "kwarter wosa "+ get_hour(hourint, 0);
    }
    if (hoursfrac % 1 === 0.5) {
        termyn = "hanter wosa "+ get_hour(hourint, 0);
    }
    if (hoursfrac % 1 === 0.75) {
        termyn = "kwarter dhe "+ mutate(get_hour(hourint+1,0),2)
    }
    return termyn;
}

function get_hour(hour, minute) {
    var h = "";
    var hour12 = 0;
    var ampm = "";
    if (hour % 24 === 0) {
        h = "hanternos";
    }
    else if (hour === 12) {
        h = "hanterdydh";
    }
    else {
        hour12 = hour % 12;
        if (hour < 12) {
            ampm = " myttinweyth";
        }
        else if (hour < 18) {
            ampm = " dohajydhweyth";
        }
        else {
            ampm = " gorthugherweyth";
        }
        h = numberkw_noun(hour12, "eur", fem=true) + ampm;
/* I considered only using "eur" on the quarter hours
   but decided not to for the time being
          if ([0,15,30,45].indexOf(minute) !== -1) {
             h = .numberkw(hour12) + " eur" + ampm;
         }
          else {
             h = numberkw(hour12) + ampm;
         }
          */
        }
    return h;
}

function termyn_exact(hour, minute) {
    var termyn = "";
    if (minute === 0) {
        termyn = get_hour(hour, minute);
    }
    else if (minute === 15) {
        termyn = "kwarter wosa " + get_hour(hour, minute);
    }
    else if (minute === 30)  {
        termyn = "hanter wosa "+ get_hour(hour, minute);
    }
    else if (minute === 45) {
        termyn = "kwarter dhe "+ mutate(get_hour(hour+1, minute),2);
    }
    else {
        if (minute < 30) {
            termyn = numberkw_noun(minute, "mynysenn", fem=true) + " wosa " + get_hour(hour, minute);
        }
        else {
            termyn = numberkw_noun(60-minute, "mynysenn", fem=true) + " dhe " + mutate(get_hour(hour+1, minute),2);
            }
        }
    return termyn;
}
    
function dydhyas(timenow, blydhen = false) {
    var wday, mday, mon, yr;
    wday = dydhyow[timenow.getDay()];
    mday = numberkw_ord(timenow.getDate());
    mon = misyow[timenow.getMonth()];    
    if (blydhen) {
        yr = timenow.getFullYear();
        date_kw = wday + " " + mday + " mis-"+mon+" "+yr.toString();
        }
    else {
        date_kw = wday + " " + mday + " mis-"+mon;
        }
    if ((timenow.getDate() === 5) && (timenow.getMonth() === 3)) {
        date_kw += "<br><span>Dydh Gool Peran Lowen!</span>"
    }
    return date_kw;
}

function refreshTermynDydhyas() {
    var timenow = new Date();
    if (args.dydh) {
        if (args.blydhen) {
            date_kw = dydhyas(timenow,blydhen=true);
        }
    else {
            date_kw = dydhyas(timenow);
        }
        console.log(date_kw);
        $("#datekw").text(date_kw);
    }

    if ((args.nes) || (args.kewar)) {
        var h = timenow.getHours();
        var m = timenow.getMinutes();
        var timestr = ("0"+h.toString()).slice(-2) + ":" + ("0"+m.toString()).slice(-2);
        console.log(timestr);
        $("#timefigs").text(timestr);
        if (args.nes) {
            var timeapprox = termyn_approx(timenow.getHours(), timenow.getMinutes());
            timeapprox = timeapprox.charAt(0).toUpperCase() + timeapprox.slice(1);
            console.log(timeapprox);
            $("#timeapprox").text(timeapprox);
        }
    if (args.kewar) {
        var timeexact = termyn_exact(timenow.getHours(), timenow.getMinutes());
        timeexact = timeexact.charAt(0).toUpperCase() + timeexact.slice(1);
        console.log(timeexact);
        $("#timeexact").text(timeexact);
        }
    if (args.gorhemmyn) {
        var gorhemmyn = new Gorhemmyn();
        console.log(gorhemmyn.gorhemmyn);
        $("#gorhemmyn").text(gorhemmyn.gorhemmyn);
        }
    }    
    
}
var args = {dydh: true,
            blydhen: true,
            nes: true,
            kewar: true,
            gorhemmyn: true};
                
$(document).ready(function()
{
    refreshTermynDydhyas();
    setInterval(refreshTermynDydhyas, 1000);        
});    
