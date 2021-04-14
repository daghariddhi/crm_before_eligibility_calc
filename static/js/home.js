window.addEventListener("resize", resizeFunction);
var mq = window.matchMedia("(max-width:1200px)");
landtext = document.getElementsByClassName("landing-title")[0];
landsub = document.getElementsByClassName("landing-subtitle")[0];
landvec = document.getElementsByClassName("landing-vector")[0];

var land_text = ["Demo Text one", "Demo Text two", "Demo Text three"];
var landsub_text = [
    "long lorem epsum dolor one",
    "long lorem epsum dolor two",
    "long lorem epsum dolor three",
];
var vec_loc = [
    "assets/images/gamer-colour.svg",
    "assets/images/handshake-colour.svg",
    "assets/images/revenue-graph-colour.svg",
];

var i;
var counter = 0;

setInterval(function () {
    landtext.innerHTML = land_text[counter];
    landsub.innerHTML = landsub_text[counter];
    landvec.src = vec_loc[counter];

    counter++;
    if (counter >= 3) {
        counter = 0;
    }
}, 5000);

function resizeFunction() {
    if (!mq.matches) {
        landtext.classList.remove("display-4");
        landtext.classList.add("display-3");
        landsub.style.fontSize = "1.5rem";
    } else {
        landtext.classList.add("display-4");
        landtext.classList.remove("display-3");
        landsub.style.fontSize = "1rem";
    }
}

resizeFunction();

function closeMenu() {
    document.getElementById("navbar").style.width = "0%";
    document.getElementsByTagName("BODY")[0].style.backgroundColor = "";
}
function openMenu() {
    document.getElementById("navbar").style.width = "20vw";
}

var accordions = document.getElementsByClassName("accordion");

for (var i = 0; i < accordions.length; i++) {
    accordions[i].onclick = function () {
        this.classList.toggle("is-open");

        var content = this.nextElementSibling;
        if (content.style.maxHeight) {
            // accordion is currently open, so close it
            content.style.maxHeight = null;
        } else {
            // accordion is currently closed, so open it
            content.style.maxHeight = content.scrollHeight + "px";
        }
    };
}

$(".count").counterUp({
    delay: 50,
    time: 2000,
});
