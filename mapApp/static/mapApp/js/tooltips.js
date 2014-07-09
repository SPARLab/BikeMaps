// TOOLTIP POPUPS FOR INDEX

// Tool tip controls
$('#helpBtn').tipsy({gravity: 'w', delayIn: 200, fade: true});
$('.leaflet-control-zoom-in').tipsy({gravity:'w', delayIn: 1000, fade: true});
$('.leaflet-control-zoom-out').tipsy({gravity:'w', delayIn: 1000, fade: true});
$('.leaflet-draw-draw-marker').tipsy({gravity:'w', delayIn: 1000, fade: true});
$('.leaflet-draw-draw-polyline').tipsy({gravity:'w', delayIn: 1000, fade: true});
$('.leaflet-draw-draw-polygon').tipsy({gravity:'w', delayIn: 1000, fade: true});
$('.leaflet-draw-edit-remove').tipsy({gravity:'w', delayIn: 1000, fade: true});
$('.leaflet-draw-edit-edit').tipsy({gravity:'w', delayIn: 1000, fade: true});
$('.leaflet-control-geocoder').tipsy({gravity:'e', delayIn:1000, fade: true, title: function(){ return "Search for an address"}});
$('.leaflet-control-layers-toggle').tipsy({gravity:'e', trigger: 'manual', title: function(){ return "Layer control"}, fade: true});

$('#helpBtn').click(function(){toggleTooltips("show")});
$('#map').click(function(){toggleTooltips("hide")});

function toggleTooltips(t){
    $('.leaflet-control-zoom-in').tipsy(t);
    $('.leaflet-control-zoom-out').tipsy(t);
    $('.leaflet-draw-draw-marker').tipsy(t);
    $('.leaflet-draw-draw-polyline').tipsy(t);
    $('.leaflet-draw-draw-polygon').tipsy(t);
    $('.leaflet-draw-edit-remove').tipsy(t);
    $('.leaflet-draw-edit-edit').tipsy(t);
    $('.leaflet-control-layers-toggle').tipsy(t);           
    $('.leaflet-control-geocoder').tipsy(t);           
};