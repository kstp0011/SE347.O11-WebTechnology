function switchTheme() {
    var body = document.body;
    // Switch between themes
    body.classList.toggle("dark-theme");

    // Save theme preference in local storage
    if (body.classList.contains("dark-theme")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}