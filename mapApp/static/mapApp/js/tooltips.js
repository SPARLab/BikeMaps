$(document).ready(function(){
	// search control
	$('.leaflet-control-geocoder').tooltip({placement:'right', delay:400, title: function(){ return "Search for an address"}});
 	// delete points control
 	$('.leaflet-right .leaflet-draw-edit-remove').tooltip({placement:'left', delay: 400, title: function(){return 'Delete user points'}});
	// All left side controls
	$('.leaflet-left .leaflet-control a').tooltip({placement:'right', delay: 400});
});