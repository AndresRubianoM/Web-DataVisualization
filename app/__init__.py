from flask import Flask


def create_app():
    #Instance and configure
    app = Flask(__name__, instance_relative_config = True)

    #Prevents errors if the enviroment is for Production
    if app.config['ENV'] == 'production':
        app.config.from_object("config.DevelopmentConfig")
    else:
        app.config.from_object("config.Config")
        

    return app
