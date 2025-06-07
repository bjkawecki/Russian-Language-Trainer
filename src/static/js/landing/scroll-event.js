window.addEventListener("scroll", (event) => {
    let scroll = this.scrollY;
    if (scroll > 10) {
        document.getElementById("landingheader").classList.add("border-b", "border-gray-100", "dark:border-gray-700");
    } else {
        document.getElementById("landingheader").classList.remove("border-b", "border-gray-100", "dark:border-gray-700");
    }
});
