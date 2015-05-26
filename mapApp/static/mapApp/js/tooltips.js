$(function(){
	// search control
	$('.leaflet-control-geocoder').tooltip({placement:'right', delay:400, title: function(){ return "Search for an address"}});

	map.on('drawControlReady', function(){
		// delete points control
	 	$('.leaflet-right a.leaflet-draw-edit-remove').tooltip({placement:'left', delay: 400, title: function(){return 'Delete user points'}});
		// All left side controls
		$('.leaflet-left .leaflet-control a').tooltip({placement:'right', delay: 400});
	});
});
