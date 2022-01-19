/*
Define special zones
*/

// Bounding box object that contains extent of area, action to take for that area, and boolean storing whether the action has been run
var bboxes = [{
  geoid: 'winnipeg_ca',
  bbox: {
    xmin: -97.35,
    ymin: 49.71,
    xmax: -96.995716,
    ymax: 49.991
  },
  action: function() {
    runWinnipegRaffle();
  },
  wasActionRun: false
}];

// This is a simple rectangular geographic representation of the boundaries of Winnipeg
var bboxBoundWinnipeg = L.latLngBounds([L.latLng([bboxes[0].bbox.ymax, bboxes[0].bbox.xmax]), L.latLng([bboxes[0].bbox.ymin, bboxes[0].bbox.xmin])]);

/*
Functions to check if location is within a special zone
*/
function checkSpecialZone(in_location, bbox) {
  console.log('checking special zone');
  var neCorner = L.latLng([bbox.bbox.ymin, bbox.bbox.xmin]);
  var swCorner = L.latLng([bbox.bbox.ymax, bbox.bbox.xmax]);

  if (L.latLngBounds([swCorner, neCorner]).contains(in_location)) {
    if (!bbox.wasActionRun) {
      console.log('Running action for ' + bbox.geoid);
      bbox.action();
      bbox.wasActionRun = true;
    } else {
      console.log('already ran action ' + bbox.geoid);
    }
  }
}

function checkSpecialZonePoly(in_extent, bbox, bboxBound) {
  console.log('checking special zone');

  if (bboxBound.intersects(in_extent)) {
    if (!bbox.wasActionRun) {
      console.log('Running action for ' + bbox.geoid);
      bbox.action();
      bbox.wasActionRun = true;
    } else {
      console.log('already ran action ' + bbox.geoid);
    }

  }

}

// The Debounce technique allow us to “group” multiple sequential calls in a single one. Don't want to check for special area extent on every map move event if user is scrolling around and exploring

function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this,
      args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

var checkSpecialZonePolyDebounce = debounce(function() {
  checkSpecialZonePoly(map.getBounds(), bboxes[0], bboxBoundWinnipeg);
}, 500);

/*
Action to take based on special zone
*/
function runWinnipegRaffle() {
  console.log('running winnipeg raffle code');

  var wpgRaffle = confirm("Hi, we noticed you are in Winnipeg. Would you like to participate in the Bikemaps Winnipeg Raffle ?");
  if (wpgRaffle) {
    var wpgWin = window.open('https://google.com', '_blank');
    wpgWin.focus(); // causing error 'cannot read propery focus of null'
  }

  // This is creating an empty modal that doesn't close - probably missing some code
  // setTimeout(function() {
  //   //attach an event handler to hide the window if they click the btn
  //   $(".btn-wpgRaffle").on("click", function() {
  //     $("#wpg-raffle").modal('hide');
  //   });
  //   //show the raffle dialog
  //   $("#wpg-raffle").modal('show');
  //   $(".wpgRaffleNav").show();
  // }, 1500);

}
