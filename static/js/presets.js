// called at start
function getLocalStorage() {
  // Split local storage and get all individual name=value pairs in an array
  let deviceArr = Object.keys(localStorage);

  let cleaned_list = {};
  for (let i of deviceArr) {
    let temp = localStorage.getItem(i).split("=");
    let list_of_devices = JSON.parse(temp[0]);

    // Code to deal with Browser Extensions injecting JS
    if (Object.prototype.toString.call(list_of_devices) == "[object Array]") {
      cleaned_list[i.trim()] = list_of_devices;
    }
  }
  // console.log(cleaned_list);
  return cleaned_list;
}

drawChart();

function drawChart() {
  cleaned_list = getLocalStorage();
  let text = "";
  if (Object.keys(cleaned_list).length !== 0) {
    // Modding html with cookie name and length of the cookie list
    let preset_chart = document.getElementById("preset_chart");

    for (let key in cleaned_list) {
      var value = cleaned_list[key];

      text += `
           <a class="list-group-item list-group-item-action" onclick="clickFunction(this)" data-toggle="modal" data-target="#confirm-Modal" role="button" aria-disabled="true" >
                 ${key}
               <span class="badge badge-primary badge-pill ml-2"> ${value.length} </span>
           </a>
         `;
    }
  } else {
    text += ` <h4> No presets saved... </h4> `;
  }
  preset_chart.innerHTML = text;
}

// clicking desired preset
function clickFunction(e) {
  let text = "";

  // getting the name of the cookie from inner text
  target = e.text.split("\n")[1].trim();

  // Displaying modal with Name of item
  let count = 0;
  for (let device of cleaned_list[target]) {
    text += `<tr>
       <th scope="row"> ${count + 1}</th>
       <td>${device["name"].replaceAll("/", "<br>")}</td>
       <td>${device["firmware"]}</td>
     </tr>`;
    count++;
  }
  let modal_body = document.getElementById("modal-table-body");
  modal_body.innerHTML = text;
}

//Triggering download on click
function initDownload() {
  let array_copy = [...cleaned_list[target]];
  let interval = setInterval(download, 1500, array_copy);

  function download(urls) {
    let url = urls.pop();

    let a = document.createElement("a");
    a.setAttribute("href", url["url"]);
    a.setAttribute("target", "_parent");
    a.click();

    if (urls.length == 0) {
      clearInterval(interval);
    }
  }
}

function deleteCookie() {
  localStorage.removeItem(target);
  drawChart();
}
