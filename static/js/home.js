// Select all body cells and assign a click action detector to all
// Highlight selected elements and change their class value

let ready2download = [];

function clickFunction(e, data) {
  if (e.className.includes("selected")) {
    e.style.backgroundColor = "";
    e.classList.remove("selected");

    // Filters out the un-selected element from the array
    ready2download = ready2download.filter(function (el) {
      return !~el.indexOf(data[1]);
    });
  } else {
    e.style.backgroundColor = "#E0BBE4";
    e.classList.add("selected");
    ready2download.push([data[0][0], data[1], data[2]]);
  }

  toggle_download_button();
  toggle_clear_button();
}

// Selecting all in one column
function selectAll(e) {
  let allChildren = e.parentNode.getElementsByTagName("tbody")[0].rows;
  for (let i of allChildren) {
    i.onclick.apply(i);
  }
}

// Modding status of download button
let download_button = document.getElementById("download-button");
download_button.addEventListener("click", displayPrompt);
function toggle_download_button() {
  if (ready2download.length != 0) {
    download_button.classList.remove("btn-outline-danger", "disabled");
    download_button.classList.add("btn-danger");
  } else {
    download_button.classList.add("btn-outline-danger", "disabled");
  }
}

// Modding status of cookie preset button
let preset_button = document.getElementById("preset-button");
preset_button.addEventListener("click", displayPresetForm);

let preset_form = document.getElementById("preset-form");

function displayPrompt() {
  // Modal Form
  let modal_body = document.getElementById("modal-table-body");
  text = "";
  for (let i of ready2download) {
    text += `  <tr>
    <th scope="row">${ready2download.indexOf(i) + 1}</th>
    <td>${i[0]}</td>
    <td>${i[2]}</td>
  </tr>`;
  }
  modal_body.innerHTML = text;

  // Preset Button - hide on condition
  if (ready2download.length < 2) {
    preset_button.classList.add("d-none");
  } else {
    preset_button.classList.remove("d-none");
    preset_form.classList.add("d-none");
  }
}

// Called when Preset Button Clicked
function displayPresetForm() {
  preset_button.classList.add("d-none");
  preset_form.classList.remove("d-none");
}

// Preset + button
let preset_add_button = document.getElementById("preset-add");
preset_add_button.addEventListener("click", savePreset);

// Preset input form
let preset_name = document.getElementById("preset-name");
preset_name.onkeydown = function (e) {
  if (window.event.keyCode == "13") {
    savePreset();
  }
};

function savePreset() {
  // Save Cookie with name if no error
  if (preset_name.value.trim() == "") {
    alert("Empty names are not allowed");
  } else {
    createCookie(preset_name.value, JSON.stringify(ready2download), 365);
    alert("Saved cookie with title: " + String(preset_name.value));
  }

  // Clear form input
  preset_name.value = "";
}

function createCookie(name, value, days) {
  var expires;
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toGMTString();
  } else {
    expires = "";
  }
  document.cookie =
    name.replace(/\s/g, "_") + "=" + value + expires + "; path=/";
}

//Triggering download on click
function initDownload() {
  let interval = setInterval(download, 1500, ready2download);

  function download(urls) {
    let url = urls.pop();

    let a = document.createElement("a");
    dl_text = url[0] + "_" + url[2] + "_Restore.ipsw";
    a.download = dl_text;
    console.log(dl_text);
    a.setAttribute("href", url[1]);
    a.setAttribute("target", "_parent");
    a.click();

    if (urls.length == 0) {
      clearInterval(interval);
      clrAll();
    }
  }
}

// Clear All-Button
let clear_button = document.getElementById("clear-button");
clear_button.addEventListener("click", clrAll);

function toggle_clear_button() {
  if (ready2download.length != 0) {
    clear_button.classList.remove("d-none");
  } else {
    clear_button.classList.add("d-none");
  }
}

function clrAll() {
  ready2download = [];
  toggle_download_button();
  toggle_clear_button();

  let table = document.querySelectorAll("tr");
  table.forEach(function (e) {
    e.style.backgroundColor = "";
    e.classList.remove("selected");
  });
}

// disable text selection on page
document.onselectstart = function () {
  return false;
};
