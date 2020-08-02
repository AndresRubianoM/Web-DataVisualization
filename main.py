import os 
import json
from flask import  render_template, request, redirect, url_for, session
from werkzeug import secure_filename

#Bokeh imports
from bokeh.resources import CDN
from bokeh.embed import json_item

#Local Imports
#Function create and configure the app
from app import create_app
#Function that manage the verifications of files extensions
from app.verifications import verify_extensions
#Function to tranform the data file for the templates
from app.transform_to_list import Transform
#Function context buttons 
from app.buttons_context_aux import context_buttons
#Function to plot 
from app.plots_functions import pie_graph, bar_graph, histogram_plot, line_plot, scatter_plot, select_and_plot




#Create and configure the Flask instance
app = create_app()


@app.route('/')
def index():
    '''Principal route check all the information necesary and render the templates'''
    #Get the name of the file
    filename = session.get('file_data_name')
    context = {}

    #Check each one of the buttons information
    buttons_plot_data = {
        'Pie': {'add': session.get('Pie-add'),
                'remove': session.get('Pie-remove')},

        'Bar': {'add': session.get('Bar-add'),
                'remove': session.get('Bar-remove')},

        'Histogram':{'add': session.get('Histogram-add'),
                'remove': session.get('Histogram-remove')},
        
        'Line': {'add': session.get('Line-add'),
                'remove': session.get('Line-remove')},
        
        'Scatter': {'add': session.get('Scatter-add'),
                    'remove': session.get('Scatter-remove')},

    }
    
    #Confirm the file exists and is permited.
    if filename is not None:
        # Class that take the file and parsed to render
        table = Transform(filename, app.config['UPLOAD_FOLDER'])
        #Links needed for the bokeh plots
        context['resources'] = CDN.render()
        #Values fot the table
        context['head'] = table.list_values[0]
        context['data'] = table.list_values[1::]
        #Values for the buttons (needs to reassing the actual values to the session to not acumulate the same values)
        context['pie_col_add'], context['pie_col_remove'], session['Pie-add'], session['Pie-remove'] = context_buttons(buttons_plot_data['Pie']['add'],
                                                                                                                       buttons_plot_data['Pie']['remove'], 
                                                                                                                       context['head'])

        context['bar_col_add'], context['bar_col_remove'], session['Bar-add'], session['Bar-remove'] = context_buttons(buttons_plot_data['Bar']['add'],
                                                                                                                       buttons_plot_data['Bar']['remove'], 
                                                                                                                       context['head'])

        context['hist_col_add'], context['hist_col_remove'], session['Histogram-add'], session['Histogram-remove'] = context_buttons(buttons_plot_data['Histogram']['add'],
                                                                                                                       buttons_plot_data['Histogram']['remove'], 
                                                                                                                       context['head'])
        
        context['line_col_add'], context['line_col_remove'], session['Line-add'], session['Line-remove'] = context_buttons(buttons_plot_data['Line']['add'],
                                                                                                                       buttons_plot_data['Line']['remove'], 
                                                                                                                       context['head'])
        
        context['scatter_col_add'], context['scatter_col_remove'], session['Scatter-add'], session['Scatter-remove'] = context_buttons(buttons_plot_data['Scatter']['add'],
                                                                                                                       buttons_plot_data['Scatter']['remove'], 
                                                                                                                       context['head'])
        
    return render_template('start.html', **context)


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    '''Function manage the uploading of the files and verifications'''
    if request.method == 'POST':
        #verifys if the file exists (the name was specified in the html <input>)
        if 'uploaded_data' not in request.files:
            print('file exists in request')
            redirect(url_for('index'))
        
        file = request.files['uploaded_data']

        #Verify the file actually was loaded
        if file.filename == '':
            print('None file was selected')
            redirect(url_for('index'))
        
        #if the extension file is permited the file is save 
        if verify_extensions(file.filename):
            filename = secure_filename(file.filename)
            #Change the real name for a simpleone to manage the functions
            #new_filename = 'data' + '.' + filename.split('.')[-1]

            #create directory if doesnt exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])

            #save the data and pass the name of the file to the session
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['file_data_name'] = filename

            return redirect(url_for('index'))
    
    return redirect(url_for('index'))


@app.route('/columns', methods=['POST'])
def columns_data():
    '''Get the values from the buttons for each plot and each. Keeps the values on a session'''
    if request.method == 'POST':
        #Confirms the form have the key
        if len(list(request.form.keys())) == 0:
            return redirect(url_for('index'))

        #Get the key and its value of each one of the buttons per plot
        key = list(request.form.keys())[0]
        col = request.form.get(key)

        #Pass the information of the session to a temporal variable if exists and if is not None
        if key in session:
            if session[key] is not None:
                available_cols = session[key]   
            else: 
                available_cols = []  
        else:
            available_cols = []
        
        #Save the actual data and reassign the data to the session.
        available_cols.append(col)
        session[key] = available_cols
        
        return redirect(url_for('index'))


@app.route('/plot_pie')
def plot_pie():
    p = select_and_plot(session, 'Pie-add', pie_graph, app.config['UPLOAD_FOLDER'])
    return  json.dumps(json_item(p, "Pie-image"))


@app.route('/plot_bar')
def plot_bar():
    p = select_and_plot(session, 'Bar-add', bar_graph, app.config['UPLOAD_FOLDER'])
    return  json.dumps(json_item(p, "Bar-image"))


@app.route('/plot_hist')
def plot_hist():
    p = select_and_plot(session, 'Histogram-add', histogram_plot, app.config['UPLOAD_FOLDER'])
    return  json.dumps(json_item(p, "Histogram-image"))


@app.route('/plot_line')
def plot_line():
    p = select_and_plot(session, 'Line-add', line_plot, app.config['UPLOAD_FOLDER'])
    return  json.dumps(json_item(p, "Line-image"))


@app.route('/plot_scatter')
def plot_scatter():
    p = select_and_plot(session, 'Scatter-add', scatter_plot, app.config['UPLOAD_FOLDER'])
    return  json.dumps(json_item(p, "Scatter-image"))

        

    

        
        

