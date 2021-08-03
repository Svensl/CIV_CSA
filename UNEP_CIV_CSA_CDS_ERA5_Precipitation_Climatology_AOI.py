"""This workflow is part of the document:
https://cds.climate.copernicus.eu/toolbox/doc/how-to/13_how_to_calculate_climatologies_and_anomalies/13_how_to_calculate_climatologies_and_anomalies.html
"""
import cdstoolbox as ct

# Initialise the application and provide a title
@ct.application(
    description='Climatology mean and standard deviation for precipitation based on the 19-year climatology 1981-2020 for Louomidouo in Côte d Ivoire'
)

# Define output widget
@ct.output.livefigure()

# Define the application function
def plot_climatologies():
    '''
    Computes climatological means and standard deviation of monthly precipitation values for a period of ten year. Plot results in a line graph.
    
    Returns:
    - interactive livefigure
    '''
    
    # Retrieve ERA5 monthly averaged data on single levels - precipitation for 10 years
    prec_monthly_mean = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'product_type':'monthly_averaged_reanalysis',
            'variable':'total_precipitation',
            'year':[
                '1980','1981', '1982', '1983',
                '1984', '1985', '1986',
                '1987', '1988', '1989',
                '1990', '1991', '1992',
                '1993', '1994', '1995',
                '1996', '1997', '1998',
                '1999', '2000', '2001',
                '2002', '2003', '2004',
                '2005', '2006', '2007',
                '2008', '2009', '2010',
                '2011', '2012', '2013',
                '2014', '2015', '2016',
                '2017', '2018', '2019',
                '2020', '2021'
            ],
            'month': list(range(1, 12 + 1)),
            'time':'00:00',
            'grid':[3, 3],
        }
    )

######################################################
# Calculate monthly climatologies for a 19-year period
###################################################### 
    prec_monthly_climatologies = ct.climate.climatology_mean(
        data=prec_monthly_mean, 
        start='1981', 
        stop='2020', 
        frequency='month'
    )

######################################################
# Calculate the standard deviation of a climatology for a 10-year period
######################################################
    prec_monthly_climatology_std = ct.climate.climatology_std(  
        data=prec_monthly_mean
    )


######################################################
# Extract location information
######################################################
    # Extract time-series information for climatological means
    loc = ct.geo.extract_point(
        prec_monthly_climatologies, 
        lon=-2.903,
        lat=9.035
    )
    
    # Extract time-series for climatological standard deviation
    loc_std = ct.geo.extract_point(
        prec_monthly_climatology_std, 
        lon=-2.903,
        lat=9.035
    )

######################################################
# Plotting example
######################################################
    fig = ct.chart.plot_climatology(
        loc, 
        start_from=int(1), 
        error_y=loc_std,
    )
            
    # Return the plot to be shown as livefigure        
    return fig   
