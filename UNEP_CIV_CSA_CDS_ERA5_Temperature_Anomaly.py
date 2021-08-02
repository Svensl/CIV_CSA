#"""This workflow is part of the document:
#https://cds.climate.copernicus.eu/toolbox/doc/how-to/13_how_to_calculate_climatologies_and_anomalies/13_how_to_calculate_climatologies_and_anomalies.html
#"""
import cdstoolbox as ct

# Initialise the application and provide a title
@ct.application(
    description='Yearly anomalies of 2m air temperature in AOI - relative to 1981-2010 climate normal period'
)

# Define an output widget
@ct.output.livefigure()

# Define the application function
def calculate_anomalies():
    '''
    Computes climate anomalies of monthly 2m air temperature values for AOI for 41 years (1979-2019) based on the climate normal period 1981-2010. Plot results in a bar chart.
    
    Returns:
    - interactive livefigure
    '''

    # Retrieve monthly 2m air temperature data from 1979 to 2019 for AOI
    t2m_monthly_mean = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'product_type':'monthly_averaged_reanalysis',
            'variable':'2m_temperature',
            'year': [ '1979','1980','1981','1982','1983','1984','1985','1986','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015', '2016', '2017', '2018', '2019'
                    ],
            'month': list(range(1, 12 + 1)),
            'time':'00:00',
            'grid':[0.25, 0.25],
            'area':['10', '-3.6', '7.5', '-2']
        }
    )

#####################################################
# Calculate the temperature anomalies providing the interval for the normal period
#####################################################

    t2m_anomalies = ct.climate.anomaly(
        t2m_monthly_mean,
        interval=['1981','2010']
    )

#####################################################
# Average the values for AOI
#####################################################
    # Calculate the spatial average to give one anomaly value per month for the AOI
    t2m_anomalies_aoi = ct.geo.spatial_average(
        t2m_anomalies
    )

#####################################################
# Resample from monthly values to mean values per year
#####################################################
    t2m_anomalies_aoi_yearly = ct.cube.resample(
        t2m_anomalies_aoi, freq='year'
    )

#################################################
# Plotting example
#################################################     
# Define the resulting figure as a bar chart representing the yearly anomalies of 2m air temperature for AOI    
    
    # Set general information on the plot style, e.g. width and height, title of x and y axes etc. The dictionary is then used when the figure object is defined
    layout_kwargs = {  
        'width':800,
        'height':500,
        'legend': {'orientation':'h',
                  'y':-0.15,
                  'x':0.1},
        'yaxis': {
            'zeroline': False,
            'title':'Anomaly in deg Celsius'
        },
        'margin':{'t':25},
        'xaxis':{
            'title': 'Year'
        }
    }
    
    # Defines the color of the bar plot; blue where the anomaly is positive and red where it is positive.   
    bar_color = ct.cube.where(
        t2m_anomalies_aoi_yearly > 0,
        'rgb(0.77,0.23,0.23)',
        'rgb(0.19,0.49,0.72)'
    )
    
    # Plot the anomalies as a bar plot   
    fig = ct.chart.bar(
        t2m_anomalies_aoi_yearly,
        bar_kwargs={
            'name':'2m air temperature'
        },
        marker = {'color': bar_color},
        layout_kwargs=layout_kwargs
    )
   
    # Return the plot to be shown as livefigure
    return fig  
    