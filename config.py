import os # Variables de entorno

class Config(object):
    SECRET_KEY = 'secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/flask' # conectate a msql con el usuario root con la puesword en localhost a la base de datos flask
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost/saenz_performance' # conectate a msql con el usuario root con la puesword en localhost a la base de datos flask
    SQLALCHEMY_TRACK_MODIFICATIONS = False