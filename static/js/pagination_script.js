window.onload = (event) => {

    let buttons = document.querySelectorAll(".page-item")
    //
    // for (let i = 1; i < buttons.length - 1; i++) {
    //     let link = buttons[i].querySelector(".page-link")
    //     link.innerHTML = i.toString()
    //     link.href = "/" + i
    // }

    // buttons[0].addEventListener("click", update_pagination)
    buttons[4].addEventListener("click", shift_right)

};

function shift_right() {
   let buttons = document.querySelectorAll(".page-item")

    for (let i = 1; i < buttons.length - 1; i++) {
        let link = buttons[i].querySelector(".page-link")
        link.innerHTML = parseInt(link.textContent) + 1
        link.href = "/" + link.textContent
    }
}