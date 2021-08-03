import cdstoolbox as ct

# Define the title and description of your application.
@ct.application(title='Climate chart application', description='This application generates a climate chart displaying the 10 year (2009-2019) average temperature and rainfall conditions for Louomidouo in Côte d Ivoire.')

# Define the output widget for an interactive livefigure
@ct.output.livefigure()

def create_climate_chart():
    '''
    The function retrieves, processes and visualizes data in order to create a climate chart for a specific location.
    
    Parameters:
    lon(float): Float value representing the longitude degrees for a specific location
    lat(float): Float value representing the latitude degrees for a specific location
    
    Returns:
    interactive livefigure
    '''
    
    #######################################################################################
    # 1. RETRIEVE THREE DIFFERENT DATASETS OVER A DEFINED TIME RANGE
    #######################################################################################
    
    # 1a. RetrieveERA5 monthly averaged data on single levels - 2m air temperature for 10 years
    t2m_monthly_mean = ct.catalogue.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'variable':'2m_temperature',
        'year':['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'],
        'month':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12'
        ],
        'time':'00:00',
        'grid':[3,3],
        'product_type':'monthly_averaged_reanalysis'
    })
   
    # 1b. Retrieve ERA5 hourly data on single levels - 2m air temperature for 10 years, in order to calculate minimum and maximum temperature values
    t2m_hourly = ct.catalogue.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'variable':'2m_temperature',
        'year':['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'],
        'month':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12'
        ],
        'day':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
            '13','14','15',
            '16','17','18',
            '19','20','21',
            '22','23','24',
            '25','26','27',
            '28','29','30',
            '31'
        ],
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ],
        'grid':[3,3]
    })

    # 1c. Retrieve ERA5 hourly data on single levels - Total precipitation for 10 years, in order to calculate the monthly total amount (sums) of precipitation per month
    tp_hourly = ct.catalogue.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'variable':'total_precipitation',
        'year':[
            '2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'
        ],
        'month':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12'
        ],
        'day':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
            '13','14','15',
            '16','17','18',
            '19','20','21',
            '22','23','24',
            '25','26','27',
            '28','29','30',
            '31'
        ],
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ],
        'grid':[3,3]
    })

    #######################################################################################
    # 2. RESAMPLE 2M AIR TEMPERATURE AND TOTAL PRECIPITATION HOURLY DATA
    ####################################################################################### 
    
    # 2a. Resample 2m air temperature hourly data to daily minimum and maximum values
    # Calculate the daily maximum 2m air temperature value with .cube.resample
    t2m_max = ct.cube.resample(t2m_hourly, freq='day', dim='time', how='max')
    # Calculate the daily minimum 2m air temperature value with .cube.resample
    t2m_min = ct.cube.resample(t2m_hourly, freq='day', dim='time', how='min')
    
    # 2b. Resample total precipitation hourly data to monthly total sums
    # Convert total precipitation from flux (m/s) to hourly accumulated column of water (mm)    
    tp_hourly_column = tp_hourly * 3600 * 1000
    # Update the unit of the data object with .cdm.update_attributes
    tp_hourly_column = ct.cdm.update_attributes(tp_hourly_column, {'units': 'mm'})
    
    # Calculate the total amount of precipitation per month, with .cube.resample and 'sum'
    tp_monthly_sums = ct.cube.resample(tp_hourly_column, freq='month', closed='right', dim='time',how='sum')    
    print(tp_monthly_sums)
   

    #######################################################################################
    # 3. GENERATE CLIMATOLOGY MEANS FOR EACH MONTH
    #######################################################################################
    
    # Create the average 2m air temperature for each month for minimum, maximum and mean temperature with .climate.climatology.mean
    t2m_min_climatology = ct.climate.climatology_mean(t2m_min, frequency='month')
    t2m_max_climatology = ct.climate.climatology_mean(t2m_max, frequency='month') 
    t2m_mean_climatology = ct.climate.climatology_mean(t2m_monthly_mean, frequency='month')   
    
    # Create the average total precipitation amount for each month with .climate.climatology.mean
    tp_climatology = ct.climate.climatology_mean(tp_monthly_sums, frequency='month')

    
    #######################################################################################
    # 4. SELECT A LOCATION, DEFINED BY LATITUDE AND LONGITUDE VALUES
    #######################################################################################   
    
    # Extract the average minimum temperature for each month for the selected location with .geo.extract.point
    t2m_min_loc = ct.geo.extract_point(t2m_min_climatology, lon=-2.903, lat=9.035)

    # Extract the average maximum temperature for each month for the selected location with .geo.extract.point   
    t2m_max_loc = ct.geo.extract_point(t2m_max_climatology, lon=-2.903, lat=9.035)

    # Extract the average mean temperature for each month for the selected location with .geo.extract.point
    t2m_mean_loc = ct.geo.extract_point(t2m_mean_climatology, lon=-2.903, lat=9.035)
    
    # Extract the average total precipitation amount for each month for the selected location with .geo.extract.point   
    tp_loc = ct.geo.extract_point(tp_climatology, lon=-2.903, lat=9.035)

    
    #######################################################################################
    # 5. GENERATE AN INTERACTIVE CLIMATE CHART
    #######################################################################################
    
    # Set general information on the plot style, e.g. width and height, title of x and y axes etc. The dictionary is then used when the figure object is defined
    layout_kwargs = {  
        'width':1000,
        'height':700,
        'legend': {'orientation':'h',
                  'y':-0.15,
                  'x':0.1},
        'yaxis': {
            'overlaying':'y2',
            'zeroline': False,
            'title':'2m air temperature in deg C'
        },
        'margin':{'t':25},
        'xaxis':{
            'tickvals':[1,2,3,4,5,6,7,8,9,10,11,12],
            'ticktext':['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            'title': 'Month'
        },
        'yaxis2': {
            'showgrid': False,
            'side': 'right',
            'zeroline': False,
            'title': 'Total precipitation in mm'
        }
    }

    # Define resulting figure as a bar chart representing the monthly total precipitation sums   
    fig = ct.chart.bar(tp_loc,
                      bar_kwargs={
                          'name':'Total precipitation',
                          'yaxis': 'y2'
                      },
                      marker={
                          'color':'lightsteelblue'
                      },
                      layout_kwargs=layout_kwargs)
    
     # Add a line plot for 2m mean temperature to the plot   
    fig = ct.chart.line(t2m_mean_loc,
                  fig=fig,
                  scatter_kwargs={
                      'name':'Mean temperature',
                      'mode':'lines'
                  },
                  marker = {
                       'color':'firebrick'
                  },
                  layout_kwargs=layout_kwargs
                  )
    
     # Add a line plot for 2m maximum temperature to the plot      
    fig = ct.chart.line(t2m_max_loc, 
                  fig=fig,
                  scatter_kwargs={
                      'name':'Maximum temperature',
                      'mode': 'lines'
                  },
                  line={
                      'dash':'dash',
                      'width':3
                  },
                  marker = {
                      'color':'firebrick'
                  },
                  layout_kwargs=layout_kwargs
                 )

     # Add a line plot for 2m minimum temperature to the plot   
    fig = ct.chart.line(t2m_min_loc, 
                  fig=fig,
                  scatter_kwargs={
                      'name':'Minimum temperature',
                      'mode':'lines'
                  },
                  line={
                      'dash':'dot',
                      'width':3
                  },                  
                  marker= {
                      'color':'firebrick'
                  },
                  fill='tonexty',
                  fillcolor='rgba(178,34,34,0.2)',
                  layout_kwargs=layout_kwargs
                 )

    # Return the plot to be shown as livefigure
    return fig
