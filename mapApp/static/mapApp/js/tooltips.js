$(function(){
	// search control
	$('.leaflet-control-geocoder').tooltip({placement:'right', delay:400, title: function(){ return "Search for an address"}});

	map.on('drawControlReady', function(){
		// All left side controls
		$('.leaflet-left .leaflet-control a').tooltip({placement:'right', delay: 400});
	});
});
