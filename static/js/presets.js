console.dir(document.domain);

console.log(document.URL);
console.log(document.title);
document.title = "Hi";

// console.log(document.getElementById("list"));

// get by class name
var chart_elements = document.getElementsByClassName("list-group-item");

// Selecting first element to bold
// chart[0].style.fontWeight = "bold";

// // Changing all elements - normally
// for (var i = 0; i < chart.length; i++) {
//   chart[i].style.fontWeight = "bold";
// }

// for each - easier
for (let i of chart_elements) {
  i.style.fontWeight = "bold";
}

var ch = document.querySelector(".list-group");

console.log(ch.children);

// Dynamically adding element
var newButton = document.createElement("div");
newButton.className = "download";

console.log(newButton);
