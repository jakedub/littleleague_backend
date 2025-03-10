window.onload = function() {
    // Log to confirm the script is loaded
    console.log("Initializing map...");

    // Fetch coordinates and polygons from hidden fields
    const coordinates = JSON.parse(document.getElementById('coordinates').value);
    const polygons = JSON.parse(document.getElementById('polygons').value);

    console.log("Coordinates: ", coordinates);
    console.log("Polygons: ", polygons);

    // Check if coordinates and polygons are valid
    if (!coordinates || !coordinates.length) {
        console.log("No valid coordinates to display.");
        return;
    }

    // Initialize the map
    const map = new H.Map(
        document.getElementById('map'),
        platform.createDefaultLayers().vector.normal.map,
        {
            zoom: 10,
            center: { lat: parseFloat(document.getElementById('latitude').value), lng: parseFloat(document.getElementById('longitude').value) }
        }
    );

    // Add markers
    coordinates.forEach(function(coord) {
        console.log("Adding marker at: ", coord);
        const marker = new H.map.Marker({ lat: coord[0], lng: coord[1] });
        map.addObject(marker);
    });

    // Add polygons
    polygons.forEach(function(polygonCoords) {
        console.log("Adding polygon with coordinates: ", polygonCoords);
        const latLngs = polygonCoords.map(function(coord) {
            return { lat: coord[0], lng: coord[1] };
        });
        const polygon = new H.map.Polygon(latLngs);
        map.addObject(polygon);
    });
};