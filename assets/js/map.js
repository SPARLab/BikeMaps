//new global "map" and marker variables
		var map = null;
		//The URL of the script that sends the data from the results spreadsheet to the map
		var DATA_SERVICE_URL = "https://script.google.com/macros/s/AKfycbw--oZZPlJ76nTEnwf8K4Y7SfwIsBNYhJWQnMn3Ib7grQR0IC6n/exec?jsonp=callback";
		//Marker variables
		var marker = null;
				
		//Set these variables as global to allow use anywhere
		//These Variables hold the submitted data
		var UserData = new Array;
		var UserPts = new Array;
		var pointArray;
		var heatmap;
		var existingRoutesLayer;
		var flayer;
		var hflayer;
		var markers = []
		
		//New infowindow variable this is used for the clicking infowindow
		var infowindow = new google.maps.InfoWindow(
			{ 
			size: new google.maps.Size(150,100)
			});
		
		//A function to create the marker and set up the event window function 
		//This function is for clicking on the map to create markers
		//This is the window for submitting data
		function createMarker(latlng, name, html) {
			var contentString = html;
			var marker = new google.maps.Marker({
				position: latlng,
				map: map,
				zIndex: Math.round(latlng.lat()*-100000)<<5
				});

				google.maps.event.addListener(marker, 'click', function() {
					infowindow.setContent(contentString); 
					infowindow.open(map,marker);
					});
				google.maps.event.trigger(marker, 'click');    
				return marker;
			}
		 
		// This function creates the map
		function initialize() {
		
			//Map options, where to centre the map, map type, and zoom
			var myLatLng = new google.maps.LatLng(48.43, -123.3657);
			var mapOptions = {
				zoom: 13,
				//Center is set to victoria
				center: myLatLng,
				mapTypeControl: true,
				mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
				navigationControl: true,
				//Map type
				mapTypeId: google.maps.MapTypeId.ROADMAP
			}
		
			//Create map object	
			map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
		    
		    // City of Victoria existing bike routes KML
            var existingRoutesLayer = new google.maps.KmlLayer({
              url: 'http://www.victoria.ca/assets/City~Hall/Forms~Publications/BikeRoutes.kmz',
              suppressInfoWindows: true, //This line removes the default info window
              map: map 
            });
            // existingRoutesLayer.setMap(map)

			// Add bike trails layer from google
			var bikeLayer = new google.maps.BicyclingLayer(); 	
			bikeLayer.setMap(map);
		  
			//This varialble holds the state of the fusion tables heatmap
			tfToggle = false;
			
			//ICBC data fusion layer
			flayer = new google.maps.FusionTablesLayer({
				query: {
				  select: 'Coords',
				  from: '1WDge-1KzFL09clevuULwEP63ucgI6aAvwKnChGM'
				},
				
				//Controls the heatmap of the ICBC layer
				//The heatmap is controlled by a button
				heatmap: {
					enabled: false
				}
				
			});
			
			//ICBC data fusion layer heatmap
			hflayer = new google.maps.FusionTablesLayer({
				query: {
				select: 'Coords',
				from: '1WDge-1KzFL09clevuULwEP63ucgI6aAvwKnChGM'
				},
				
				//Controls the heatmap of the ICBC layer
				heatmap: {
					enabled: true
				}
				
			});

			//Closes any existing infowindows when the map is clicked
			google.maps.event.addListener(map, 'click', function() {
				infowindow.close();
				}); 
		
			//Create a variable for the directions service to allow road/trail selection
			//This is used to jump to the nearest road or trail when the map is clicked
			var directionsService = new google.maps.DirectionsService();
		
			//call function to create marker when map is clicked
			google.maps.event.addListener(map, 'click', function(event) {
				//Location of click variable
				var replatlng = event.latLng
				//html link to google form for the infowindow
				//The form is pre-filled with the location from the map
				var html = "<a href='https://docs.google.com/forms/d/1ZK0R36K2_XCJfw_OBrk8pNxxXOo2fP9XLoDtmHHGLOk/viewform?entry.1855664511&entry.611983853&entry.361318600="+replatlng+"'>Click to Report an Accident</a><br /><b></b>";
				
				//Create a request to get the closest road/path to the click on the map
				var request = {
					origin:event.latLng, 
					destination:event.latLng,
					//The walking mode allows the markers to snap to paths and roads
					travelMode: google.maps.DirectionsTravelMode.WALKING
					};			
				
				//Check if the location clicked is acceptable, if not snap to the nearest path or road and create a marker
				directionsService.route(request, function(response, status) {
					if (status == google.maps.DirectionsStatus.OK) {
						marker = createMarker(response.routes[0].legs[0].start_location, "name", html);
					}
				});
				
				//Clear any previously existing markers	left from clicking
				if (marker) {
					marker.setMap(null);
					marker = null;
					}
			});
			
			//This segment creates markers from the spreadsheet data, accessing the json output script from google drive
			//Once this script initializes it sends data to the callback function
			var scriptElement = document.createElement('script');
			scriptElement.src = DATA_SERVICE_URL;
			document.getElementsByTagName('head')[0].appendChild(scriptElement);						
		}
		
		//This function is running off of data from a script in the google drive responses spreadsheet
		function callback(data) {
			//Create a new array to store the info from the user-submitted data spreadsheet	
			//We will create one array to use for the heatmap (it needs a special type) and one for the markers and info windows
			//This loops through the spreadsheet data to reformat it to create markers and infowindows
			//We start counting at one to avoid the first row of data that has the column names
			for (var i = 1; i < data.length; i++) {
				//Get the coordinates from the google form and create markers
				//The next three lines get the coordinates from the form data and splits it into lat and long
				var coor = data[i][15];
				var repl = coor.replace("(","");
				var repl2 = repl.replace (")","");
				//This is an array that holds the lat and long
				var splt = repl2.split(",",2);
				//This variable houses the text for the infowindow
				var infoUser = "<p>This incident location was <br> reported by a citizen. </p>";
				//Fill the array for the markers and infowindows
				UserData[i] = [splt[0],splt[0],splt[1],infoUser];
				//Fill the array for the heatmaps
				var latNum= Number(splt[0]);
				var lonNum = Number(splt[1]);
				UserPts [i-1] = new google.maps.LatLng(latNum,lonNum);
			}	
					
			//Point array used as part of a heat map for the UserData
			pointArray = new google.maps.MVCArray(UserPts);
			
			//Create the heatmap from the input data
			//This is controlled by a button
			heatmap = new google.maps.visualization.HeatmapLayer({
			  data: pointArray
			});
			


			//For setting the markers with the array
			//Call the setmarkers function to load the user data markers
			setMarkers(map, UserData);
			//Create an infowindow for the user submitted data, the content is just a placeholder
			infowindow = new google.maps.InfoWindow({
				content: "loading..."
				});
			
			//This function creates the markers for the user data
			//It loops through the json output from the google spreadsheet code
			//And creates a marker for each point
			function setMarkers(map, umarkers) {
				for (var i = 1; i < umarkers.length; i++) {
					var sites = umarkers[i];
					var siteLatLng = new google.maps.LatLng(sites[1], sites[2]);
					var marker = new google.maps.Marker({
						position: siteLatLng,
						map: map,
						title: sites[0],
						html: sites[3]
					});

					var contentString = "Some content";
					markers.push(marker);
					google.maps.event.addListener(marker, "click", function () {
						infowindow.setContent(this.html);
						infowindow.open(map, this);
					});
				}
			}

			
		}
		
	  	//Function to toggle the user data heatmap
		function toggleHeatmap() {
			heatmap.setMap(heatmap.getMap() ? null : map);
		}
		
		// Removes the markers from the map, but keeps them in the array.
		function toggleUserData() {
			if (markers[0].getMap() == map)
				{
				//Call the setAllMap function to toggle the points
				setAllMap(null)
				}
			else
				{
				setAllMap(map)
				}
		}	
		
			// Sets the map on all markers in the array.
			//This function is secondary to the User data toggle
			function setAllMap(map) {
				for (var i = 0; i < markers.length; i++) {
					markers[i].setMap(map);
				}
			}		
		
		
		//Toggle the ICBC data points
		function toggleICBC() {
			flayer.setMap(flayer.getMap() ? null : map);
		}
			
		//Toggle the ICBC heatmap
		function toggleICBCHM() {
			hflayer.setMap(hflayer.getMap() ? null : map);
		}

		// TODO
		// function changeRadius() {
		//   heatmap.set('radius', heatmap.get('radius') ? null : 20);
		// }

		google.maps.event.addDomListener(window, 'load', initialize);

		