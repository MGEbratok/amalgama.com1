const changeThemeBut = document.getElementById("change-theme-but")

changeThemeBut.addEventListener("click", function(){
    document.body.classList.toggle("change-theme")

    const theme = localStorage.getItem("theme")
    console.log(theme)
    localStorage.setItem("theme", "change theme")
})