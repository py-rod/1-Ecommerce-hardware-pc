document.addEventListener("DOMContentLoaded", function () {
    var navbar = document.querySelector("#header .header-nav");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 0) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });
});