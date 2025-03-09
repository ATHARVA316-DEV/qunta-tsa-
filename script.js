// // static/script.js

// // Initialize the map centered on Mysuru
// let map = L.map('map').setView([12.3100, 76.6600], 13);

// // Add OpenStreetMap tiles
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//   attribution: '&copy; OpenStreetMap contributors'
// }).addTo(map);

// let markers = [];
// let routeLayer;

// // Function to add markers for each bus stop
// function addMarkers(busStops, coordinates) {
//   // Remove any existing markers
//   markers.forEach(marker => map.removeLayer(marker));
//   markers = [];

//   for (let i = 0; i < busStops.length; i++) {
//     let marker = L.marker(coordinates[i]).addTo(map)
//       .bindPopup(`<b>${busStops[i]}</b>`);
//     markers.push(marker);
//   }
// }

// // On initial load, fetch data to display markers
// fetch("/solve")
//   .then(response => response.json())
//   .then(data => {
//     addMarkers(data.bus_stops, data.coordinates);
//   })
//   .catch(error => console.error("Error fetching data:", error));

// // Handle button click to solve the routing problem
// document.getElementById("solveBtn").addEventListener("click", function() {
//   fetch("/solve")
//     .then(response => response.json())
//     .then(data => {
//       document.getElementById("result").innerText = `Optimal Route Distance: ${data.total_distance.toFixed(2)} km`;
//       addMarkers(data.bus_stops, data.coordinates);
//       drawRoute(data.coordinates, data.route);
//     })
//     .catch(error => console.error("Error:", error));
// });

// function drawRoute(coordinates, route) {
//   // Remove an existing route if present
//   if (routeLayer) {
//     map.removeLayer(routeLayer);
//   }
  
//   // Build an array of LatLng objects according to the route order
//   let routeCoords = route.map(index => coordinates[index]);
//   routeLayer = L.polyline(routeCoords, { color: 'blue', weight: 4 }).addTo(map);
  
//   // Adjust map view to fit the route
//   map.fitBounds(routeLayer.getBounds());
// }


// static/script.js

// Initialize the map centered on Mysuru
// // static/script.js

// // Initialize the map centered on Mysuru
// let map = L.map('map').setView([12.3100, 76.6600], 13);

// // Add OpenStreetMap tiles
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//   attribution: '&copy; OpenStreetMap contributors'
// }).addTo(map);

// let markers = [];
// let routeLayer;
// let busMarker; // Global bus marker reference

// // Function to add markers for each bus stop
// function addMarkers(busStops, coordinates) {
//   // Remove any existing markers
//   markers.forEach(marker => map.removeLayer(marker));
//   markers = [];

//   for (let i = 0; i < busStops.length; i++) {
//     let marker = L.marker(coordinates[i]).addTo(map)
//       .bindPopup(`<b>${busStops[i]}</b>`);
//     markers.push(marker);
//   }
// }

// // On initial load, fetch data to display markers
// fetch("/solve")
//   .then(response => response.json())
//   .then(data => {
//     addMarkers(data.bus_stops, data.coordinates);
//   })
//   .catch(error => console.error("Error fetching data:", error));

// // Handle button click to solve the routing problem
// document.getElementById("solveBtn").addEventListener("click", function() {
//   fetch("/solve")
//     .then(response => response.json())
//     .then(data => {
//       document.getElementById("result").innerText = `Optimal Route Distance: ${data.total_distance.toFixed(2)} km`;
//       addMarkers(data.bus_stops, data.coordinates);
//       // Call the animated route drawing function
//       drawRoute(data.coordinates, data.route);
//     })
//     .catch(error => console.error("Error:", error));
// });

// // Animate bus marker from one coordinate to the next over a given duration (ms)
// function animateBusMovement(startCoord, endCoord, duration, marker) {
//   return new Promise((resolve) => {
//     let startTime = null;
//     function step(timestamp) {
//       if (!startTime) startTime = timestamp;
//       let progress = (timestamp - startTime) / duration;
//       if (progress > 1) progress = 1;
//       // Linear interpolation for latitude and longitude
//       let lat = startCoord[0] + (endCoord[0] - startCoord[0]) * progress;
//       let lon = startCoord[1] + (endCoord[1] - startCoord[1]) * progress;
//       marker.setLatLng([lat, lon]);
//       if (progress < 1) {
//         window.requestAnimationFrame(step);
//       } else {
//         resolve();
//       }
//     }
//     window.requestAnimationFrame(step);
//   });
// }

// async function drawRoute(coordinates, route) {
//   // Remove existing route if present
//   if (routeLayer) {
//     map.removeLayer(routeLayer);
//   }
  
//   // Initialize polyline with the starting coordinate
//   let routeCoords = [coordinates[route[0]]];
//   routeLayer = L.polyline(routeCoords, { color: 'blue', weight: 4 }).addTo(map);
  
//   // Remove previous bus marker if exists
//   if (busMarker) {
//     map.removeLayer(busMarker);
//   }
  
//   // Create a bus marker with a custom bus icon (use your own image URL as needed)
//   let busIcon = L.icon({
//     iconUrl: 'https://cdn-icons-png.flaticon.com/512/61/61231.png',
//     iconSize: [32, 32],
//     iconAnchor: [16, 16],
//   });
//   // Start the bus at the first coordinate
//   busMarker = L.marker(coordinates[route[0]], { icon: busIcon }).addTo(map);
  
//   let cumulativeDistance = 0;
  
//   // Loop over each segment of the route
//   for (let i = 0; i < route.length - 1; i++) {
//     let startCoord = coordinates[route[i]];
//     let endCoord = coordinates[route[i+1]];
    
//     // Calculate segment distance (using rough Euclidean conversion; 1 degree ~ 111 km)
//     let dx = endCoord[0] - startCoord[0];
//     let dy = endCoord[1] - startCoord[1];
//     let segmentDistance = Math.sqrt(dx * dx + dy * dy) * 111; // in km
//     cumulativeDistance += segmentDistance;
    
//     // Animate the bus marker along this segment over 1 second (1000 ms)
//     await animateBusMovement(startCoord, endCoord, 1000, busMarker);
    
//     // After animation, update the polyline by adding the new endpoint
//     routeCoords.push(endCoord);
//     routeLayer.setLatLngs(routeCoords);
    
//     // Update a display element with the segment and cumulative distances
//     document.getElementById("result").innerText =
//       `Segment Distance: ${segmentDistance.toFixed(2)} km, Cumulative: ${cumulativeDistance.toFixed(2)} km`;
    
//     // Wait 1 second before moving to the next segment
//     await new Promise(resolve => setTimeout(resolve, 1000));
//   }
  
//   // Adjust map view to fit the entire route after animation
//   map.fitBounds(routeLayer.getBounds());
// }
// static/script.js

// Initialize the map centered on Mysuru
let map = L.map('map').setView([12.3100, 76.6600], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let markers = [];
let routeLayer;
let busMarker; // Global bus marker reference

// Function to add markers for each bus stop
function addMarkers(busStops, coordinates) {
  // Remove any existing markers
  markers.forEach(marker => map.removeLayer(marker));
  markers = [];

  for (let i = 0; i < busStops.length; i++) {
    let marker = L.marker(coordinates[i]).addTo(map)
      .bindPopup(`<b>${busStops[i]}</b>`);
    markers.push(marker);
  }
}

// On initial load, fetch data to display markers
fetch("/solve")
  .then(response => response.json())
  .then(data => {
    addMarkers(data.bus_stops, data.coordinates);
  })
  .catch(error => console.error("Error fetching data:", error));

// Handle button click to solve the routing problem
document.getElementById("solveBtn").addEventListener("click", function() {
  fetch("/solve")
    .then(response => response.json())
    .then(data => {
      document.getElementById("result").innerText = `Optimal Route Distance: ${data.total_distance.toFixed(2)} km`;
      addMarkers(data.bus_stops, data.coordinates);
      // Call the animated route drawing function
      drawRoute(data.coordinates, data.route);
    })
    .catch(error => console.error("Error:", error));
});

// Animate bus marker from one coordinate to the next over a given duration (ms)
function animateBusMovement(startCoord, endCoord, duration, marker) {
  return new Promise((resolve) => {
    let startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      let progress = (timestamp - startTime) / duration;
      if (progress > 1) progress = 1;
      // Linear interpolation for latitude and longitude
      let lat = startCoord[0] + (endCoord[0] - startCoord[0]) * progress;
      let lon = startCoord[1] + (endCoord[1] - startCoord[1]) * progress;
      marker.setLatLng([lat, lon]);
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        resolve();
      }
    }
    window.requestAnimationFrame(step);
  });
}

async function drawRoute(coordinates, route) {
  // Remove existing route if present
  if (routeLayer) {
    map.removeLayer(routeLayer);
  }
  
  // Initialize polyline with the starting coordinate
  let routeCoords = [coordinates[route[0]]];
  routeLayer = L.polyline(routeCoords, { color: 'blue', weight: 4 }).addTo(map);
  
  // Remove previous bus marker if exists
  if (busMarker) {
    map.removeLayer(busMarker);
  }
  
  // Create a bus marker with a custom bus icon (changed appearance)
  let busIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/61/61230.png', // New bus icon URL
    iconSize: [48, 48],       // Increased size for a bolder look
    iconAnchor: [24, 24],     // Center of the icon as anchor
    popupAnchor: [0, -24]     // Popup position relative to the icon
  });
  // Start the bus at the first coordinate with the new icon
  busMarker = L.marker(coordinates[route[0]], { icon: busIcon }).addTo(map);
  
  let cumulativeDistance = 0;
  
  // Loop over each segment of the route
  for (let i = 0; i < route.length - 1; i++) {
    let startCoord = coordinates[route[i]];
    let endCoord = coordinates[route[i+1]];
    
    // Calculate segment distance (using rough Euclidean conversion; 1 degree ~ 111 km)
    let dx = endCoord[0] - startCoord[0];
    let dy = endCoord[1] - startCoord[1];
    let segmentDistance = Math.sqrt(dx * dx + dy * dy) * 111; // in km
    cumulativeDistance += segmentDistance;
    
    // Animate the bus marker along this segment over 1 second (1000 ms)
    await animateBusMovement(startCoord, endCoord, 1000, busMarker);
    
    // After animation, update the polyline by adding the new endpoint
    routeCoords.push(endCoord);
    routeLayer.setLatLngs(routeCoords);
    
    // Update a display element with the segment and cumulative distances
    document.getElementById("result").innerText =
      `Segment Distance: ${segmentDistance.toFixed(2)} km, Cumulative: ${cumulativeDistance.toFixed(2)} km`;
    
    // Wait 1 second before moving to the next segment
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Adjust map view to fit the entire route after animation
  map.fitBounds(routeLayer.getBounds());
}
