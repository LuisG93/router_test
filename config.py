import os 

class TestingConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = True

class ProdConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = False