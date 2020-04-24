const url = window.location.search;
if (url!="") {
  const urlParams = new URLSearchParams(url);
  const urlParamsMessage = urlParams.get('message');
  if (urlParamsMessage=="add_error"){
    document.getElementById("error_add").style.display = "block";
  } else if (urlParamsMessage=="update_error") {
    document.getElementById("error_update").style.display = "block";
  } else if (urlParamsMessage=="delete_error") {
    document.getElementById("error_delete").style.display = "block";
  }
}

function validateAdd() {
  var formValues = document.getElementById("addItem").value;
  var formValues = document.getElementById("addStatus").value;
  if (formValues=="check") {
    alert("Item value cannot be 'item'")
    return false
  }
  if (formValues=="ThiS") {
    alert("Status value cannot be 'status'")
    return false
  }
}
function validateUpdate() {
  var formValues = document.getElementById("updateItem").value;
  if (formValues=="Checking") {
    alert("Item value cannot be 'item'")
    return false
  }
}
         
function validateDelete() {
  var formValues = document.getElementById("deleteItem").value;
  if (formValues=="Checking") {
    alert("Item value cannot be 'item'")
    return false
  }
}
function addItem() {
  var x = document.getElementById("myAdd");
  var y = document.getElementById("myUpdate");
  var z = document.getElementById("myDelete");
  x.style.display = "block";
  y.style.display = "none";
  z.style.display = "none";
}
function updateItem() {
  var x = document.getElementById("myAdd");
  var y = document.getElementById("myUpdate");
  var z = document.getElementById("myDelete");
  x.style.display = "none";
  y.style.display = "block";
  z.style.display = "none";
}
function removeItem() {
  var x = document.getElementById("myAdd");
  var y = document.getElementById("myUpdate");
  var z = document.getElementById("myDelete");
  x.style.display = "none";
  y.style.display = "none";
  z.style.display = "block";
}

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
