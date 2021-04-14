window.addEventListener("resize", resizeFunction);
var mq = window.matchMedia("(max-width:1200px)");

var i;
x = document.getElementsByClassName("navbar")[0];
b1 = document.getElementsByClassName("brand-logo1")[0];
b2 = document.getElementsByClassName("brand-logo2")[0];

function resizeFunction() {
    if (!mq.matches) {
        window.onscroll = function () {
            scrollFunction();
        };
        function scrollFunction() {
            if (
                document.body.scrollTop > 60 ||
                document.documentElement.scrollTop > 60
            ) {
                x.classList.remove("navbar-dark");
                x.classList.add("navbar-light");
                x.classList.add("floatingNav");
                x.style.backgroundColor = "white";
                document.getElementById("menu-icon").style.color = "black";
                b2.classList.add("d-inline-block");
                b1.classList.add("d-none");
                b1.classList.remove("d-inline-block");
                b2.classList.remove("d-none");
            } else {
                x.classList.remove("navbar-light");
                x.classList.add("navbar-dark");
                x.classList.remove("floatingNav");
                x.style.backgroundColor = "transparent";
                document.getElementById("menu-icon").style.color = "white";
                b1.classList.add("d-inline-block");
                b2.classList.add("d-none");
                b2.classList.remove("d-inline-block");
                b1.classList.remove("d-none");
            }
        }

        scrollFunction();
    } else {
        window.onscroll = function () {
            scrollFunction();
        };

        function scrollFunction() {
            if (
                document.body.scrollTop > 60 ||
                document.documentElement.scrollTop > 60
            ) {
                x.classList.remove("navbar-dark");
                x.classList.add("navbar-light");
                x.classList.add("floatingNav");
                x.style.backgroundColor = "white";
                document.getElementById("menu-icon").style.color = "black";
                b2.classList.add("d-inline-block");
                b1.classList.add("d-none");
                b1.classList.remove("d-inline-block");
                b2.classList.remove("d-none");
            } else {
                x.classList.remove("navbar-light");
                x.classList.add("navbar-dark");
                x.classList.remove("floatingNav");
                x.style.backgroundColor = "#00171f";
                document.getElementById("menu-icon").style.color = "white";
                b1.classList.add("d-inline-block");
                b2.classList.add("d-none");
                b2.classList.remove("d-inline-block");
                b1.classList.remove("d-none");
            }
        }

        scrollFunction();
    }
}

resizeFunction();
