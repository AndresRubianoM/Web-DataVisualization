import os 
from flask import  render_template, request, redirect, url_for, flash, session
from werkzeug import secure_filename

#Local Imports
#Function create and configure the app
from app import create_app
#Function that manage the verifications of files extensions
from app.verifications import verify_extensions
#Function to tranform the data file for the templates
from app.transform_to_list import Transform



#Create and configure the Flask instance
app = create_app()


@app.route('/')
def index():
    #Get the name of the file
    filename = session.get('file_data_name')
    context = {}
    #Confirm the file exists and is permited.
    if filename is not None:
        table = Transform(filename, app.config['UPLOAD_FOLDER'])
        context['head'] = table.list_values[0]
        context['data'] = table.list_values[1::]

    return render_template('start.html', **context)


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
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

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['file_data_name'] = filename
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))


        

            




