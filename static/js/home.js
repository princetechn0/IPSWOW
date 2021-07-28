// Select all body cells and assign a click action detector to all
// Highlight selected elements and change their class value

var ready2download = [];
var toDownload = [];

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
  var allChildren = e.parentNode.getElementsByTagName("tbody")[0].rows;
  for (let i of allChildren) {
    i.onclick.apply(i);
  }
}

// Modding status of download button
var download_button = document.getElementById("download-button");
function toggle_download_button() {
  if (ready2download.length != 0) {
    download_button.classList.remove("btn-outline-danger", "disabled");
    download_button.classList.add("btn-danger");
  } else {
    download_button.classList.add("btn-outline-danger", "disabled");
  }
}

download_button.addEventListener("click", displayPrompt);
function displayPrompt() {
  var warning =
    ready2download.length +
    " tab(s) will be opened. \n Javascript is a bit tricky when it comes to downloading large files.";
  var modal_output = document.getElementById("modal-table-body");

  text = "";
  for (let i of ready2download) {
    text += `  <tr>
    <th scope="row">${ready2download.indexOf(i) + 1}</th>
    <td>${i[0]}</td>
    <td>${i[2]}</td>
  </tr>`;
  }
  modal_output.innerHTML = text;

  var modal_footer = document.getElementById("modal-table-footer");
  modal_footer.innerHTML = `
  <span class="mx-auto w-100"> FYI: ${ready2download.length} files will be downloaded</span>
  <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
  <button type="button" class="btn btn-primary" data-dismiss="modal" onclick="initDownload()">Download!</button>
  `;
}

//Triggering download on click
function initDownload() {
  var interval = setInterval(download, 1000, ready2download);

  function download(urls) {
    var url = urls.pop();

    var a = document.createElement("a");
    // a.setAttribute("download", url[0][0] + "_" + url[2] + "_Restore.ipsw");
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
var clear_button = document.getElementById("clear-button");
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

  var table = document.querySelectorAll("tr");
  table.forEach(function (e) {
    e.style.backgroundColor = "";
    e.classList.remove("selected");
  });
}

// disable text selection on page
document.onselectstart = function () {
  return false;
};
