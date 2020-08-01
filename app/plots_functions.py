from math import pi
import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Category20, Spectral5
from bokeh.transform import cumsum, factor_cmap

#local imports
from .transform_to_list import Transform


def select_and_plot(session, name_button, plot_function, upload_folder):
    """Function to manage the data and plot selection

    session: session of Flask
    name_button: Name of the button that pass the form value (String)
    plot_function: Plot function (function)
    upload_folder: Name of the folder where the file is (string)"""

    #Define the data to be graph
    filename = session.get('file_data_name')
    #Columns added to be plot
    data_graph = session.get(name_button)
    #Organize the data and make the plot
    if (data_graph is not None) and (len(data_graph) > 0):
        #Get the table 
        table = Transform(filename, upload_folder)
        #Select the specified data
        table_selected_data = table.select_data(data_graph)
        #Plot
        p = plot_function(data_graph, table_selected_data)

        return p
    else:
        return None



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
    """Function to make the bar plot, take the columns transform into float values. 
    the FIRST COLUMN MUST BE CATEGORICAL, the other numerical and will be added to the plot
    
    col_names: list of the column names
    data: list of lists of the values for each column"""

    #Take the first column, MUST BE CATEGORICAL
    data_bokeh = {
        'categorical': data[0],
    }

    #Organize the dictionary information
    bar_data = transform_to_num(col_names, data)
    data_bokeh.update(bar_data)
    data_bokeh['data_col']= list(bar_data.keys())
    
    #Define necessary columns for multiple bars
    x = [(categ, data) for categ in data_bokeh['categorical'] for data in data_bokeh['data_col']]
    ##Organize all the numerical data in a single list
    counts = []
    for i in range(len(data[0])):
        for name in bar_data.keys():
            counts.append(bar_data[name][i])
    
    #Transform the dictionary into the format required by bokeh
    source = ColumnDataSource(data = dict(x = x, counts = counts))

    #Bokeh plot configuration
    p = figure(plot_height = 500, plot_width = 900, x_range = FactorRange(*x))
    p.vbar(x = 'x', top = 'counts', width = 0.9, line_color = 'white', source = source,
     fill_color = factor_cmap('x', palette = Spectral5, factors = data_bokeh['data_col'], start = 1, end = 2) )
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1.2
    
    return p
           
   

def histogram_plot(col_names, data):
    """Function to make the histogram, only show one variable 
    
    col_names: list of the column names
    data: list of lists of the values for each column"""

    #transform to numerical data
    hist_data = transform_to_num(col_names, data)

    #Calculate and define the histogram data
    hist, edges = np.histogram(list(hist_data.values())[0], density = True, bins = 30)

    #Bokeh plot configuration
    p = figure(plot_height = 500, plot_width = 900)
    p.quad(top = hist, bottom = 0, left = edges[:-1], right = edges[1:], line_color = 'white')

    return p 


def line_plot(col_names, data):
    """Function to make the line plot, the FIRST COLUMN will be the x axis and the others will be added
    
    col_names: list of the column names
    data: list of lists of the values for each column"""

    #Transform to numerical data
    line_data = transform_to_num(col_names, data)
    
    #Transform the dictionary into the format required by bokeh
    source = ColumnDataSource(line_data)

    #Bokeh plot configuration
    p = figure(plot_height = 500, plot_width = 900)
    for key, color in zip(range(len(line_data.keys())), Category20[20]):
        if key != 0:
            p.line(x = list(line_data.values())[0], y = list(line_data.values())[key], color = color, 
            legend_label = list(line_data.keys())[key])

    return p 
    

def scatter_plot(col_names, data):
    """Function to make the scatter plot, the FIRST COLUMN will be the x axis and the others will be added
    
    col_names: list of the column names
    data: list of lists of the values for each column"""

    #Transform to numerical data
    scatter_data = transform_to_num(col_names, data)

    #Transform the dictionary into the format required by bokeh
    source = ColumnDataSource(scatter_data)

    #Bokeh plot configuration
    p = figure(plot_height = 500, plot_width = 900)
    for key, color in zip(range(len(scatter_data.keys())), Category20[20]):
        if key != 0:
            p.scatter(x = list(scatter_data.values())[0], y = list(scatter_data.values())[key], color = color, 
            fill_alpha = 0.6, legend_label = list(scatter_data.keys())[key])

    return p 






