$(document).ready(function () {
  $('.sidenav').sidenav({
    edge: "right",
    inDuration: "750"
  });
  $('select').formSelect();
  $('.tooltipped').tooltip();
  $('.scrollspy').scrollSpy({
    scrollOffset: 1,
    getActiveElement: function (id) {
      return 'a[href="#' + id + '"]'
  }});
});


function videoUpload() {
  let element = document.getElementById("toggle_video");
  if ($(element).hasClass('toggle-video')) {
    // if it is, remove.
    $(element).removeClass('toggle-video')
  } else {
    // otherwise just add muted.
    $(element).addClass('toggle-video')
  }
};

function audioUpload() {
  let element = document.getElementById("toggle_audio");
  if ($(element).hasClass('toggle-audio')) {
    // if it is, remove.
    $(element).removeClass('toggle-audio')
  } else {
    // otherwise just add muted.
    $(element).addClass('toggle-audio')
  }
};

function submissionUpload() {
  let element = document.getElementById("submission_style");
  if ($(element).hasClass('toggle-sub-styles')) {
    // if it is, remove.
    $(element).removeClass('toggle-sub-styles')
  } else {
    // otherwise just add muted.
    $(element).addClass('toggle-sub-styles')
  }
};

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.fixed-action-btn');
  var instances = M.FloatingActionButton.init(elems, {
    direction: 'left'
  });
});
      