// Coordinates of your campus
var campusLat = 13.406040212295862;
var campusLon = 123.37548833100324;

// Initialize the map
var map = L.map('campusMap').setView([13.405517911030056, 123.37713024219663], 19);

// Tile layer using OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 18,
    maxZoom: 21,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Parking spaces and their status
var parkingLots = [
    { name: "Lot IP001", coords: [[13.40558217180716, 123.37700866717411], [13.40556195106628, 123.37701939601084]], status: "occupied" },
    { name: "Lot IP002", coords: [[13.40558017180716, 123.37702439601084], [13.40555995106628, 123.37703512484695]], status: "available" },
    { name: "Lot IP003", coords: [[13.40557817180716, 123.37704012484695], [13.40555795106628, 123.37705085368306]], status: "available" },
    { name: "Lot IP004", coords: [[13.40557617180716, 123.37705685368306], [13.40555595106628, 123.37706758251917]], status: "reserved" },
    { name: "Lot IP005", coords: [[13.40557517180716, 123.37707358251917], [13.40555495106628, 123.37708431135528]], status: "available" },
    { name: "Lot IP006", coords: [[13.40557417180716, 123.37708931135528], [13.40555395106628, 123.37710004019139]], status: "available" },
    { name: "Lot IP007", coords: [[13.40557217180716, 123.37710404019139], [13.40555195106628, 123.37711476802750]], status: "available" },
    { name: "Lot IP008", coords: [[13.40557017180716, 123.37711876802750], [13.40554995106628, 123.37712949686361]], status: "available" },
    { name: "Lot IP009", coords: [[13.40556917180716, 123.37713349686361], [13.40554895106628, 123.37714422569972]], status: "occupied" },
    { name: "Lot IP010", coords: [[13.40556917180716, 123.37714822569972], [13.40554895106628, 123.37715895453583]], status: "occupied" }
];


// Add parking lot rectangles
parkingLots.forEach(lot => {
    var color;
    if (lot.status === "available") {
        color = "#34ff12"; // Green for available
    } else if (lot.status === "reserved") {
        color = "#7db7ff"; // Blue for reserved
    } else if (lot.status === "occupied") {
        color = "#ff5858"; // Red for occupied
    }
    
    // Add the rectangle to the map
    L.rectangle(lot.coords, { color: color, weight: 1 }).addTo(map)
        .bindPopup(`${lot.name}: ${lot.status.charAt(0).toUpperCase() + lot.status.slice(1)}`);
});