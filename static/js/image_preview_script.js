
window.onclick = (event) => {
  let id_avatar = document.getElementById("id_avatar")
  id_avatar.onchange = evt => {
    const [file] = id_avatar.files
    if (file) {
      preview.src = URL.createObjectURL(file)
      preview.style.display = 'inline'
    }
  }

};