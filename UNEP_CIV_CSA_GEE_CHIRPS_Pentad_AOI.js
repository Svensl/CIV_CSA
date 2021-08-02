// Import AOI boundary.
var civ_aoi = ee.FeatureCollection('users/schmitzleuffen/UNEP_CIV_CSA_Villages_Buffer150km')

// Print AOI object.
print(civ_aoi);

// Add AOI outline to the Map as a layer.
Map.centerObject(civ_aoi, 6);
Map.addLayer(civ_aoi);

// Import CHIRPS Pentad image collection.
var chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/PENTAD");

// Define a date range of interest; here, a start date is defined and the end
// date is determined by advancing 40 year from the start date.

var start = ee.Date('1980-01-01');
var dateRange = ee.DateRange(start, start.advance(40, 'year'));

// Filter the CHIRPS collection to include only images intersecting the desired
// date range.
var CHIRPS = chirps.filterDate(dateRange);

// Select the precipitation data band.
var chirpsprec = CHIRPS.select('precipitation');
//Sset image acquisition time.
var chirpsm = chirpsprec.map(function(img) {
  return img
    .copyProperties(img, ['system:time_start']);
});
// Chart time series of CHIRPS for AOI in 1980-2020.
var ts1 = ui.Chart.image.series({
  imageCollection: chirpsm,
  region: civ_aoi,
  reducer: ee.Reducer.mean(),
  scale: 1000,
  xProperty: 'system:time_start'})
  .setOptions({
     title: 'CHIRPS Pentad 1980-2020 Time Series',
     vAxis: {title: 'CHIRPS Millimeters'}});
print(ts1);
// Calculate mean monthly precipitation for AOI in 1980-2020.
var clippedchirpsm = chirpsm.mean().clip(civ_aoi);

// Add clipped image layer to the map.
Map.addLayer(clippedchirpsm, {
  min: 0, max: 80,
  palette: ['blue', 'limegreen', 'yellow', 'darkorange', 'red']},
  'Mean precipitation, 1980');
  
  // Export the image to your Google Drive account.
Export.image.toDrive({
  image: clippedchirpsm,
  description: 'CHIRPS_Pent_civ_aoi',
  folder: 'CIV_CSA',
  region: civ_aoi,
  scale: 1000,
  crs: 'EPSG:4326',
  maxPixels: 1e10});