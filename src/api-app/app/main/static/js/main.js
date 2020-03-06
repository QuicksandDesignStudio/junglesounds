/*
This is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

Copyright (c) 2020 Romit Raj
Copyright (c) 2020 Thejesh GN
*/

let player;
let tableBody;
let submitModal;

let userId = 1; //debug
let rowCount = 0;

let playing = false;
let tagging = false;
let hadlingKeyPress = true;
let submitting = false;

let tags = [];
let categories = [];

let BASE_URL = "http://127.0.0.1:5000/api/";

let API_ENDPOINTS = {
  categories: "categories",
  samples: "samples",
  sample: "sample",
  download: "download",
  classifications: "classifications"
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

let sampleParameters = {
  totalNumberOfSamples: 0,
  totalNumberOfPages: 0,
  activeSamples: [],
  activeSampleIndex: -1,
  activePage: -1
};

$(document).ready(function() {
  //show the modal
  $("#submitmodal").modal("show");

  //element references
  player = $("#player")[0];
  tableBody = $("#tag_table");
  submitModal = $("#submitmodal");

  //get categories
  $.get(BASE_URL + API_ENDPOINTS.categories, function(data, response) {
    categories = data["categories"];
  });

  //get 1st set of samples
  LoadSamplePagePriority(0, 1);

  //setup key presses
  $(document).keyup(function(e) {
    HandleKeyPress(e.which);
  });
});

//Try and load samples with 0 reviews first
/*
Needs Update : This is a problematic way to implement this because once all the useful samples have been reviewed, 
this will keep loading the same unreviewed stuff again and again
*/
function LoadSamplePagePriority(reviewNumber, pageNumber) {
  //get all sounds files in page
  $.ajax({
    url: BASE_URL + API_ENDPOINTS.samples,
    type: "get",
    data: {
      no_of_reviews: reviewNumber,
      per_page: 2,
      page: pageNumber
    },
    success: function(response) {
      if (reviewNumber == 0 && response["samples"].length == 0) {
        //there are no samples left with 0 response
        LoadSamplePage(pageNumber);
      } else {
        //there are some samples with 0 responses
        SetupSampleParameters(response);
      }
    },
    error: function(xhr) {
      console.log(xhr);
    }
  });
}

//Try and load samples without caring about numebr of reviews
function LoadSamplePage(pageNumber) {
  //get all sounds files in page
  $.ajax({
    url: BASE_URL + API_ENDPOINTS.samples,
    type: "get",
    data: {
      per_page: 2,
      page: pageNumber
    },
    success: function(response) {
      SetupSampleParameters(response);
    },
    error: function(xhr) {
      console.log(xhr);
    }
  });
}

//Setup current state tracker of samples
function SetupSampleParameters(response) {
  sampleParameters.totalNumberOfSamples = response["pagination"].total;
  sampleParameters.totalNumberOfPages = response["pagination"].pages;
  sampleParameters.activePage = response["pagination"].page;
  sampleParameters.activeSamples = response["samples"];
  sampleParameters.activeSampleIndex = 0;

  //setup first audio file
  SetupAudio(
    sampleParameters.activeSamples[sampleParameters.activeSampleIndex]
  );
}

//Setup Audio
function SetupAudio(currentSample) {
  //take a couple of seconds - this can get annoying - to be reviewed
  setTimeout(function() {
    let soundSrc =
      BASE_URL + API_ENDPOINTS.download + `/${currentSample.sample_file_name}`;
    console.log(`Loading audio file : ${soundSrc}`);
    player.src = soundSrc;
    player.load();

    //add load event
    player.onloadeddata = function() {
      //reset submit switch
      submitting = false;
      //hide modal if it is there
      $("#submitmodal").modal("hide");
    };
  }, 2000);
}

//Handle Keyboard Shortcuts
function HandleKeyPress(keycode) {
  if (hadlingKeyPress && !submitting) {
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
          $("#tagging_button").attr("src", "img/tagging.png");
          $("#tagging_text").html("Stop Tagging");
        } else {
          tagging = false;
          $("#tagging_button").attr("src", "img/not_tagging.png");
          $("#tagging_text").html("Start Tagging");
          if (currentTagDetails.startTime != player.currentTime) {
            currentTagDetails.endTime = player.currentTime;
            AddTag();
          }
        }
    }
  }
}

//Handle Button presses
function TaggingButtonClick() {
  if (!submitting) {
    if (!tagging) {
      tagging = true;
      currentTagDetails.startTime = player.currentTime;
      $("#tagging_button").attr("src", "img/tagging.png");
      $("#tagging_text").html("Stop Tagging");
    } else {
      tagging = false;
      $("#tagging_button").attr("src", "img/not_tagging.png");
      $("#tagging_text").html("Start Tagging");
      if (currentTagDetails.startTime != player.currentTime) {
        currentTagDetails.endTime = player.currentTime;
        AddTag();
      }
    }
  }
}

//Add a tag to the Tag Table
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

//setup values in the tag rows (placeholders won't work)
function SetupValues(rowCount, startTime, endTime, tag) {
  $(`#${rowCount}_start_time`).val(startTime);
  $(`#${rowCount}_end_time`).val(endTime);
}

//Setup focus events so when a user is editing time etc, the keyboard shortcuts don't work
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

//Callback for deleting a row and doing various array operations to reset the table
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

//get all the categories
function GetCategories() {
  allCategories = "";
  categories.forEach(function(category) {
    allCategories += `<option value="${category["id"]}">${category["category"]}</option>`;
  });
  return allCategories;
}

//Submit Tags
function Submit() {
  if (!submitting) {
    $("#submitmodal").modal("show"); //show the modal
    submitting = true; //switch

    if (tags.length > 0) {
      //do we have tags
      let allSubmissions = [];
      //common elements across all tags
      allSubmissions.push({
        sampleId:
          sampleParameters.activeSamples[sampleParameters.activeSampleIndex].id,
        userId: userId,
        recordedTime:
          sampleParameters.activeSamples[sampleParameters.activeSampleIndex]
            .recorded_time,
        recordedLocation:
          sampleParameters.activeSamples[sampleParameters.activeSampleIndex]
            .recorded_location
      });
      //iterate through tags
      for (let i = 0; i < tags.length; i++) {
        let startTime = parseFloat($(`#${i}_start_time`).val());
        let endTime = parseFloat($(`#${i}_end_time`).val());
        let tag = parseInt($(`#${i}_tag`).val());
        if (!isNaN(tag)) {
          //only add if a tag has been selected
          allSubmissions.push({
            startTime: startTime,
            endTime: endTime,
            tag: tag
          });
        }
      }
      if (allSubmissions.length > 1) {
        //the legnth has to be more than 1, the first element is just the common stuff

        //setup a common callback for all the POST requests
        let requestCallback = new allRequestsCompleted({
          numRequest: allSubmissions.length - 1,
          //single callback for all POST requests
          singleCallback: function() {
            console.log("Loading Next Sample After Submitting Tags");
            LoadNextSample();
          }
        });

        //Iterate through tags and make POST requests
        for (let i = 1; i < allSubmissions.length; i++) {
          $.ajax({
            url: BASE_URL + API_ENDPOINTS.classifications,
            type: "post",
            data: {
              sample_id: allSubmissions[0].sampleId,
              user_id: allSubmissions[0].userId,
              category_id: allSubmissions[i].tag,
              start_time: allSubmissions[i].startTime,
              end_time: allSubmissions[i].endTime,
              recorded_time: allSubmissions[0].recordedTime,
              recorded_location: allSubmissions[0].recordedLocation
            },
            success: function(response) {
              requestCallback.requestComplete(true);
            },
            error: function(xhr) {
              console.log(xhr);
            }
          });
        }
      } else {
        //there were no non NaN tags
        console.log("Loading Next Sample With No Tag Submissions");
        LoadNextSample();
      }
    } else {
      //there were no tags
      console.log("Loading Next Sample With No Tag Submissions");
      LoadNextSample();
    }
  }
}

function LoadNextSample() {
  //delete all tag rows
  for (let i = 0; i < tags.length; i++) {
    DeleteRow(i);
  }

  if (
    sampleParameters.activeSampleIndex ==
    sampleParameters.activeSamples.length - 1
  ) {
    //this was the last sample in the current sample array
    if (sampleParameters.activePage == sampleParameters.totalNumberOfPages) {
      //last page - this was the last sample - we don't have any more
      //load first one
      LoadSamplePagePriority(0, 1);
    } else {
      //we are at the end of the page not at the end of pages
      //load new page
      LoadSamplePagePriority(0, sampleParameters.activePage + 1);
    }
  } else {
    //we are not at the end of this page
    sampleParameters.activeSampleIndex++;
    SetupAudio(
      sampleParameters.activeSamples[sampleParameters.activeSampleIndex]
    );
  }
}

/*
Handle multiple AJAX requests with one callback
Courtesy Michael Russel
https://jsfiddle.net/subhaze/EN8nc/6/
*/
let allRequestsCompleted = (function() {
  var numRequestToComplete, requestsCompleted, callBacks, singleCallBack;

  return function(options) {
    if (!options) options = {};
    numRequestToComplete = options.numRequest || 0;
    requestsCompleted = options.requestsCompleted || 0;
    callBacks = [];
    var fireCallbacks = function() {
      for (var i = 0; i < callBacks.length; i++) callBacks[i]();
    };
    if (options.singleCallback) callBacks.push(options.singleCallback);
    this.addCallbackToQueue = function(isComplete, callback) {
      if (isComplete) requestsCompleted++;
      if (callback) callBacks.push(callback);
      if (requestsCompleted == numRequestToComplete) fireCallbacks();
    };
    this.requestComplete = function(isComplete) {
      if (isComplete) requestsCompleted++;
      if (requestsCompleted == numRequestToComplete) fireCallbacks();
    };
    this.setCallback = function(callback) {
      callBacks.push(callBack);
    };
  };
})();

//Tag Template
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
