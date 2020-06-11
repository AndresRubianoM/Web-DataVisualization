#Local Imports
#Function create and configure the app
from app import create_app

#Create and configure the Flask instance
app = create_app()


@app.route('/')
def hello():
    return 'hello world'