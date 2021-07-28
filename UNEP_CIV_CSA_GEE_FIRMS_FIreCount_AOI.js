var civ_aoi = ee.FeatureCollection('users/schmitzleuffen/UNEP_CIV_CSA_Villages_Buffer150km');
civ_aoi = civ_aoi.geometry(); // variable which has the shapefile
Map.centerObject(civ_aoi);  
Map.addLayer(civ_aoi, {color: 'red'}, 'geodesic polygon');
//fire 
var dataset = ee.ImageCollection('FIRMS').select('confidence')
var years = ee.List.sequence(2003,2020) // list of yrs from 2003-2020
 var maps = ee.ImageCollection(years.map(function(year){
var startDate = ee.Date.fromYMD(year,1,1)
var endDate = ee.Date.fromYMD(year,12,31)
var myImg = dataset.filter(ee.Filter.date(startDate,endDate)).max().gt(100).set("system:time_start",startDate)
return myImg
}))
print(ui.Chart.image.seriesByRegion({imageCollection:maps,
regions:civ_aoi,
reducer:ee.Reducer.count(), //count 
scale:1000}).setOptions({title: 'Fire count',
lineWidth: 1,
pointSize: 3}));
 Map.addLayer(maps.max().clip(civ_aoi), {min:0,max:1,palette:['red']}, 'Fires');
