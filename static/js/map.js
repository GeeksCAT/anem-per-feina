// Map configuration setup

// TODO: Add attribution plugin
const attribution =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

const OSMTiles = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

// Geojson Layer utils
function createPopup(data) {
  // TODO: And url to see company offers in detail
  return `
  <div><b>${data.company_name}</b><br>
  Open positions: ${data.opening_positions} </span><br>
  Location: ${data.city}, ${data.country}<br>
  <a href="#">See offers</a>
  </div>
  `;
}

function onEachFeature(feature, layer) {
  if (feature.properties) {
    layer.bindPopup(createPopup(feature.properties));
  }
}

// Map utils
var markerStyle = {
  icon: "info",
  iconColor: "white",
  prefix: "fa",
  markerColor: "green",
};
var jobMarker = L.AwesomeMarkers.icon(markerStyle);

var clusterOptions = {
  disableClusteringAtZoom: 10,
  zoomToBoundsOnClick: true,
  spiderLegPolylineOptions: { weight: 1.5, color: "#000", opacity: 0.5 },
};

// Data Layers
var jobsClusterLayer = L.markerClusterGroup(clusterOptions);
var jobsGeoJSON = L.geoJSON([], {
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, { icon: jobMarker });
  },
  onEachFeature: onEachFeature,
});

// Base map
var overlayMaps = {
  Jobs: jobsClusterLayer,
};

var map = L.map("mapid", {
  center: [42.0, 1.3],
  zoom: 8,
  maxZoom: 16,
  layers: jobsClusterLayer, //default selected layers
});

//  Terrain layer
L.tileLayer(OSMTiles, {
  attribution: attribution,
}).addTo(map);

// Add layers to map
jobsClusterLayer.addLayer(jobsGeoJSON);
map.addLayer(jobsClusterLayer);

//  add control layers
L.control.layers({}, overlayMaps).addTo(map);

// add user location plugin
let opts = {"flyTo": true};
L.control.locate(opts).addTo(map);

// Populate map with jobs offers

async function getJobsData() {
  let url = `http://${window.location.host}/api/map`;
  await fetch(url, {
    method: "GET",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    referrerPolicy: "no-referrer",
  })
    .then(function (response) {
      return response.json();
    })
    .then((data) => {
      jobsGeoJSON.addData(data);
      jobsClusterLayer.addLayer(jobsGeoJSON);
    });
}

window.onload = (event) => {
  getJobsData();
};
