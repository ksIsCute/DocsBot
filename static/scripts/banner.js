function bannerclose() {
  var item = document.getElementById("banner");
  item.classList.toggle("close");
  setTimeout(() => {
    item.remove()
  }, 550)
}
function bouncearrow() {
  document.getElementById("arrow").classList.toggle("bounce")
}