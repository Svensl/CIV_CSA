// Import AOI boundary.
var civ_aoi = ee.FeatureCollection('users/schmitzleuffen/UNEP_CIV_CSA_Villages_Buffer150km')

// Print AOI object.
print(civ_aoi);

// Add AOI outline to the Map as a layer.
Map.centerObject(civ_aoi, 6);
Map.addLayer(civ_aoi);

// Import LST image collection.
var modis = ee.ImageCollection('MODIS/MOD11A2');

// Define a date range of interest; here, a start date is defined and the end
// date is determined by advancing 20 year from the start date. LST starts in 2000.

var start = ee.Date('2000-01-01');
var dateRange = ee.DateRange(start, start.advance(20, 'year'));

// Filter the LST collection to include only images intersecting the desired
// date range.
var mod11a2 = modis.filterDate(dateRange);

// Select only the 1km day LST data band.
var modLSTday = mod11a2.select('LST_Day_1km');
// Scale to Kelvin and convert to Celsius, set image acquisition time.
var modLSTc = modLSTday.map(function(img) {
  return img
    .multiply(0.02)
    .subtract(273.15)
    .copyProperties(img, ['system:time_start']);
});
// Chart time series of LST for AOI in 2000.
var ts1 = ui.Chart.image.series({
  imageCollection: modLSTc,
  region: civ_aoi,
  reducer: ee.Reducer.mean(),
  scale: 1000,
  xProperty: 'system:time_start'})
  .setOptions({
     title: 'LST 2000-2020 Time Series',
     vAxis: {title: 'LST Celsius'}});
print(ts1);
// Calculate 8-day mean temperature for AOI in 2000-2020.
var clippedLSTc = modLSTc.mean().clip(civ_aoi);

// Add clipped image layer to the map.
Map.addLayer(clippedLSTc, {
  min: 20, max: 40,
  palette: ['blue', 'limegreen', 'yellow', 'darkorange', 'red']},
  'Mean temperature, 1980');

// Export the image to your Google Drive account.
Export.image.toDrive({
  image: clippedLSTc,
  description: 'LST_Celsius_civ_aoi',
  folder: 'CIV_CSA',
  region: civ_aoi,
  scale: 1000,
  crs: 'EPSG:4326',
  maxPixels: 1e10});