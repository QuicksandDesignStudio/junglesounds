let player;
let tableBody;
let marking;
let playing = false;
let tagging = false;
let hadlingKeyPress = true;
let rowCount = 0;
let tags = [];
let categories = [];
let BASE_URL = "http://127.0.0.1:5000/api/";
let API_ENDPOINTS = {
  categories: "categories"
};

let currentTagDetails = {
  startTime: 0.0,
  endTime: 0.0,
  tag: null
};

let keys = {
  space: 32,
  s: 83,
  front: 39,
  back: 37
};

$(document).ready(function() {
  player = $("#player")[0];
  tableBody = $("#tag_table");
  marking = $("#marking");
  $(document).keyup(function(e) {
    HandleKeyPress(e.which);
  });
  $("body").focus(function(e) {
    hadlingKeyPress = true;
    console.log("here");
  });
  //get categories
  $.get(BASE_URL + API_ENDPOINTS.categories, function(data, response) {
    categories = data["categories"];
  });
});

function HandleKeyPress(keycode) {
  if (hadlingKeyPress) {
    switch (keycode) {
      case keys.space:
        if (!playing) {
          playing = true;
          player.play();
        } else {
          playing = false;
          player.pause();
        }
        break;
      case keys.front:
        player.currentTime += 0.5;
        break;
      case keys.back:
        player.currentTime -= 0.5;
        break;
      case keys.s:
        if (!tagging) {
          tagging = true;
          currentTagDetails.startTime = player.currentTime;
          marking.css("opacity", "1");
        } else {
          tagging = false;
          marking.css("opacity", "0");
          if (currentTagDetails.startTime != player.currentTime) {
            currentTagDetails.endTime = player.currentTime;
            AddTag();
          }
        }
    }
  }
}

function AddTag() {
  $("#tag_table:last-child").append(
    getTagRow(
      rowCount,
      currentTagDetails.startTime,
      currentTagDetails.endTime,
      currentTagDetails.tag
    )
  );
  SetupValues(
    rowCount,
    currentTagDetails.startTime,
    currentTagDetails.endTime,
    currentTagDetails.tag
  );
  tags.push($(`#${rowCount}`));

  rowCount++;
  SetupFocusEvents();
}

function SetupValues(rowCount, startTime, endTime, tag) {
  $(`#${rowCount}_start_time`).val(startTime);
  $(`#${rowCount}_end_time`).val(endTime);
}

function SetupFocusEvents(elementId) {
  for (let i = 0; i < tags.length; i++) {
    $(`#${i}_start_time`).focus(function() {
      hadlingKeyPress = false;
    });
    $(`#${i}_start_time`).focusout(function() {
      hadlingKeyPress = true;
    });
    $(`#${i}_end_time`).focus(function() {
      hadlingKeyPress = false;
    });
    $(`#${i}_end_time`).focusout(function() {
      hadlingKeyPress = true;
    });
  }
}

function DeleteRow(rowId) {
  console.log(`Delete Row : ${rowId}`);
  let index = -1;
  for (let i = 0; i < tags.length; i++) {
    if (rowId == parseInt(tags[i].attr("id"))) {
      index = i;
    }
  }

  tags.splice(index, 1);

  for (let i = 0; i < tags.length; i++) {
    let currentTag = tags[i];
    let currentTagId = currentTag.attr("id");
    currentTag.attr("id", i);
    $(`#${currentTagId}_start_time`).attr("id", `${i}_start_time`);
    $(`#${currentTagId}_start_time`).attr("name", `${i}_start_time`);
    $(`#${currentTagId}_end_time`).attr("id", `${i}_end_time`);
    $(`#${currentTagId}_end_time`).attr("name", `${i}_end_time`);
    $(`#${currentTagId}_tag`).attr("id", `${i}_tag`);
    $(`#${currentTagId}_row_tag`).text(i + 1);
    $(`#${currentTagId}_row_tag`).attr("id", `${i}_row_tag`);
    $(`#${currentTagId}_delete`).attr("onclick", `DeleteRow(${i})`);
    $(`#${currentTagId}_delete`).attr("id", `${i}_delete`);
  }

  $(`#${rowId}`).remove();
  rowCount--;
  SetupFocusEvents();
}

function getTagRow(rowCount, startTime, endTime, tag) {
  let tableRow = `<tr id="${rowCount}">
    <th id="${rowCount}_row_tag" scope="row">${rowCount + 1}</th>
    <td>
        <div class="input-group mb-3">
            <input
            type="text"
            class="form-control"
            placeholder="${startTime}"
            id="${rowCount}_start_time"
            name="${rowCount}_start_time"
            />
        </div>
    </td>
    <td>
        <div class="input-group mb-3">
            <input
            type="text"
            class="form-control"
            placeholder="${endTime}"
            id="${rowCount}_end_time"
            name="${rowCount}_end_time"
            />
        </div>
    </td>
    <td>
      <select class="custom-select" id="${rowCount}_tag">
        <option selected="true" disabled="disabled">Choose</option>
        ${GetCategories()}
      </select>
    </td>
    <td>
      <button type="button" class="btn btn-danger" id="${rowCount}_delete" onclick="DeleteRow(${rowCount})">Delete</button>
    </td>
  </tr>`;
  return tableRow;
}

function GetCategories() {
  allCategories = "";
  categories.forEach(function(category) {
    allCategories += `<option value="${category["id"]}">${category["category"]}</option>`;
  });
  return allCategories;
}

function Submit() {
  if (tags.length > 0) {
    let submissionTags = [];
    submissionTags.push({ wav_name: "some.wav" });
    for (let i = 0; i < tags.length; i++) {
      let start_time = $(`#${i}_start_time`).val();
      let end_time = $(`#${i}_end_time`).val();
      let tag = $(`#${i}_tag`).val();
      submissionTags.push({
        start_time: `${start_time}`,
        end_time: `${end_time}`,
        tag: `${tag}`
      });
    }
    console.log(submissionTags);
  } else {
    alert("You don't have any tags to submit");
  }
}
