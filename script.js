const darkModeBtn = document.getElementById("darkModeBtn");

darkModeBtn.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
});

// Logic cho menu trên di động
const menuBtn = document.querySelector(".menu-btn");
const navLinks = document.querySelector(".navbar ul");

menuBtn.addEventListener("click", () => {
    navLinks.classList.toggle("show");
});