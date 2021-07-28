// Import AOI boundary.
var civ_aoi = ee.FeatureCollection('users/schmitzleuffen/UNEP_CIV_CSA_Villages_Buffer150km')

// Print AOI object.
print(civ_aoi);

// Add AOI outline to the Map as a layer.
Map.centerObject(civ_aoi, 6);
Map.addLayer(civ_aoi);

// Import ERA5 image collection.
var era5 = ee.ImageCollection("ECMWF/ERA5/MONTHLY");

// Define a date range of interest; here, a start date is defined and the end
// date is determined by advancing 40 year from the start date.

var start = ee.Date('1980-01-01');
var dateRange = ee.DateRange(start, start.advance(40, 'year'));

// Filter the ERA collection to include only images intersecting the desired
// date range.
var modera5 = era5.filterDate(dateRange);

// Select only the mean_2m_air_temperature data band.
var modEra5day = modera5.select('mean_2m_air_temperature');
// Convert to Celsius, set image acquisition time.
var modERA5c = modEra5day.map(function(img) {
  return img
    .subtract(273.15)
    .copyProperties(img, ['system:time_start']);
});
// Chart time series of ERA5 for AOI in 1980.
var ts1 = ui.Chart.image.series({
  imageCollection: modERA5c,
  region: civ_aoi,
  reducer: ee.Reducer.mean(),
  scale: 1000,
  xProperty: 'system:time_start'})
  .setOptions({
     title: 'ERA5 1980-2020 Time Series',
     vAxis: {title: 'ERA5 Celsius'}});
print(ts1);
// Calculate 8-day mean temperature for AOI in 1980-2020.
var clippedERA5c = modERA5c.mean().clip(civ_aoi);

// Add clipped image layer to the map.
Map.addLayer(clippedERA5c, {
  min: 22.5, max: 32.5,
  palette: ['blue', 'limegreen', 'yellow', 'darkorange', 'red']},
  'Mean temperature, 1980-2020');