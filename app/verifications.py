#Possible extensions
ALLOWED_EXTENSIONS = ['csv', 'json', 'xml', 'html']

def verify_extensions(file_name):
    return file_name.split('.')[-1].lower() in ALLOWED_EXTENSIONS