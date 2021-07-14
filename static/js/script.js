$(document).ready(function () {
  $('.sidenav').sidenav({
    edge: "right",
    inDuration: "750"
  });
  $('select').formSelect();
  $('input#input_text, textarea#student_answer').characterCounter();
  $('.tooltipped').tooltip();
  $('.scrollspy').scrollSpy({
    scrollOffset: 1,
    getActiveElement: function (id) {
      return 'a[href="#' + id + '"]'
    }
  });

  // Limit Teacher to only choose one 
  // alternative for student submission 
  // per lesson: 
  $("#text_answer").click(function () {
    if ($("#text_answer").is(':checked'))
      $("#file_answer").prop("checked", false);
  });

  $("#file_answer").click(function () {
    if ($("#file_answer").is(':checked'))
      $("#text_answer").prop("checked", false);
  });

  // Code Institutes custom validator for 
  // select inputs with Materialize  
  validateMaterializeSelect();

  function validateMaterializeSelect() {
    let classValid = {
      "border-bottom": "1px solid #4caf50",
      "box-shadow": "0 1px 0 0 #4caf50"
    };
    let classInvalid = {
      "border-bottom": "1px solid #f44336",
      "box-shadow": "0 1px 0 0 #f44336"
    };
    if ($("select.validate").prop("required")) {
      $("select.validate").css({
        "display": "block",
        "height": "0",
        "padding": "0",
        "width": "0",
        "position": "absolute"
      });
    }
    $(".select-wrapper input.select-dropdown").on("focusin", function () {
      $(this).parent(".select-wrapper").on("change", function () {
        if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
          $(this).children("input").css(classValid);
        }
      });
    }).on("click", function () {
      if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
        $(this).parent(".select-wrapper").children("input").css(classValid);
      } else {
        $(".select-wrapper input.select-dropdown").on("focusout", function () {
          if ($(this).parent(".select-wrapper").children("select").prop("required")) {
            if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
              $(this).parent(".select-wrapper").children("input").css(classInvalid);
            }
          }
        });
      }
    });
  }
});

function videoUpload() {
  let video = document.getElementById("toggle_video");
  let audio = document.getElementById("mute_audio");
  let audio_box = document.getElementById("toggle_audio")
  if ($(video).hasClass('toggle-video')) {
    // if the class is there, remove it
    // and make element visable
    $(video).removeClass('toggle-video')
    // also hide audio option since video is picked
    $(audio).addClass('mute-audio')
    // also if audio_box is already open, hide it
    $(audio_box).addClass('mute-audio')
    // lets make sure to uncheck video
    // since we now want audio
  } else {
    // hide element by adding class
    $(video).addClass('toggle-video')
    // make audio an option again
    $(audio).removeClass('mute-audio')
    // make audio box an option again
    $(audio_box).removeClass('mute-audio')
  }
};


function audioUpload() {
  let audio = document.getElementById("toggle_audio");
  let video = document.getElementById("mute_video");
  let video_box = document.getElementById("toggle_video")
  let video_checkbox = document.getElementById("has_video")
  if ($(audio).hasClass('toggle-audio')) {
    // if the class is there, remove it
    // and make element visable
    $(audio).removeClass('toggle-audio')
    // also hide video option since audio is picked
    $(video).addClass('mute-video')
    // also if video_box is already open, hide it
    $(video_box).addClass('mute-video')
    // lets make sure to uncheck video
    // since we now want audio
  } else {
    /// hide element by adding class
    $(audio).addClass('toggle-audio')
    // make video an option again
    $(video).removeClass('mute-video')
    // make audio box an option again
    $(video_box).removeClass('mute-video')
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