var civ_aoi = ee.FeatureCollection('users/schmitzleuffen/UNEP_CIV_CSA_Villages_Buffer150km');
civ_aoi = civ_aoi.geometry(); // variable which has the shapefile

// Add AOI outline to the Map as a layer.
Map.centerObject(civ_aoi, 6);
Map.addLayer(civ_aoi);

// Get the loss image.
// This dataset is updated yearly, so we get the latest version.
var gfc2020 = ee.Image("UMD/hansen/global_forest_change_2020_v1_8");
var gfc2020clip = ee.Image("UMD/hansen/global_forest_change_2020_v1_8").clip(civ_aoi);
var lossImage = gfc2020.select(['loss']);
var lossAreaImage = lossImage.multiply(ee.Image.pixelArea());

var lossYear = gfc2020.select(['lossyear']);
var lossByYear = lossAreaImage.addBands(lossYear).reduceRegion({
  reducer: ee.Reducer.sum().group({
    groupField: 1
    }),
  geometry: civ_aoi,
  scale: 30,
  maxPixels: 1e9
  
});
print(lossByYear);

//Formatting Yearly Loss Numbers
var statsFormatted = ee.List(lossByYear.get('groups'))
  .map(function(el) {
    var d = ee.Dictionary(el);
    return [ee.Number(d.get('group')).format("20%02d"), d.get('sum')];
  });
var statsDictionary = ee.Dictionary(statsFormatted.flatten());
print(statsDictionary);

//Charting loss numbers
var chart = ui.Chart.array.values({
  array: statsDictionary.values(),
  axis: 0,
  xLabels: statsDictionary.keys()
}).setChartType('ColumnChart')
  .setOptions({
    title: 'AOI Yearly Forest Loss',
    hAxis: {title: 'Year', format: '####'},
    vAxis: {title: 'Area (square meters)'},
    legend: { position: "none" },
    lineWidth: 1,
    pointSize: 3
  });
print(chart);

//Adding image to map

var treeLossVisParam = {
  bands: ['lossyear'],
  min: 0,
  max: 20,
  palette: ['yellow', 'red'],
};
Map.addLayer(gfc2020, treeLossVisParam, 'tree loss year');

// Export the image to your Google Drive account.
Export.image.toDrive({
  image: gfc2020clip,
  description: 'GFC_Clip_AOI',
  folder: 'CIV_CSA',
  region: civ_aoi,
  scale: 1000,
  crs: 'EPSG:4326',
  maxPixels: 1e10});
