$(document).ready(function () {
  $('.sidenav').sidenav({edge: "right", inDuration: "750"});
  $('select').formSelect();
  $('.tooltipped').tooltip();
});

$('.pushpin-demo-nav').each(function () {
  var $this = $(this);
  var $target = $('#' + $(this).attr('data-target'));
  $this.pushpin({
    top: $target.offset().top,
    bottom: $target.offset().top + $target.outerHeight() - $this.height()
  });
});