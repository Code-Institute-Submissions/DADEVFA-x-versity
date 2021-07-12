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

  validateMaterializeSelect();
  function validateMaterializeSelect() {
      let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
      let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
      if ($("select.validate").prop("required")) {
          $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
      }
      $(".select-wrapper input.select-dropdown").on("focusin", function () {
          $(this).parent(".select-wrapper").on("change", function () {
              if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
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