$(document).ready(function () {
  $('.sidenav').sidenav({
    edge: "right",
    inDuration: "750"
  });
  $('select').formSelect();
  $('.tooltipped').tooltip();
});

const scrollspy = document.querySelectorAll(".scrollspy");
M.ScrollSpy.init(scrollspy, {
  getActiveElement: function (id) {
    return 'a[href="#' + id + '"]';
  },
})


var slider = document.getElementById('due_date');
noUiSlider.create(slider, {
 start: [20, 80],
 connect: true,
 step: 1,
 orientation: 'horizontal',
 range: {
   'min': 0,
   'max': 100
 },
 format: wNumb({
   decimals: 0
 })
});
