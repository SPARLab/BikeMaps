// TOOLTIP POPUPS FOR INDEX

// Tool tip definitions. Uses title attribut of html tag.
$(document).ready(function(){
 	// layer control
	$('.leaflet-control-layers-toggle').tipsy({gravity:'e', trigger: 'manual', title: function(){ return "Layer control"}, fade: true});
	// search control
	$('.leaflet-control-geocoder').tipsy({gravity:'e', delayIn:400, fade: true, title: function(){ return "Search for an address"}});
 	// delete points control
 	$('.leaflet-right .leaflet-draw-edit-remove').prop('title', 'Delete user points');
 	$('.leaflet-right .leaflet-draw-edit-remove').tipsy({gravity:'e', delayIn: 400, fade: true});
	// help button
	$('.leaflet-bar-part').tipsy({gravity:'e', delayIn: 200, fade: true});

	// All left side controls
	$('.leaflet-left .leaflet-control a').tipsy({gravity:'w', delayIn: 400, fade: true});
	
	$('#map').click(function(){toggleTooltips("hide")});

	// Used to toggle all tooltips on or off
	function toggleTooltips(t){
	    $('.leaflet-control-zoom a').tipsy(t);
	    $('.leaflet-control-zoom-out').tipsy(t);

	    $('.leaflet-draw-draw-marker').tipsy(t);
	    $('.leaflet-draw-draw-polyline').tipsy(t);
	    $('.leaflet-draw-draw-polygon').tipsy(t);
	  
	    $('.leaflet-draw-edit-remove').tipsy(t);
	    $('.leaflet-draw-edit-edit').tipsy(t);
		$('.leaflet-right .leaflet-draw-edit-remove').tipsy(t);

	    $('.leaflet-control-layers-toggle').tipsy(t);           

	    $('.leaflet-control-geocoder').tipsy(t);

	    $('.gps-button').tipsy(t);     	
	};
});