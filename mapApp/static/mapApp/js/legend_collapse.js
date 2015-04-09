$(document).ready(function(){
  // Control sublegend collapsing
  $("input.layer-toggle").click(function(e) {
    layerClicked = window[e.target.value];
    checked = e.target.checked;
    subLegend = $(e.target).siblings(".legend-subtext");
    if(checked){
      map.addLayer(layerClicked);
      subLegend.collapse("show");
    }
    else if (map.hasLayer(layerClicked) && !checked) {
      map.removeLayer(layerClicked);
      subLegend.collapse("hide");
    }
  });
  

  // Control legend collapsing (modified code from leaflet/src/L.control.layers)
  var container = $('#legend .leaflet-control-layers');

  $(window).resize( function(e){
    if( $(window).width() < 700 ){
      var link = $('#legend .leaflet-control-layers-toggle'),
      map = $('#map');

      if (!L.Browser.android) {
        container.mouseenter(expand);
        container.mouseleave(collapse);
      }

      if (L.Browser.touch) {
        link.click(function(e){
          e.stopPropagation();
          expand();
        });
      } else {
        link.focus(expand);
      }

      map.click(collapse);
    }

    else {
      expand();
    }
  });
  $(window).trigger('resize'); //Call event handler on load

  function expand() {
    container.addClass('leaflet-control-layers-expanded');
  };

  function collapse() {
    container.removeClass('leaflet-control-layers-expanded');
  };
});
