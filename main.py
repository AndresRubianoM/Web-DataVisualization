import os 
from flask import  render_template, request, redirect, url_for, session
from werkzeug import secure_filename

#Local Imports
#Function create and configure the app
from app import create_app
#Function that manage the verifications of files extensions
from app.verifications import verify_extensions
#Function to tranform the data file for the templates
from app.transform_to_list import Transform
#Function context buttons 
from app.buttons_context_aux import context_buttons



#Create and configure the Flask instance
app = create_app()


@app.route('/')
def index():
    '''Principal route check all the information necesary and render the templates'''
    #Get the name of the file
    filename = session.get('file_data_name')
    context = {}

    #Check each one of the buttons information
    add_pie = session.get('pie-add')
    remove_pie = session.get('pie-remove')

    #Confirm the file exists and is permited.
    if filename is not None:
        # Class that take the file and parsed to render
        table = Transform(filename, app.config['UPLOAD_FOLDER'])
        #Values fot the table
        context['head'] = table.list_values[0]
        context['data'] = table.list_values[1::]
        #Values for the buttons (needs to reassing the actual values to the session to not acumulate the same values)
        context['pie_col_add'], context['pie_col_remove'], session['pie-add'], session['pie-remove'] = context_buttons(add_pie, remove_pie, context['head'])
        
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
        




            
        
        


        

            




