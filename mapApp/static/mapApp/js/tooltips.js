// TOOLTIP POPUPS FOR INDEX

// Tool tip definitions. Uses title attribut of html tag.
 $(document).ready(function(){
 	$('#helpBtn').tipsy({gravity: 'w', delayIn: 200, fade: true});

	$('.leaflet-control-zoom a').tipsy({gravity:'w', delayIn: 1000, fade: true});
	$('.leaflet-control-geocoder').tipsy({gravity:'e', delayIn:1000, fade: true, title: function(){ return "Search for an address"}});
	$('.leaflet-control-layers-toggle').tipsy({gravity:'e', trigger: 'manual', title: function(){ return "Layer control"}, fade: true});
	$('.leaflet-draw-section a').tipsy({gravity:'w', delayIn: 1000, fade: true});

	// Used to toggle all tooltips on or off
	function toggleTooltips(t){
		if(t==='show'){
		 	$('#helpBtn').attr('title', "Click map to close tooltips");
		}
		else{
		 	$('#helpBtn').attr('title', "Get Help");
		}

	    $('.leaflet-control-zoom a').tipsy(t);
	    $('.leaflet-control-zoom-out').tipsy(t);

	    $('.leaflet-draw-draw-marker').tipsy(t);
	    $('.leaflet-draw-draw-polyline').tipsy(t);
	    $('.leaflet-draw-draw-polygon').tipsy(t);
	  
	    $('.leaflet-draw-edit-remove').tipsy(t);
	    $('.leaflet-draw-edit-edit').tipsy(t);

	    $('.leaflet-control-layers-toggle').tipsy(t);           

	    $('.leaflet-control-geocoder').tipsy(t);         	
	};

	// Toggle tooltips on and off with button
	$('#helpBtn').click(function(){toggleTooltips("show")});
	$('#map').click(function(){toggleTooltips("hide")});
});