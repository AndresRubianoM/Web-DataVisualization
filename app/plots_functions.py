from math import pi
import itertools

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Category20, Spectral5
from bokeh.transform import cumsum, factor_cmap

def transform_to_num(col_names, data):
    """Transform the strings value into floats, the categorical values will be left apart, the 
    return will be a dictionary.

    col_names: list of the column names
    data: list of lists of the values for each column"""

    int_data = {}

    for name, row in zip(col_names, data):
        
        try:
            for i in range(len(row)):
                row[i] = float(row[i])

            int_data[name] = row
        except ValueError:
            continue   
    
    return int_data
    

def pie_graph( col_names, data):
    """Function to make the pie plot, take the columns transform into float values and sum all the values to make
    the plot (it can't do a pie plot per row).
    
    col_names: list of the column names
    data: list of lists of the values for each column"""
    
    #Summarize the columns
    pie_data = transform_to_num(col_names, data)
    for name, row in pie_data.items():
            pie_data[name] = sum(row)

        
    #Define the final data for the graph (format)
    data_bokeh = {'legends': list(pie_data.keys()),
                  'values': list(pie_data.values()),
                  'color': Category20[20]}

    data_bokeh['angles'] = []
    for name, val in pie_data.items():
        angle = val/sum(list(pie_data.values())) * 2 * pi
        data_bokeh['angles'].append(angle)
    
    #Transform the dictionary into the format required by bokeh
    source = ColumnDataSource(data_bokeh)

    #Bokeh plot configuration
    p = figure(plot_height = 600, plot_width = 800, tools = 'hover', tooltips = "@legends: @values")
    p.wedge(x = 0, y = 1, radius =0.6, start_angle = cumsum('angles', include_zero = True), 
            end_angle = cumsum('angles'), legend_field = 'legends', fill_color = 'color', 
            line_color ='white', source = source)

    return p

     

def bar_graph(col_names, data):

    data_bokeh = {
        'categorical': data[0],
    }

    #Summarize the columns
    bar_data = transform_to_num(col_names, data)
    for name, row in bar_data.items():
        data_bokeh[name] = row

    data_bokeh['data_col']= list(bar_data.keys())
    
    x = [(categ, data) for categ in data_bokeh['categorical'] for data in data_bokeh['data_col']]
    counts = []
    for i in range(len(data[0])):
        for name in bar_data.keys():
            counts.append(bar_data[name][i])
    
    
    source = ColumnDataSource(data = dict(x = x, counts = counts))

    p = figure(plot_height = 500, plot_width = 900, x_range = FactorRange(*x))
    p.vbar(x = 'x', top = 'counts', width = 0.9, line_color = 'white', source = source,
     fill_color = factor_cmap('x', palette = Spectral5, factors = data_bokeh['data_col'], start = 1, end = 2) )

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1.2
    
    return p
           
   


def histogram_plot():
    pass


def line_plot():
    pass


def scatter_plot():
    pass





