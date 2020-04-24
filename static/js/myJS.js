

function showSchedule() {
  var x = document.getElementById("mySchedule");
  var y = document.getElementById("myButton");
  if (x.style.display === "none") {
    x.style.display = "block";
    y.style.display = "none"
  } else {
    x.style.display = "none";
  }
}
