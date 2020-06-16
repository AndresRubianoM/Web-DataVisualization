class Config():
    DEBUG = False
    SECRET_KEY = "PROBE"
    UPLOAD_FOLDER = r".\_uploads"
    MAX_CONTENT_LENGHT = 16 * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True



    

